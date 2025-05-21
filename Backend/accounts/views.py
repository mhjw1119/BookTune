from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserSerializer, CustomTokenObtainPairSerializer
from json import loads
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.kakao.views import KakaoOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView

User = get_user_model()

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        # JWT 토큰 생성
        token = CustomTokenObtainPairSerializer.get_token(user)
        refresh_token = str(token)
        access_token = str(token.access_token)
        
        res = Response(
            {
                "user": serializer.data,
                "message": "회원가입에 성공했습니다.",
                "token": {
                    "access": access_token,
                    "refresh": refresh_token,
                },
            },
            status=status.HTTP_200_OK,
        )
        
        return res

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    response = Response({
        "message": "로그아웃되었습니다."
    }, status=status.HTTP_200_OK)
    return response

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    if request.method == 'GET':
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://localhost:5173"  # Vite 기본 포트
    client_class = OAuth2Client

    def get_response(self):
        response = super().get_response()
        if self.user:
            # 필수 필드가 비어있는지 확인
            required_fields = ['nickname']
            empty_fields = [field for field in required_fields if not getattr(self.user, field)]
            
            if empty_fields:
                response.data['requires_additional_info'] = True
                response.data['empty_fields'] = empty_fields
        return response

class KakaoLogin(SocialLoginView):
    adapter_class = KakaoOAuth2Adapter
    callback_url = "http://localhost:5173"  # Vite 기본 포트
    client_class = OAuth2Client

    def get_response(self):
        response = super().get_response()
        if self.user:
            # 필수 필드가 비어있는지 확인
            required_fields = ['nickname']
            empty_fields = [field for field in required_fields if not getattr(self.user, field)]
            
            if empty_fields:
                response.data['requires_additional_info'] = True
                response.data['empty_fields'] = empty_fields
        return response
