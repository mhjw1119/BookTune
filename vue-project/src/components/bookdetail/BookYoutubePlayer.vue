<template>
  <div class="rounded-box px-6 py-6 flex flex-col items-center min-h-[120px]">
    <span class="section-title mb-2">AI 추천 음악</span>
    <div class="w-full flex justify-center">
      <iframe 
        v-if="videoUrl"
        class="rounded-lg shadow border border-gray-200" 
        width="320" 
        height="180" 
        :src="getYoutubeEmbedUrl(videoUrl)"
        title="YouTube video" 
        allowfullscreen
      ></iframe>
      <div v-else class="text-gray-500">
        아직 연결된 영상이 없습니다.
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  videoUrl: {
    type: String,
    default: ''
  }
})

const getYoutubeEmbedUrl = (url) => {
  if (!url) return ''
  // YouTube URL에서 비디오 ID 추출
  const videoId = url.split('v=')[1]?.split('&')[0] || 
                 url.split('youtu.be/')[1]?.split('?')[0] ||
                 url.split('embed/')[1]?.split('?')[0]
  
  if (!videoId) return url // 유효한 YouTube URL이 아닌 경우 원래 URL 반환
  return `https://www.youtube.com/embed/${videoId}`
}
</script>

<style scoped>
.rounded-box {
  border: 2.5px solid #222;
  border-radius: 1rem;
  background: #fff;
  box-shadow: 0 2px 8px 0 rgba(0,0,0,0.03);
}

.section-title {
  font-family: 'Noto Sans KR', sans-serif;
  font-weight: 700;
  font-size: 1.1rem;
  color: #222;
}
</style> 