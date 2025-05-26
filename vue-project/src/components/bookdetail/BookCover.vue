<template>
  <div class="rounded-box flex flex-col items-center justify-center p-6 min-h-[340px]">
    <span class="section-title mb-2 text-lg"></span>
    <img :src="cover || 'https://placehold.co/220x300?text=Book+Cover'" :alt="title" class="rounded-lg shadow-md border border-gray-200 mt-2 cover-img">
  </div>
</template>

<script setup>
defineProps({
  cover: {
    type: String,
    default: ''
  },
  title: {
    type: String,
    default: ''
  }
})
</script>

<style scoped>
.rounded-box {
  background: #fff;
  border-radius: 1rem;
  box-shadow: 0 4px 24px rgba(0,0,0,0.08);
  border: 1px solid #eee;
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 340px;
}

.section-title {
  font-family: 'Noto Sans KR', sans-serif;
  font-weight: 700;
  font-size: 1.1rem;
  color: #222;
  margin-bottom: 1rem;
  padding: 0 1.5rem;
}

.cover-img {
  width: 100%;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  border: 1px solid #ddd;
  margin-top: 1rem;
}
</style> 