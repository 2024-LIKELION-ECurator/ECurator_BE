from django.urls import path
from .views import (
    DiaryCreateView, DiaryUpdateView, DiaryDetailView,
    DiaryDeleteView, DiaryListView
)

urlpatterns = [
    path('create/', DiaryCreateView.as_view(), name='diary-create'),
    path('detail/<int:pk>/', DiaryDetailView.as_view(), name='diary-detail'),
    path('update/<int:pk>/', DiaryUpdateView.as_view(), name='diary-update'),
    path('delete/<int:pk>/', DiaryDeleteView.as_view(), name='diary-delete'),
    path('list/', DiaryListView.as_view(), name='diary-list'),
]
