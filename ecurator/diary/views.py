from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Diary
from .serializers import DiarySerializer
from datetime import date

# Create
class DiaryCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = DiarySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_200_OK)

# Update
class DiaryUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            # 오늘 날짜 가져오기
            today = date.today()
            # 주어진 pk와 작성자, 오늘 날짜가 일치하는 일기 가져오기
            diary = Diary.objects.get(pk=pk, author=request.user, created_at__date=today)
        except Diary.DoesNotExist:
            return Response({"error": "Diary not found, not authorized, or not today's diary"}, status=status.HTTP_200_OK)
        
        serializer = DiarySerializer(diary, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_200_OK)

# Detail
class DiaryDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            diary = Diary.objects.get(pk=pk, author=request.user)
        except Diary.DoesNotExist:
            return Response({"error": "Diary not found or not authorized"}, status=status.HTTP_200_OK)
        
        serializer = DiarySerializer(diary)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Delete
class DiaryDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            diary = Diary.objects.get(pk=pk, author=request.user)
        except Diary.DoesNotExist:
            return Response({"error": "Diary not found or not authorized"}, status=status.HTTP_202_ACCEPTED)
        
        diary.delete()
        return Response({"message": "Diary deleted successfully"}, status=status.HTTP_200_OK)

# List
class DiaryListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        diaries = Diary.objects.filter(author=request.user)
        serializer = DiarySerializer(diaries, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
