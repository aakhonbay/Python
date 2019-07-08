from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^add_user$', views.add_user),
    url(r'^login$', views.login),
    url(r'^welcome$', views.welcome),
    url(r'^logout$', views.logout),
    url(r'^friend/(?P<id>\d+)$', views.friend),
    url(r'^user/(?P<id>\d+)$', views.user),
    url(r'^delete/(?P<id>\d+)$', views.delete)
  ]
