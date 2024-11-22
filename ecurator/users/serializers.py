from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import ValidationError

User = get_user_model()

# 회원가입, 로그인
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'nickname', 'birthdate']

    def validate_password(self, value):
        try:
            validate_password(value)  # Django의 비밀번호 검증 함수
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            nickname=validated_data['nickname'],
            birthdate=validated_data['birthdate']
        )
        return user
    
# 마이페이지
class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['profile_image', 'nickname', 'birthdate']
