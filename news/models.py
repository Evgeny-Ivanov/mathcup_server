from django.contrib.postgres.fields import JSONField
from django.db import models


class News(models.Model):
    header = models.CharField(max_length=100)
    content = JSONField()
    date = models.DateTimeField(auto_now_add=True)
