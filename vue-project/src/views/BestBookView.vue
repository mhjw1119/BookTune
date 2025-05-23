<template>
  <BestBook :books="bestBooks" />
</template>

<script setup>
import { computed } from 'vue'
import { useBookStore } from '@/stores/books'
import BestBook from '@/components/BestBook.vue'

const store = useBookStore()

// 상위 5개의 베스트셀러만 선택
const bestBooks = computed(() => {
  return store.books.slice(0, 5)
})
</script> 