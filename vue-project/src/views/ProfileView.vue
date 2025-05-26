<template>
  <div class="profile-layout">
    <div class="w-full border-t my-8" style="border-color: rgba(0,0,0,0.1);"></div>

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
        <!-- 프로필 헤더 섹션 추가 -->
        <div class="profile-header">
          <div class="profile-image-section">
            <img
              v-if="profileImageUrl"
              :src="profileImageUrl"
              alt="프로필 이미지"
              class="profile-image-preview"
            />
            <div v-else class="profile-image-placeholder">이미지 없음</div>
          </div>
          <div class="profile-info">
            <h2 class="profile-nickname">{{ nickname }}</h2>
            <div class="profile-stats">
              <div class="stat-item">
                <span class="stat-value">{{ followersCount }}</span>
                <span class="stat-label">팔로워</span>
              </div>
              <div class="stat-item">
                <span class="stat-value">{{ followingsCount }}</span>
                <span class="stat-label">팔로잉</span>
              </div>
            </div>
            <button 
              v-if="!isOwnProfile" 
              @click="toggleFollow" 
              :class="['follow-button', { 'following': isFollowing }]"
            >
              {{ isFollowing ? '언팔로우' : '팔로우' }}
            </button>
          </div>
        </div>

        <div class="tab-buttons">
          <button 
            v-for="tab in visibleTabs" 
            :key="tab.id"
            @click="currentTab = tab.id"
            :class="['tab-button', { active: currentTab === tab.id }]"
          >
            {{ getTabName(tab.id) }}
          </button>
        </div>

        <div class="tab-content">
          <!-- 프로필 조회 탭 -->
          <div v-if="currentTab === 'profile-view'" class="tab-pane">
            <div class="profile-view-content">
              <div class="profile-info-section">
                <div class="profile-image-section">
                  <img
                    v-if="profileImageUrl"
                    :src="profileImageUrl"
                    alt="프로필 이미지"
                    class="profile-image-preview"
                  />
                  <div v-else class="profile-image-placeholder">이미지 없음</div>
                </div>
                <div class="profile-details">
                  <h3 class="profile-detail-title">닉네임</h3>
                  <p class="profile-detail-content">{{ nickname }}</p>
                  
                  <h3 class="profile-detail-title">좋아하는 장르</h3>
                  <div class="profile-genres">
                    <span 
                      v-for="genre in selectedGenres" 
                      :key="genre" 
                      class="genre-tag"
                    >
                      {{ genre }}
                    </span>
                    <span v-if="!selectedGenres.length" class="no-genres">선택된 장르가 없습니다</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 프로필 수정 탭 -->
          <div v-if="currentTab === 'profile-edit' && isOwnProfile" class="tab-pane">
            <!-- 프로필 이미지 업로드/미리보기 -->
            <div class="profile-image-section">
              <label for="profileImageInput" class="profile-image-label">
                <img
                  v-if="profileImageUrl"
                  :src="profileImageUrl"
                  alt="프로필 이미지"
                  class="profile-image-preview"
                />
                <div v-else class="profile-image-placeholder">이미지 추가</div>
                <input
                  id="profileImageInput"
                  type="file"
                  accept="image/*"
                  @change="onImageChange"
                  style="display: none"
                />
              </label>
            </div>

            <form @submit.prevent="updateProfile" class="profile-form">
              <div class="form-row">
                <label for="nickname" class="form-label">닉네임</label>
                <input id="nickname" v-model="nickname" class="input-box" />
              </div>
              <div class="form-row">
                <label for="description" class="form-label">좋아하는 장르</label>
                <div class="genre-checkboxes">
                  <label v-for="genre in genres" :key="genre" class="checkbox-label">
                    <input 
                      type="checkbox" 
                      :value="genre" 
                      :checked="selectedGenres.includes(genre)"
                      @change="toggleGenre(genre)"
                    />
                    {{ genre }}
                  </label>
                </div>
              </div>
              <button type="submit" class="form-button">저장</button>
            </form>
          </div>

          <!-- 좋아요한 책 탭 -->
          <div v-if="currentTab === 'liked-books'" class="tab-pane">
            <BookList v-if="likedBooks.length" :books="likedBooks" />
            <div v-else class="empty-message">좋아요한 책이 없습니다.</div>
          </div>

          <!-- 좋아요한 스레드 탭 -->
          <div v-if="currentTab === 'liked-threads'" class="tab-pane">
            <ThreadLikeList v-if="likedThreads.length" :threads="likedThreads" :is-own-profile="isOwnProfile" @refresh-threads="handleRefreshLikedThreads" />
            <div v-else class="empty-message">좋아요한 스레드가 없습니다.</div>
          </div>

          <!-- 내가 작성한 스레드 탭 -->
          <div v-if="currentTab === 'my-threads'" class="tab-pane">
            <ThreadMyList v-if="myThreads.length" :threads="myThreads" />
            <div v-else class="empty-message">작성한 스레드가 없습니다.</div>
          </div>

          <div v-if="currentTab === 'my-music'" class="tab-pane">
            <MySongList v-if="mySongs.length" :songs="mySongs" />
            <div v-else class="empty-message">만든 음악이 없습니다.</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import BookList from '@/components/BookList.vue'
