from django.conf.urls import url

from subscription.views import payment_callback

urlpatterns = [
    url(r'^payment-callback/$', payment_callback, name='payment_callback'),

]
