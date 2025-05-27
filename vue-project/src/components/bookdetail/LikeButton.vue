<template>
  <button class="heart-btn" @click="toggleLike">
    <span
      class="insta-heart"
      :class="{ liked: isLiked, animate: animateHeart, hovered: isHeartHovered }"
      @mouseenter="isHeartHovered = true"
      @mouseleave="isHeartHovered = false"
    >
      <svg viewBox="0 0 48 48" width="80" height="80">
        <path
          :fill="isLiked || isHeartHovered ? '#ff3b5c' : '#ddd'"
          d="M34.6 6c-3.4 0-6.4 1.7-8.6 4.3C23.8 7.7 20.8 6 17.4 6 11.6 6 7 10.6 7 16.4c0 9.1 10.2 15.7 16.2 20.7.5.4 1.2.4 1.7 0C30.8 32.1 41 25.5 41 16.4 41 10.6 36.4 6 34.6 6z"
        />
      </svg>
    </span>
  </button>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useBookStore } from '@/stores/books'
import axios from 'axios'

const props = defineProps({
  isbn: {
    type: String,
    required: true
  }
})

const store = useBookStore()
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

    const response = await axios.get(`${store.API_URL}/api/books/${props.isbn}/like-status/`, {
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

    const result = await store.toggleLike(props.isbn)
    isLiked.value = result.status === 'liked'
    
    animateHeart.value = false;
    setTimeout(() => {
      animateHeart.value = true;
      setTimeout(() => animateHeart.value = false, 400);
    }, 0);

  } catch (e) {
    if (e.response?.status === 401) {
      alert('로그인이 필요합니다.')
    } else {
      alert('좋아요 처리 중 오류가 발생했습니다.')
    }
  }
}

onMounted(() => {
  checkLikeStatus()
})
</script>

<style scoped>
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
  padding: 0;
}

.insta-heart {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.15s;
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