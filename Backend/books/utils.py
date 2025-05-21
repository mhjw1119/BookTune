# books/utils.py
# 알라딘 API로 DB 구축하기.

import requests
from decouple import config
import requests
from pprint import pprint
from .models import Books

ALADIN_API_URL = config('ALADIN_API_URL')
ALADIN_API_KEY = config('ALADIN_API_KEY')


def fetch_and_save_books(total_pages=20, results_per_page=50):
    for page in range(1, total_pages + 1):
        params = {
            'ttbkey': ALADIN_API_KEY,
            'QueryType': 'Bestseller',
            'Cover': 'Big',
            'MaxResults': str(results_per_page),
            'start': str(page),
            'SearchTarget': 'Book',
            'output': 'js',
            'Version': '20131101'
        }

        response = requests.get(ALADIN_API_URL, params=params).json()

        for item in response.get('item', []):
            raw_category = item.get('categoryName', '')
            category_parts = raw_category.split('>')
            category_main = category_parts[1] if len(category_parts) > 1 else ''  # 2번째 항목 추출

            Books.objects.update_or_create(
                isbn=item['isbn'],
                defaults={
                    'title': item['title'],
                    'category_name': category_main,
                    'pubdate': item['pubDate'],
                    'publisher': item['publisher'],
                    'author': item['author'],
                    'description': item['description'],
                    'cover': item['cover'],
                    'customer_review': item['customerReviewRank'],
                    'best_rank': item['bestRank'],
                }
            )
