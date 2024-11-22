from rest_framework import serializers
from .models import *

class MyMoodHistorySerializer(serializers.ModelSerializer):
    emotion_name = serializers.SerializerMethodField()

    class Meta:
        model = MyMoodHistory
        fields = ("emotion_name", "date")

    def get_emotion_name(self, obj):
        return obj.emotion.name