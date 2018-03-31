from django.core.mail import send_mail
from django.conf import settings
from application.celery import app
from .models import Round


@app.task
def send_notification_mail(round_id):
    round = Round.objects.get(id=round_id)
    emails = []
    for user in round.users.all():
        emails.append(user.email)

    start = round.start.strftime("%d.%m.%y %H:%M")
    send_mail(
        'Напоминание',
        'Раунд %s начнется %s по Москве' % (round.name, start),
        settings.DEFAULT_FROM_EMAIL,
        emails
    )


@app.task
def send_join_round_mail(round_name, email):
    send_mail(
        'Регистрация на раунд',
        '''
        Вы записались на ранд %s.
        Мы заблаговременно уведомим вас о начале раунда.

        С уважением, Администрация сайта MathCup
        ''' % (round_name),
        settings.DEFAULT_FROM_EMAIL,
        [email]
    )
