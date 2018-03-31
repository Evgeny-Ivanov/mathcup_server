from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings
from django.core.cache import caches
from application.celery import app

cache_sign_up = caches['sign_up']


@app.task
def send_verification_email(email):
    confirmation_key = get_random_string()
    timeout = 60 * 60 * 3  # 3 часа
    cache_sign_up.set(email, confirmation_key, timeout)

    message = '''
        Вы получили это письмо, потому что ваш адрес электронной почты был указан при регистрации на сайте математической олимпиады MathCup.
        Чтобы подтвердить регистрацию, воспользуйтесь кодом <b>%s</b>  в течении 3х часов
    '''

    send_mail(
        'Пожалуйста, подтвердите свою регистрацию',
        message % confirmation_key,
        settings.DEFAULT_FROM_EMAIL,
        [email],
        html_message=message % confirmation_key
    )
