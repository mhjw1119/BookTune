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
        class="like-btn" 
        @click.stop="toggleLike" 
        :class="{ 'is-liked': isLiked }"
      >
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
            <source :src="getAudioFileUrl(thread.audio_file)" type="audio/mpeg">
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
    default: false
  }
})

const store = useBookStore()
const router = useRouter()
const isDetailOpen = ref(false)

const emit = defineEmits(['like-toggled', 'thread-deleted', 'thread-updated'])

// 좋아요 상태를 props의 thread에서 직접 사용
const isLiked = computed(() => {
  console.log('Thread ID:', props.thread.id, 'Is Liked:', props.thread.is_liked)
  return props.thread.is_liked
})

const likeCount = computed(() => props.thread.like_count || 0)

const getProfileImageUrl = (profileImage) => {
  if (!profileImage) return ''
  if (profileImage.startsWith('http')) return profileImage
  return 'http://localhost:8000' + profileImage
}

const getAudioFileUrl = (audioFile) => {
  if (!audioFile) return ''
  if (audioFile.startsWith('http')) return audioFile
  return 'http://localhost:8000' + audioFile
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
    console.log('Like status response:', response.data)
    // 서버에서 받은 좋아요 상태로 업데이트
    if (response.data.is_liked !== props.thread.is_liked) {
      props.thread.is_liked = response.data.is_liked
      // 부모 컴포넌트에 상태 변경 알림
      emit('like-toggled', {
        threadId: props.thread.id,
        isLiked: response.data.is_liked,
        likeCount: props.thread.like_count
      })
    }
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

    console.log('Toggling like:', {
      threadId: props.thread.id,
      currentIsLiked,
      currentLikeCount
    })

    // 서버 요청
    const response = await axios.post(
      `${store.API_URL}/api/books/threads/${props.thread.id}/like/`,
      {},
      { headers: { Authorization: `Bearer ${access}` } }
    )

    console.log('Like toggle response:', response.data)

    // 서버 응답이 성공하면 상태 업데이트
    if (response.data.status === 'liked' || response.data.status === 'unliked') {
      const newIsLiked = response.data.status === 'liked'
      props.thread.is_liked = newIsLiked
      props.thread.like_count = newIsLiked ? currentLikeCount + 1 : currentLikeCount - 1
      // 부모 컴포넌트에 상태 변경 알림
      emit('like-toggled', {
        threadId: props.thread.id,
        isLiked: newIsLiked,
        likeCount: newIsLiked ? currentLikeCount + 1 : currentLikeCount - 1
      })
    } else {
      throw new Error('좋아요 상태가 일치하지 않습니다.')
    }
  } catch (err) {
    console.error('Like toggle error:', err)
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
  background: rgb(255, 255, 255);
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  width: 600px;
  max-width: 600px;
  min-width: 600px;
  flex-shrink: 0;
  margin: 0 auto;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  border: 1px solid rgba(0, 0, 0, 0.15);

}

.thread-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.thread-header {
  display: flex;
  justify-content: space-between;
  align-itms: center;
  margin-bottom: 1rem;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.profile-thumb {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  object-fit: cover;
  margin-right: 0.5rem;
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