from django.conf.urls import url
from . import views        
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^dashboard$', views.dashboard),
    url(r'^add$', views.add),
    url(r'^createitem$', views.createitem),
    url(r'^item/(?P<id>\d+)$', views.showitem),
    url(r'^logout$', views.logout),
]