from rest_framework import serializers
from .models import CreatedSong


class CreatedSongSerializer(serializers.ModelSerializer):
    audio_file_url = serializers.SerializerMethodField()
    user_username = serializers.SerializerMethodField()
    book_title = serializers.SerializerMethodField()

    class Meta:
        model = CreatedSong
        fields = [
            'id',
            'user',
            'user_username',
            'book',
            'book_title',
            'task_id',
            'prompt',
            'audio_file',
            'audio_file_url',
            'audio_url',
            'title',
            'duration',
            'created_at',
            'status'
        ]
        read_only_fields = ['id', 'created_at', 'status', 'task_id']

    def get_audio_file_url(self, obj):
        if obj.audio_file:
            return self.context['request'].build_absolute_uri(obj.audio_file.url)
        return None

    def get_user_username(self, obj):
        return obj.user.username if obj.user else None

    def get_book_title(self, obj):
        return obj.book.title if obj.book else None 