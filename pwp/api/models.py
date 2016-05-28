from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Article(models.Model):
    topic = models.TextField()
    article_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey('User')

class Comment(models.Model):
    comment_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    rule = models.ForeignKey('Article', on_delete=models.CASCADE)
    user = models.ForeignKey('User')

class User(models.Model):
    nickname = models.CharField(max_length=30)
    realname = models.CharField(max_length=50)
