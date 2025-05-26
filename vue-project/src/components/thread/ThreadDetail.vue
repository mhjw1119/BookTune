<template>
  <div v-if="isOpen && props.thread" class="thread-detail-modal">
    <div class="modal-overlay" @click="closeModal"></div>
    <div class="modal-content">
      <button class="close-button" @click="closeModal">&times;</button>
      
      <div class="thread-header">
        <div class="user-info">
          <img
            v-if="props.thread.user?.profile_image"
            :src="getProfileImageUrl(props.thread.user.profile_image)"
            alt="프로필 이미지"
            class="profile-thumb"
          />
          <span class="username">{{ props.thread.user?.nickname }}</span>
          <span class="date">{{ formatDate(props.thread.created_at) }}</span>
        </div>
        <div class="thread-actions">
          <button class="like-btn" @click="toggleLike" :class="{ 'is-liked': props.thread.is_liked }">
            <span class="heart-icon">♥</span>
            <span class="like-count">{{ props.thread.like_count || 0 }}</span>
          </button>
          <div v-if="isAuthor" class="author-actions">
            <button class="edit-btn" @click="startEdit" v-if="!isEditing">수정</button>
            <button class="delete-btn" @click="confirmDelete">삭제</button>
          </div>
        </div>
      </div>

      <div class="thread-body">
        <img :src="props.thread.book?.cover" alt="책 커버" class="book-cover">
        <div class="thread-content">
          <p class="book-title">{{ props.thread.book?.title }}</p>
          <div v-if="!isEditing">
            <p class="thread-text">{{ props.thread.content }}</p>
          </div>
          <div v-else class="edit-form">
            <textarea 
              v-model="editedContent" 
              class="edit-textarea"
              placeholder="내용을 수정하세요..."
            ></textarea>
            <div class="edit-actions">
              <button class="save-btn" @click="saveEdit">저장</button>
              <button class="cancel-btn" @click="cancelEdit">취소</button>
            </div>
          </div>
          <div v-if="props.thread.audio_file" class="audio-player">
            <audio controls>
              <source :src="props.thread.audio_file" type="audio/mpeg">
              브라우저가 오디오 재생을 지원하지 않습니다.
            </audio>
          </div>
        </div>
      </div>

      <div class="comments-section">
        <h3 class="comment-title">댓글</h3>
        <div class="comment-list">
          <div v-for="comment in comments" :key="comment.id" class="comment-item">
            <div class="comment-header">
              <img 
                v-if="comment.user?.profile_image"
                :src="getProfileImageUrl(comment.user.profile_image)" 
                alt="프로필 이미지" 
                class="profile-thumb"
              >
              <span class="comment-author">{{ comment.user?.nickname }}</span>
              <span class="comment-date">{{ formatDate(comment.created_at) }}</span>
              <button 
                v-if="isCommentAuthor(comment) && comment.id" 
                class="delete-comment-btn" 
                @click="confirmDeleteComment(comment)"
              >삭제</button>
            </div>
            <p class="comment-content">{{ comment.content }}</p>
          </div>
        </div>
        
        <div class="comment-form">
          <textarea 
            v-model="newComment" 
            placeholder="댓글을 작성하세요..."
            class="comment-input"
          ></textarea>
          <button @click="submitComment" class="submit-comment">댓글 작성</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const props = defineProps({
  threadId: {
    type: Number,
    required: true
  },
  isOpen: {
    type: Boolean,
    required: true
  },
  thread: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['close', 'like-toggled', 'thread-deleted', 'thread-updated'])

// 상태 변수들
const comments = ref([])
const newComment = ref('')
const isEditing = ref(false)
const editedContent = ref('')
const currentUser = ref(null)

// router 설정 추가
const router = useRouter()

// 유틸리티 함수들
const getProfileImageUrl = (profileImage) => {
  if (!profileImage) return ''
  if (profileImage.startsWith('http')) return profileImage
  return 'http://localhost:8000' + profileImage
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  if (isNaN(date.getTime())) return ''
  return date.toLocaleDateString('ko-KR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// API 호출 함수들
const fetchComments = async () => {
  try {
    const access = localStorage.getItem('access')
    const res = await axios.get(
      `http://localhost:8000/api/books/threads/${props.threadId}/comments/`,
      { headers: { Authorization: `Bearer ${access}` } }
    )
    comments.value = res.data.sort((a, b) => new Date(a.created_at) - new Date(b.created_at))
  } catch (error) {
    console.error('댓글을 불러오는데 실패했습니다:', error)
  }
}

const getCurrentUser = async () => {
  try {
    const access = localStorage.getItem('access')
    if (!access) return

    const res = await axios.get('http://localhost:8000/api/auth/profile/', {
      headers: { Authorization: `Bearer ${access}` }
    })
    currentUser.value = res.data
  } catch (error) {
    console.error('사용자 정보를 불러오는데 실패했습니다:', error)
  }
}

// watch 설정
watch(() => props.isOpen, (newValue) => {
  if (newValue) {
    fetchComments()
    getCurrentUser()
  }
}, { immediate: true })

const toggleLike = async () => {
  const access = localStorage.getItem('access')
  if (!access) {
    alert('로그인이 필요합니다.')
    return
  }

  try {
    // 현재 상태를 미리 저장
    const currentLikeCount = props.thread.like_count || 0
    const currentIsLiked = props.thread.is_liked

    // 부모 컴포넌트에 상태 변경 알림
    emit('like-toggled', { 
      threadId: props.threadId,
      isLiked: !currentIsLiked,
      likeCount: currentIsLiked ? currentLikeCount - 1 : currentLikeCount + 1
    })

    // 서버 요청
    const res = await axios.post(
      `http://localhost:8000/api/books/threads/${props.threadId}/like/`,
      {},
      { headers: { Authorization: `Bearer ${access}` } }
    )

    // 서버 응답이 실패하면 원래 상태로 되돌림
    if (res.data.status !== (!currentIsLiked ? 'liked' : 'unliked')) {
      emit('like-toggled', { 
        threadId: props.threadId,
        isLiked: currentIsLiked,
        likeCount: currentLikeCount
      })
      throw new Error('좋아요 상태가 일치하지 않습니다.')
    }
  } catch (error) {
    if (error.response?.status === 401) {
      alert('로그인이 필요합니다.')
    } else {
      alert('좋아요 처리 중 오류가 발생했습니다.')
    }
  }
}

const isAuthor = computed(() => {
  if (!currentUser.value || !props.thread) return false
  return currentUser.value.id === props.thread.user?.id
})

const closeModal = () => {
  emit('close')
}

const isCommentAuthor = (comment) => {
  if (!currentUser.value || !comment.user) return false
  return currentUser.value.id === comment.user.id
}

const confirmDeleteComment = (comment) => {
  if (!comment || !comment.id) {
    console.error('댓글 정보가 올바르지 않습니다:', comment)
    return
  }
  
  if (confirm('이 댓글을 삭제하시겠습니까?')) {
    deleteComment(comment.id)
  }
}

const deleteComment = async (commentId) => {
  if (!commentId) {
    console.error('댓글 ID가 없습니다')
    return
  }

  try {
    const access = localStorage.getItem('access')
    await axios.delete(
      `http://localhost:8000/api/books/threads/${props.threadId}/comments/${commentId}/delete/`,
      { headers: { Authorization: `Bearer ${access}` } }
    )
    // 댓글 목록에서 삭제된 댓글 제거
    comments.value = comments.value.filter(comment => comment.id !== commentId)
  } catch (error) {
    console.error('댓글 삭제 실패:', error)
    alert('댓글 삭제에 실패했습니다.')
  }
}

const submitComment = async () => {
  if (!newComment.value.trim()) return

  try {
    const access = localStorage.getItem('access')
    const res = await axios.post(
      `http://localhost:8000/api/books/threads/${props.threadId}/comments/create/`,
      { content: newComment.value },
      { headers: { Authorization: `Bearer ${access}` } }
    )
    
    // 새 댓글 데이터 구성 - 서버 응답 데이터를 그대로 사용
    comments.value.push(res.data)
    newComment.value = ''
    
    // 댓글 목록 새로고침
    await fetchComments()
  } catch (error) {
    console.error('댓글 작성 실패:', error)
    alert('댓글 작성에 실패했습니다.')
  }
}

const startEdit = () => {
  editedContent.value = props.thread.content
  isEditing.value = true
}

const cancelEdit = () => {
  isEditing.value = false
  editedContent.value = ''
}

const saveEdit = async () => {
  try {
    const access = localStorage.getItem('access')
    await axios.put(
      `http://localhost:8000/api/books/threads/${props.threadId}/update/`,
      { content: editedContent.value },
      { headers: { Authorization: `Bearer ${access}` } }
    )
    await fetchComments()
    isEditing.value = false
    // 수정된 스레드 정보를 부모 컴포넌트에 전달
    emit('thread-updated', { 
      threadId: props.threadId,
      content: editedContent.value 
    })
    emit('close')
  } catch (error) {
    alert('수정에 실패했습니다.')
  }
}

const confirmDelete = () => {
  if (confirm('정말로 이 스레드를 삭제하시겠습니까?')) {
    deleteThread()
  }
}

const deleteThread = async () => {
  try {
    const access = localStorage.getItem('access')
    await axios.delete(
      `http://localhost:8000/api/books/threads/${props.threadId}/delete/`,
      { headers: { Authorization: `Bearer ${access}` } }
    )
    // 삭제된 스레드 ID를 부모 컴포넌트에 전달
    emit('thread-deleted', props.threadId)
    emit('close')
  } catch (error) {
    alert('삭제에 실패했습니다.')
  }
}

onMounted(() => {
  if (props.isOpen) {
    fetchComments()
    getCurrentUser()
  }
})
</script>

<style scoped>
.thread-detail-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
}

.modal-content {
  position: relative;
  background: white;
  padding: 2rem;
  border-radius: 1rem;
  width: 90%;
  max-width: 800px;
  max-height: 90vh;
  overflow-y: auto;
  z-index: 1001;
}

.close-button {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #666;
}

.thread-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
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
  margin-bottom: 2rem;
}

.book-cover {
  width: 180px;
  height: 240px;
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
    align-items: left;

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

.comments-section {
  margin-top: 2rem;
  border-top: 1px solid #eee;
  padding-top: 2rem;
}

.comment-list {
  margin-bottom: 2rem;
}

.comment-item {
  padding: 1rem;
  border-bottom: 1px solid #eee;
}

.comment-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
  color: #666;
}

.comment-header .profile-thumb {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  object-fit: cover;
  border: 1px solid #eee;
}

.comment-author {
  font-weight: 500;
  color: #333;
}

.comment-date {
  color: #888;
  font-size: 0.85rem;
}

.comment-content {
  line-height: 1.4;
  text-align: left;
  padding-left: 2.5rem;
  color: #333;
  margin-top: 0.5rem;
}

.comment-form {
  margin-top: 1rem;
}

.comment-input {
  width: 100%;
  min-height: 100px;
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 0.5rem;
  margin-bottom: 1rem;
  resize: vertical;
}

.submit-comment {
  background: #61bef8;
  color: white;
  border: none;
  padding: 0.8rem 1.5rem;
  border-radius: 0.5rem;
  cursor: pointer;
  font-weight: bold;
}

.submit-comment:hover {
  background: #0078c8;
}

.thread-actions {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.author-actions {
  display: flex;
  gap: 0.5rem;
}

.edit-btn, .delete-btn {
  padding: 0.5rem 1rem;
  border-radius: 20px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s;
}

.edit-btn {
  background: #61bef8;
  color: white;
  border: none;
}

.edit-btn:hover {
  background: #0078c8;
}

.delete-btn {
  background: #ff6b81;
  color: white;
  border: none;
}

.delete-btn:hover {
  background: #ff4757;
}

.edit-form {
  margin-top: 1rem;
}

.edit-textarea {
  width: 100%;
  min-height: 150px;
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 0.5rem;
  margin-bottom: 1rem;
  resize: vertical;
}

.edit-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
}

.save-btn, .cancel-btn {
  padding: 0.5rem 1.5rem;
  border-radius: 0.5rem;
  cursor: pointer;
  font-weight: 500;
}

.save-btn {
  background: #61bef8;
  color: white;
  border: none;
}

.save-btn:hover {
  background: #0078c8;
}

.cancel-btn {
  background: #f1f2f6;
  color: #666;
  border: none;
}

.cancel-btn:hover {
  background: #dfe4ea;
}

.comment-title {
  text-align: left;
  text-align: left;
  padding-left: 2.5rem;
  color: #333;
  margin-top: 0.5rem;
  margin-bottom: 1rem;
  font-size: 1.2rem;
  font-weight: 600;
}

.delete-comment-btn {
  margin-left: auto;
  padding: 0.3rem 0.8rem;
  border-radius: 15px;
  background: #ff6b81;
  color: white;
  border: none;
  font-size: 0.8rem;
  cursor: pointer;
  transition: all 0.2s;
}

.delete-comment-btn:hover {
  background: #ff4757;
}
</style> 