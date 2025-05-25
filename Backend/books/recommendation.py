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

def get_genre_similarity(user_genres, book_genres):
    """사용자의 선호 장르와 책의 장르 간의 유사도를 계산"""
    if not user_genres or not book_genres:
        return 0.0
    
    # 장르 일치 개수 계산
    matching_genres = len(set(user_genres) & set(book_genres))
    # 전체 장르 수로 나누어 유사도 계산
    total_genres = len(set(user_genres) | set(book_genres))
    return matching_genres / total_genres if total_genres > 0 else 0.0

def recommend_books(user, top_n=5):
    model = Word2Vec.load("word2vec_books.model")
    
    # 사용자의 찜한 책들 가져오기
    liked_books = user.liked_books.all()
    if not liked_books.exists():
        return Books.objects.none()

    # Word2Vec 기반 벡터 계산
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
        # Word2Vec 기반 유사도 계산
        text = f"{book.title} {book.description} {book.author} {book.category_name or ''} {book.main_category or ''}"
        tokens = preprocess_text(text)
        word_vecs = [model.wv[word] for word in tokens if word in model.wv]
        if not word_vecs:
            continue
        book_vector = np.mean(word_vecs, axis=0)
        word2vec_similarity = np.dot(user_vector, book_vector) / (
            np.linalg.norm(user_vector) * np.linalg.norm(book_vector)
        )

        # 장르 기반 유사도 계산
        book_genres = [book.category_name] if book.category_name else []
        genre_similarity = get_genre_similarity(user.favorite_genres, book_genres)

        # 최종 유사도 계산 (Word2Vec 70%, 장르 30% 가중치)
        final_similarity = 0.7 * word2vec_similarity + 0.3 * genre_similarity
        similarities.append((book, final_similarity))

    # 유사도 순으로 정렬 후 top_n개 추천
    similarities.sort(key=lambda x: x[1], reverse=True)
    recommended_books = [book for book, _ in similarities[:top_n]]
    return recommended_books
