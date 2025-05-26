# save_books_json.py

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BookTune.settings')  # 설정 파일 경로 맞게 수정
django.setup()

import json
from books.models import Books

# 모든 책 데이터 가져오기
books = Books.objects.all()

# 필요한 필드만 선택하여 데이터 구성
books_data = []
for book in books:
    book_dict = {
        'model': 'books.books',
        'pk': book.pk,
        'fields': {
            'isbn': book.isbn,
            'cover': book.cover,
            'title': book.title,
            'author': book.author,
            'publisher': book.publisher,
            'pubdate': book.pubdate.strftime('%Y-%m-%d'),
            'customer_review': book.customer_review,
            'recommended_song': book.recommended_song,
            'category_name': book.category_name,
            'description': book.description,
            'best_rank': book.best_rank,
            'main_category': book.main_category
        }
    }
    books_data.append(book_dict)

# JSON 파일로 저장
with open("books.json", "w", encoding="utf-8") as f:
    json.dump(books_data, f, ensure_ascii=False, indent=4)
