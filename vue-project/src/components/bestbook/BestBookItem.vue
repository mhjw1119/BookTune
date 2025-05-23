<template>
  <div class="book-card" @click="navigateToDetail">
    <button class="heart-btn" @click.stop="toggleLike">
      <span :class="{ liked: isLiked }">♥</span>
    </button>
    <div class="rank-badge">{{ book.best_rank }}</div>
    <img :src="book.cover" :alt="book.title" class="book-cover">
    <div class="book-info">
      <h3 class="book-title">{{ book.title }}</h3>
      <p class="book-author">{{ book.author }}</p>
      <p class="book-publisher">{{ book.publisher }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useBookStore } from '@/stores/books'
import axios from 'axios'

const router = useRouter()
const store = useBookStore()
const props = defineProps({
  book: {
    type: Object,
    required: true
  }
})

const isLiked = ref(props.book.is_liked ?? false)

const toggleLike = async () => {
  try {
    const result = await store.toggleLike(props.book.isbn)
    isLiked.value = result.status === 'liked'
  } catch (e) {
    alert('로그인이 필요합니다.')
  }
}

const navigateToDetail = () => {
  router.push({
    name: 'BookDetail',
    params: { isbn: props.book.isbn }
  })
}
</script>

<style scoped>
.book-card {
  position: relative;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 1rem;
  background: #fff;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  cursor: pointer;
  transition: transform 0.2s ease-in-out;
}

.book-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.rank-badge {
  position: absolute;
  top: -10px;
  left: -10px;
  background: linear-gradient(45deg, #FF6B6B, #FF8E8E);
  color: white;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
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
  color: #333;
}

.book-author, .book-publisher {
  color: #666;
  font-size: 0.9rem;
  margin: 0.25rem 0;
}

.heart-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  background: none;
  border: none;
  cursor: pointer;
  outline: none;
  font-size: 2.3rem;
  z-index: 2;
}

.heart-btn span {
  color: #bbb;
  transition: color 0.2s;
}

.heart-btn span.liked {
  color: #ff6b81;
}

.heart-btn:hover span {
  color: #ff3b5c;
}
</style> 