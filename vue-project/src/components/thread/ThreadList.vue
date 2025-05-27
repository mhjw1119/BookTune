<template>
  <div 
    class="thread-list"
    ref="scrollContainer"
    @mousedown="onMouseDown"
    @mousemove="onMouseMove"
    @mouseup="onMouseUp"
    @mouseleave="onMouseUp"
  >
    <div v-if="loading" class="loading">
      로딩 중...
    </div>
    <div v-else-if="error" class="error">
      {{ error }}
    </div>
    <div v-else-if="threads.length === 0" class="empty">
      아직 작성된 스레드가 없습니다.
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

const props = defineProps({
  bookId: {
    type: [String, Number],
    required: true
  },
  isbn: {
    type: String,
    required: true
  }
})

const store = useBookStore()
const threads = ref([])
const loading = ref(true)
const error = ref(null)
const isOwnProfile = computed(() => true)

// 마우스 드래그 스크롤 관련
const scrollContainer = ref(null)
let isDown = false
let startX = 0
let scrollLeft = 0

const onMouseDown = (e) => {
  isDown = true
  scrollContainer.value.style.cursor = 'grabbing'
  startX = e.pageX - scrollContainer.value.offsetLeft
  scrollLeft = scrollContainer.value.scrollLeft
}

const onMouseMove = (e) => {
  if (!isDown) return
  e.preventDefault()
  const x = e.pageX - scrollContainer.value.offsetLeft
  const walk = (x - startX) * 2 // 스크롤 속도 조절
  scrollContainer.value.scrollLeft = scrollLeft - walk
}

const onMouseUp = () => {
  isDown = false
  scrollContainer.value.style.cursor = 'grab'
}

const fetchThreads = async () => {
  try {
    const access = localStorage.getItem('access')
    if (!access) {
      error.value = '로그인이 필요합니다.'
      loading.value = false
      return
    }

    const response = await axios.get(`${store.API_URL}/api/books/${props.isbn}/threads/`, {
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
  }
}

onMounted(() => {
  fetchThreads()
})
</script>

<style scoped>
.thread-list {
  width: 100%;
  overflow-x: auto;
  padding-bottom: 1rem;
  cursor: grab;
  user-select: none; /* 텍스트 선택 방지 */
}

.thread-list:active {
  cursor: grabbing;
}

.loading, .error, .empty {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.error {
  color: #ef4444;
}

.threads-container {
  display: flex;
  flex-direction: row;
  gap: 1.5rem;
  padding: 0.5rem;
  min-width: min-content;
}

/* 스크롤바 스타일링 */
.thread-list::-webkit-scrollbar {
  height: 8px;
}

.thread-list::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

.thread-list::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}

.thread-list::-webkit-scrollbar-thumb:hover {
  background: #555;
}
</style> 