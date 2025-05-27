<template>
  <div class="best-books-container">
    <h2 class="section-title"></h2>
    <div class="books-grid">
      <BestBookItem 
        v-for="book in books" 
        :key="book.isbn" 
        :book="book"
      />
    </div>
  </div>
</template>

<script setup>
import BestBookItem from './bestbook/BestBookItem.vue'

defineProps({
  books: {
    type: Array,
    required: true
  }
})
</script>

<style scoped>
.best-books-container {
  margin-top: 1rem;
  padding: 2rem;
  /* background-color: rgb(229, 250, 250); */
}

.section-title {
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 2rem;
  color: #333;
}

.books-grid {
  display: grid;
  grid-template-columns: repeat(10, 1fr); /* 5열 고정 */
  gap: 2rem;
}
</style>