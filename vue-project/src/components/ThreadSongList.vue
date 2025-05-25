<template>
  <div class="thread-list">
    <div v-for="thread in threads" :key="thread.id" class="thread-item">
      <div class="thread-content">{{ thread.content }}</div>
      <div class="thread-book">{{ thread.book?.title }}</div>
      <div class="thread-like">좋아요: {{ thread.like_count }}</div>
      <div class="thread-audio" v-if="thread.audio_file">
        <audio controls>
          <source :src="'http://localhost:8000' + thread.audio_file" type="audio/mpeg">
        </audio>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'

const props = defineProps({ 
  threads: {
    type: Array,
    required: true
  }
})

onMounted(() => {
  console.log('ThreadSongList mounted, threads:', props.threads)
  if (props.threads.length > 0) {
    console.log('첫 번째 스레드 상세 데이터:', {
      id: props.threads[0].id,
      content: props.threads[0].content,
      book: props.threads[0].book,
      audio_file: props.threads[0].audio_file,
      like_count: props.threads[0].like_count
    })
  }
})
</script>

<style scoped>
.thread-list {
  margin-top: 1.5rem;
}
.thread-item {
  background: #fff;
  border-radius: 0.5rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.07);
  padding: 1rem;
  margin-bottom: 1rem;
}
.thread-content {
  font-weight: bold;
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
  white-space: pre-wrap;
}
.thread-book {
  color: #666;
  margin-top: 0.3rem;
}
.thread-like {
  color: #888;
  margin-top: 0.3rem;
  font-size: 0.95rem;
}
.thread-audio {
  margin-top: 1rem;
}
.thread-audio audio {
  width: 100%;
  max-width: 300px;
}
</style> 