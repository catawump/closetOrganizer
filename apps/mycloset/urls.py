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
    url(r'^wear/(?P<id>\d+)$', views.wearitem),
    url(r'^wash/(?P<id>\d+)$', views.washitem),
    url(r'^washall$', views.washall),
    url(r'^laundry$', views.laundry),
    url(r'^viewitem/(?P<id>\d+)$', views.viewitem),
    url(r'^manage$', views.manage),
    url(r'^outfits$', views.outfits),
    url(r'^addoutfit$', views.addoutfit),
    url(r'^createoutfit$', views.createoutfit),
    url(r'^favitem/(?P<id>\d+)$', views.favitem),
    url(r'^delete/(?P<id>\d+)$', views.delete),
    url(r'^deleteoutfit/(?P<id>\d+)$', views.deleteoutfit),
    url(r'^logout$', views.logout),
]