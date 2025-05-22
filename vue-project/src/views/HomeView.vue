<template>
  <!-- 2단 그리드로 Best/Recommend 배치 -->
  <div class="main-content-grid grid grid-cols-1 md:grid-cols-2 gap-12 w-full max-w-6xl mx-auto mt-12 px-6 pb-16">
    <!-- Best Section -->
    <section class="bg-white border border-gray-300 rounded-xl shadow-md p-8 flex flex-col">
      <h2 class="section-title text-gray-800 mb-8 text-center">Best</h2>
      <BestBook />
    </section>
    <!-- Recommend Section -->
    <section class="bg-white border border-gray-300 rounded-xl shadow-md p-8 flex flex-col">
      <h2 class="section-title text-gray-800 mb-8 text-center">Recommend</h2>
      <RecommendBook />
    </section>
  </div>
</template>

<script setup>
import BestBook from '@/components/BestBook.vue'
import RecommendBook from '@/components/RecommendBook.vue'
</script>

<style scoped>
.section-title {
  font-family: 'Indie Flower', cursive;
  font-size: 3rem;
  letter-spacing: 0.03em;
  font-weight: bold;
}
.main-content-grid {
  min-height: 500px;
}
</style>