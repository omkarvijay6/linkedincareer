from django.conf.urls import url

from payments.views import payment_callback, payment

urlpatterns = [
    url(r'^payment/$', payment, name='payment'),

]