from rest_framework import serializers
from .models import Tournament


class TournamentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    is_completed = serializers.BooleanField(read_only=True)

    class Meta:
        model = Tournament
        fields = (
            'id',
            'name',
            'is_completed',
            'is_published',
        )
