from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core.validators import EmailValidator
import re

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    favorite_genres = serializers.ListField(child=serializers.CharField(), required=False)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'password2', 'nickname', 'favorite_genres')
        extra_kwargs = {
            'password': {'write_only': True},
        }
    
    def validate_username(self, value):
        if len(value) < 4:
            raise serializers.ValidationError("사용자명은 4자 이상이어야 합니다.")
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("이미 사용 중인 사용자명입니다.")
        return value
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("이미 사용 중인 이메일입니다.")
        return value
    
    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("비밀번호는 8자 이상이어야 합니다.")
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError("비밀번호는 최소 1개의 소문자를 포함해야 합니다.")
        if not re.search(r'[0-9]', value):
            raise serializers.ValidationError("비밀번호는 최소 1개의 숫자를 포함해야 합니다.")
        return value
    
    def validate_nickname(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("닉네임은 2자 이상이어야 합니다.")
        return value

    def validate(self, data):
        if data.get('password') != data.get('password2'):
            raise serializers.ValidationError({"password": "비밀번호가 일치하지 않습니다."})
        return data
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # 추가적인 사용자 정보를 토큰에 추가
        token['username'] = user.username
        token['email'] = user.email
        token['nickname'] = user.nickname

        return token 