from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    answer = serializers.CharField(write_only=True)

    class Meta:
        model = Task
        fields = ('id', 'text', 'answer')


class TaskSerializerWithAnswer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'text', 'answer')