import ThreadLikeList from '@/components/thread/ThreadLikeList.vue'
import ThreadMyList from '@/components/thread/ThreadMyList.vue'
import { useBookStore } from '@/stores/books'
import MySongList from '@/components/createmusic/MySongList.vue'

const route = useRoute()
const genres = [
  '문학', '인문/사회', '자기계발/실용', '예술/문화', '학습/교육', '아동/청소년', '만화'
]

const tabs = [
  { id: 'profile-view', name: '프로필 조회' },
  { id: 'profile-edit', name: '프로필 수정' },
  { id: 'liked-books', name: '좋아요한 책' },
  { id: 'liked-threads', name: '좋아요한 스레드' },
  { id: 'my-threads', name: '내가 작성한 스레드' },
  { id: 'my-music', name: '내가 만든 음악' }
]

const currentTab = ref('profile-view')
const nickname = ref('')
const selectedGenres = ref([])
const likedBooks = ref([])
const likedThreads = ref([])
const myThreads = ref([])
const mySongs = ref([])
const store = useBookStore()
const profileImage = ref(null)
const profileImageUrl = ref('')
const followersCount = ref(0)
const followingsCount = ref(0)
const isFollowing = ref(false)
const currentUserId = ref(null)
const loggedInUserId = ref(null)

// 현재 로그인한 사용자의 ID를 가져오는 함수
const getLoggedInUserId = async () => {
  try {
    const access = localStorage.getItem('access')
    if (!access) return null
    
    const response = await axios.get('http://localhost:8000/api/auth/profile/', {
      headers: { Authorization: `Bearer ${access}` }
    })
    loggedInUserId.value = response.data.id
    console.log('로그인한 사용자 ID:', loggedInUserId.value)
    return response.data.id
  } catch (error) {
    console.error('로그인한 사용자 정보를 가져오는데 실패했습니다:', error)
    return null
  }
}

// 현재 보고 있는 프로필이 자신의 것인지 확인
const isOwnProfile = computed(() => {
  console.log('현재 프로필 ID:', currentUserId.value)
  console.log('로그인한 사용자 ID:', loggedInUserId.value)
  if (!currentUserId.value || !loggedInUserId.value) return false
  return String(currentUserId.value) === String(loggedInUserId.value)
})

// 보여줄 탭 필터링
const visibleTabs = computed(() => {
  if (isOwnProfile.value) {
    return tabs
  }
  return tabs.filter(tab => tab.id !== 'profile-edit' && tab.id !== 'my-music')
})

const onImageChange = (e) => {
  const file = e.target.files[0]
  if (file) {
    profileImage.value = file
    profileImageUrl.value = URL.createObjectURL(file)
  }
}

const toggleGenre = (genre) => {
  const index = selectedGenres.value.indexOf(genre)
  if (index === -1) {
    selectedGenres.value.push(genre)
  } else {
    selectedGenres.value.splice(index, 1)
  }
}

const toggleFollow = async () => {
  try {
    const access = localStorage.getItem('access')
    const response = await axios.post(
      `http://localhost:8000/api/auth/${currentUserId.value}/follow/`,
      {},
      {
        headers: { Authorization: `Bearer ${access}` }
      }
    )
    
    isFollowing.value = response.data.status === 'followed'
    // 팔로워 수 업데이트
    followersCount.value += isFollowing.value ? 1 : -1
  } catch (error) {
    console.error('팔로우/언팔로우 에러:', error)
  }
}

// 좋아요한 스레드 새로고침 함수
const handleRefreshLikedThreads = async () => {
  try {
    const access = localStorage.getItem('access')
    const userId = currentUserId.value
    const resThreads = await axios.get(`http://localhost:8000/api/books/threads/liked/${userId}/`, {
      headers: { Authorization: `Bearer ${access}` }
    })
    likedThreads.value = resThreads.data
  } catch (error) {
    console.error('좋아요한 스레드 새로고침 에러:', error)
  }
}

