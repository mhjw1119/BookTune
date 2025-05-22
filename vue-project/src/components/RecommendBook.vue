<template>
  <div class="recommend-books">
    <div class="books-grid">
      <div v-for="book in recommendBooks" :key="book.fields.isbn" class="book-card">
        <img :src="book.fields.cover" :alt="book.fields.title" class="book-cover">
        <div class="book-info">
          <h3 class="book-title">{{ book.fields.title }}</h3>
          <p class="book-author">{{ book.fields.author }}</p>
          <p class="book-category">{{ book.fields.category_name }}</p>
          <div class="book-music">
            <span class="music-icon">🎵</span>
            <a :href="book.fields.recommended_song" target="_blank" class="music-link">추천 음악</a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useBookStore } from '@/stores/books'

const store = useBookStore()
const recommendBooks = ref([])

// onMounted(async () => {
//   await store.getBooks()
//   // customer_review가 높은 순으로 정렬하여 상위 4개 도서 표시
//   recommendBooks.value = [...store.books]
//     .sort((a, b) => b.fields.customer_review - a.fields.customer_review)
//     .slice(0, 4)
// })
</script>

<style scoped>
.recommend-books {
  width: 100%;
}

.books-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 2rem;
}

.book-card {
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
  font-size: 1.1rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.book-author, .book-category {
  color: #666;
  font-size: 0.9rem;
  margin: 0.25rem 0;
}

.book-music {
  margin-top: 1rem;
  padding-top: 0.5rem;
  border-top: 1px solid #eee;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.music-icon {
  font-size: 1.2rem;
}

.music-link {
  color: #e74c3c;
  text-decoration: none;
  font-size: 0.9rem;
}

.music-link:hover {
  text-decoration: underline;
}
</style> 