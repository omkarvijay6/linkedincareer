import requests

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from paypal.standard.forms import PayPalPaymentsForm

# Create your views here.
from payments.enums import StatusChoices
from payments.models import Order
from payments.services import get_payment_gateway_url, update_user_payment, validate_payment_payload, get_service, \
    place_order_for_user


def payment_callback(request):
    payment_payload = request.GET
    user = request.user
    secure_is_valid = validate_payment_payload(payment_payload)
    if secure_is_valid:
        payment = update_user_payment(user, payment_payload)
        if payment.status == StatusChoices.successful.value:
            redirect_url = reverse('payment_successful')
        else:
            redirect_url = reverse('payment_failed')
    else:
        redirect_url = reverse('forbidden')
    return HttpResponseRedirect(redirect_url)


@login_required
def redirect_to_payment_gateway(request, amount, service_nk, country_code=None):
    user = request.user
    service = get_service(service_nk)
    payment_gateway_url = get_payment_gateway_url(user, amount, service, country_code)
    return redirect(payment_gateway_url)


@login_required
def paypal_payment(request, amount, service_nk, country_code):
    # payment_url = "https://www.sandbox.paypal.com/cgi-bin/webscr"

    # posted = {'cancel_return': 'https://globalindeedcareers.herokuapp.com/payments/paypal/cancel/',
    #           'cmd': '_xclick', 'return': 'https://globalindeedcareers.herokuapp.com/payments/paypal/return/',
    #           'business': 'omkarvijay5@gmail.com', 'item_name': 'name of the item', 'charset': 'utf-8',
    #           'amount': '1.00', 'custom': 'Upgrade all users!', 'submit.x': u'85',
    #           'notify_url': 'https://globalindeedcareers.herokuapp.com/payments/paypal/notify/',
    #           'invoice': '283472938498342387','no_shipping': '1', 'currency_code': 'USD', 'submit.y': '17'}
    user = request.user
    service = get_service(service_nk)
    order = place_order_for_user(user, service, amount, country_code)
    paypal_dict = {
        "business": request.user.email,
        "amount": str(amount),
        "item_name": service.name,
        "invoice": order.merch_txn_ref,
        "notify_url": "https://globalindeedcareers.herokuapp.com" + reverse('paypal_notify'),
        "return_url": "https://globalindeedcareers.herokuapp.com/" + reverse('paypal_return'),
        "cancel_return": "https://globalindeedcareers.herokuapp.com/" + reverse('paypal_cancel'),
        "custom": "Upgrade all users!",  # Custom command to correlate to some function later (optional)
    }
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {'order': order, 'service': service, 'form': form}
    return render(request, "payment_order.html", context)

@login_required
def view_that_asks_for_money(request):

    # What you want the button to do.
    paypal_dict = {
        "business": request.user.email,
        "amount": "1.00",
        "item_name": "name of the item",
        "invoice": "283472938498342387",
        "notify_url": "https://globalindeedcareers.herokuapp.com/payments/paypal/notify/",
        "return_url": "https://globalindeedcareers.herokuapp.com/payments/paypal/return/",
        "cancel_return": "https://globalindeedcareers.herokuapp.com/payments/paypal/cancel/",
        "custom": "Upgrade all users!",  # Custom command to correlate to some function later (optional)
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    return render(request, "payment.html", context)

@csrf_exempt
def paypal_notify(request):
    print "notify called"
    post_data = request.POST
    invoice = post_data['invoice']
    amount = eval(post_data['payment_gross'])
    txn_id = post_data['txn_id']
    try:
        order = Order.objects.get(merch_txn_ref=invoice)
    except Order.DoesNotExist:
        return render(request, "payment_error.html", {})
    if order.amount != amount:
        return render(request, "payment_error.html", {})
    payment = order.payment
    payment.transaction_num = txn_id
    payment.status = post_data['payment_status'][0] if post_data['payment_status'] else None
    payment.save()
    context = {'payment': payment}
    return render(request, "payment_successful.html", context)

@login_required
@csrf_exempt
def paypal_return(request):
    print "returned"
    print request.POST
    print request.GET
    return render(request, "payment.html", {})

@login_required
def paypal_cancel(request):
    print "cancel"
    print request.POST
    print request.GET
    return render(request, "payment.html", {})