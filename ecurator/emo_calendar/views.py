from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import *
from .serializers import *
from .utils import *

"""
- 작성자 연결
- 감정 update
- 다이어리 끌어오기
- is authen
- 응답코드
"""

class MyMoodHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, year, month):
        emotions = MyMoodHistory.objects.filter(
            author=request.user,
            date__year=year,
            date__month=month
        )

        serializer = MyMoodHistorySerializer(emotions, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        emotion_name = request.data.get('emotion')
        date = request.data.get('date')

        try:
            emotion = Emotion.objects.get(name=emotion_name)
        except Emotion.DoesNotExist:
            return Response({"error": "존재하지 않는 감정입니다."}, status=status.HTTP_404_NOT_FOUND)

        # 현재 로그인한 사용자의 해당 날짜 감정 기록 조회
        user_mood_history = MyMoodHistory.objects.filter(author=request.user, date=date)

        if user_mood_history.exists():
            return Response({"error": "해당 날짜에 이미 감정이 기록되어 있습니다."}, status=status.HTTP_400_BAD_REQUEST)

        # 감정 기록 생성 및 저장
        mood_history = MyMoodHistory(author=request.user, emotion=emotion, date=date)
        mood_history.save()

        serializer = MyMoodHistorySerializer(mood_history)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# movie api
class StoreAllMovies(APIView):
    def post(self, request):
        emotions = ["happy", "sad", "surprised", "loving", "sleepy", "nervous", "pensive", "relieved", "joyful"]
        for emotion in emotions:
            fetch_and_store_movies(emotion)
        return Response({"message": "Movies for all emotions have been fetched and stored."})

# music api
class FetchAllMusicView(APIView):
    def post(self, request, *args, **kwargs):
        fetch_and_store_all_music()  # 모든 감정에 대한 음악을 가져오기
        return Response({'message': 'Successfully fetched music for all emotions.'}, status=status.HTTP_200_OK)

# book api
class FetchAllBookView(APIView):
    def post(self, request, *args, **kwargs):
        fetch_and_store_books()  # 모든 감정에 대한 음악을 가져오기
        return Response({'message': 'Successfully fetched books for all emotions.'}, status=status.HTTP_200_OK)