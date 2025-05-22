from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('categories/', views.book_categories, name='book_categories'),
    path('<str:isbn>/', views.book_detail, name='book_detail'),
    path('<str:isbn>/threads/', views.book_threads, name='book_threads'),
    path('<str:isbn>/threads/create/', views.create_thread, name='create_thread'),
    path('threads/<int:thread_id>/like/', views.like_thread, name='like_thread'),
]
