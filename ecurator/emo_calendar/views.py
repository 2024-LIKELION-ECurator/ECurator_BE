from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

from .models import *
from .serializers import *

"""
- 작성자 연결
- 하루에 하나의 감정만 등록 가능하도록
- 감정 update
- 다이어리 끌어오기
"""

class MyMoodHistoryView(APIView):

    def get(self, request, year, month):
        emotions = MyMoodHistory.objects.filter(Q(date__year=year) & Q(date__month=month))
        serializer = MyMoodHistorySerializer(emotions, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        emotion_name = request.data.get('emotion')
        date = request.data.get('date')

        try:
            emotion = Emotion.objects.get(name=emotion_name)
        except Emotion.DoesNotExist:
            return Response({"error": "존재하지 않는 감정입니다."}, status=status.HTTP_404_NOT_FOUND)

        mood_history = MyMoodHistory(emotion=emotion, date=date)
        mood_history.save()

        serializer = MyMoodHistorySerializer(mood_history)
        return Response(serializer.data, status=status.HTTP_201_CREATED)