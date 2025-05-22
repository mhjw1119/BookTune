<template>
  <div class="search-result-container">
    <h2 class="search-title">'{{ keyword }}' 검색 결과</h2>
    <div v-if="books.length === 0" class="no-result">검색 결과가 없습니다.</div>
    <div v-else class="books-grid">
      <BookItem v-for="book in books" :key="book.isbn" :book="book" />
    </div>
  </div>
</template>

<script setup>
import BookItem from './BookItem.vue'

defineProps({
  keyword: {
    type: String,
    required: true
  },
  books: {
    type: Array,
    required: true
  }
})
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
</style> 