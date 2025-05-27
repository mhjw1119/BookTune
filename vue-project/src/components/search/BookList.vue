<template>
  <div class="search-result-container">
    <h2 class="search-title">'{{ keyword }}' 검색 결과</h2>
    <div v-if="isLoading" class="loading-state">
      <div class="loading-spinner"></div>
      <p>검색 결과를 불러오는 중...</p>
    </div>
    <div v-else-if="books.length === 0" class="no-result">검색 결과가 없습니다.</div>
    <div v-else class="books-grid">
      <BookItem v-for="book in books" :key="book.isbn" :book="book" />
    </div>
  </div>
</template>

<script setup>
import BookItem from './BookItem.vue'
import { ref } from 'vue'

const props = defineProps({
  keyword: {
    type: String,
    required: true
  },
  books: {
    type: Array,
    required: true
  }
})

const isLoading = ref(true)

// 컴포넌트가 마운트되면 로딩 상태를 false로 변경
setTimeout(() => {
  isLoading.value = false
}, 500)
</script>

<style scoped>
.search-result-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.search-title {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 2rem;
  color: #333;
}

.no-result {
  text-align: center;
  color: #bbb;
  margin-top: 2rem;
}

.books-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 2rem;
}

.loading-state {
  text-align: center;
  padding: 2rem;
  color: #666;
  font-size: 1.1rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 3px solid #e0e0e0;
  border-top: 3px solid #0078c8;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style> 