import requests
import logging
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserSerializer, CustomTokenObtainPairSerializer, ProfileSerializer
from .utils import get_or_create_social_user, generate_jwt_for_user
from decouple import config
from django.shortcuts import get_object_or_404

KAKAO_CLIENT_ID = config('KAKAO_CLIENT_ID')
KAKAO_SECRET = config('KAKAO_SECRET')
GOOGLE_CLIENT_ID = config('GOOGLE_CLIENT_ID')
GOOGLE_SECRET = config('GOOGLE_SECRET')


logger = logging.getLogger(__name__)
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
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        serializer = UserSerializer(
            request.user, 
            data=request.data, 
            partial=True, 
            context={'request': request}
        )
        if serializer.is_valid(raise_exception=True):
            # 파일이 있으면 직접 할당
            if 'profile_image' in request.FILES:
                request.user.profile_image = request.FILES['profile_image']
                request.user.save()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    serializer = ProfileSerializer(user, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.user in user.followers.all():
        user.followers.remove(request.user)
        return Response({'status': 'unfollowed'}, status=status.HTTP_200_OK)
    else:
        user.followers.add(request.user)
        return Response({'status': 'followed'}, status=status.HTTP_200_OK)



class KakaoLoginView(APIView):
    def post(self, request):
        code = request.data.get("code")
        redirect_uri = "http://localhost:5173/auth/kakao/callback"

        # 1. 카카오 토큰 요청
        token_res = requests.post("https://kauth.kakao.com/oauth/token", data={
            "grant_type": "authorization_code",
            "client_id": KAKAO_CLIENT_ID,
            "redirect_uri": redirect_uri,
            "code": code
        })

        print("🔴 Kakao Token Response:", token_res.text)

        token_data = token_res.json()
        access_token = token_data.get("access_token")

        if not access_token:
            return Response({"error": "Token request failed"}, status=status.HTTP_400_BAD_REQUEST)

        # 2. 사용자 정보 요청
        user_res = requests.get("https://kapi.kakao.com/v2/user/me", headers={
            "Authorization": f"Bearer {access_token}"
        })
        user_data = user_res.json()

        print("🔵 Kakao User Info:", user_data)

        kakao_id = user_data.get("id")
        email = user_data.get("kakao_account", {}).get("email")

        if not email:
            return Response({"error": "이메일 제공에 동의해야 합니다."}, status=status.HTTP_400_BAD_REQUEST)

        # # 카카오 설정에서 진짜 이메일 받아오는 거 해야할 듯 -> 유찬 사업자등록..
        # ### 이메일이 없으면 임시 이메일 생성
        # if not email:
        #     email = f"kakao_{kakao_id}@example.com"
        #     print("⚠️ 이메일이 없어 임시 이메일 사용:", email)
        # ###

        user = get_or_create_social_user("kakao", kakao_id, email)
        tokens = generate_jwt_for_user(user)

        return Response(tokens, status=200)


# 구글 로그인 관련
class GoogleLoginView(APIView):
    def post(self, request):
        code = request.data.get("code")
        redirect_uri = "http://localhost:5173/auth/google/callback"

        # 1. 토큰 요청
        token_res = requests.post("https://oauth2.googleapis.com/token", data={
            "code": code,
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_SECRET,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code",
        })

        print("🔴 Google Token Response:", token_res.text)

        token_json = token_res.json()
        access_token = token_json.get("access_token")

        # 2. 사용자 정보 요청
        user_res = requests.get("https://www.googleapis.com/oauth2/v2/userinfo", headers={
            "Authorization": f"Bearer {access_token}"
        })
        user_data = user_res.json()

        print("🔵 Google User Info:", user_data)

        google_id = user_data.get('id')
        email = user_data.get("email")

        user = get_or_create_social_user("google", google_id, email)
        tokens = generate_jwt_for_user(user)

        return Response(tokens, status=status.HTTP_200_OK)