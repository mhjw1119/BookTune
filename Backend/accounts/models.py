from django.db import models
from django.contrib.auth.models import AbstractUser
from multiselectfield import MultiSelectField

# Create your models here.

class User(AbstractUser):
    provider = models.CharField(max_length=20, null=True, blank=True)
    social_id = models.CharField(max_length=100, null=True, blank=True)
    nickname = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=100)
    

class UserProfile(models.Model):
    like_category = models.ManyToManyField(Category, related_name='like_category')
    like_book = models.ManyToManyField(Book, related_name='like_book')
    like_song = models.ManyToManyField(Song, related_name='like_song')

