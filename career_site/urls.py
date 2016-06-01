from django.conf.urls import url

from views import index, about, services, news

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^about/', about, name='about'),
    url(r'^services/', services, name='services'),
    url(r'^news/', news, name='news'),
]