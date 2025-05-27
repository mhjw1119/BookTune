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
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
  /* background-color: rgb(229, 250, 250); */
}

.section-title {
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 2rem;
  color: #333;
  text-align: center;
}

.books-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2rem;
  padding: 0 1rem;
}

@media (max-width: 1200px) {
  .books-grid {
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 1.5rem;
  }
}

@media (max-width: 768px) {
  .best-books-container {
    padding: 1.5rem 1rem;
  }

  .section-title {
    font-size: 1.75rem;
    margin-bottom: 1.5rem;
  }

  .books-grid {
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 1.25rem;
  }
}

@media (max-width: 480px) {
  .best-books-container {
    padding: 1rem 0.75rem;
  }

  .section-title {
    font-size: 1.5rem;
    margin-bottom: 1.25rem;
  }

  .books-grid {
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    gap: 1rem;
    padding: 0 0.5rem;
  }
}

@media (max-width: 360px) {
  .books-grid {
    grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
    gap: 0.75rem;
  }
}
</style>