<template>
  <div class="home-container">
    <section class="best-books-section">
      <h2 class="section-title">베스트셀러</h2>
      <BestBook />
    </section>
    
    <section class="recommend-books-section">
      <h2 class="section-title">추천 도서</h2>
      <RecommendBook />
    </section>
  </div>
</template>

<script setup>
import BestBook from '@/components/BestBook.vue'
import RecommendBook from '@/components/RecommendBook.vue'
</script>

<style scoped>
.home-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.section-title {
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 1.5rem;
  color: #333;
  border-bottom: 2px solid #e74c3c;
  padding-bottom: 0.5rem;
}

.best-books-section,
.recommend-books-section {
  margin-bottom: 3rem;
}
</style>