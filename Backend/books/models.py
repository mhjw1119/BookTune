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
    category_name = models.CharField(max_length=30)
    description = models.TextField()
    best_rank = models.IntegerField()
    main_category = models.CharField(max_length=50, null=True, blank=True)
    like_books = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_books')
    
    def like_count(self):
        return self.likes.count()

class Thread_song(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    audio_file = models.FileField(upload_to="user_song/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField()
    likesongs = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_songs')

    def like_count(self):
        return self.like_users.count()
    
class Thread_comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    thread = models.ForeignKey(Thread_song, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
