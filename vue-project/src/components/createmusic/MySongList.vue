<template>
    <div>
      <h2 class="profile-likes-title">내가 만든 노래</h2>
      <div v-if="songs.length" class="songs-container">
        <div v-for="song in songs" :key="song.id" class="my-song-card">
          <div class="song-info">
            <h3 class="song-title">{{ song.title }}</h3>
            <div class="song-controls">
              <audio v-if="song.audio_file_url" controls :src="song.audio_file_url"></audio>
              <a 
                v-if="song.audio_file_url" 
                :href="song.audio_file_url" 
                download 
                class="download-button"
              >
                다운로드
              </a>
            </div>
          </div>
        </div>
      </div>
      <div v-else class="empty-message">아직 만든 노래가 없습니다.</div>
    </div>
  </template>
  
  <script setup>
  defineProps({ songs: Array })
  </script>
  
  <style scoped>
  .songs-container {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    padding: 1rem;
  }
  
  .my-song-card {
    background: white;
    border-radius: 0.5rem;
    padding: 1.5rem;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }
  
  .song-info {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }
  
  .song-title {
    font-size: 1.25rem;
    font-weight: 600;
    color: #333;
    margin: 0;
  }
  
  .song-controls {
    display: flex;
    align-items: center;
    gap: 1rem;
  }
  
  .download-button {
    padding: 0.5rem 1rem;
    background-color: #6366f1;
    color: white;
    border-radius: 0.375rem;
    text-decoration: none;
    font-weight: 500;
    transition: background-color 0.2s;
  }
  
  .download-button:hover {
    background-color: #4f46e5;
  }
  
  .empty-message {
    text-align: center;
    padding: 2rem;
    color: #666;
    font-style: italic;
  }
  
  audio {
    width: 100%;
    max-width: 300px;
  }
  </style>