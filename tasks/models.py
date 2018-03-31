from django.contrib.postgres.fields import JSONField
from django.db import models
from rounds.models import Round


class Task(models.Model):
    text = JSONField()
    answer = models.TextField()
    round = models.ForeignKey(Round, on_delete=models.CASCADE)
    weight = models.IntegerField(default=1, help_text='сложность вопроса')
