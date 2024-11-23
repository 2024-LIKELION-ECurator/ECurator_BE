# diary/serializers.py
from rest_framework import serializers
from .models import Diary

class DiarySerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Diary
        fields = ['id', 'author', 'title', 'content', 'created_at', 'updated_at']
