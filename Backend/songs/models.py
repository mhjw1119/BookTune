from django.db import models
from django.conf import settings

# Create your models here.

class CreatedSong(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    audio_file = models.FileField(upload_to="aisong/", blank=True, null=True)