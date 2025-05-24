from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from .models import Books, Thread_song
from .serializers import BookSerializer, ThreadSongSerializer
# from .recommendation import recommend_books_word2vec
# Create your views here.

@api_view(['GET'])
def book_list(request):
    books = Books.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def book_detail(request, isbn):
    book = get_object_or_404(Books, isbn=isbn)
    serializer = BookSerializer(book)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def book_categories(request):
    categories = Books.objects.values_list('category_name', flat=True).distinct()
    return Response(list(categories))

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_thread(request, isbn):
    book = get_object_or_404(Books, isbn=isbn)
    serializer = ThreadSongSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save(user=request.user, book=book)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def book_threads(request, isbn):
    book = get_object_or_404(Books, isbn=isbn)
    threads = Thread_song.objects.filter(book=book)
    serializer = ThreadSongSerializer(threads, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_thread(request, thread_id):
    thread = get_object_or_404(Thread_song, id=thread_id)
    if request.user in thread.like_users.all():
        thread.like_users.remove(request.user)
        return Response({'status': 'unliked'})
    else:
        thread.like_users.add(request.user)
        return Response({'status': 'liked'})
    
# @api_view(['GET'])
# def get_word2vec_recommendations(request):
#     user = request.user
#     recommended_books = recommend_books_word2vec(user)
#     serializer = BookSerializer(recommended_books, many=True)
#     return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_book(request, isbn):
    book = Books.objects.get(isbn=isbn)
    if request.user in book.like_books.all():
        book.like_books.remove(request.user)
        return Response({'status': 'unliked'}, status=status.HTTP_200_OK)
    else:
        book.like_books.add(request.user)
        return Response({'status': 'liked'}, status=status.HTTP_200_OK)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def liked_books(request):
    books = Books.objects.filter(like_books=request.user)
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def liked_threads(request):
    threads = Thread_song.objects.filter(like_users=request.user)
    serializer = ThreadSongSerializer(threads, many=True, context={'request': request})
    return Response(serializer.data)
