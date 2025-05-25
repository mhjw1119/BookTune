<template>
  <button class="like-button" @click="toggleLike" :class="{ 'is-liked': isLiked }">
    <span class="heart-icon">♥</span>
    <span class="like-text">{{ isLiked ? '좋아요 취소' : '좋아요' }}</span>
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
.like-button {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  border: 2px solid #ff6b81;
  border-radius: 50px;
  background: white;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 1.1rem;
  font-weight: 600;
}

.like-button:hover {
  background: #fff0f2;
  transform: scale(1.05);
}

.like-button.is-liked {
  background: #ff6b81;
  color: white;
}

.heart-icon {
  font-size: 1.5rem;
  line-height: 1;
}

.like-text {
  font-family: 'Noto Sans KR', sans-serif;
}
</style> 