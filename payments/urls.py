from django.conf.urls import url
from django.views.generic import TemplateView

from payments.views import redirect_to_payment_gateway, view_that_asks_for_money, paypal_notify, paypal_return, \
    paypal_cancel, paypal_payment, include_cover_letter

urlpatterns = [
    url(r'^redirect/payment-gateway/(?P<amount>\d+)/(?P<service_nk>\w+)/(?P<country_code>\w+)/$',
        redirect_to_payment_gateway, name='payment_with_country'),
    url(r'^redirect/payment-gateway/(?P<amount>\d+)/(?P<service_nk>\w+)/$', redirect_to_payment_gateway,
        name='payment_without_country'),
    url(r'^successful/$', TemplateView.as_view(template_name="payment_successful.html"), name="payment_successful"),
    url(r'^failed/$', TemplateView.as_view(template_name="payment_failed.html"), name="payment_failed"),
    url(r'^forbidden/$', TemplateView.as_view(template_name="forbidden.html"), name="forbidden"),

    url(r'^paypal/$', view_that_asks_for_money, name='paypal'),
    url(r'^paypal/notify/$', paypal_notify, name='paypal_notify'),
    url(r'^paypal/return/$', paypal_return, name='paypal_return'),
    url(r'^paypal/cancel/$', paypal_cancel, name='paypal_cancel'),

    # url(r'^paypal/payment/(?P<amount>\d+)/(?P<service_nk>\w+)/$', paypal_payment, name="paypal_payment")
    url(r'^paypal/payment-gateway/(?P<amount>\d+)/(?P<service_nk>\w+)/(?P<country_code>\w+)/$',
        paypal_payment, name='paypal_payment_with_country'),
    url(r'^paypal/payment-gateway/(?P<amount>\d+)/(?P<service_nk>\w+)/$', paypal_payment,
        name='paypal_payment_without_country'),
    url(r'^include/cover-letter/$', include_cover_letter, name='include_cover_letter'),

]
