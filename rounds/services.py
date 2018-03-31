from django.db.models import Sum, Case, When, F
from django.utils import timezone
from answers.models import UserAnswer
from users.models import User
from .tasks import send_notification_mail


class RoundSummarizeService(object):
    @staticmethod
    def score_expression():
        return Sum(Case(
            When(correct=True, then=F('task__weight')),
            When(correct=False, then=0)
        ))

    @staticmethod
    def get_round_rating(round):
        # Очень сложный запрос - возможно нужно написать сырой запрос
        user_answers = UserAnswer.objects.filter(task__round=round)

        queryset = user_answers\
            .values('user')\
            .annotate(score=RoundSummarizeService.score_expression())\
            .order_by('-score')

        rating = []
        place = 1
        previous_item = None
        for item in queryset:
            if item['score'] == 0:
                break

            if previous_item is not None and previous_item['score'] != item['score']:
                place += 1

            item['place'] = place
            item['user'] = User.objects.get(pk=item['user'])
            rating.append(item)

            if len(rating) > round.winners_count and previous_item['score'] != item['score']:
                break

            previous_item = item

        return rating

    @staticmethod
    def get_user_score(round, user):
        user_answers = UserAnswer.objects.filter(task__round=round, user=user)
        return user_answers.aggregate(score=RoundSummarizeService.score_expression())


class RoundHelpersService(object):
    @staticmethod
    def configure_notifications(round):
        time_left_seconds = (round.start - timezone.now()).total_seconds()
        hour = 60 * 60

        countdown_hour = time_left_seconds - hour
        countdown_day = time_left_seconds - 24 * hour

        if countdown_hour > 0:
            send_notification_mail.apply_async(
                [round.id],
                countdown=countdown_hour,
                expires=countdown_hour + hour
            )

        if countdown_day > 0:
            send_notification_mail.apply_async(
                [round.id],
                countdown=countdown_day,
                expires=countdown_day + 12 * hour
            )

    @staticmethod
    def configure_final_round(round):
        for item_round in round.tournament.round_set.all():
            rating = RoundSummarizeService.get_round_rating(item_round)
            for user_result in rating:
                round.users.add(user_result['user'])
