from django.db import models
from tasks.models import Task
from users.models import User


class UserAnswer(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    answer = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    correct = models.BooleanField(default=False)

    class Meta:
        unique_together = (("task", "user"),)
