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
        fields = [
            'isbn', 'cover', 'title', 'author', 'publisher',
            'pubdate', 'customer_review', 'recommended_song',
            'category_name', 'description', 'best_rank',
            'main_category'
        ]

class ThreadSongSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    like_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    book = BookSerializer(read_only=True)

    class Meta:
        model = Thread_song
        fields = [
            'id', 'user', 'book', 'song', 'created_at',
            'title', 'content', 'like_count', 'is_liked'
        ]
        read_only_fields = ['user', 'book', 'created_at']

    def get_like_count(self, obj):
        return obj.like_users.count()

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user in obj.like_users.all()
        return False

    def create(self, validated_data):
        # song 필드는 request.data에서 직접 받아야 함
        song_id = self.context.get('request').data.get('song')
        if not song_id:
            raise serializers.ValidationError({'song': 'This field is required.'})
        
        validated_data['song_id'] = song_id
        return super().create(validated_data) 