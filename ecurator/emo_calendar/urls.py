from django.urls import path
from .views import *

urlpatterns = [
    path('emotion-history/<int:year>/<int:month>/', MyMoodHistoryView.as_view()),
    path('emotion-history/', MyMoodHistoryView.as_view()),
    path('emotion-history/<int:id>/', MyMoodHistoryView.as_view()),
    path('store-all-movies/', StoreAllMovies.as_view()),
    path('fetch-all-music/', FetchAllMusicView.as_view(), name='fetch_all_music'),
    path('fetch-all-book/', FetchAllBookView.as_view(), name='fetch_all_book'),
    path('main/', MainView.as_view()),
    path('main/<str:emotion>/', MainContentView.as_view(), name='main-content'),
]