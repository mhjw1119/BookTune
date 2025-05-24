from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from books.models import Book
User = get_user_model()

# Create your models here.

class CreatedSong(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, blank=True, help_text="음악이 생성된 책")
    task_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    prompt = models.TextField(help_text="음악 생성을 위한 프롬프트")
    audio_file = models.FileField(upload_to="aisong/", blank=True, null=True)
    audio_url = models.URLField(help_text="Suno API에서 제공하는 원본 오디오 URL", null=True, blank=True)
    title = models.CharField(max_length=255, help_text="음악 제목", null=True, blank=True)
    duration = models.FloatField(help_text="음악 길이(초)", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', '생성 대기중'),
            ('processing', '생성 중'),
            ('completed', '생성 완료'),
            ('failed', '생성 실패')
        ],
        default='pending'
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title or 'Untitled'} - {self.user.username}"

