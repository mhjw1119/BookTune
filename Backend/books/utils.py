# books/utils.py
# 알라딘 API로 DB 구축하기.

import requests
from decouple import config
import requests
from pprint import pprint
from .models import Books
from openai import OpenAI

ALADIN_API_URL = config('ALADIN_API_URL')
ALADIN_API_KEY = config('ALADIN_API_KEY')
OPENAI_API_KEY = config('OPENAI_API_KEY')

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

from openai import OpenAI

client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """
너는 책 소개를 바탕으로 차분하고 감각적인 음악을 추천해주는 어시스턴트야.
조건1 : 유튜브 라이브 링크는 제외할 것.
조건2 : {URL : https://www.youtube.com/watch?v=oWbXyiwXFLc} 형식으로만 답변할 것.
조건3 : 답변은 부가적인 설명 없이 조건2 형식으로만 할 것.
"""

def get_music_url_from_openai(book_intro: str) -> str:
    user_prompt = f"책 소개 : {book_intro}"
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # 또는 "gpt-3.5-turbo"
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT.strip()},
            {"role": "user", "content": user_prompt.strip()},
        ],
        temperature=0.7,
    )

    content = response.choices[0].message.content.strip()
    return content if "https://www.youtube.com/watch" in content else ""

def update_books_with_recommended_song():
    books = Books.objects.all()
    for book in books:
        if not book.recommended_song:
            intro = book.description if book.description else book.title
            url = get_music_url_from_openai(intro)
            if url:
                book.recommended_song = url
                book.save()
