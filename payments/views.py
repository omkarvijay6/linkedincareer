from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.core.urlresolvers import reverse

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
