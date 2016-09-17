from django.conf.urls import url
from django.views.generic import TemplateView

from payments.views import redirect_to_payment_gateway

urlpatterns = [
    url(r'^redirect/payment-gateway/(?P<amount>\d+)/(?P<service_nk>\w+)/(?P<country_code>\w+)/$', redirect_to_payment_gateway, name='payment_with_country'),
    url(r'^redirect/payment-gateway/(?P<amount>\d+)/(?P<service_nk>\w+)/$', redirect_to_payment_gateway, name='payment_without_country'),
    url(r'^successful/$', TemplateView.as_view(template_name="payment_successful.html"), name="payment_successful"),
    url(r'^failed/$', TemplateView.as_view(template_name="payment_failed.html"), name="payment_failed"),
    url(r'^forbidden/$', TemplateView.as_view(template_name="forbidden.html"), name="forbidden"),

]
