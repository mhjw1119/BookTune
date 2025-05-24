<template>
  <div class="rounded-box px-6 py-6 min-h-[120px]">
    <span class="section-title block mb-2 text-center">책 소개</span>
    <p class="text-gray-700 leading-relaxed">
      {{ description || '책 소개가 없습니다.' }}
    </p>
  </div>
</template>

<script setup>
defineProps({
  description: {
    type: String,
    default: ''
  }
})
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