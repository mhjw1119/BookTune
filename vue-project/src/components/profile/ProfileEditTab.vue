<template>
  <div class="profile-edit-content">
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
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const props = defineProps({
  initialNickname: {
    type: String,
    required: true
  },
  initialGenres: {
    type: Array,
    default: () => []
  },
  profileImageUrl: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update-profile'])

const genres = [
  '문학', '인문/사회', '자기계발/실용', '예술/문화', '학습/교육', '아동/청소년', '만화'
]

const nickname = ref(props.initialNickname)
const selectedGenres = ref([...props.initialGenres])
const profileImage = ref(null)
const newProfileImageUrl = ref(props.profileImageUrl)

const onImageChange = (e) => {
  const file = e.target.files[0]
  if (file) {
    profileImage.value = file
    newProfileImageUrl.value = URL.createObjectURL(file)
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

const updateProfile = async () => {
  try {
    const formData = new FormData()
    formData.append('nickname', nickname.value)
    formData.append('favorite_genres', JSON.stringify(selectedGenres.value))
    
    if (profileImage.value) {
      formData.append('profile_image', profileImage.value)
    }

    emit('update-profile', {
      formData,
      nickname: nickname.value,
      selectedGenres: selectedGenres.value,
      profileImageUrl: newProfileImageUrl.value
    })
  } catch (error) {
    console.error('프로필 업데이트 에러:', error)
  }
}
</script>

<style scoped>
.profile-edit-content {
  display: flex;
  flex-direction: column;
  gap: 2rem;
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
</style> 