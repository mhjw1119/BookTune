<template>
  <div class="book-detail">
    <main class="main-content">
      <!-- Loading State -->
      <div v-if="loading" class="loading">
        <div>로딩 중...</div>
      </div>
      <!-- Error State -->
      <div v-else-if="error" class="error">
        <div>{{ error }}</div>
      </div>
      <!-- Content -->
      <template v-else>
        <!-- Book Title -->
        <h1 class="book-title">{{ book?.title || '책 제목' }}</h1>
        <div class="content-container">
          <!-- Book Cover -->
          <div class="cover-container">
            <BookCover 
              :cover="book?.cover"
              :title="book?.title"
              class="book-cover"
            />
          </div>
          <!-- Book Info & Description -->
          <div class="info-container">
            <BookInfo 
              :author="book?.author"
              :publisher="book?.publisher"
              class="info-section"
            />
            <BookDescription 
              :description="book?.description"
              class="info-section"
            />
            <div class="youtube-ai-container">
              <BookYoutubePlayer 
                :video-url="book?.recommended_song"
                class="youtube-section"
              />
              <AIGenerateButton 
                v-if="book && book.id"
                :book-id="book.id" 
                @generate="handleGenerateMusic" 
                class="AI-section"
              />
            </div>
          </div>
        </div>
      </template>
    </main>
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useBookStore } from '@/stores/books'
import BookCover from '@/components/bookdetail/BookCover.vue'
import BookInfo from '@/components/bookdetail/BookInfo.vue'
import BookDescription from '@/components/bookdetail/BookDescription.vue'
import BookYoutubePlayer from '@/components/bookdetail/BookYoutubePlayer.vue'
import AIGenerateButton from '@/components/bookdetail/AIGenerateButton.vue'

const props = defineProps({
  isbn: {
    type: String,
    required: true
  }
})

const route = useRoute()
const store = useBookStore()
const book = ref(null)
const loading = ref(true)
const error = ref(null)

onMounted(() => {
  axios({
    method: 'get',
    url: `${store.API_URL}/api/books/${props.isbn}/`,
  })
  .then((res) => {
    console.log(res.data)
    book.value = res.data
    loading.value = false
  })
  .catch(err => {
    console.log(err)
    error.value = '책 정보를 불러오는데 실패했습니다.'
    loading.value = false
  })
})

const handleGenerateMusic = (data) => {
  console.log('음악 생성 이벤트 수신:', data);
  generateAIMusic(data);
};

const generateAIMusic = (data) => {
  console.log('Generating AI Music for:', book.value?.title, 'Data:', data);
  // TODO: AI 음악 생성 로직 구현
};
</script>

<style scoped>
.book-detail {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #f9fafb;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2.5rem 1rem;
}

.loading, .error {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 50vh;
}

.error {
  color: #ef4444;
}

.book-title {
  font-family: 'Noto Sans KR', cursive;
  font-size: 2.8rem;
  letter-spacing: 0.1em;
  font-weight: 700;
  margin-bottom: 2.5rem;
  text-align: center;
}

.content-container {
  width: 100%;
  max-width: 1200px;
  display: grid;
  grid-template-columns: 1fr 3fr;
  gap: 2rem;
  margin-left: -20px;

}

.cover-container {
  display: flex;
  justify-content: flex-start;
  margin-left: 0px;
}

.book-cover {
  width: 400px;
  max-width: 400px;
  height: 560px;
  margin : 0px;
  border: 0px;
}

.info-container {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.info-section {
  width: 100%;
  padding: 1.5rem;
  background: white;
  border-radius: 1rem;
}

@media (max-width: 768px) {
  .content-container {
    grid-template-columns: 1fr;
  }
  
  .book-cover {
    max-width: 400px;
    margin: 0 auto;
  }

}

.youtube-ai-container {
  display: flex;
  gap: 2rem;
  align-items: flex-start;
  margin-right: -64px;
}

.youtube-section {
  flex: 1;
  margin-left: 0px;
  margin-right: 0px;
  border: 0px;    
}

.AI-section {
  width: auto;
  min-width: 200px;
  min-height: 200px;
}
</style>