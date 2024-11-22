from django.urls import path
from .views import *

urlpatterns = [
    path('emotion-history/<int:year>/<int:month>/', MyMoodHistoryView.as_view()),
    path('emotion-history/', MyMoodHistoryView.as_view()),
    path('store-all-movies/', StoreAllMovies.as_view()),
]