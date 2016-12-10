from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from paypal.standard.forms import PayPalPaymentsForm

# Create your views here.
from payments.enums import StatusChoices
from payments.services import get_payment_gateway_url, update_user_payment, validate_payment_payload, get_service


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
def view_that_asks_for_money(request):

    # What you want the button to do.
    paypal_dict = {
        "business": request.user.email,
        "amount": "1.00",
        "item_name": "name of the item",
        "invoice": "28347293849834",
        "notify_url": "https://globalindeedcareers.herokuapp.com/payments/paypal/notify/" + reverse('paypal-ipn'),
        "return_url": "https://globalindeedcareers.herokuapp.com/payments/paypal/return/",
        "cancel_return": "https://globalindeedcareers.herokuapp.com/payments/paypal/cancel/",
        "custom": "Upgrade all users!",  # Custom command to correlate to some function later (optional)
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    return render(request, "payment.html", context)

@login_required
def paypal_notify(request):
    return render(request, "payment.html", {})

@login_required
@csrf_exempt
def paypal_return(request):
    print request.POST
    return render(request, "payment.html", {})

@login_required
def paypal_cancel(request):
    return render(request, "payment.html", {})