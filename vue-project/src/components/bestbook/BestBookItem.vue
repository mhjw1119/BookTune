<template>
  
  <div class="book-card" @click="navigateToDetail">
    <button class="heart-btn" @click.stop="toggleLike">
      <span
        class="insta-heart"
        :class="{ liked: isLiked, animate: animateHeart, hovered: isHeartHovered }"
        @mouseenter="isHeartHovered = true"
        @mouseleave="isHeartHovered = false"
      >
        <svg viewBox="0 0 48 48" width="56" height="56">
          <path
            :fill="isLiked || isHeartHovered ? '#ff3b5c' : '#ddd'"
            d="M34.6 6c-3.4 0-6.4 1.7-8.6 4.3C23.8 7.7 20.8 6 17.4 6 11.6 6 7 10.6 7 16.4c0 9.1 10.2 15.7 16.2 20.7.5.4 1.2.4 1.7 0C30.8 32.1 41 25.5 41 16.4 41 10.6 36.4 6 34.6 6z"
          />
        </svg>
      </span>
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
import { ref, onMounted } from 'vue'
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

const isLiked = ref(false)
const animateHeart = ref(false)
const isHeartHovered = ref(false)

const checkLikeStatus = async () => {
  try {
    const access = localStorage.getItem('access')
    if (!access) {
      isLiked.value = false
      return
    }

    const response = await axios.get(`${store.API_URL}/api/books/${props.book.isbn}/like-status/`, {
      headers: { Authorization: `Bearer ${access}` }
    })
    isLiked.value = response.data.is_liked
  } catch (error) {
    console.error('Error checking like status:', error)
    isLiked.value = false
  }
}

const toggleLike = async () => {
  try {
    const access = localStorage.getItem('access')
    if (!access) {
      alert('로그인이 필요합니다.')
      return
    }

    const result = await store.toggleLike(props.book.isbn)
    isLiked.value = result.status === 'liked'
    // 하트 애니메이션 트리거
    animateHeart.value = false
    void animateHeart.value
    setTimeout(() => {
      animateHeart.value = true
      setTimeout(() => (animateHeart.value = false), 400)
    }, 0)
  } catch (e) {
    if (e.response?.status === 401) {
      alert('로그인이 필요합니다.')
    } else {
      alert('좋아요 처리 중 오류가 발생했습니다.')
    }
  }
}

const navigateToDetail = () => {
  router.push({
    name: 'BookDetail',
    params: { isbn: props.book.isbn }
  })
}

onMounted(() => {
  checkLikeStatus()
})
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
  right: 0px;
  background: none;
  border: none;
  cursor: pointer;
  outline: none;
  font-size: 2.3rem;
  z-index: 2;
}

.insta-heart {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.15s;
}
.insta-heart.liked {
  /* 좋아요 상태일 때 하트 색상은 SVG에서 fill로 처리 */
}
.insta-heart.animate {
  animation: heart-bounce 0.4s;
}
@keyframes heart-bounce {
  0% { transform: scale(1); }
  20% { transform: scale(1.3); }
  40% { transform: scale(0.95); }
  60% { transform: scale(1.1); }
  80% { transform: scale(0.98); }
  100% { transform: scale(1); }
}
</style> 