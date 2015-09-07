from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.search, name='index'),
    url(r'^search$', views.search, name='search'),
    url(r'^results/(?P<slug_id>[a-zA-Z0-9\-]+)$', views.countdown, name='countdown'),
    url(r'^shows$', views.shows, name='shows')
]
