from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render_to_response
from django.core.urlresolvers import reverse


# Create your views here.
from django.template import RequestContext


def payment_callback(request):
    return redirect(reverse('index'))

@login_required
def payment(request):
    return render_to_response('payment.html', {}, context_instance=RequestContext(request))
