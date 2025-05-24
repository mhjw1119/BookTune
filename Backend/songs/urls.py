from django.urls import path, include
from . import views

urlpatterns = [
    path('generate/', views.generate_music, name='generate-music'),
    path('callback/', views.suno_webhook_callback, name='callback'),
    path('song_list/', views.get_user_songs, name='get_user_songs'),
]
