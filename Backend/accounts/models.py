from django.db import models
from django.contrib.auth.models import AbstractUser
from multiselectfield import MultiSelectField

# Create your models here.

# 장르 선택지
GENRE_CHOICES = [
    ('문학', '문학'),
    ('인문/사회', '인문/사회'),
    ('자기계발/실용', '자기계발/실용'),
    ('예술/문화', '예술/문화'),
    ('학습/교육', '학습/교육'),
    ('아동/청소년', '아동/청소년'),
    ('만화', '만화'),
]

class User(AbstractUser):
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers')
    provider = models.CharField(max_length=20, null=True, blank=True)
    social_id = models.CharField(max_length=100, null=True, blank=True)
    nickname = models.CharField(max_length=20, default='콩콩이든')
    email = models.EmailField(max_length=100)
    favorite_genres = models.JSONField(default=list, blank=True)  # 여러 장르 저장
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)