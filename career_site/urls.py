from django.conf.urls import url

from views import index, about, services, news, contact

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^about/', about, name='about'),
    url(r'^services/', services, name='services'),
    url(r'^news/', news, name='news'),
    url(r'^contact/', contact, name='contact'),
]