import random
from django.core.management.base import BaseCommand
from answers.models import UserAnswer
from users.models import User
from rounds.models import Round


class Command(BaseCommand):
    help = ''

    def add_arguments(self, parser):
        parser.add_argument('round_id', nargs='+', type=int)

    def handle(self, *args, **options):
        for round_id in options['round_id']:
            users = User.objects.all()
            round = Round.objects.get(id=round_id)
            if round.is_final:
                users = round.users

            for user in users:
                for task in round.task_set.all():
                    correct = random.choice([True, False])
                    answer = '¯\_(ツ)_/¯'
                    if correct:
                        answer = task.answer
                    UserAnswer.objects.create(
                        task=task,
                        answer=answer,
                        user=user,
                        correct=correct
                    )

            self.stdout.write(self.style.SUCCESS('Раунд "%s" успешно заполнен' % round.id))