onMounted(async () => {
  const access = localStorage.getItem('access')
  if (!access) {
    console.log('액세스 토큰이 없습니다.')
    return
  }

  // URL에서 사용자 ID 가져오기
  const userId = route.params.userId
  if (!userId) {
    console.log('URL에 사용자 ID가 없습니다.')
    return
  }
  currentUserId.value = userId
  console.log('URL에서 가져온 사용자 ID:', userId)

  // 로그인한 사용자의 ID 가져오기
  await getLoggedInUserId()

  try {
    // 프로필 정보 가져오기
    const res = await axios.get(`http://localhost:8000/api/auth/profile/${userId}/`, {
      headers: { Authorization: `Bearer ${access}` }
    })
    
    nickname.value = res.data.nickname
    followersCount.value = res.data.followers_count
    followingsCount.value = res.data.followings_count
    isFollowing.value = res.data.is_following
    
    // 장르 데이터 처리
    if (res.data.favorite_genres) {
      try {
        let genresData = res.data.favorite_genres
        if (typeof genresData === 'string') {
          try {
            genresData = JSON.parse(genresData)
            if (Array.isArray(genresData) && genresData.length > 0 && typeof genresData[0] === 'string') {
              try {
                genresData = JSON.parse(genresData[0])
              } catch (e) {
                console.log('두 번째 파싱 실패, 현재 데이터 사용')
              }
            }
          } catch (e) {
            console.log('첫 번째 파싱 실패, 현재 데이터 사용')
          }
        }
        selectedGenres.value = Array.isArray(genresData) ? genresData : []
      } catch (e) {
        console.error('장르 데이터 파싱 에러:', e)
        selectedGenres.value = []
      }
    }

    // 프로필 이미지 경로 처리
    if (res.data.profile_image) {
      if (res.data.profile_image.startsWith('http')) {
        profileImageUrl.value = res.data.profile_image
      } else {
        profileImageUrl.value = 'http://localhost:8000' + res.data.profile_image
      }
    }

    // 좋아요한 책 - 현재 사용자의 좋아요한 책만 가져오기
    const resBooks = await axios.get(`http://localhost:8000/api/books/liked/${userId}/`, {
      headers: { Authorization: `Bearer ${access}` }
    })
    likedBooks.value = resBooks.data

    // 좋아요한 스레드 - 현재 사용자의 좋아요한 스레드만 가져오기
    const resThreads = await axios.get(`http://localhost:8000/api/books/threads/liked/${userId}/`, {
      headers: { Authorization: `Bearer ${access}` }
    })
    likedThreads.value = resThreads.data

    // 내가 작성한 스레드
    const resMyThreads = await axios.get(`http://localhost:8000/api/books/threads/user/${userId}/`, {
      headers: { Authorization: `Bearer ${access}` }
    })
    myThreads.value = resMyThreads.data

    // 내가 만든 음악
    const resMySongs = await axios.get(`http://localhost:8000/api/songs/song_list/`, {
      headers: { Authorization: `Bearer ${access}` }
    })
    mySongs.value = resMySongs.data
  } catch (error) {
    console.error('프로필 로드 에러:', error)
    if (error.response) {
      console.error('에러 응답:', error.response.data)
      console.error('에러 상태:', error.response.status)
    }
  }
})

const updateProfile = async () => {
  try {
    const access = localStorage.getItem('access')
    const formData = new FormData()
    formData.append('nickname', nickname.value)
    formData.append('favorite_genres', JSON.stringify(selectedGenres.value))
    
    if (profileImage.value) {
      formData.append('profile_image', profileImage.value)
    }

    const response = await axios.put('http://localhost:8000/api/auth/profile/', formData, {
      headers: {
        Authorization: `Bearer ${access}`,
        'Content-Type': 'multipart/form-data'
      }
    })
    
    alert('프로필이 저장되었습니다!')
  } catch (error) {
    console.error('프로필 업데이트 에러:', error)
    alert('프로필 저장 중 오류가 발생했습니다.')
  }
}

