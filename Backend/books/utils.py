# books/utils.py
# 알라딘 API로 DB 구축하기.

import requests
from decouple import config
import requests
from pprint import pprint
from .models import Books
from openai import OpenAI
from django.db.models import Q

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

            # description이 비어있지 않은 경우에만 저장
            if item.get('description'):
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

def remove_books_without_description():
    """
    description이 비어있는 책들을 삭제하는 함수
    비어있는 경우: None, '', 공백문자로만 이루어진 경우
    """
    # Q 객체를 사용하여 description이 None이거나 빈 문자열이거나 공백만 있는 경우를 모두 처리
    empty_books = Books.objects.filter(
        Q(description__isnull=True) |  # None인 경우
        Q(description='') |            # 빈 문자열인 경우
        Q(description__regex=r'^\s*$') # 공백만 있는 경우
    )
    
    # 삭제될 책의 수를 저장
    deleted_count = empty_books.count()
    
    # 책 삭제
    empty_books.delete()
    
    return {
        'deleted_count': deleted_count,
        'message': f'{deleted_count}개의 description이 비어있는 책이 삭제되었습니다.'
    }

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

CATEGORY_MAPPING = {
    '소설/시/희곡': '문학',
    '에세이': '문학',
    '고전': '문학',
    '인문학': '인문/사회',
    '사회과학': '인문/사회',
    '역사': '인문/사회',
    '종교/역학': '인문/사회',
    '자기계발': '자기계발/실용',
    '경제경영': '자기계발/실용',
    '요리/살림': '자기계발/실용',
    '건강/취미': '자기계발/실용',
    '예술/대중문화': '예술/문화',
    '여행': '예술/문화',
    '수험서/자격증': '학습/교육',
    '외국어': '학습/교육',
    '컴퓨터/모바일': '학습/교육',
    '과학': '학습/교육',
    '만화': '아동/청소년',
    '어린이': '아동/청소년',
    '청소년': '아동/청소년',
    '유아': '아동/청소년',
    '좋은부모': '아동/청소년'
}

def update_main_category():
    from .models import Books
    updated = 0
    for book in Books.objects.all():
        mapped = CATEGORY_MAPPING.get(book.category_name, '기타')
        if book.main_category != mapped:
            book.main_category = mapped
            book.save()
            updated += 1
    print(f"{updated}권의 main_category가 업데이트되었습니다.")