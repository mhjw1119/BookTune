<template>
  <div class="profile-layout">
    <div class="flex items-center gap-8 nav-bar">
      <a href="#" class="nav-link text-gray-800">
        <RouterLink :to="{ name: 'home'}">Home</RouterLink>
      </a>
    </div>
    <div class="flex flex-col items-center text-center pt-32">
      <span class="logo text-gray-900">PROFILE</span>
    </div>
    <div class="profile-content">
      <div class="profile-tabs">
        <div class="tab-buttons">
          <button 
            v-for="tab in tabs" 
            :key="tab.id"
            @click="currentTab = tab.id"
            :class="['tab-button', { active: currentTab === tab.id }]"
          >
            {{ tab.name }}
          </button>
        </div>

        <div class="tab-content">
          <!-- 프로필 수정 탭 -->
          <div v-if="currentTab === 'profile'" class="tab-pane">
            <h2 class="profile-likes-title">프로필 수정</h2>
            <form @submit.prevent="updateProfile" class="profile-form">
              <div class="form-row">
                <label for="nickname">닉네임:</label>
                <input id="nickname" v-model="nickname" class="input-box" />
              </div>
              <div class="form-row">
                <label>좋아하는 장르:</label>
                <div class="genre-checkboxes">
                  <label v-for="genre in genres" :key="genre" class="checkbox-label">
                    <input type="checkbox" :value="genre" v-model="selectedGenres" />
                    {{ genre }}
                  </label>
                </div>
              </div>
              <button type="submit" class="form-button">저장</button>
            </form>
          </div>

          <!-- 좋아요한 책 탭 -->
          <div v-if="currentTab === 'liked-books'" class="tab-pane">
            <h2 class="profile-likes-title">좋아요한 책</h2>
            <BookList v-if="likedBooks.length" :books="likedBooks" />
            <div v-else class="empty-message">좋아요한 책이 없습니다.</div>
          </div>

          <!-- 좋아요한 스레드 탭 -->
          <div v-if="currentTab === 'liked-threads'" class="tab-pane">
            <h2 class="profile-likes-title">좋아요한 스레드</h2>
            <ThreadLikeList v-if="likedThreads.length" :threads="likedThreads" />
            <div v-else class="empty-message">좋아요한 스레드가 없습니다.</div>
          </div>

          <!-- 내가 작성한 스레드 탭 -->
          <div v-if="currentTab === 'my-threads'" class="tab-pane">
            <h2 class="profile-likes-title">내가 작성한 스레드</h2>
            <ThreadMyList v-if="myThreads.length" :threads="myThreads" />
            <div v-else class="empty-message">작성한 스레드가 없습니다.</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import BookList from '@/components/BookList.vue'
import ThreadLikeList from '@/components/thread/ThreadLikeList.vue'
import ThreadMyList from '@/components/thread/ThreadMyList.vue'
import { useBookStore } from '@/stores/books'

const genres = [
  '문학', '인문/사회', '자기계발/실용', '예술/문화', '학습/교육', '아동/청소년'
]

const tabs = [
  { id: 'profile', name: '프로필 수정' },
  { id: 'liked-books', name: '좋아요한 책' },
  { id: 'liked-threads', name: '좋아요한 스레드' },
  { id: 'my-threads', name: '내가 작성한 스레드' }
]

const currentTab = ref('profile')
const nickname = ref('')
const selectedGenres = ref([])
const likedBooks = ref([])
const likedThreads = ref([])
const myThreads = ref([])
const store = useBookStore()

onMounted(async () => {
  const access = localStorage.getItem('access')
  if (!access) return

  // 프로필 정보 가져오기
  const res = await axios.get('http://localhost:8000/api/auth/profile/', {
    headers: { Authorization: `Bearer ${access}` }
  })
  nickname.value = res.data.nickname
  selectedGenres.value = res.data.favorite_genres || []

  // 좋아요한 책
  const resBooks = await axios.get('http://localhost:8000/api/books/liked/', {
    headers: { Authorization: `Bearer ${access}` }
  })
  likedBooks.value = resBooks.data

  // 좋아요한 스레드
  const resThreads = await axios.get('http://localhost:8000/api/books/threads/liked/', {
    headers: { Authorization: `Bearer ${access}` }
  })
  likedThreads.value = resThreads.data

  // 내가 작성한 스레드
  const resMyThreads = await axios.get('http://localhost:8000/api/books/threads/', {
    headers: { Authorization: `Bearer ${access}` }
  })
  myThreads.value = resMyThreads.data.filter(thread => thread.user.id === res.data.id)
})

const updateProfile = async () => {
  const access = localStorage.getItem('access')
  await axios.put('http://localhost:8000/api/auth/profile/', {
    nickname: nickname.value,
    favorite_genres: selectedGenres.value
  }, {
    headers: { Authorization: `Bearer ${access}` }
  })
  alert('프로필이 저장되었습니다!')
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Indie+Flower&family=Noto+Sans+KR:wght@400;700&family=Pacifico&display=swap');

.profile-layout {
  min-height: 100vh;
  background: #f7f8fa;
}

.logo {
  font-family: 'Indie Flower', cursive;
  font-size: 6rem;
  letter-spacing: 0.05em;
}

.nav-bar {
  padding: 2rem 0 0 2rem;
}

.nav-link {
  font-family: 'Indie Flower', cursive;
  font-size: 2rem;
  transition: color 0.2s;
  font-weight: bold;
  color: #000000;
  text-decoration: none;
}

.nav-link:hover {
  color: #6366f1;
}

.nav-link:active {
  color: #6366f1;
}

.profile-content {
  margin-top: 3rem;
  padding: 0 2rem;
}

.profile-tabs {
  max-width: 1200px;
  margin: 3rem auto;
  background: white;
  border-radius: 1rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.07);
  overflow: hidden;
}

.tab-buttons {
  display: flex;
  border-bottom: 1px solid #e5e7eb;
  background: #f9fafb;
}

.tab-button {
  padding: 1rem 2rem;
  font-size: 1.1rem;
  font-weight: 500;
  color: #4b5563;
  background: none;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
  position: relative;
}

.tab-button:hover {
  color: #6366f1;
}

.tab-button.active {
  color: #6366f1;
}

.tab-button.active::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 0;
  right: 0;
  height: 2px;
  background: #6366f1;
}

.tab-content {
  padding: 2rem;
}

.tab-pane {
  animation: fadeIn 0.3s ease-in-out;
}

.profile-form {
  max-width: 600px;
  margin: 0 auto;
  background: #fff;
  padding: 2rem;
  border-radius: 1rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.07);
}

.form-row {
  margin-bottom: 1.5rem;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.input-box {
  width: 100%;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  padding: 0.5rem 1rem;
  font-size: 1rem;
  margin-top: 0.5rem;
  margin-bottom: 0.5rem;
}

.genre-checkboxes {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-top: 0.5rem;
}

.checkbox-label {
  display: flex;
  align-items: center;
  font-size: 1rem;
}

.form-button {
  font-family: 'Indie Flower', cursive;
  font-size: 1.2rem;
  font-weight: bold;
  padding: 0.5rem 2rem;
  border: 2px solid #333;
  border-radius: 0.5rem;
  background-color: white;
  transition: all 0.2s ease-in-out;
  margin-top: 1rem;
}

.form-button:hover {
  background-color: #f3f4f6;
}

.profile-likes-title {
  font-family: 'Indie Flower', cursive;
  font-size: 2rem;
  margin-bottom: 1.5rem;
  color: #333;
}

.empty-message {
  text-align: center;
  padding: 3rem;
  color: #666;
  font-style: italic;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>