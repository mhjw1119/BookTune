<template>
  <div class="book-card" @click="navigateToDetail">
    <img :src="book.cover" :alt="book.title" class="book-cover">
    <div class="book-info">
      <h3 class="book-title">{{ book.title }}</h3>
      <p class="book-author">{{ book.author }}</p>
      <p class="book-publisher">{{ book.publisher }}</p>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()
const props = defineProps({
  book: {
    type: Object,
    required: true
  }
})

const navigateToDetail = () => {
  router.push({
    name: 'BookDetail',
    params: { isbn: props.book.isbn }
  })
}
</script>

<style scoped>
.book-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 1rem;
  background: #fff;
  box-shadow: 0 2px 8px 0 rgba(0,0,0,0.04);
  cursor: pointer;
  transition: transform 0.2s ease-in-out;
}

.book-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
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