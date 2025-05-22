from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

# 인증 관련 URL 패턴
auth_patterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('logout/', views.logout, name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # 소셜 로그인
    path('google/', views.GoogleLogin.as_view(), name='google_login'),
    path('kakao/', views.KakaoLogin.as_view(), name='kakao_login'),
]

# 사용자 관련 URL 패턴
user_patterns = [
    path('profile/', views.user_profile, name='user_profile'),
    path('profile/update/', views.user_profile, name='user_profile_update'),
]

urlpatterns = auth_patterns + user_patterns 