# books/recommendation.py

from gensim.models import Word2Vec
from books.models import Books
from konlpy.tag import Okt
import numpy as np
import re

# 불용어 리스트 (train_word2vec.py에서 사용한 것과 동일하게 유지)
stopwords = set([
    "이", "그", "저", "것", "수", "들", "등", "더", "는", "의", "가", "에", "를",
    "으로", "도", "다", "하고", "한", "하다", "되다", "있다", "없다", "이다", "있음"
])

okt = Okt()

def preprocess_text(text):
    text = re.sub(r"[^가-힣a-zA-Z\s]", "", text).lower()
    tokens = okt.morphs(text, stem=True)
    return [t for t in tokens if t not in stopwords and len(t) > 1]

def recommend_books_word2vec(user, top_n=5):
    model = Word2Vec.load("word2vec_books.model")

    liked_books = user.liked_books.all()
    if not liked_books.exists():
        return Books.objects.none()

    # 사용자의 찜한 책들 기반 벡터 평균 생성
    vectors = []
    for book in liked_books:
        text = f"{book.title} {book.description} {book.author} {book.category_name or ''} {book.main_category or ''}"
        tokens = preprocess_text(text)
        word_vecs = [model.wv[word] for word in tokens if word in model.wv]
        if word_vecs:
            vectors.extend(word_vecs)

    if not vectors:
        return Books.objects.none()

    user_vector = np.mean(vectors, axis=0)

    # 후보 도서와 유사도 계산
    candidate_books = Books.objects.exclude(id__in=liked_books.values_list('id', flat=True))
    similarities = []

    for book in candidate_books:
        text = f"{book.title} {book.description} {book.author} {book.category_name or ''} {book.main_category or ''}"
        tokens = preprocess_text(text)
        word_vecs = [model.wv[word] for word in tokens if word in model.wv]
        if not word_vecs:
            continue
        book_vector = np.mean(word_vecs, axis=0)
        similarity = np.dot(user_vector, book_vector) / (
            np.linalg.norm(user_vector) * np.linalg.norm(book_vector)
        )
        similarities.append((book, similarity))

    # 유사도 순으로 정렬 후 top_n개 추천
    similarities.sort(key=lambda x: x[1], reverse=True)
    recommended_books = [book for book, _ in similarities[:top_n]]
    return recommended_books
