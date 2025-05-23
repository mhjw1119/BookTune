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
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_books', blank=True, null=True)
    
    def like_count(self):
        return self.likes.count()

class Thread_song(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    song = models.ForeignKey(CreatedSong, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=50)
    content = models.TextField()
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_songs', blank=True)

    def like_count(self):
        return self.like_users.count()
