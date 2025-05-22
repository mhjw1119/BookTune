<template>
  <div class="search-result-container">
    <h2 class="search-title">'{{ keyword }}' 검색 결과</h2>
    <div v-if="loading" class="loading">검색 중...</div>
    <div v-else-if="books.length === 0" class="no-result">검색 결과가 없습니다.</div>
    <div v-else class="books-grid">
      <div v-for="book in books" :key="book.fields.isbn" class="book-card">
        <img :src="book.fields.cover" :alt="book.fields.title" class="book-cover">
        <div class="book-info">
          <h3 class="book-title">{{ book.fields.title }}</h3>
          <p class="book-author">{{ book.fields.author }}</p>
          <p class="book-publisher">{{ book.fields.publisher }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const books = ref([])
const loading = ref(true)
const keyword = route.query.q || ''

onMounted(async () => {
  try {
    const res = await fetch('/books.json')
    const allBooks = await res.json()
    if (keyword) {
      books.value = allBooks.filter(book =>
        book.fields.title.toLowerCase().includes(keyword.toLowerCase())
      )
    }
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
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
.loading, .no-result {
  text-align: center;
  color: #bbb;
  margin-top: 2rem;
}
.books-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 2rem;
}
.book-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 1rem;
  background: #fff;
  box-shadow: 0 2px 8px 0 rgba(0,0,0,0.04);
}
.book-cover {
  width: 100%;
  height: auto;
  border-radius: 4px;
  margin-bottom: 1rem;
}
.book-info {
  padding: 0.5rem;
}
.book-title {
  font-size: 1rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
}
.book-author, .book-publisher {
  color: #666;
  font-size: 0.9rem;
  margin: 0.25rem 0;
}
</style>