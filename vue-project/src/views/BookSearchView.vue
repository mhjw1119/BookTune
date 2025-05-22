<template>
  <div class="search-result-container">
    <!-- {{ store.books[0].title }} -->
    <h2 class="search-title">'{{ keyword }}' 검색 결과</h2>
    <div v-if="filteredBooks.length === 0" class="no-result">검색 결과가 없습니다.</div>
    <div v-else class="books-grid">
      <BookSearchItem v-for="book in filteredBooks" :key="book.isbn" :book="book" />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useBookStore } from '@/stores/books'
import BookSearchItem from '@/components/BookSearchItem.vue'

const route = useRoute()
const store = useBookStore()
const keyword = route.query.q || ''

const filteredBooks = computed(() => {
  const bookList = Array.isArray(store.books) ? store.books : []
  return bookList.filter(book => {
    const lowerKeyword = keyword.toLowerCase()
    return (
      (book.title && book.title.toLowerCase().includes(lowerKeyword)) ||
      (book.author && book.author.toLowerCase().includes(lowerKeyword))
    )
  })
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