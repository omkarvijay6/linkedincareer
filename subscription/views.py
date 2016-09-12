from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render_to_response
from django.core.urlresolvers import reverse
from migs_mastercard import MigsClient


# Create your views here.
from django.template import RequestContext


def payment_callback(request):
    print "callback recieved"
    return redirect(reverse('index'))


@login_required
def payment(request):
    migs_client = MigsClient()
    encoded_url = migs_client.generate_get_url()
    return redirect(encoded_url)
