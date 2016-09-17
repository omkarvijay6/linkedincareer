from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render_to_response

# Create your views here.
from django.template import RequestContext
from payments.enums import StatusChoices
from payments.services import get_payment_gateway_url, update_user_payment, validate_payment_payload


def payment_callback(request):
    payment_payload = request.GET
    user = request.user
    secure_is_valid = validate_payment_payload(payment_payload)
    if secure_is_valid:
        payment = update_user_payment(user, payment_payload)
        if payment.status == StatusChoices.approved.value:
            payment_template = 'payment_receipt.html'
        else:
            payment_template = 'payment_receipt.html'
        return render_to_response(payment_template, {'payment': payment},
                                  context_instance=RequestContext(request))
    else:
        return render_to_response('payment_forbidden.html', {},
                                  context_instance=RequestContext(request))


@login_required
def redirect_to_payment_gateway(request, amount):
    user = request.user
    payment_gateway_url = get_payment_gateway_url(user, amount)
    return redirect(payment_gateway_url)
