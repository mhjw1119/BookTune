from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('categories/', views.book_categories, name='book_categories'),
    path('liked/', views.liked_books, name='liked_books'),
    path('threads/', views.thread_list, name='thread_list'),
    path('threads/<int:thread_id>/', views.thread_detail, name='thread_detail'),
    path('threads/<int:thread_id>/like/', views.like_thread, name='like_thread'),
    path('threads/<int:thread_id>/like-status/', views.thread_like_status, name='thread_like_status'),
    path('threads/<int:thread_id>/comments/', views.thread_comments, name='thread_comments'),
    path('threads/<int:thread_id>/comments/<int:comment_id>/delete/', views.delete_thread_comment, name='delete_thread_comment'),
    path('threads/<int:thread_id>/comments/create/', views.create_thread_comment, name='create_thread_comment'),
    path('threads/liked/', views.liked_threads, name='liked_threads'),
    path('recommendations/', views.get_word2vec_recommendations, name='get_word2vec_recommendations'),
    path('<str:isbn>/', views.book_detail, name='book_detail'),
    path('<str:isbn>/likes/', views.like_book, name='like_book'),
    path('<str:isbn>/like-status/', views.book_like_status, name='book_like_status'),
    path('<str:isbn>/threads/', views.book_threads, name='book_threads'),
    path('<str:isbn>/threads/create/', views.create_thread, name='create_thread'),
    path('threads/<int:thread_id>/update/', views.update_thread, name='update_thread'),
    path('threads/<int:thread_id>/delete/', views.delete_thread, name='delete_thread'),
]
