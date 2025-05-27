<template>
    <div>
      <h2 class="profile-likes-title">내가 만든 노래</h2>
      <div v-if="songs.length" class="songs-container">
        <div v-for="song in songs" :key="song.id" class="my-song-card">
          <div class="song-info">
            <div class="book-info" v-if="song.book">
              <img :src="song.book.cover" :alt="song.book.title" class="book-cover">
              <div class="book-details">
                <h4 class="book-title">{{ song.book.title }}</h4>
                <p class="book-author">{{ song.book.author }}</p>
              </div>
            </div>
            <div class="song-header">
              <h3 class="song-title">{{ song.title || '제목 없음' }}</h3>
              <p class="song-date">{{ formatDate(song.created_at) }}</p>
            </div>
            <div class="song-controls">
              <audio v-if="song.audio_file_url" controls :src="song.audio_file_url"></audio>
            </div>
          </div>
        </div>
      </div>
      <div v-else class="empty-message">아직 만든 노래가 없습니다.</div>
    </div>
  </template>
  
  <script setup>
  import { defineProps } from 'vue'
  
  const props = defineProps({ 
    songs: {
      type: Array,
      required: true
    }
  })
  
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
  </script>
  
  <style scoped>
  .profile-likes-title {
    font-size: 1.8rem;
    font-weight: 700;
    color: #1a1a1a;
    margin-bottom: 2rem;
    text-align: left;
    padding: 0 1rem;
  }
  
  .songs-container {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 2rem;
    padding: 1rem;
  }
  
  .my-song-card {
    background: linear-gradient(145deg, #ffffff, #f5f7fa);
    border-radius: 1rem;
    padding: 1.5rem;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
  }
  
  .my-song-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 4px;
    background: linear-gradient(90deg, #6366f1, #60a5fa);
    opacity: 0;
    transition: opacity 0.3s ease;
  }
  
  .my-song-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  }
  
  .my-song-card:hover::before {
    opacity: 1;
  }
  
  .song-info {
    display: flex;
    flex-direction: column;
    gap: 1.25rem;
  }
  
  .book-info {
    display: flex;
    gap: 1rem;
    align-items: center;
    padding-bottom: 1rem;
    border-bottom: 1px solid #e5e7eb;
  }
  
  .book-cover {
    width: 80px;
    height: 120px;
    object-fit: cover;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }
  
  .book-details {
    flex: 1;
    min-width: 0;
  }
  
  .book-title {
    font-size: 1.1rem;
    font-weight: 600;
    color: #1a1a1a;
    margin-bottom: 0.5rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  
  .book-author {
    font-size: 0.9rem;
    color: #666;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  
  .song-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
  }
  
  .song-title {
    font-size: 1.2rem;
    font-weight: 600;
    color: #1a1a1a;
    margin: 0;
  }
  
  .song-date {
    font-size: 0.85rem;
    color: #666;
    margin: 0;
  }
  
  .song-controls {
    margin-top: 0.5rem;
  }
  
  .song-controls audio {
    width: 100%;
    height: 40px;
    border-radius: 20px;
  }
  
  .empty-message {
    text-align: center;
    padding: 2rem;
    color: #666;
    font-style: italic;
  }
  </style>