<template>
  <div class="thread-card" @click="openThreadDetail">
    <div class="thread-header">
      <div class="user-info">
        <img
          v-if="thread.user.profile_image"
          :src="getProfileImageUrl(thread.user.profile_image)"
          alt="프로필 이미지"
          class="profile-thumb"
        />
      
        <span class="username">{{ thread.user.nickname }}</span>
        <span class="date">{{ formatDate(thread.created_at) }}</span>
      </div>
      <button 
        v-if="isOwnProfile"
        class="like-btn" 
        @click.stop="toggleLike" 
        :class="{ 'is-liked': isLiked }"
      >
        <span class="heart-icon">♥</span>
        <span class="like-count">{{ likeCount }}</span>
      </button>
      <div v-else class="like-btn disabled">
        <span class="heart-icon">♥</span>
        <span class="like-count">{{ likeCount }}</span>
      </div>
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

  <ThreadDetail
    v-if="isDetailOpen"
    :thread-id="thread.id"
    :thread="thread"
    :is-open="isDetailOpen"
    :is-own-profile="isOwnProfile"
    @close="closeThreadDetail"
    @like-toggled="handleLikeToggled"
    @thread-deleted="handleThreadDeleted"
    @thread-updated="handleThreadUpdated"
  />
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useBookStore } from '@/stores/books'
import axios from 'axios'
import ThreadDetail from './ThreadDetail.vue'

const props = defineProps({
  thread: {
    type: Object,
    required: true
  },
  isOwnProfile: {
    type: Boolean,
    default: true
  }
})

const store = useBookStore()
const router = useRouter()
const isDetailOpen = ref(false)

const emit = defineEmits(['like-toggled', 'thread-deleted', 'thread-updated'])

// 좋아요 상태를 props의 thread에서 직접 사용
const isLiked = computed(() => props.thread.is_liked)
const likeCount = computed(() => props.thread.like_count || 0)

const getProfileImageUrl = (profileImage) => {
  if (!profileImage) return ''
  if (profileImage.startsWith('http')) return profileImage
  return 'http://localhost:8000' + profileImage
}

const checkLikeStatus = async () => {
  try {
    const access = localStorage.getItem('access')
    if (!access) {
      return
    }

    const response = await axios.get(`${store.API_URL}/api/books/threads/${props.thread.id}/like-status/`, {
      headers: { Authorization: `Bearer ${access}` }
    })
    // computed 값은 직접 변경하지 않음
    // 필요하다면 emit 등으로 부모에게 알릴 수 있음
  } catch (error) {
    console.error('Error checking like status:', error)
  }
}

const toggleLike = async () => {
  try {
    const access = localStorage.getItem('access')
    if (!access) {
      alert('로그인이 필요합니다.')
      return
    }

    // 현재 상태를 미리 저장
    const currentLikeCount = props.thread.like_count || 0
    const currentIsLiked = props.thread.is_liked

    // 부모 컴포넌트에 상태 변경 알림
    emit('like-toggled', {
      threadId: props.thread.id,
      isLiked: !currentIsLiked,
      likeCount: currentIsLiked ? currentLikeCount - 1 : currentLikeCount + 1
    })

    // 서버 요청
    const response = await axios.post(
      `${store.API_URL}/api/books/threads/${props.thread.id}/like/`,
      {},
      { headers: { Authorization: `Bearer ${access}` } }
    )

    // 서버 응답이 실패하면 원래 상태로 되돌림
    if (response.data.status !== (!currentIsLiked ? 'liked' : 'unliked')) {
      emit('like-toggled', {
        threadId: props.thread.id,
        isLiked: currentIsLiked,
        likeCount: currentLikeCount
      })
      throw new Error('좋아요 상태가 일치하지 않습니다.')
    }
  } catch (err) {
    if (err.response?.status === 401) {
      alert('로그인이 필요합니다.')
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

const openThreadDetail = () => {
  isDetailOpen.value = true
}

const closeThreadDetail = () => {
  isDetailOpen.value = false
}

const handleLikeToggled = (data) => {
  // ThreadDetail에서 받은 좋아요 이벤트를 부모 컴포넌트로 전달
  emit('like-toggled', data)
}

const handleThreadDeleted = (threadId) => {
  emit('thread-deleted', threadId)
}

const handleThreadUpdated = (data) => {
  emit('thread-updated', data)
}

onMounted(() => {
  checkLikeStatus()
})
</script>

<style scoped>
.thread-card {
  background: white;
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  min-width: 400px; /* 최소 너비 설정 */
  max-width: 400px; /* 최대 너비 설정 */
  flex-shrink: 0; /* 카드가 압축되지 않도록 설정 */
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.thread-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.15);
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
  gap: 0.5rem;
}

.profile-thumb {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  object-fit: cover;
  border: 1px solid #eee;
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
  gap: 1rem;
}

.book-cover {
  width: 80px;
  height: 120px;
  object-fit: cover;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.thread-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.book-title {
  font-weight: 600;
  color: #444;
  font-size: 1rem;
}

.thread-text {
  color: #333;
  line-height: 1.6;
  font-size: 0.95rem;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.audio-player {
  margin-top: auto;
}

.audio-player audio {
  width: 100%;
  max-width: 250px;
}

.like-btn.disabled {
  background: #f1f2f6;
  color: #666;
  border: 1px solid #ddd;
  cursor: not-allowed;
}

.like-btn.disabled:hover {
  background: #f1f2f6;
}
</style> 