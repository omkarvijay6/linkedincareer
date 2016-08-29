from django.conf.urls import url

from subscription.views import payment_callback, payment

urlpatterns = [
    url(r'^payment-callback/$', payment_callback, name='payment_callback'),
    url(r'^payment/$', payment, name='payment'),

]
