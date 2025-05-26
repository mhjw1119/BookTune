<template>
  <div v-if="isOpen" class="thread-detail-modal">
    <div class="modal-overlay" @click="closeModal"></div>
    <div class="modal-content">
      <button class="close-button" @click="closeModal">&times;</button>
      
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
        <div class="thread-actions">
          <button class="like-btn" @click="toggleLike" :class="{ 'is-liked': thread.is_liked }">
            <span class="heart-icon">♥</span>
            <span class="like-count">{{ thread.like_count || 0 }}</span>
          </button>
          <div v-if="isAuthor" class="author-actions">
            <button class="edit-btn" @click="startEdit" v-if="!isEditing">수정</button>
            <button class="delete-btn" @click="confirmDelete">삭제</button>
          </div>
        </div>
      </div>

      <div class="thread-body">
        <img :src="thread.book.cover" alt="책 커버" class="book-cover">
        <div class="thread-content">
          <p class="book-title">{{ thread.book.title }}</p>
          <div v-if="!isEditing">
            <p class="thread-text">{{ thread.content }}</p>
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
          <div v-if="thread.audio_file" class="audio-player">
            <audio controls>
              <source :src="thread.audio_file" type="audio/mpeg">
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
              <img :src="getProfileImageUrl(comment.user.profile_image)" alt="프로필 이미지" class="profile-thumb">
              <span class="comment-author">{{ comment.user?.nickname }}</span>
              <span class="comment-date">{{ formatDate(comment.created_at) }}</span>
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
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'

const props = defineProps({
  thread: {
    type: Object,
    required: true
  },
  isOpen: {
    type: Boolean,
    required: true
  }
})

const emit = defineEmits(['close', 'like-toggled', 'thread-deleted'])

const comments = ref([])
const newComment = ref('')
const isEditing = ref(false)
const editedContent = ref('')
const currentUser = ref(null)

const isAuthor = computed(() => {
  return currentUser.value && props.thread?.user?.id === currentUser.value.id
})

const getProfileImageUrl = (profileImage) => {
  if (!profileImage) return ''
  if (profileImage.startsWith('http')) return profileImage
  return 'http://localhost:8000' + profileImage
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

const closeModal = () => {
  emit('close')
}

const toggleLike = async () => {
  try {
    const access = localStorage.getItem('access')
    const res = await axios.post(
      `http://localhost:8000/api/books/threads/${props.thread.id}/likes/`,
      {},
      { headers: { Authorization: `Bearer ${access}` } }
    )
    emit('like-toggled', { threadId: props.thread.id, isLiked: res.data.status === 'liked' })
  } catch (error) {
    alert('로그인이 필요합니다.')
  }
}

const fetchComments = async () => {
  try {
    const access = localStorage.getItem('access')
    const res = await axios.get(
      `http://localhost:8000/api/books/threads/${props.thread.id}/comments/`,
      { headers: { Authorization: `Bearer ${access}` } }
    )
    comments.value = res.data
  } catch (error) {
    console.error('댓글을 불러오는데 실패했습니다:', error)
  }
}

const submitComment = async () => {
  if (!newComment.value.trim()) return

  try {
    const access = localStorage.getItem('access')
    const res = await axios.post(
      `http://localhost:8000/api/books/threads/${props.thread.id}/comments/create/`,
      { content: newComment.value },
      { headers: { Authorization: `Bearer ${access}` } }
    )
    comments.value.push(res.data)
    newComment.value = ''
  } catch (error) {
    alert('댓글 작성에 실패했습니다.')
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
    if (currentUser.value.id === props.thread.user.id) {
      console.log(currentUser.value.id, props.thread.user.id)
    }
  } catch (error) {
    console.error('사용자 정보를 불러오는데 실패했습니다:', error)
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
    const res = await axios.put(
      `http://localhost:8000/api/books/threads/${props.thread.id}/update/`,
      { content: editedContent.value },
      { headers: { Authorization: `Bearer ${access}` } }
    )
    props.thread = res.data
    isEditing.value = false
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
      `http://localhost:8000/api/books/threads/${props.thread.id}/delete/`,
      { headers: { Authorization: `Bearer ${access}` } }
    )
    emit('close')
    emit('thread-deleted', props.thread.id)
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
</style> 