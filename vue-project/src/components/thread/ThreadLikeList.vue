<template>
  <div class="thread-like-list">
    <div v-if="loading" class="loading">로딩 중...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else-if="threads.length === 0" class="empty">좋아요한 스레드가 없습니다.</div>
    <div
      v-else
      class="thread-grid"
      ref="scrollContainer"
      @mousedown="onMouseDown"
      @mousemove="onMouseMove"
      @mouseup="onMouseUp"
      @mouseleave="onMouseUp"
    >
      <ThreadItem
        v-for="thread in threads"
        :key="thread.id"
        :thread="thread"
        :is-own-profile="isOwnProfile"
        @like-toggled="handleLikeToggle"
      />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import ThreadItem from './ThreadItem.vue'

const props = defineProps({
  threads: {
    type: Array,
    required: true
  },
  isOwnProfile: {
    type: Boolean,
    default: false
  }
})

const loading = ref(false)
const error = ref(null)
const emit = defineEmits(['refresh-threads'])

// 마우스 드래그 스크롤 관련
const scrollContainer = ref(null)
let isDown = false
let startX = 0
let scrollLeft = 0

const onMouseDown = (e) => {
  isDown = true
  startX = e.pageX - scrollContainer.value.offsetLeft
  scrollLeft = scrollContainer.value.scrollLeft
}
const onMouseMove = (e) => {
  if (!isDown) return
  e.preventDefault()
  const x = e.pageX - scrollContainer.value.offsetLeft
  const walk = (x - startX)
  scrollContainer.value.scrollLeft = scrollLeft - walk
}
const onMouseUp = () => {
  isDown = false
}

const handleLikeToggle = async ({ threadId, isLiked, likeCount }) => {
  try {
    const access = localStorage.getItem('access')
    if (!access) {
      error.value = '로그인이 필요합니다.'
      return
    }

    // 현재 상태를 미리 저장
    const currentThread = props.threads.find(t => t.id === threadId)
    if (!currentThread) return

    const currentLikeCount = currentThread.like_count || 0
    const currentIsLiked = currentThread.is_liked

    // 서버 요청
    const response = await axios.post(
      `http://localhost:8000/api/books/threads/${threadId}/like/`,
      {},
      { headers: { Authorization: `Bearer ${access}` } }
    )

    // 서버 응답 로그 추가
    console.log('좋아요 요청 전 상태:', currentIsLiked)
    console.log('서버 응답:', response.data)

    // 성공적으로 처리된 경우 부모에게 새로고침 요청
    emit('refresh-threads')
  } catch (err) {
    console.error('좋아요 토글 실패:', err)
    error.value = '좋아요 상태 변경에 실패했습니다.'
  }
}
</script>

<style scoped>
.thread-like-list {
  width: 100%;
  height: 100%;
  overflow-y: auto;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.thread-grid {
  display: flex;
  flex-direction: row;
  gap: 1.5rem;
  overflow-x: auto;
  padding: 1.5rem;
  cursor: grab;
  scrollbar-width: thin;
  scrollbar-color: #bbb #eee;
}
.thread-grid:active {
  cursor: grabbing;
}
.thread-grid::-webkit-scrollbar {
  height: 10px;
}
.thread-grid::-webkit-scrollbar-thumb {
  background: #bbb;
  border-radius: 5px;
}
.thread-grid::-webkit-scrollbar-track {
  background: #eee;
  border-radius: 5px;
}
.loading {
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
.thread-like-list::-webkit-scrollbar {
  width: 8px;
}

.thread-like-list::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.1);
  border-radius: 4px;
}

.thread-like-list::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 4px;
}

.thread-like-list::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 0, 0, 0.3);
}
</style> 