from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from payments.migs_mastercard import MigsClient

# Create your views here.

def payment_callback(request):
    print "callback recieved"
    return redirect(reverse('index'))


@login_required
def redirect_to_payment_gateway(request):
    migs_client = MigsClient()
    encoded_url = migs_client.generate_get_url()
    return redirect(encoded_url)
