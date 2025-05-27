<template>
  <div class="book-info">
    <div class="info-container">
      <div class="info-item">
        <span class="section-title">저자명 :</span>
        <span class="info-text">{{ author }}</span>
      </div>
      <div class="info-item">
        <span class="section-title">출판사 :</span>
        <span class="info-text">{{ publisher }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  author: {
    type: String,
    default: ''
  },
  publisher: {
    type: String,
    default: ''
  }
})
</script>

<style scoped>
.book-info {
  display: flex;
  justify-content: flex-start;
  align-items: flex-start;
  width: 100%;
}

.info-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 0;
  width: 100%;
}

.info-item {
  display: flex;
  gap: 1rem;
}

.section-title {
  font-family: 'Noto Sans KR', sans-serif;
  font-weight: 700;
  font-size: 1.1rem;
  color: #222;
  min-width: 70px;
}

.info-text {
  font-family: 'Noto Sans KR', sans-serif;
  color: #374151;
  font-weight: 500;
  flex-grow: 1;
}
</style> 