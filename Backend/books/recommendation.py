# books/recommendation.py

import os
from gensim.models import Word2Vec
from books.models import Books
from konlpy.tag import Okt
import numpy as np
import re
from django.conf import settings
from .utils import CATEGORY_MAPPING

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

def recommend_books(user, top_n=10):
    try:
        # 모델 파일 경로 설정
        model_path = os.path.join(settings.BASE_DIR, 'ml', 'word2vec_books.model')
        
        # 사용자의 찜한 책들 가져오기
        liked_books = user.liked_books.all()
        
        # 찜한 책이 없는 경우 선호 장르 기반으로 추천
        if not liked_books.exists():
            if not user.favorite_genres:
                return Books.objects.none()
            
            # 선호 장르에 해당하는 책들 추천 (main_category 기준)
            return Books.objects.filter(
                main_category__in=user.favorite_genres
            ).order_by('-customer_review')[:top_n]
        
        # 모델 파일 존재 확인
        if not os.path.exists(model_path):
            print(f"Warning: Word2Vec model not found at {model_path}")
            # 기본 추천: 사용자의 찜한 책과 같은 장르의 책 추천
            # 사용자가 찜한 책들의 장르 수집
            user_genres = set()
            for book in liked_books:
                if book.main_category:
                    user_genres.add(book.main_category)
            
            # 같은 장르의 다른 책들 추천
            return Books.objects.filter(main_category__in=user_genres).exclude(
                id__in=liked_books.values_list('id', flat=True)
            )[:top_n]
        
        # Word2Vec 모델 로드
        model = Word2Vec.load(model_path)

        # Word2Vec 기반 벡터 계산
        vectors = []
        for book in liked_books:
            text = f"{book.title} {book.description} {book.author} {book.category_name or ''} {book.main_category or ''}"
            tokens = preprocess_text(text)
            word_vecs = [model.wv[word] for word in tokens if word in model.wv]
            if word_vecs:
                vectors.extend(word_vecs)

        if not vectors:
            # 벡터 계산이 실패한 경우 선호 장르 기반으로 추천
            if user.favorite_genres:
                return Books.objects.filter(
                    main_category__in=user.favorite_genres
                ).order_by('-customer_review')[:top_n]
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
            book_genres = [book.main_category] if book.main_category else []
            genre_similarity = get_genre_similarity(user.favorite_genres, book_genres)

            # 최종 유사도 계산 (Word2Vec 70%, 장르 30% 가중치)
            final_similarity = 0.7 * word2vec_similarity + 0.3 * genre_similarity
            similarities.append((book, final_similarity))

        # 유사도 순으로 정렬 후 top_n개 추천
        similarities.sort(key=lambda x: x[1], reverse=True)
        recommended_books = [book for book, _ in similarities[:top_n]]
        return recommended_books

    except Exception as e:
        print(f"Error in recommend_books: {str(e)}")
        # 에러 발생 시 선호 장르 기반으로 추천
        if user.favorite_genres:
            return Books.objects.filter(
                main_category__in=user.favorite_genres
            ).order_by('-customer_review')[:top_n]
        return Books.objects.none()
