"""linkedincareer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from payments.views import payment_callback

urlpatterns = [
    url(r'^godzillaroar/', admin.site.urls),
    url(r'^', include('career_site.urls')),
    url(r'^users/', include('users.urls')),
    url(r'^payments/', include('payments.urls')),
    url(r'^core/', include('core.urls')),
    url(r'^subscription/payment-callback/$', payment_callback, name='payment_callback'),

    url(r'^paypal/', include('paypal.standard.ipn.urls')),
]
