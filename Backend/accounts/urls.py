from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('logout/', views.logout, name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # 소셜 로그인
    path('google/login/', views.GoogleLogin.as_view(), name='google_login'),
    path('kakao/login/', views.KakaoLogin.as_view(), name='kakao_login'),
] 