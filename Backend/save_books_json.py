# save_books_json.py

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BookTune.settings')  # 설정 파일 경로 맞게 수정
django.setup()

import json
from django.core.serializers import serialize
from books.models import Books

data = serialize('json', Books.objects.all())
parsed = json.loads(data)

with open("books_hangul.json", "w", encoding="utf-8") as f:
    json.dump(parsed, f, ensure_ascii=False, indent=4)
