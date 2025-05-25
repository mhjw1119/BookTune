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
      <!-- 프로필 이미지 업로드/미리보기 (폼 위에 추가) -->
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
      <div class="profile-likes">
        <h2 class="profile-likes-title">좋아요한 책</h2>
        <BookList v-if="likedBooks.length" :books="likedBooks" />
        <div v-else>좋아요한 책이 없습니다.</div>
        <h2>좋아요한 스레드</h2>
        <ThreadSongList v-if="likedThreads.length" :threads="likedThreads" />
        <div v-else>좋아요한 스레드가 없습니다.</div>
      </div>
    </div>
    <MySongList :songs="mySongs" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import BookList from '@/components/BookList.vue'
import ThreadSongList from '@/components/ThreadSongList.vue'
import { useBookStore } from '@/stores/books'
import MySongList from '@/components/createmusic/MySongList.vue'

const genres = [
  '문학', '인문/사회', '자기계발/실용', '예술/문화', '학습/교육', '아동/청소년'
]
const nickname = ref('')
const selectedGenres = ref([])
const likedBooks = ref([])
const likedThreads = ref([])
const store = useBookStore()

// 프로필 이미지 관련
const profileImage = ref(null)
const profileImageUrl = ref('')
const mySongs = ref([])

const onImageChange = (e) => {
  const file = e.target.files[0]
  if (file) {
    profileImage.value = file
    profileImageUrl.value = URL.createObjectURL(file)
  }
}

onMounted(async () => {
  const access = localStorage.getItem('access')
  const res = await axios.get('http://localhost:8000/api/auth/profile/', {
    headers: { Authorization: `Bearer ${access}` }
  })
  nickname.value = res.data.nickname
  selectedGenres.value = res.data.favorite_genres || []

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

  // 좋아요한 ThreadSong (API 경로 수정)
  const resThreads = await axios.get('http://localhost:8000/api/books/threads/liked/', {
    headers: { Authorization: `Bearer ${access}` }
  })
  likedThreads.value = resThreads.data

  // 내가 만든 노래
  const resMySongs = await axios.get('http://localhost:8000/api/songs/song_list/', {
    headers: { Authorization: `Bearer ${access}` }
  })
  console.log('mySongs:', resMySongs.data)
  mySongs.value = resMySongs.data
})

const updateProfile = async () => {
  const access = localStorage.getItem('access')
  const formData = new FormData()
  formData.append('nickname', nickname.value)
  formData.append('favorite_genres', JSON.stringify(selectedGenres.value))
  if (profileImage.value) {
    formData.append('profile_image', profileImage.value)
  }
  await axios.put('http://localhost:8000/api/auth/profile/', formData, {
    headers: {
      Authorization: `Bearer ${access}`,
      'Content-Type': 'multipart/form-data'
    }
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
.profile-form {
  max-width: 400px;
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
</style>