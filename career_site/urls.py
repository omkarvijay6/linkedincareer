from django.conf.urls import url

from views import index, about, services, news, contact, right_connect, professional_resume, executive_service, \
    combo_services, privacy_policy, t_and_c

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^about/', about, name='about'),
    url(r'^services/', services, name='services'),
    url(r'^news/', news, name='news'),
    url(r'^contact/', contact, name='contact'),
    url(r'^right-connect/', right_connect, name='right_connect'),
    url(r'^professional-resume/', professional_resume, name='professional_resume'),
    url(r'^executive-level-services/', executive_service, name='executive_service'),
    url(r'^combo-services/', combo_services, name='combo_services'),
    url(r'^privacy-policy/', privacy_policy, name='privacy_policy'),
    url(r'^terms-and-conditions/', t_and_c, name='t_and_c'),

]
