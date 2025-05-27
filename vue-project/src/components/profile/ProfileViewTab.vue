<template>
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
</template>

<script setup>
defineProps({
  nickname: {
    type: String,
    required: true
  },
  profileImageUrl: {
    type: String,
    default: ''
  },
  selectedGenres: {
    type: Array,
    default: () => []
  }
})
</script>

<style scoped>
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
  display: flex;
  justify-content: center;
}

.profile-image-preview {
  width: 120px;
  height: 120px;
  object-fit: cover;
  border-radius: 50%;
  border: 2px solid #ddd;
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
</style> 