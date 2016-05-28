from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^auth$', views.AuthHandler, name='auth'),
    url(r'^articles$', views.ArticleHandler, name='articles'),
    url(r'^articles/(?P<article_id>\d+)$', views.ArticleHandler, name='article'),
    url(r'^users$', views.UserHandler, name='users'),
    url(r'^users/(?P<user_id>\d+)$', views.UserHandler, name='user'),
    url(r'^comments$', views.CommentHandler, name='comments'),
    url(r'^comments/(?P<comment_id>\d+)$', views.CommentHandler, name='comments'),
    #url(r'^articles/(?P<article_id>\d+)/comments$')
    #users
    #users id
# users id comments
# users id articles
# comments
# comments id
]
