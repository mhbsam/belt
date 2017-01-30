from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^registration$', views.registration),
    url(r'^login$', views.login),
    url(r'^logoff$', views.logoff),
    url(r'^appointments$', views.appointments),
    url(r'^addapp$', views.addapp),
    url(r'^delete/(?P<task_id>\d+)$', views.delete),
    url(r'^edit/(?P<task_id>\d+)$', views.edit),
]
