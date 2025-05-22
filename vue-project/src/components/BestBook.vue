<template>
  {{ books }}

</template>

<script setup>

import { onMounted } from 'vue';
import { useBookStore } from '@/stores/books';
const store = useBookStore()

onMounted(() => {
  store.getBooks()
})

</script>


<style scoped>

</style>