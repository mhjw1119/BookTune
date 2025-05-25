<template>
  <div class="thread-my-list">
    <div v-if="loading" class="loading">로딩 중...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else-if="threads.length === 0" class="empty">작성한 스레드가 없습니다.</div>
    <div v-else class="thread-grid">
      <ThreadItem
        v-for="thread in threads"
        :key="thread.id"
        :thread="thread"
        @like-toggled="handleLikeToggle"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import ThreadItem from './ThreadItem.vue'

const props = defineProps({
  threads: {
    type: Array,
    required: true
  }
})

const loading = ref(false)
const error = ref(null)

const handleLikeToggle = async (threadId, isLiked) => {
  try {
    const access = localStorage.getItem('access')
    if (!access) {
      error.value = '로그인이 필요합니다.'
      return
    }

    await axios.post(`http://localhost:8000/api/books/threads/${threadId}/like/`, {}, {
      headers: { Authorization: `Bearer ${access}` }
    })
  } catch (err) {
    console.error('좋아요 토글 실패:', err)
    error.value = '좋아요 상태 변경에 실패했습니다.'
  }
}
</script>

<style scoped>
.thread-my-list {
  padding: 1rem;
}

.thread-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
  padding: 1rem;
}

.loading {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.error {
  text-align: center;
  padding: 2rem;
  color: #dc2626;
}

.empty {
  text-align: center;
  padding: 2rem;
  color: #666;
  font-style: italic;
}
</style> 