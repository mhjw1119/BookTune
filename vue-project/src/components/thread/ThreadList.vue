<template>
  <div class="thread-list">
    <h2 class="thread-list-title">전체 스레드</h2>
    <div v-if="loading" class="loading">
      로딩 중...
    </div>
    <div v-else-if="error" class="error">
      {{ error }}
    </div>
    <div v-else class="threads-container">
      <div v-for="thread in threads" :key="thread.id" class="thread-card">
        <div class="thread-header">
          <div class="user-info">
            <span class="username">{{ thread.user.username }}</span>
            <span class="date">{{ formatDate(thread.created_at) }}</span>
          </div>
          <button class="like-btn" @click="toggleLike(thread)" :class="{ 'is-liked': thread.is_liked }">
            <span class="heart-icon">♥</span>
            <span class="like-count">{{ thread.like_count }}</span>
          </button>
        </div>
        <div class="thread-content">
          <p class="book-title">{{ thread.book.title }}</p>
          <p class="thread-text">{{ thread.content }}</p>
        </div>
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
import axios from 'axios'
import { useBookStore } from '@/stores/books'

const store = useBookStore()
const threads = ref([])
const loading = ref(true)
const error = ref(null)

const fetchThreads = async () => {
  try {
    const access = localStorage.getItem('access')
    if (!access) {
      error.value = '로그인이 필요합니다.'
      loading.value = false
      return
    }

    const response = await axios.get(`${store.API_URL}/api/books/threads/`, {
      headers: { Authorization: `Bearer ${access}` }
    })
    threads.value = response.data
    loading.value = false
  } catch (err) {
    console.error('Error fetching threads:', err)
    error.value = '스레드를 불러오는데 실패했습니다.'
    loading.value = false
  }
}

const toggleLike = async (thread) => {
  try {
    const access = localStorage.getItem('access')
    if (!access) {
      alert('로그인이 필요합니다.')
      return
    }

    const response = await axios.post(
      `${store.API_URL}/api/books/threads/${thread.id}/like/`,
      {},
      { headers: { Authorization: `Bearer ${access}` } }
    )
    
    thread.is_liked = response.data.status === 'liked'
    thread.like_count += response.data.status === 'liked' ? 1 : -1
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
  fetchThreads()
})
</script>

<style scoped>
.thread-list {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.thread-list-title {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 2rem;
  color: #333;
}

.loading, .error {
  text-align: center;
  padding: 2rem;
  font-size: 1.2rem;
  color: #666;
}

.error {
  color: #ef4444;
}

.threads-container {
  display: grid;
  gap: 1.5rem;
}

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

.thread-content {
  margin-bottom: 1rem;
}

.book-title {
  font-weight: 600;
  color: #444;
  margin-bottom: 0.5rem;
}

.thread-text {
  color: #333;
  line-height: 1.6;
}

.audio-player {
  margin-top: 1rem;
}

.audio-player audio {
  width: 100%;
}
</style> 