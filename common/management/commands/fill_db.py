from django.core.management.base import BaseCommand
from answers.models import UserAnswer
from users.models import User
from rounds.models import Round
import random


class Command(BaseCommand):
    help = ''

    def add_arguments(self, parser):
        parser.add_argument('round_id', nargs='+', type=int)

    def handle(self, *args, **options):
        users = User.objects.all()
        for round_id in options['round_id']:
            round = Round.objects.get(id=round_id)
            for user in users:
                for task in round.task_set.all():
                    UserAnswer.objects.create(
                        task=task,
                        answer='1',
                        user=user,
                        correct=random.choice([True, False])
                    )

            self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"' % round.id))
