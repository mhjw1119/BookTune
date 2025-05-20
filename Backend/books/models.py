from django.db import models
from django.conf import settings
from songs.models import CreatedSong
# Create your models here.


class Books(models.Model):
    isbn = models.CharField(max_length=15)
    cover = models.URLField()
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    publisher = models.CharField(max_length=50)
    pubdate = models.DateField()
    customer_review = models.IntegerField()
    recommended_song = models.URLField(blank=True, null=True)

class Thread_song(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_songs')
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    song = models.ForeignKey(CreatedSong, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=50)
    content = models.TextField()