from rest_framework import serializers
from .models import *

class MyMoodHistorySerializer(serializers.ModelSerializer):
    emotion_name = serializers.SerializerMethodField()

    class Meta:
        model = MyMoodHistory
        fields = ("emotion_name", "date")

    def get_emotion_name(self, obj):
        return obj.emotion.name

class MusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = ("title", "author")

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ("title", "author")

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("title", "author")

class MainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emotion
        fields = ["name"]