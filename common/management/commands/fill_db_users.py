import random
from django.core.management.base import BaseCommand
from mimesis import Person
from mimesis.enums import Gender
from users.models import User


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        person = Person('ru')
        for i in range(25):
            gender = random.choice([Gender.FEMALE, Gender.MALE])
            user = User.objects.create_user(
                email=person.email(),
                password='12345'
            )

            user.first_name = person.name(gender=gender)
            user.last_name = person.last_name(gender=gender)

            user.save()

        self.stdout.write(self.style.SUCCESS('Пользователи успешно созданы'))
