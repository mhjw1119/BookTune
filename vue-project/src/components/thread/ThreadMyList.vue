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
  width: 100%;
  height: 100%;
  overflow-y: auto;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.thread-grid {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  width: 100%;
}

.loading, .error, .empty {
  text-align: center;
  padding: 1.5rem;
  color: #666;
  width: 100%;
  background: var(--glass-bg);
  border-radius: 12px;
  border: 1px solid var(--glass-border);
  backdrop-filter: var(--glass-blur);
  -webkit-backdrop-filter: var(--glass-blur);
}

.error {
  color: #dc2626;
}

.empty {
  font-style: italic;
}

/* 스크롤바 스타일링 */
.thread-my-list::-webkit-scrollbar {
  width: 8px;
}

.thread-my-list::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.1);
  border-radius: 4px;
}

.thread-my-list::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 4px;
}

.thread-my-list::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 0, 0, 0.3);
}
</style> 