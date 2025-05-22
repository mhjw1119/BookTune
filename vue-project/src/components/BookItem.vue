<template>
  <div class="book-item">
    <div v-for="book in books" :key="book.fields.isbn" class="book-card">
      <img :src="book.fields.cover" :alt="book.fields.title" class="book-cover">
      <div class="book-info">
        <h3 class="book-title">{{ book.fields.title }}</h3>
        <p class="book-author">{{ book.fields.author }}</p>
        <p class="book-publisher">{{ book.fields.publisher }}</p>
        <p class="book-category">{{ book.fields.category_name }}</p>
        <p class="book-rank">베스트 랭킹: {{ book.fields.best_rank }}위</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useBookStore } from '@/stores/books';
const store = useBookStore()

onMounted(() => {
  store.getBooks()
})
</script>

<style scoped>
.book-item {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
  padding: 2rem;
}

.book-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 1rem;
  transition: transform 0.2s;
}

.book-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0,0,0,0.1);
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
  font-size: 1.2rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.book-author, .book-publisher, .book-category {
  color: #666;
  margin: 0.25rem 0;
}

.book-rank {
  color: #e74c3c;
  font-weight: bold;
  margin-top: 0.5rem;
}
</style>