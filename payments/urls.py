from django.conf.urls import url

from payments.views import redirect_to_payment_gateway

urlpatterns = [
    url(r'^redirect/payment-gateway/(?P<amount>\d+)/$', redirect_to_payment_gateway, name='payment'),

]