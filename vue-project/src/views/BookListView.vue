<template>

  <div class="book-list-view">
    <div class="tab-bar">
      <RouterLink
        v-for="genre in genres"
        :key="genre"
        :to="{ name: 'BookList', query: { genre } }"
        class="tab-btn"
        :class="{ active: $route.query.genre === genre }"
      >
        {{ genre }}
      </RouterLink>
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

const genres = [
  '문학', '인문/사회', '자기계발/실용', '예술/문화', '학습/교육', '아동/청소년', '만화'
]

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
@import url('https://fonts.googleapis.com/css2?family=Indie+Flower&display=swap');

body {
  background: linear-gradient(to bottom, #6f8dc7, #d0e1ff);
}



.tab-bar {
  display: flex;
  justify-content: center;
  gap: 3rem;
  margin-bottom: 2.5rem;
  position: relative;
  
}

.tab-btn {
  margin-top: 1rem;
  font-family: 'Noto Sans KR', sans-serif;
  font-size: 1.5rem;
  font-weight: bold;
  color: #bdbdbd;
  background: none;
  border: none;
  outline: none;
  cursor: pointer;
  padding: 0 1.5rem 0.5rem 1.5rem;
  position: relative;
  transition: color 0.2s;
  text-decoration: none;
}

.tab-btn.active {
  color: #222;
}

.tab-btn.active::after {
  content: '';
  display: block;
  margin: 0 auto;
  margin-top: 0.2rem;
  width: 60%;
  height: 2px;
  background: #e5e7eb;
  border-radius: 1px;
}
</style> 