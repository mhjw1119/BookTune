# import os
# import django
# import sys

# # Django 설정
# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BookTune.settings')
# django.setup()

# import re
# from gensim.models import Word2Vec
# from konlpy.tag import Okt
# from books.models import Books

# # 불용어 목록 정의
# stopwords = set([
#     "이", "그", "저", "것", "수", "들", "등", "더", "는", "의", "가", "에", "를",
#     "으로", "도", "다", "하고", "한", "하다", "되다", "있다", "없다", "이다", "있음"
# ])

# okt = Okt()
# tokenized_corpus = []

# # 도서 데이터 전처리
# books = Books.objects.all()
# for book in books:
#     # 사용할 필드 조합
#     raw_text = f"{book.title} {book.description} {book.author} {book.category_name or ''} {book.main_category or ''}"

#     # 특수문자 제거 + 소문자 변환
#     clean_text = re.sub(r"[^가-힣a-zA-Z\s]", "", raw_text).lower()

#     # 형태소 분석 + 불용어 제거
#     tokens = okt.morphs(clean_text, stem=True)
#     tokens = [token for token in tokens if token not in stopwords and len(token) > 1]  # 단어 길이 1 이하 제거

#     if tokens:
#         tokenized_corpus.append(tokens)

# # Word2Vec 학습
# if tokenized_corpus:
#     model = Word2Vec(sentences=tokenized_corpus, vector_size=100, window=5, min_count=2, workers=4)
#     model.save("word2vec_books.model")
#     print("✅ Word2Vec 모델이 성공적으로 저장되었습니다.")
# else:
#     print("⚠️ 토큰화된 문서가 없어 학습을 수행하지 않았습니다.")
