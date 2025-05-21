from django.db import models
from django.contrib.auth.models import AbstractUser
from multiselectfield import MultiSelectField

# Create your models here.

class User(AbstractUser):
    MUSIC_GENRES = [
        ('pop', 'Pop'),
        ('rock', 'Rock'),
        ('jazz', 'Jazz'),
        ('hiphop', 'Hip-Hop'),
        ('classical', 'Classical'),
    ]

    BOOK_GENRES = [
        ('fiction', 'Fiction'),
        ('non_fiction', 'Non-Fiction'),
        ('mystery', 'Mystery'),
        ('fantasy', 'Fantasy'),
        ('biography', 'Biography'),
    ]

    provider = models.CharField(max_length=20, null=True, blank=True)
    social_id = models.CharField(max_length=100, null=True, blank=True)
    nickname = models.CharField(max_length=20)
    age = models.IntegerField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    
    # 음악 및 도서 장르 선택 필드
    favorite_music_genres = MultiSelectField(
        choices=MUSIC_GENRES,
        max_choices=5,
        max_length=100,
        null=True,
        blank=True
    )
    
    favorite_book_genres = MultiSelectField(
        choices=BOOK_GENRES,
        max_choices=5,
        max_length=100,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.username