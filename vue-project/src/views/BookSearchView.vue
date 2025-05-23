<template>
  <div class="search-container">
    <div v-if="loading" class="loading-state">
      <p>검색 중...</p>
    </div>
    <div v-else-if="error" class="error-state">
      <p>{{ error }}</p>
    </div>
    <BookList 
      v-else
      :keyword="keyword"
      :books="filteredResults"
    />
  </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useBookStore } from '@/stores/books'
import BookList from '@/components/search/BookList.vue'

const route = useRoute()
const store = useBookStore()
const keyword = ref(route.query.q || '')
const searchResults = ref([])
const loading = ref(false)
const error = ref(null)

// API로 받아온 결과에서 검색어와 일치하는 항목만 필터링
const filteredResults = computed(() => {
  if (!keyword.value.trim()) return searchResults.value
  
  const lowerKeyword = keyword.value.toLowerCase()
  return searchResults.value.filter(book => {
    return (
      (book.title && book.title.toLowerCase().includes(lowerKeyword)) ||
      (book.author && book.author.toLowerCase().includes(lowerKeyword))
    )
  })
})

const performSearch = async () => {
  if (!keyword.value.trim()) {
    searchResults.value = []
    return
  }

  loading.value = true
  error.value = null

  try {
    // store의 searchBooks 메서드 사용하여 API 검색
    const results = await store.searchBooks(keyword.value)
    searchResults.value = results
  } catch (err) {
    console.error('Search error:', err)
    error.value = '검색 중 오류가 발생했습니다.'
    searchResults.value = []
  } finally {
    loading.value = false
  }
}

// 쿼리 파라미터가 변경될 때마다 검색 수행
watch(() => route.query.q, (newQuery) => {
  keyword.value = newQuery || ''
  performSearch()
}, { immediate: true })
</script>

<style scoped>
.search-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.loading-state, .error-state {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.error-state {
  color: #dc2626;
}
</style>