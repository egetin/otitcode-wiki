from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Rule(models.Model):
  rule_text = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  modified_at = models.DateTimeField(auto_now=True)
