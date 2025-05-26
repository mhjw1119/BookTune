<template>
  <div class="thread-list">
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
        :is-own-profile="isOwnProfile"
        @like-toggled="handleLikeToggled"
        @thread-deleted="handleThreadDeleted"
        @thread-updated="handleThreadUpdated"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { useBookStore } from '@/stores/books'
import ThreadItem from './ThreadItem.vue'

const store = useBookStore()
const threads = ref([])
const loading = ref(true)
const error = ref(null)
const isOwnProfile = computed(() => true)

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

const handleThreadDeleted = (threadId) => {
  threads.value = threads.value.filter(thread => thread.id !== threadId)
}

const handleThreadUpdated = ({ threadId, content }) => {
  const thread = threads.value.find(t => t.id === threadId)
  if (thread) {
    thread.content = content
    thread.updated_at = new Date().toISOString()
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
  text-align: center;
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 2rem;
  color: #333;
}

.loading, .error {
  text-align: center;
  padding: 2rem;
  font-size: 1.2rem;
  color: #ffffff;
}

.error {
  color: #ef4444;
}

.threads-container {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 2rem;
  justify-items: center;
}
</style> 