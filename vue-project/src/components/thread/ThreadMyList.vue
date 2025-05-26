<template>
  <div class="thread-my-list">
    <div v-if="loading" class="loading">로딩 중...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else-if="threads.length === 0" class="empty">작성한 스레드가 없습니다.</div>
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
  display: flex;
  flex-direction: row;
  gap: 2rem;
  overflow-x: auto;
  padding: 1rem;
  cursor: grab;
  scrollbar-width: thin;
  scrollbar-color: #bbb #eee;
  align-items: flex-start;
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