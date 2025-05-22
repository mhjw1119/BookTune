<template>
  <div class="best-books">
    <div class="books-grid">
      <div v-for="book in store.books.slice(0, 5)" :key="book.isbn" class="book-card">
        <div class="rank-badge">{{ book.best_rank }}</div>
        <img :src="book.cover" :alt="book.title" class="book-cover">
        <div class="book-info">
          <h3 class="book-title">{{ book.title }}</h3>
          <p class="book-author">{{ book.author }}</p>
          <p class="book-publisher">{{ book.publisher }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useBookStore } from '@/stores/books'

const store = useBookStore()


// onMounted(async () => {
//   await store.getBooks()
//   bestBooks.value = store.books.value
//     ? store.books.value.slice(0, 5)
//     : []
//   if (bestBooks != null) {
//     console.log(bestBooks.value)
//   }
// })

</script>

<style scoped>
.best-books {
  width: 100%;
}

.books-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 2rem;
}

.book-card {
  position: relative;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 1rem;
  transition: transform 0.2s;
  background: white;
}

.book-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0,0,0,0.1);
}

.rank-badge {
  position: absolute;
  top: -10px;
  left: -10px;
  background: #e74c3c;
  color: white;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 1.2rem;
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
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.book-author, .book-publisher {
  color: #666;
  font-size: 0.9rem;
  margin: 0.25rem 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>