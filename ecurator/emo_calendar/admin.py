from django.contrib import admin
from .models import *

admin.site.register(MyMoodHistory)
admin.site.register(Emotion)
admin.site.register(Movie)
admin.site.register(Music)
admin.site.register(Book)