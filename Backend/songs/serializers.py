from rest_framework import serializers
from .models import CreatedSong


class CreatedSongSerializer(serializers.ModelSerializer):
    audio_file_url = serializers.SerializerMethodField()
    user_username = serializers.SerializerMethodField()
    book_title = serializers.SerializerMethodField()

    class Meta:
        model = CreatedSong
        fields = ['id', 'book', 'prompt', 'audio_file', 'audio_url', 'title', 
                 'duration', 'created_at', 'status', 'audio_file_url', 'user_username', 'book_title']
        read_only_fields = ['id', 'created_at', 'status']

    def get_audio_file_url(self, obj):
        request = self.context.get('request', None)
        if obj.audio_file and request:
            return request.build_absolute_uri(obj.audio_url)
        return obj.audio_url if obj.audio_url else None

    def get_user_username(self, obj):
        return obj.user.username if obj.user else None

    def get_book_title(self, obj):
        return obj.book.title if obj.book else None 