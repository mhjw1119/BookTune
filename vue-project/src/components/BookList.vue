<template>
  <div class="book-list">
    <h1 class="book-title">Book List</h1>
    <div class="best-books-container">
      <h2 class="section-title"></h2>
      <div v-if="!books.length" class="loading-state">
        <p>도서를 불러오는 중...</p>
      </div>
      <div v-else class="books-grid">
        <BestBookItem 
          v-for="book in pagedBooks" 
          :key="book.isbn" 
          :book="book"
        />
      </div>
      <div class="pagination" v-if="totalPages > 1">
        <button @click="goToPage(currentPage - 1)" :disabled="currentPage === 1">이전</button>
        <span v-for="page in displayedPages" :key="page">
          <button
            :class="{ active: page === currentPage }"
            @click="goToPage(page)"
          >{{ page }}</button>
        </span>
        <button @click="goToPage(currentPage + 1)" :disabled="currentPage === totalPages">다음</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import BestBookItem from './bestbook/BestBookItem.vue'

const props = defineProps({
  books: {
    type: Array,
    required: true
  }
})

const route = useRoute()
const router = useRouter()

const pageSize = 30
const totalPages = computed(() => Math.ceil(props.books.length / pageSize))

// 쿼리스트링에서 page 읽기, 없으면 1
const currentPage = ref(Number(route.query.page) || 1)

// 표시할 페이지 번호 계산
const displayedPages = computed(() => {
  const pages = []
  const maxPages = 5 // 한 번에 표시할 최대 페이지 수
  
  if (totalPages.value <= maxPages) {
    // 전체 페이지가 maxPages보다 작으면 모든 페이지 표시
    for (let i = 1; i <= totalPages.value; i++) {
      pages.push(i)
    }
  } else {
    // 현재 페이지 주변의 페이지들 표시
    let start = Math.max(1, currentPage.value - Math.floor(maxPages / 2))
    let end = start + maxPages - 1
    
    if (end > totalPages.value) {
      end = totalPages.value
      start = Math.max(1, end - maxPages + 1)
    }
    
    for (let i = start; i <= end; i++) {
      pages.push(i)
    }
  }
  
  return pages
})

const pagedBooks = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  return props.books.slice(start, start + pageSize)
})

function goToPage(page) {
  if (page >= 1 && page <= totalPages.value) {
    router.replace({ query: { ...route.query, page } })
  }
}

// 쿼리스트링이 바뀌면 currentPage도 바꿔줌
watch(
  () => route.query.page,
  (newPage) => {
    currentPage.value = Number(newPage) || 1
  }
)
</script>

<style scoped>
.book-title {
  font-family: 'Indie Flower', cursive;
  font-size: 2rem;
  font-weight: 700;
  text-align: center;
  margin-bottom: -1rem;
  color: #333;
}

.best-books-container {
  padding: 2rem;
}

.section-title {
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 2rem;
  color: #333;
}

.books-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 2rem;
}

.pagination {
  display: flex;
  justify-content: center;
  gap: 0.5rem;
  margin-top: 2rem;
}
.pagination button {
  padding: 0.4rem 0.8rem;
  border: 1px solid #ddd;
  background: #fff;
  border-radius: 4px;
  cursor: pointer;
}
.pagination button.active {
  background: #6366f1;
  color: #fff;
  font-weight: bold;
}
.pagination button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.loading-state {
  text-align: center;
  padding: 2rem;
  color: #666;
  font-size: 1.1rem;
}
</style>