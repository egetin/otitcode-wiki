from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^auth$', views.AuthHandler, name='auth'),
    url(r'^articles$', views.ArticleHandler, name='articles'),
    url(r'^articles/(?P<article_id>\d+)$', views.ArticleHandler, name='article'),
    url(r'^articles/(?P<article_id>\d+)/comments$', views.ArticleCommentHandler, name='articlecomment'),
    url(r'^comments$', views.CommentHandler, name='comments'),
    url(r'^comments/(?P<comment_id>\d+)$', views.CommentHandler, name='comments'),
    url(r'^users$', views.UserHandler, name='users'),
    url(r'^users/(?P<user_id>\d+)$', views.UserHandler, name='user'),
    url(r'^users/(?P<user_id>\d+)/articles$', views.UserArticleHandler, name='userarticle'),
    url(r'^users/(?P<user_id>\d+)/comments$', views.UserCommentHandler, name='usercomment'),
]
