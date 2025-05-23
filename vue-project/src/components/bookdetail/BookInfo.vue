<template>
  <div class="rounded-box flex flex-row items-center justify-between px-6 py-4">
    <div>
      <span class="section-title">저자명 :</span>
      <span class="ml-2 text-gray-700 font-medium">{{ author }}</span>
    </div>
    <div>
      <span class="section-title">출판사 :</span>
      <span class="ml-2 text-gray-700 font-medium">{{ publisher }}</span>
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