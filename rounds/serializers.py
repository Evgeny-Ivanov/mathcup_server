from rest_framework import serializers
from tasks.models import Task
from users.serializers import UserSerializer
from tasks.serializers import TaskSerializer
from .models import Round
from .services import RoundHelpersService


class RoundSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    tasks = TaskSerializer(many=True, source='task_set', write_only=True)
    is_join = serializers.SerializerMethodField(read_only=True)

    def get_is_join(self, round):
        request = self.context.get('request')
        return request.user in round.users.all()

    class Meta:
        model = Round
        fields = (
            'id',
            'tournament',
            'name',
            'winners_count',
            'start',
            'end',
            'is_final',
            'tasks',
            'is_join',
            'is_published',
        )

    def create(self, validated_data):
        task_set = validated_data.pop('task_set', [])
        round = Round.objects.create(**validated_data)

        for task_data in task_set:
            Task.objects.create(round=round, **task_data)

        if round.is_final:
            RoundHelpersService.configure_final_round(round)

        RoundHelpersService.configure_notifications(round)

        return round


class RoundRatingSerializer(serializers.Serializer):
    place = serializers.IntegerField()
    user = UserSerializer()
    score = serializers.IntegerField()


class UserScoreSerializer(serializers.Serializer):
    score = serializers.IntegerField()
