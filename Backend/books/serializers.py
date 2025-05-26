from rest_framework import serializers
from .models import Books, Thread_song, Thread_comment
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'nickname', 'profile_image']

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
        return obj.likesongs.count()

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user in obj.likesongs.all()
        return False
    
class ThreadCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Thread_comment
        fields = ['id', 'user', 'thread', 'content', 'created_at', 'updated_at']
        read_only_fields = ['user', 'thread', 'created_at', 'updated_at']

class ThreadCommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread_comment
        fields = ['content']
        read_only_fields = ['user', 'thread']