from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
import random
from datetime import date

from .models import *
from .serializers import *
from .utils import *
from diary.models import Diary

# 캘린더/메인페이지
class MyMoodHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, year, month):
        emotions = MyMoodHistory.objects.filter(
            author=request.user,
            date__year=year,
            date__month=month
        ).order_by('date')

        diaries = Diary.objects.filter(
            author=request.user,
            created_at__year=year,
            created_at__month=month
        )

        emo_serializer = MyMoodHistorySerializer(emotions, many=True)
        dia_serializer = MyDiarySerializer(diaries, many=True)

        response = {
            "emotion": emo_serializer.data,
            "diary": dia_serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request):
        emotion_name = request.data.get('emotion')
        date = request.data.get('date')

        try:
            emotion = Emotion.objects.get(name=emotion_name)
        except Emotion.DoesNotExist:
            return Response({"error": "존재하지 않는 감정입니다."}, status=status.HTTP_202_ACCEPTED)

        # 현재 로그인한 사용자의 해당 날짜 감정 기록 조회
        user_mood_history = MyMoodHistory.objects.filter(author=request.user, date=date)

        if user_mood_history.exists():
            return Response({"error": "해당 날짜에 이미 감정이 기록되어 있습니다."}, status=status.HTTP_202_ACCEPTED)

        # 감정 기록 생성 및 저장
        mood_history = MyMoodHistory(author=request.user, emotion=emotion, date=date)
        mood_history.save()

        serializer = MyMoodHistorySerializer(mood_history)
        return Response({"id": mood_history.id, "data": serializer.data}, status=status.HTTP_201_CREATED)

    def put(self, request, id):
        try:
            mood_history = MyMoodHistory.objects.get(id=id, author=request.user)
        except MyMoodHistory.DoesNotExist:
            return Response({"error": "해당 감정 기록이 존재하지 않거나, 접근할 수 없습니다."}, status=status.HTTP_202_ACCEPTED)

        # 수정 가능한 날짜가 오늘인지 확인
        if mood_history.date != date.today():
            return Response({"error": "오늘 작성한 감정만 수정할 수 있습니다."}, status=status.HTTP_202_ACCEPTED)

        emotion_name = request.data.get('emotion')

        try:
            emotion = Emotion.objects.get(name=emotion_name)
        except Emotion.DoesNotExist:
            return Response({"error": "존재하지 않는 감정입니다."}, status=status.HTTP_202_ACCEPTED)

        # 감정 기록 업데이트
        mood_history.emotion = emotion
        mood_history.save()

        serializer = MyMoodHistorySerializer(mood_history)
        return Response(serializer.data, status=status.HTTP_200_OK)

# 메인 페이지
class MainView(APIView):
    permission_classes = [AllowAny]  # 모든 사용자 접근 가능

    def get(self, request):
        emotions = Emotion.objects.all()
        serializer = MainSerializer(emotions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        emotion_name = request.data.get('emotion')
        today_date = date.today()  # 현재 날짜 가져오기

        try:
            emotion = Emotion.objects.get(name=emotion_name)
        except Emotion.DoesNotExist:
            return Response({"error": "존재하지 않는 감정입니다."}, status=status.HTTP_202_ACCEPTED)

        # 현재 로그인한 사용자의 해당 날짜 감정 기록 조회
        user_mood_history = MyMoodHistory.objects.filter(author=request.user, date=today_date)

        if user_mood_history.exists():
            return Response({"error": "해당 날짜에 이미 감정이 기록되어 있습니다."}, status=status.HTTP_202_ACCEPTED)

        # 감정 기록 생성 및 저장
        mood_history = MyMoodHistory(
            author=request.user if request.user.is_authenticated else None,
            emotion=emotion,
            date=today_date
        )
        mood_history.save()

        serializer = MyMoodHistorySerializer(mood_history)
        return Response({"id": mood_history.id, "data": serializer.data}, status=status.HTTP_201_CREATED)

# 메인 콘텐츠
class MainContentView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, emotion):
        # 감정이 유효한지 확인
        if not Emotion.objects.filter(name=emotion).exists():
            return Response({"error": "Invalid emotion."}, status=status.HTTP_202_ACCEPTED)

        movies = Movie.objects.filter(emotion__name=emotion)
        musics = Music.objects.filter(emotion__name=emotion)
        books = Book.objects.filter(emotion__name=emotion)

        if not movies and not musics and not books:
            raise NotFound("No content found for this emotion.")

        # 랜덤 샘플링 (최대 4개)
        movie_list = random.sample(list(movies), min(4, movies.count())) if movies else []
        music_list = random.sample(list(musics), min(4, musics.count())) if musics else []
        book_list = random.sample(list(books), min(4, books.count())) if books else []

        movie_serializer = MovieSerializer(movie_list, many=True)
        music_serializer = MusicSerializer(music_list, many=True)
        book_serializer = BookSerializer(book_list, many=True)

        response = {
            "emotion": emotion,
            "musics": music_serializer.data,
            "movies": movie_serializer.data,
            "books": book_serializer.data
        }

        return Response(response, status=status.HTTP_200_OK)

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