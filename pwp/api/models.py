from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Article(models.Model):
    topic = models.TextField()
    article_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User)

    def __str__(self):
        return self.topic

class Comment(models.Model):
    comment_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    rule = models.ForeignKey('Article', on_delete=models.CASCADE)
    owner = models.ForeignKey(User)

    def __str__(self):
        return self.comment_text
