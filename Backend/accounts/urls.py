from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

# 인증 관련 URL 패턴
auth_patterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('logout/', views.logout, name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # 소셜 로그인
    path('social/google/', views.GoogleLoginView.as_view(), name='google_login'),
    path('social/kakao/', views.KakaoLoginView.as_view(), name='kakao_login'),
]

# 사용자 관련 URL 패턴
user_patterns = [
    path('profile/', views.user_profile, name='user_profile'),
    path('profile/update/', views.user_profile, name='user_profile_update'),
    path('profile/<int:user_id>/', views.user_profile_detail, name='user_profile_detail'),
    path('<int:user_id>/follow/', views.follow, name='follow'),
]

urlpatterns = auth_patterns + user_patterns 