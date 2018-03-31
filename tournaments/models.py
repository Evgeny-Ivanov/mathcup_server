from django.db import models
from django.utils import timezone


class TournamentManager(models.Manager):
    def running(self):
        return self.get_queryset().filter(is_completed=False)

    def completed(self):
        return self.get_queryset().filter(is_completed=True)

    def published(self):
        return self.get_queryset().filter(is_published=True)


class Tournament(models.Model):
    name = models.CharField(max_length=100)
    create_date = models.DateTimeField(default=timezone.now)
    is_published = models.BooleanField(default=False)

    def is_completed(self):
        round = self.round_set.filter(is_final=True).first()
        return round is not None and round.is_ended()

    objects = TournamentManager()
