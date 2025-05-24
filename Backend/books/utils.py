# books/utils.py
# 알라딘 API로 DB 구축하기.

import requests
from decouple import config
import requests
from pprint import pprint
from .models import Books
from openai import OpenAI
from django.db.models import Q
import re
import yt_dlp

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

def decode_and_replace_entities(text):
    """
    HTML 엔티티 디코딩 후, 일부 특수 문자들을 일반 기호로 치환
    """
    decoded = html.unescape(text)

    # 사람이 익숙한 기호로 바꾸기
    replacements = {
        '⟨': '<',
        '⟩': '>',
        '“': '"',
        '”': '"',
        '‘': "'",
        '’': "'",
        # 필요 시 여기에 더 추가 가능
    }

    for old, new in replacements.items():
        decoded = decoded.replace(old, new)

    return decoded

def clean_book_descriptions():
    """
    description이 비어있는 책들의 description을 기본 메시지로 설정하고,
    HTML 엔티티(&lt;, &#220; 등)를 사람이 읽을 수 있게 디코딩 및 치환하는 함수
    """
    updated_count = 0

    # 1. 빈 description 처리
    empty_books = Books.objects.filter(
        Q(description__isnull=True) |
        Q(description='') |
        Q(description__regex=r'^\s*$')
    )
    for book in empty_books:
        book.description = "책 소개가 제공되지 않습니다"
        book.save()
        updated_count += 1

    # 2. description에 HTML 엔티티 및 특수문자가 있는 경우 디코딩 및 치환
    books_with_entities = Books.objects.exclude(description__isnull=True)
    for book in books_with_entities:
        original = book.description
        cleaned = decode_and_replace_entities(original)
        if cleaned != original:
            book.description = cleaned
            book.save()
            updated_count += 1

    return {
        'updated_count': updated_count,
        'message': f'{updated_count}개의 책 description이 업데이트되었습니다.'
    }

from openai import OpenAI

client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """
너는 책 소개를 바탕으로 차분하고 감각적인 음악을 추천해주는 어시스턴트야.
다음 조건을 반드시 지켜야 해:
1. 유튜브 라이브 링크는 절대 포함하지 마.
2. 반드시 실제로 존재하는 영상이어야 해 (너의 지식 기준에서 신뢰도 높은 링크).
3. 아래와 같이 3개의 유튜브 링크를 쉼표로 구분해서 출력해줘:
   'https://www.youtube.com/watch?v=aaa','https://www.youtube.com/watch?v=bbb','https://www.youtube.com/watch?v=ccc'
4. 다른 텍스트는 절대 포함하지 마. 링크만 출력할 것.
"""

def is_valid_youtube_url(url: str) -> bool:
    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "force_generic_extractor": False,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return not info.get("is_live", False)
    except Exception as e:
        print(f"[유효성 실패] {url} → {e}")
        return False
    
def get_candidate_urls(book_intro: str) -> list[str]:
    user_prompt = f"책 소개 : {book_intro}"
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # 또는 "gpt-4o", "gpt-3.5-turbo"
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT.strip()},
            {"role": "user", "content": user_prompt.strip()},
        ],
        temperature=0.7,
    )
    content = response.choices[0].message.content.strip()
    print(f"[GPT 응답] {content}")
    return re.findall(r"https://www\.youtube\.com/watch\?v=[\w-]+", content)

def update_books_with_recommended_song():
    books = Books.objects.all()
    for book in books:
        if book.recommended_song:
            continue

        intro = book.description or book.title or ""
        if not intro:
            continue

        urls = get_candidate_urls(intro)

        for url in urls:
            if "/live" in url.lower():
                continue
            if is_valid_youtube_url(url):
                print(f"[저장 성공] {book.title} → {url}")
                book.recommended_song = url
                book.save()
                break

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

def clean_book_descriptions():
    """
    description이 비어있는 책들의 description을 기본 메시지로 설정하고,
    특수 문자 패턴을 제거하는 함수
    """
    # Q 객체를 사용하여 description이 None이거나 빈 문자열이거나 공백만 있는 경우를 모두 처리
    empty_books = Books.objects.filter(
        Q(description__isnull=True) |  # None인 경우
        Q(description='') |            # 빈 문자열인 경우
        Q(description__regex=r'^\s*$') # 공백만 있는 경우
    )
    
    # 특수 문자 패턴을 제거하는 정규식
    special_char_pattern = r'[&][a-zA-Z]+[;]'
    
    # 모든 책에 대해 처리
    updated_count = 0
    for book in Books.objects.all():
        needs_update = False
        
        # description이 비어있는 경우
        if book.description is None or book.description.strip() == '':
            book.description = "책 소개가 제공되지 않습니다"
            needs_update = True
        # 특수 문자 패턴이 있는 경우
        elif re.search(special_char_pattern, book.description):
            book.description = re.sub(special_char_pattern, '', book.description)
            needs_update = True
            
        if needs_update:
            book.save()
            updated_count += 1
    
    return {
        'updated_count': updated_count,
        'message': f'{updated_count}개의 책 description이 업데이트되었습니다.'
    }