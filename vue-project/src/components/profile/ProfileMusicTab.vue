<template>
  <div class="profile-music-content">
    <div class="music-list">
      <div v-if="musics.length === 0" class="empty-state">
        <p>아직 생성한 뮤직이 없습니다.</p>
        <router-link to="/create-music" class="create-music-button">
          뮤직 만들기
        </router-link>
      </div>
      
      <div v-else class="music-grid">
        <div v-for="music in musics" :key="music.id" class="music-card">
          <div class="music-cover">
            <img :src="music.coverImage" :alt="music.title" />
            <div class="music-overlay">
              <button class="play-button" @click="playMusic(music)">
                <i class="fas fa-play"></i>
              </button>
            </div>
          </div>
          <div class="music-info">
            <h3 class="music-title">{{ music.title }}</h3>
            <p class="music-book">{{ music.bookTitle }}</p>
            <div class="music-actions">
              <button class="action-button edit" @click="editMusic(music)">
                <i class="fas fa-edit"></i>
              </button>
              <button class="action-button delete" @click="deleteMusic(music)">
                <i class="fas fa-trash"></i>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const musics = ref([])

const fetchMusics = async () => {
  try {
    const response = await axios.get('/api/musics/my-musics')
    musics.value = response.data
  } catch (error) {
    console.error('뮤직 목록 조회 에러:', error)
  }
}

const playMusic = (music) => {
  // 음악 재생 로직 구현
  console.log('재생:', music)
}

const editMusic = (music) => {
  router.push(`/edit-music/${music.id}`)
}

const deleteMusic = async (music) => {
  if (confirm('정말로 이 뮤직을 삭제하시겠습니까?')) {
    try {
      await axios.delete(`/api/musics/${music.id}`)
      musics.value = musics.value.filter(m => m.id !== music.id)
    } catch (error) {
      console.error('뮤직 삭제 에러:', error)
    }
  }
}

onMounted(() => {
  fetchMusics()
})
</script>

<style scoped>
.profile-music-content {
  padding: 1rem;
}

.empty-state {
  text-align: center;
  padding: 3rem;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 1rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.empty-state p {
  color: #666;
  margin-bottom: 1.5rem;
  font-size: 1.1rem;
}

.create-music-button {
  display: inline-block;
  padding: 0.8rem 1.5rem;
  background: #0078c8;
  color: white;
  text-decoration: none;
  border-radius: 0.5rem;
  font-weight: 600;
  transition: background-color 0.2s;
}

.create-music-button:hover {
  background: #005fa3;
}

.music-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1.5rem;
  padding: 1rem 0;
}

.music-card {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 1rem;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s, box-shadow 0.2s;
}

.music-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.music-cover {
  position: relative;
  padding-top: 100%;
  overflow: hidden;
}

.music-cover img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.music-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.2s;
}

.music-card:hover .music-overlay {
  opacity: 1;
}

.play-button {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.9);
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.2s;
}

.play-button:hover {
  transform: scale(1.1);
}

.play-button i {
  color: #0078c8;
  font-size: 1.2rem;
}

.music-info {
  padding: 1rem;
}

.music-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 0.5rem;
}

.music-book {
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 1rem;
}

.music-actions {
  display: flex;
  gap: 0.5rem;
}

.action-button {
  padding: 0.5rem;
  border: none;
  border-radius: 0.3rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.action-button.edit {
  background: #e3f2fd;
  color: #0078c8;
}

.action-button.delete {
  background: #ffebee;
  color: #d32f2f;
}

.action-button:hover {
  opacity: 0.8;
}

@media (max-width: 768px) {
  .music-grid {
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 1rem;
  }
}
</style> 