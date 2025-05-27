<template>
  <div class="thread-list-view">
    <ThreadGridList />
  </div>
</template>

<script setup>
import ThreadGridList from '@/components/thread/ThreadGridList.vue'
</script>

<style scoped>
.thread-list-view {
  min-height: 100vh;
  background-color: #f8f9fa;
  padding: 2rem 0;
}
</style> 