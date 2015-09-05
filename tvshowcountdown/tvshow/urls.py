from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<slug_id>[a-zA-Z\-]+)$', views.countdown, name='countdown'),
]
