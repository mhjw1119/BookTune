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
            <ThreadLikeList v-if="likedThreads.length" :threads="likedThreads" />
            <div v-else class="empty-message">좋아요한 스레드가 없습니다.</div>
          </div>

          <!-- 내가 작성한 스레드 탭 -->
          <div v-if="currentTab === 'my-threads'" class="tab-pane">
            <ThreadMyList v-if="myThreads.length" :threads="myThreads" />
            <div v-else class="empty-message">작성한 스레드가 없습니다.</div>
          </div>

          <div v-if="currentTab === 'my-music'" class="tab-pane">
            <MusicList v-if="mySongs.length" :songs="mySongs" />
            <div v-else class="empty-message">만든 음악이 없습니다.</div>
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
  '문학', '인문/사회', '자기계발/실용', '예술/문화', '학습/교육', '아동/청소년', '만화'
]

const tabs = [
  { id: 'profile', name: '프로필 수정' },
  { id: 'liked-books', name: '좋아요한 책' },
  { id: 'liked-threads', name: '좋아요한 스레드' },
  { id: 'my-threads', name: '내가 작성한 스레드' },
  { id: 'my-music', name: '내가 만든 음악' }
]

const currentTab = ref('profile')
const nickname = ref('')
const selectedGenres = ref([])
const likedBooks = ref([])
const likedThreads = ref([])
const myThreads = ref([])
const mySongs = ref([])
const store = useBookStore()
const profileImage = ref(null)
const profileImageUrl = ref('')

const onImageChange = (e) => {
  const file = e.target.files[0]
  if (file) {
    profileImage.value = file
    profileImageUrl.value = URL.createObjectURL(file)
  }
}

const toggleGenre = (genre) => {
  console.log('토글 전 장르:', selectedGenres.value)
  const index = selectedGenres.value.indexOf(genre)
  if (index === -1) {
    selectedGenres.value.push(genre)
  } else {
    selectedGenres.value.splice(index, 1)
  }
  console.log('토글 후 장르:', selectedGenres.value)
}

onMounted(async () => {
  const access = localStorage.getItem('access')
  if (!access) return

  try {
    // 프로필 정보 가져오기
    const res = await axios.get('http://localhost:8000/api/auth/profile/', {
      headers: { Authorization: `Bearer ${access}` }
    })
    nickname.value = res.data.nickname
    
    // 장르 데이터 처리
    console.log('서버에서 받은 장르 데이터:', res.data.favorite_genres)
    
    if (res.data.favorite_genres) {
      try {
        let genresData = res.data.favorite_genres
        
        // 문자열인 경우 JSON 파싱 시도
        if (typeof genresData === 'string') {
          try {
            // 첫 번째 파싱
            genresData = JSON.parse(genresData)
            // 배열의 첫 번째 요소가 문자열인 경우 한 번 더 파싱
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
        
        // 최종적으로 배열이 아닌 경우 빈 배열로 초기화
        selectedGenres.value = Array.isArray(genresData) ? genresData : []
        console.log('최종 선택된 장르:', selectedGenres.value)
      } catch (e) {
        console.error('장르 데이터 파싱 에러:', e)
        selectedGenres.value = []
      }
    } else {
      selectedGenres.value = []
    }

    // 프로필 이미지 경로 처리
    if (res.data.profile_image) {
      if (res.data.profile_image.startsWith('http')) {
        profileImageUrl.value = res.data.profile_image
      } else {
        profileImageUrl.value = 'http://localhost:8000' + res.data.profile_image
      }
    } else {
      profileImageUrl.value = ''
    }

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
  } catch (error) {
    console.error('프로필 로드 에러:', error)
  }
})

const updateProfile = async () => {
  try {
    const access = localStorage.getItem('access')
    const formData = new FormData()
    formData.append('nickname', nickname.value)
    
    // 현재 선택된 장르만 전송 (기존 데이터 덮어쓰기)
    const genresToSave = [...selectedGenres.value]
    console.log('저장할 장르 데이터:', genresToSave)
    formData.append('favorite_genres', JSON.stringify(genresToSave))
    
    if (profileImage.value) {
      formData.append('profile_image', profileImage.value)
    }

    const response = await axios.put('http://localhost:8000/api/auth/profile/', formData, {
      headers: {
        Authorization: `Bearer ${access}`,
        'Content-Type': 'multipart/form-data'
      }
    })
    
    console.log('서버 응답:', response.data)
    
    // 저장 후 현재 선택된 장르 유지
    selectedGenres.value = genresToSave

    alert('프로필이 저장되었습니다!')
  } catch (error) {
    console.error('프로필 업데이트 에러:', error)
    alert('프로필 저장 중 오류가 발생했습니다.')
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Indie+Flower&family=Noto+Sans+KR:wght@400;700&family=Pacifico&display=swap');

.profile-layout {
  min-height: 100vh;
  background: #f7f7f7;
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

.tab-buttons {
  display: flex;
  justify-content: center;
  gap: 2rem;
  border-bottom: none;
  background: none;
  padding: 1rem 0;
}

.tab-button {
  margin-top: 1rem;
  font-family: 'Noto Sans KR', sans-serif;
  font-size: 1.5rem;
  font-weight: bold;
  color: #bdbdbd;
  background: none;
  border: none;
  outline: none;
  cursor: pointer;
  padding: 0 1.5rem 0.5rem 1.5rem;
  position: relative;
  transition: color 0.2s;
  text-decoration: none;
}

.tab-button:hover {
  color: #6fe192;
}

.tab-button.active {
  color: #000000;
}

.tab-button.active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: #000000;
}

.tab-content {
  padding: 2rem;
  margin-top: 2rem;
}

.tab-pane {
  text-align: center;
  animation: fadeIn 0.3s ease-in-out;
}

.profile-form {
  max-width: 600px;
  margin: 0 auto;
  background: #fff;
  padding: 2rem;
}

.form-row {
  margin-bottom: 2rem;
}

.form-label {
  font-weight: bold;
  margin-bottom: 0.5rem;
  display: block;
  font-size: 1.1rem;
}

.input-box {
  text-align: center;
  width: 50%;
  border: 1px solid #d1d5db;
  border-radius: 1rem;
  padding: 0.8rem 1.2rem;
  font-size: 1rem;
  background: #ffffff;
  margin-bottom: 0.2rem;
  resize: none;
}

.input-desc {
  font-size: 0.9rem;
  color: #888;
  margin-bottom: 0.5rem;
}

.genre-checkboxes {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-top: 0.5rem;
  text-align: center;
}

.checkbox-label {
  display: flex;
  align-items: center;
  font-size: 1rem;
}

.form-button {
  width:20%;
  background: #61bef8;
  color: #fff;
  font-weight: bold;
  font-size: 1.2rem;
  border: none;
  border-radius: 0.9rem;
  padding: 0.9rem 0;
  margin-top: 2rem;
  transition: background 0.2s;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

.form-button:hover {
  background: #0078c8;
}

.profile-likes-title {
  font-family: 'Noto Sans KR', sans-serif;
  font-size: 2rem;
  margin-bottom: 1.5rem;
  color: #333;
}

.empty-message {
  text-align: center;
  padding: 3rem;
  color: #666;
  font-family: 'Noto Sans KR', sans-serif;
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