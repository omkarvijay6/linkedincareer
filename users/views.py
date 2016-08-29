from django.contrib.auth import login, logout
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from users.forms import UserLoginForm


def user_login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('payment'))
    auth_form = UserLoginForm()
    if request.method == 'POST':
        nextpage = request.GET.get('next', reverse('payment'))
        auth_form = UserLoginForm(data=request.POST)
        if auth_form.is_valid():
            login(request, auth_form.get_user())
            return HttpResponseRedirect(nextpage)
        else:
            return render_to_response('login.html', {'auth_form': auth_form}, RequestContext(request))
    return render_to_response('login.html', {'auth_form': auth_form}, RequestContext(request))


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
