<template>
  <div class="thread-card">
    <div class="thread-header">
      <div class="user-info">
        <span class="username">{{ thread.user.nickname }}</span>
        <span class="date">{{ formatDate(thread.created_at) }}</span>
      </div>
      <button class="like-btn" @click="toggleLike" :class="{ 'is-liked': isLiked }">
        <span class="heart-icon">♥</span>
        <span class="like-count">{{ likeCount }}</span>
      </button>
    </div>
    <div class="thread-body">
      <img :src="thread.book.cover" alt="책 커버" class="book-cover">
      <div class="thread-content">
        <p class="book-title">{{ thread.book.title }}</p>
        <p class="thread-text">{{ thread.content }}</p>
        <div v-if="thread.audio_file" class="audio-player">
          <audio controls>
            <source :src="thread.audio_file" type="audio/mpeg">
            브라우저가 오디오 재생을 지원하지 않습니다.
          </audio>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useBookStore } from '@/stores/books'
import axios from 'axios'

const props = defineProps({
  thread: {
    type: Object,
    required: true
  }
})

const store = useBookStore()
const isLiked = ref(false)
const likeCount = ref(props.thread.like_count || 0)

const checkLikeStatus = async () => {
  try {
    const access = localStorage.getItem('access')
    if (!access) {
      isLiked.value = false
      return
    }

    const response = await axios.get(`${store.API_URL}/api/books/threads/${props.thread.id}/like-status/`, {
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

    const response = await axios.post(
      `${store.API_URL}/api/books/threads/${props.thread.id}/like/`,
      {},
      { headers: { Authorization: `Bearer ${access}` } }
    )
    
    isLiked.value = response.data.status === 'liked'
    likeCount.value += response.data.status === 'liked' ? 1 : -1
  } catch (err) {
    if (err.response?.status === 401) {
      alert('로그인이 필요합니다.')
    } else {
      alert('좋아요 처리 중 오류가 발생했습니다.')
    }
  }
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('ko-KR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(() => {
  checkLikeStatus()
})
</script>

<style scoped>
.thread-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.thread-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.username {
  font-weight: 600;
  color: #333;
}

.date {
  color: #666;
  font-size: 0.9rem;
}

.like-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border: 1px solid #ff6b81;
  border-radius: 20px;
  background: white;
  color: #ff6b81;
  cursor: pointer;
  transition: all 0.2s;
}

.like-btn:hover {
  background: #fff0f2;
}

.like-btn.is-liked {
  background: #ff6b81;
  color: white;
}

.heart-icon {
  font-size: 1.2rem;
}

.thread-body {
  display: flex;
  gap: 1.5rem;
  align-items: flex-start;
}

.book-cover {
  width: 120px;
  height: 180px;
  object-fit: cover;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.thread-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.book-title {
  font-weight: 600;
  color: #444;
  font-size: 1.1rem;
}

.thread-text {
  color: #333;
  line-height: 1.6;
}

.audio-player {
  margin-top: auto;
}

.audio-player audio {
  width: 100%;
  max-width: 300px;
}
</style> 