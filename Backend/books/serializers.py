from rest_framework import serializers
from .models import Books, Thread_song
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'nickname']

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = '__all__'
        read_only_fields = ['isbn']

class ThreadSongSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    like_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    book = BookSerializer(read_only=True)

    class Meta:
        model = Thread_song
        fields = [
            'id', 'user', 'book', 'audio_file', 'created_at',
            'content', 'like_count', 'is_liked'
        ]
        read_only_fields = ['user', 'book', 'created_at']

    def get_like_count(self, obj):
        return obj.likesongs.count()  # 수정됨

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user in obj.likesongs.all()  # 수정됨
        return False