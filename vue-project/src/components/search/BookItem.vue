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
  background: var(--glass-bg);
  border: 2px solid rgba(255, 255, 255, 0.8);
  border-radius: 16px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1),
              inset 0 0 0 1px rgba(255, 255, 255, 0.3);
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  backdrop-filter: var(--glass-blur);
  -webkit-backdrop-filter: var(--glass-blur);
  padding: 1px;
  background-color: aliceblue;
}

.book-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15),
              inset 0 0 0 1px rgba(255, 255, 255, 0.4);
  border-color: rgba(255, 255, 255, 0.9);
}

.rank-badge {
  position: absolute;
  top: 12px;
  left: 12px;
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, #2f3542, #1e272e);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  border: 2px solid white;
  z-index: 1;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

.book-cover {
  width: 100%;
  aspect-ratio: 2/3;
  object-fit: cover;
  border-bottom: 1px solid var(--glass-border);
}

.book-info {
  padding: 16px;
}

.book-title {
  font-weight: 600;
  font-size: 16px;
  color: var(--text-color);
  margin-bottom: 8px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  line-height: 1.4;
}

.book-author {
  font-size: 14px;
  color: var(--text-color);
  opacity: 0.8;
  margin-bottom: 4px;
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.book-publisher {
  font-size: 12px;
  color: var(--text-color);
  opacity: 0.6;
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.heart-btn {
  position: absolute;
  top: 12px;
  right: 12px;
  background: var(--glass-bg);
  border: 1px solid var(--glass-border);
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: var(--glass-blur);
  -webkit-backdrop-filter: var(--glass-blur);
  z-index: 1;
}

.heart-btn:hover {
  transform: scale(1.1);
  background: rgba(231, 76, 60, 0.1);
}

.heart-btn.is-liked {
  color: var(--error-color);
  border-color: var(--error-color);
}

.heart-btn.is-liked:hover {
  background: rgba(231, 76, 60, 0.1);
}

@keyframes heartBeat {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.2);
  }
  100% {
    transform: scale(1);
  }
}

.heart-btn.is-liked i {
  animation: heartBeat 0.3s ease-in-out;
}

.insta-heart {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.15s;
}

.insta-heart.liked {
  animation: heart-shake 0.5s cubic-bezier(0.36, 0, 0.66, -0.56);
}

.insta-heart.animate {
  animation: heart-shake 0.5s cubic-bezier(0.36, 0, 10, -0.56);
}

@keyframes heart-shake {
  0% { transform: scale(1) rotate(0deg); }
  15% { transform: scale(1.4) rotate(-5deg); }
  30% { transform: scale(1.4) rotate(5deg); }
  45% { transform: scale(1.4) rotate(-5deg); }
  60% { transform: scale(1.2) rotate(5deg); }
  75% { transform: scale(1.2) rotate(-5deg); }
  90% { transform: scale(1.1) rotate(0deg); }
  100% { transform: scale(1) rotate(0deg); }
}
</style>