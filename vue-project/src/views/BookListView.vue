<template>
  <div class="book-list-view">
    <div class="category-links">
      <RouterLink :to="{ name: 'BookList', query: { genre: '문학' }}" class="category-link">문학</RouterLink>
      <RouterLink :to="{ name: 'BookList', query: { genre: '인문/사회' }}" class="category-link">인문/사회</RouterLink>
      <RouterLink :to="{ name: 'BookList', query: { genre: '자기계발/실용' }}" class="category-link">자기계발/실용</RouterLink>
      <RouterLink :to="{ name: 'BookList', query: { genre: '예술/문화' }}" class="category-link">예술/문화</RouterLink>
      <RouterLink :to="{ name: 'BookList', query: { genre: '학습/교육' }}" class="category-link">학습/교육</RouterLink>
      <RouterLink :to="{ name: 'BookList', query: { genre: '아동/청소년' }}" class="category-link">아동/청소년</RouterLink>
    </div>
    <BookList :books="booklist" />
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useBookStore } from '@/stores/books'
import BookList from '@/components/BookList.vue'
import { onMounted } from 'vue'

const route = useRoute()
const store = useBookStore()
const booklist = ref([])

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

const fetchBooks = async () => {
  if (route.query.genre) {
    const result = await store.genreBooks(route.query.genre)
    booklist.value = result.filter(book => book.main_category === route.query.genre)
  } else {
    await sleep(3)
    
    await store.getBooks()
    booklist.value = store.books
  }
}

onMounted(() => {
  fetchBooks()
})

watch(() => route.query.genre, fetchBooks)
</script>

<style scoped>
.category-links {
  display: flex;
  justify-content: center;
  gap: 2rem;
  padding: 1rem 0;
  margin-bottom: 2rem;
}

.category-link {
  font-family: 'Pretendard', sans-serif;
  font-size: 1.1rem;
  color: #333;
  text-decoration: none;
  transition: color 0.2s;
}

.category-link:hover {
  color: #6366f1;
}

.category-link:active {
  color: #6366f1;
}
</style> 