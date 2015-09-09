from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.search, name='index'),
    url(r'^search$', views.search, name='search'),
    url(r'^info/(?P<slug_id>[a-zA-Z0-9\-]+)$', views.info, name='info'),
    url(r'^shows$', views.shows, name='shows')
]
