from rest_framework import serializers
from .models import UserAnswer
from .services import СheckAnswersService


class UserAnswerSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = UserAnswer
        fields = (
            'id',
            'task',
            'answer'
        )

    def create(self, validated_data):
        user = self.context['request'].user
        answer = validated_data.pop('answer')
        task = validated_data.pop('task')

        try:
            user_answer = UserAnswer.objects.get(user=user, task=task)
            user_answer.answer = answer
            user_answer.save()
        except UserAnswer.DoesNotExist:
            user_answer = UserAnswer.objects.create(
                user=user,
                answer=answer,
                task=task,
            )

        user_answer.correct = СheckAnswersService.check_answer(user_answer)

        return user_answer


class UserAnswerWithCorrectSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = UserAnswer
        fields = (
            'id',
            'task',
            'answer',
            'correct'
        )
