<template>
  <div class="min-h-screen flex flex-col bg-gray-50">
    <!-- Main Content -->
    <main class="flex-1 flex flex-col items-center px-4 py-10">
      <!-- Book Title -->
      <h1 class="handwritten mb-10 text-5xl text-center tracking-wider">{{ book?.title || '책 제목' }}</h1>
      <div class="w-full max-w-5xl grid grid-cols-1 md:grid-cols-3 gap-8">
        <!-- Book Cover -->
        <div class="rounded-box flex flex-col items-center justify-center p-6 min-h-[340px]">
          <span class="section-title mb-2 text-lg">책 커버 이미지</span>
          <img :src="book?.cover || 'https://placehold.co/220x300?text=Book+Cover'" :alt="book?.title" class="rounded-lg shadow-md border border-gray-200 mt-2">
        </div>
        <!-- Book Info & Description -->
        <div class="flex flex-col gap-6 col-span-1 md:col-span-2">
          <div class="rounded-box flex flex-row items-center justify-between px-6 py-4">
            <div>
              <span class="section-title">저자명 :</span>
              <span class="ml-2 text-gray-700 font-medium">{{ book?.author }}</span>
            </div>
            <div>
              <span class="section-title">출판사 :</span>
              <span class="ml-2 text-gray-700 font-medium">{{ book?.publisher }}</span>
            </div>
          </div>
          <div class="rounded-box px-6 py-6 min-h-[120px]">
            <span class="section-title block mb-2">책 소개</span>
            <p class="text-gray-700 leading-relaxed">
              {{ book?.description || '책 소개가 없습니다.' }}
            </p>
          </div>
          <div class="rounded-box px-6 py-6 flex flex-col items-center min-h-[120px]">
            <span class="section-title mb-2">Youtube 로드 영상</span>
            <!-- Youtube Embed Placeholder -->
            <div class="w-full flex justify-center">
              <iframe 
                v-if="book?.recommended_song"
                class="rounded-lg shadow border border-gray-200" 
                width="320" 
                height="180" 
                :src="getYoutubeEmbedUrl(book.recommended_song)"
                title="YouTube video" 
                allowfullscreen
              ></iframe>
              <div v-else class="text-gray-500">
                아직 연결된 영상이 없습니다.
              </div>
            </div>
          </div>
        </div>
      </div>
      <!-- AI Music Button -->
      <div class="w-full max-w-5xl flex justify-start mt-10">
        <button class="btn-ai-music px-10 py-5 shadow-lg" @click="generateAIMusic">make AI MUSIC</button>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useBookStore } from '@/stores/books'

const route = useRoute()
const store = useBookStore()
const book = ref(null)

const getYoutubeEmbedUrl = (url) => {
  if (!url) return ''
  // YouTube URL에서 비디오 ID 추출
  const videoId = url.split('v=')[1]?.split('&')[0] || 
                 url.split('youtu.be/')[1]?.split('?')[0] ||
                 url.split('embed/')[1]?.split('?')[0]
  
  if (!videoId) return url // 유효한 YouTube URL이 아닌 경우 원래 URL 반환
  return `https://www.youtube.com/embed/${videoId}`
}

onMounted(async () => {
  const isbn = route.query.isbn
  if (isbn) {
    // 스토어에서 책 정보 가져오기
    book.value = store.books.find(b => b.isbn === isbn)
  }
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