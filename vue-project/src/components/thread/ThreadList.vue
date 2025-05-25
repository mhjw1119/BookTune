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
      <ThreadItem
        v-for="thread in threads"
        :key="thread.id"
        :thread="thread"
        :book="thread.book"
        @like-toggled="handleLikeToggled"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useBookStore } from '@/stores/books'
import ThreadItem from './ThreadItem.vue'

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

const handleLikeToggled = ({ threadId, isLiked, likeCount }) => {
  const thread = threads.value.find(t => t.id === threadId)
  if (thread) {
    thread.is_liked = isLiked
    thread.like_count = likeCount
  }
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
</style> 