// 탭 이름 동적 변경
const getTabName = (tabId) => {
  if (tabId === 'my-threads') {
    return `${nickname.value}의 스레드`
  }
  return tabs.find(tab => tab.id === tabId)?.name || tabId
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Indie+Flower&family=Noto+Sans+KR:wght@400;700&family=Pacifico&display=swap');

.profile-layout {
  min-height: 100vh;
  background: #f7f7f7;
  padding-bottom: 3rem;
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
  font-size: 3rem;
  transition: color 0.2s;
  font-weight: bold;
  color: #000000;
  margin-right: 1.5rem;
  margin-left: 1.5rem;
  text-decoration: none;
}

.nav-link:hover {
  color: #000000;
}

.nav-link:active {
  color: #000000;
}

.nav-link a {
  color: #000000;
  text-decoration: none;
}

.nav-link a:hover {
  color: #000000;
}

.nav-link a:active {
  color: #6366f1;
}

.nav-link a.router-link-active {
  color: #6366f1;
  /* text-decoration: none; */
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

.profile-header {
  display: flex;
  align-items: center;
  padding: 2rem;
  border-bottom: 1px solid #eee;
  gap: 3rem;
}

.profile-info {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.profile-nickname {
  font-size: 2rem;
  font-weight: 700;
  color: #333;
}

.profile-stats {
  display: flex;
  gap: 2rem;
  margin-bottom: 1.5rem;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-value {
  font-size: 1.2rem;
  font-weight: 700;
  color: #333;
}

.stat-label {
  font-size: 0.9rem;
  color: #666;
}

.follow-button {
  padding: 0.6rem 1.5rem;
  border-radius: 20px;
  cursor: pointer;
  font-weight: 600;
  transition: background-color 0.2s;
  background: #0078c8;
  color: white;
  border: none;
}

.follow-button:hover {
    background-color: #005fa3;
}

.follow-button.following {
  background: #eee;
  color: #333;
  border: 1px solid #ccc;
}

.follow-button.following:hover {
    background-color: #ddd;
}

.tab-buttons {
  display: flex;
  gap: 2rem;
  border-bottom: 1px solid #eee;
  padding: 0 2rem;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}

.tab-button {
  background: none;
  border: none;
  outline: none;
  cursor: pointer;
  padding: 1rem 0;
  font-size: 1.1rem;
  color: #666;
  transition: color 0.2s, border-bottom 0.2s;
  white-space: nowrap;
}

.tab-button.active {
  color: #333;
  border-bottom: 2px solid #0078c8;
  font-weight: 600;
}

.tab-button:hover:not(.active) {
    color: #333;
}

.tab-content {
  padding: 2rem;
}

.tab-pane {
}

.profile-view-content {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.profile-info-section {
  display: flex;
  align-items: flex-start;
  gap: 2rem;
}

.profile-image-section {
}

.profile-details {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.profile-detail-title {
  font-size: 1rem;
  font-weight: 600;
  color: #555;
  margin-bottom: 0.5rem;
}

.profile-detail-content {
  font-size: 1.1rem;
  color: #333;
  margin-bottom: 1.5rem;
}

.profile-genres {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.genre-tag {
  background: #e0e7ef;
  color: #4a5568;
  padding: 0.3rem 0.8rem;
  border-radius: 15px;
  font-size: 0.9rem;
}

.no-genres {
  font-style: italic;
  color: #888;
}

.profile-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-row {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-label {
  font-size: 1rem;
  font-weight: 600;
  color: #555;
}

.input-box {
  padding: 0.8rem 1rem;
  border: 1px solid #ddd;
  border-radius: 0.5rem;
  font-size: 1rem;
}

.input-box:focus {
  outline: none;
  border-color: #0078c8;
  box-shadow: 0 0 0 2px #0078c833;
}

.form-button {
  padding: 0.8rem 1.5rem;
  background: #0078c8;
  color: white;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  font-weight: 600;
  transition: background-color 0.2s;
  align-self: flex-start;
  margin-top: 1rem;
}

.form-button:hover {
  background-color: #005fa3;
}

.genre-checkboxes {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.3rem;
  font-size: 1rem;
  color: #333;
}

.checkbox-label input[type="checkbox"] {
  /* Custom checkbox styling if needed */
}

.empty-message {
  text-align: center;
  padding: 2rem;
  color: #666;
  font-style: italic;
  background: #f9f9f9;
  border-radius: 0.5rem;
  margin-top: 1.5rem;
  border: 1px solid #eee;
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

.profile-image-section {
  display: flex;
  justify-content: center;
  margin-bottom: 1.5rem;
}

.profile-image-label {
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.profile-image-preview {
  width: 120px;
  height: 120px;
  object-fit: cover;
  border-radius: 50%;
  border: 2px solid #ddd;
  margin-bottom: 0.5rem;
}

.profile-image-placeholder {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background: #f3f4f6;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #aaa;
  font-size: 1rem;
  border: 2px dashed #ddd;
  margin-bottom: 0.5rem;
}
</style>