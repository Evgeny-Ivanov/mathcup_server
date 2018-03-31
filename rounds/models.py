from django.db import models
from users.models import User
from django.utils import timezone
from tournaments.models import Tournament


class RoundManager(models.Manager):
    def published(self):
        return self.get_queryset().filter(is_published=True)


class Round(models.Model):
    tournament = models.ForeignKey(Tournament, models.CASCADE)
    name = models.CharField(max_length=100)
    winners_count = models.IntegerField()
    users = models.ManyToManyField(
        User,
        help_text='Список пользователей, подписавшихся на уведомления'
    )
    start = models.DateTimeField()
    end = models.DateTimeField()
    is_final = models.BooleanField()
    is_published = models.BooleanField(default=False)

    def is_started(self):
        return self.start < timezone.now()

    def is_running(self):
        return self.start < timezone.now() < self.end

    def is_ended(self):
        return self.end < timezone.now()

    objects = RoundManager()
