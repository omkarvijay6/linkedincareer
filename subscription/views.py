from django.shortcuts import redirect
from django.core.urlresolvers import reverse


# Create your views here.

def payment_callback(request):
    return redirect(reverse('index'))
