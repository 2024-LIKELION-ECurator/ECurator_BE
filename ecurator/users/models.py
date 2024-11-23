from django.contrib.auth.models import AbstractUser
from django.db import models

# 사용할 필드
# username, password는 기본 제공 사용
# nickname, birthdate는 필드 추가 사용
# profile_image는 default로 사용

class CustomUser(AbstractUser):
    nickname = models.CharField(max_length=50, unique=True, blank=False)
    birthdate = models.DateField(null=True, blank=False)
    profile_image = models.ImageField(
        upload_to='profile_images/', 
        default='profile_images/default.png'
    )

    def __str__(self):
        return self.username
