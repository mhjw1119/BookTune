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
            <LikeButton 
              :isbn="props.isbn"
              class="like-button-container"
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
              <ThreadButton 
                v-if="book && book.id"
                :book-id="book.id" 
                :isbn="props.isbn"
                @generate="handleGenerateMusic" 
                class="AI-section"
              />
            </div>
          </div>
        </div>
        <!-- Thread List Section -->
        <div class="thread-list-section">
          <h2 class="section-title">이 책에 대한 스레드</h2>
          <ThreadList 
            v-if="book && book.id"
            :book-id="book.id"
            :isbn="props.isbn"
          />
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
import ThreadButton from '@/components/bookdetail/ThreadButton.vue'
import LikeButton from '@/components/bookdetail/LikeButton.vue'
import ThreadList from '@/components/thread/ThreadList.vue'

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
  font-family: 'Noto Sans KR', sans-serif;
  font-size: 2.2rem;
  line-height: 1.4;
  letter-spacing: -0.02em;
  font-weight: 700;
  margin-bottom: 2.5rem;
  text-align: center;
  padding: 0 2rem;
  max-width: 800px;
  word-break: keep-all;
  overflow-wrap: break-word;
  color: #1a1a1a;
  position: relative;
  display: inline-block;
}

.book-title::after {
  content: '';
  display: block;
  width: 800px;
  height: 1px;
  background: linear-gradient(90deg, #c7c7ca, #d3d4d4);
  margin: 1rem auto 0;
  border-radius: 2px;
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
  position: relative;
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
  border: 0px;
  border-radius: 1rem;
}

@media (max-width: 768px) {
  .book-title {
    font-size: 1.8rem;
    padding: 0 1rem;
    width: 90%;
  }
  
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
  min-height: 100px;
  margin-top: 3rem;
}

.like-button-container {
  position: absolute;
  top: 15px;
  right: 15px;
  bottom: auto;
  left: auto;
  transform: none;
  z-index: 10;
}

.thread-list-section {
  width: 100%;
  max-width: 1200px;
  margin-top: 3rem;
  padding: 0 1rem;
}

.section-title {
  font-family: 'Noto Sans KR', sans-serif;
  font-size: 1.8rem;
  font-weight: 700;
  color: #1a1a1a;
  margin-bottom: 2rem;
  text-align: left;
}
</style>