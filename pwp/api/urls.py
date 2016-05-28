from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^auth/$', views.Auth, name='Auth'),
    url(r'^articles/$', views.GetArticles, name='GetArticles'),
]
