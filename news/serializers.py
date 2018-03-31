from rest_framework import serializers
from .models import News


class NewsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = News
        fields = (
            'id',
            'header',
            'content',
            'date',
        )
