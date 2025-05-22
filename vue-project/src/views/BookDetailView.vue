<template>
  <div class="min-h-screen flex flex-col bg-gray-50">
    <!-- Main Content -->
    <main class="flex-1 flex flex-col items-center px-4 py-10">
      <!-- Loading State -->
      <div v-if="loading" class="flex items-center justify-center min-h-[50vh]">
        <div class="text-gray-500">로딩 중...</div>
      </div>
      <!-- Error State -->
      <div v-else-if="error" class="flex items-center justify-center min-h-[50vh]">
        <div class="text-red-500">{{ error }}</div>
      </div>
      <!-- Content -->
      <template v-else>
        <!-- Book Title -->
        <h1 class="handwritten mb-10 text-5xl text-center tracking-wider">{{ book?.title || '책 제목' }}</h1>
        <div class="w-full max-w-5xl grid grid-cols-1 md:grid-cols-3 gap-8">
          <!-- Book Cover -->
          <BookCover 
            :cover="book?.cover"
            :title="book?.title"
          />
          <!-- Book Info & Description -->
          <div class="flex flex-col gap-6 col-span-1 md:col-span-2">
            <BookInfo 
              :author="book?.author"
              :publisher="book?.publisher"
            />
            <BookDescription 
              :description="book?.description"
            />
            <BookYoutubePlayer 
              :video-url="book?.recommended_song"
            />
          </div>
        </div>
        <AIGenerateButton @generate="generateAIMusic" />
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

const generateAIMusic = () => {
  // TODO: AI 음악 생성 로직 구현
  console.log('Generating AI Music for:', book.value?.title)
}
</script>

<style scoped>
.handwritten {
  font-family: 'Noto Sans KR', cursive;
  font-size: 2.8rem;
  letter-spacing: 0.1em;
  font-weight: 700;
}

.section-title {
  font-family: 'Noto Sans KR', sans-serif;
  font-weight: 700;
  font-size: 1.1rem;
  color: #222;
}

.rounded-box {
  border: 2.5px solid #222;
  border-radius: 1rem;
  background: #fff;
  box-shadow: 0 2px 8px 0 rgba(0,0,0,0.03);
}

.btn-ai-music {
  font-family: 'Inter', 'Noto Sans KR', sans-serif;
  font-size: 1.3rem;
  font-weight: 700;
  letter-spacing: 0.05em;
  background: linear-gradient(90deg, #6366f1 0%, #60a5fa 100%);
  color: #fff;
  border: none;
  border-radius: 0.75rem;
  box-shadow: 0 2px 8px 0 rgba(99,102,241,0.08);
  transition: background 0.2s, transform 0.1s;
}

.btn-ai-music:hover {
  background: linear-gradient(90deg, #4f46e5 0%, #2563eb 100%);
  transform: translateY(-2px) scale(1.03);
}
</style>