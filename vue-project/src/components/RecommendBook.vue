<template>
  <div class="recommended-books">
    
    <!-- 로딩 상태 -->
    <div v-if="store.loading" class="loading-state">
      <p>추천 도서를 불러오는 중...</p>
    </div>

    <!-- 에러 상태 -->
    <div v-else-if="store.error" class="error-state">
      <p>{{ store.error }}</p>
      <button @click="retryLoading" class="retry-button">다시 시도</button>
    </div>

    <!-- 추천 도서가 없는 경우 -->
    <div v-else-if="!store.recommendedBooks.length" class="empty-state">
      <p>아직 추천할 도서가 없습니다. 도서를 찜해보세요!</p>
    </div>

    <!-- 추천 도서 목록 -->
    <div v-else class="books-grid">
      <BookItem
        v-for="book in store.recommendedBooks"
        :key="book.isbn"
        :book="book"
      />
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useBookStore } from '@/stores/books'
import BookItem from '@/components/search/BookItem.vue'

const store = useBookStore()

const retryLoading = async () => {
  await store.getRecommendedBooks()
}

// 컴포넌트 마운트 시 추천 도서 로드
onMounted(async () => {
  await store.getRecommendedBooks()
})
</script>

<style scoped>
.recommended-books {
  width: 100%;
  padding: 2rem 0;
}

.section-title {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 1.5rem;
  color: #333;
}

.loading-state,
.error-state,
.empty-state {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.retry-button {
  margin-top: 1rem;
  padding: 0.5rem 1rem;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.retry-button:hover {
  background-color: #45a049;
}

.books-grid {
  display: grid;
  justify-content: center; /* 그리드를 가운데 정렬 */
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2rem;
  max-width: 1280px; /* 최대 너비 제한 */
  margin: 0 auto;     /* 수평 중앙 정렬 */
}
</style>