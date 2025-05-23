<template>
  <div class="thread-list">
    <div v-for="thread in threads" :key="thread.id" class="thread-item">
      <div class="thread-title">{{ thread.title }}</div>
      <div class="thread-book">{{ thread.book.title }}</div>
      <div class="thread-like">좋아요: {{ thread.like_count }}</div>
    </div>
  </div>
</template>
<script setup>
defineProps({ threads: Array })
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
.thread-title {
  font-weight: bold;
  font-size: 1.1rem;
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
</style> 