<template>
    <div>
      <h2 class="profile-likes-title">내가 만든 노래</h2>
      <div v-if="songs.length">
        <div v-for="song in songs" :key="song.id" class="my-song-card">
          <p>{{ song.title }}</p>
          <audio v-if="song.audio_file_url" controls :src="song.audio_file_url"></audio>
        </div>
      </div>
      <div v-else>아직 만든 노래가 없습니다.</div>
    </div>
  </template>
  
  <script setup>
  defineProps({ songs: Array })
  </script>
  
  <style scoped>
  .my-song-card {
    margin-bottom: 1rem;
  }
  </style>