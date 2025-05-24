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
  justify-content: center;
  align-items: center;
  width: 100%;
}

.info-container {
  display: flex;
  justify-content: center;
  gap: 4rem;
  padding: 1rem;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.section-title {
  font-family: 'Noto Sans KR', sans-serif;
  font-weight: 700;
  font-size: 1.1rem;
  color: #222;
}

.info-text {
  font-family: 'Noto Sans KR', sans-serif;
  color: #374151;
  font-weight: 500;
}
</style> 