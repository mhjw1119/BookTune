<template>
  <div class="profile-bookmark-content">
    <div class="bookmark-list">
      <div v-if="bookmarks.length === 0" class="empty-state">
        <p>아직 북마크한 책이 없습니다.</p>
        <router-link to="/books" class="browse-books-button">
          책 둘러보기
        </router-link>
      </div>
      
      <div v-else class="bookmark-grid">
        <div v-for="book in bookmarks" :key="book.id" class="book-card">
          <router-link :to="`/books/${book.id}`" class="book-link">
            <div class="book-cover">
              <img :src="book.coverImage" :alt="book.title" />
              <div class="book-overlay">
                <span class="book-genre">{{ book.genre }}</span>
              </div>
            </div>
            <div class="book-info">
              <h3 class="book-title">{{ book.title }}</h3>
              <p class="book-author">{{ book.author }}</p>
              <div class="book-meta">
                <span class="book-publisher">{{ book.publisher }}</span>
                <button 
                  class="bookmark-button"
                  @click.prevent="toggleBookmark(book)"
                  :class="{ 'bookmarked': book.isBookmarked }"
                >
                  <i class="fas" :class="book.isBookmarked ? 'fa-heart' : 'fa-heart-o'"></i>
                </button>
              </div>
            </div>
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const bookmarks = ref([])

const fetchBookmarks = async () => {
  try {
    const response = await axios.get('/api/books/bookmarks')
    bookmarks.value = response.data
  } catch (error) {
    console.error('북마크 목록 조회 에러:', error)
  }
}

const toggleBookmark = async (book) => {
  try {
    if (book.isBookmarked) {
      await axios.delete(`/api/books/${book.id}/bookmark`)
      bookmarks.value = bookmarks.value.filter(b => b.id !== book.id)
    } else {
      await axios.post(`/api/books/${book.id}/bookmark`)
      book.isBookmarked = true
    }
  } catch (error) {
    console.error('북마크 토글 에러:', error)
  }
}

onMounted(() => {
  fetchBookmarks()
})
</script>

<style scoped>
.profile-bookmark-content {
  padding: 1rem;
}

.empty-state {
  text-align: center;
  padding: 3rem;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 1rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.empty-state p {
  color: #666;
  margin-bottom: 1.5rem;
  font-size: 1.1rem;
}

.browse-books-button {
  display: inline-block;
  padding: 0.8rem 1.5rem;
  background: #0078c8;
  color: white;
  text-decoration: none;
  border-radius: 0.5rem;
  font-weight: 600;
  transition: background-color 0.2s;
}

.browse-books-button:hover {
  background: #005fa3;
}

.bookmark-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1.5rem;
  padding: 1rem 0;
}

.book-card {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 1rem;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s, box-shadow 0.2s;
}

.book-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.book-link {
  text-decoration: none;
  color: inherit;
  display: block;
}

.book-cover {
  position: relative;
  padding-top: 140%;
  overflow: hidden;
}

.book-cover img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.book-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  padding: 0.5rem;
  background: linear-gradient(to bottom, rgba(0, 0, 0, 0.7), transparent);
}

.book-genre {
  color: white;
  font-size: 0.8rem;
  background: rgba(0, 0, 0, 0.6);
  padding: 0.3rem 0.6rem;
  border-radius: 1rem;
}

.book-info {
  padding: 1rem;
}

.book-title {
  font-size: 1rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 0.5rem;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.book-author {
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 0.5rem;
}

.book-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.book-publisher {
  font-size: 0.8rem;
  color: #888;
}

.bookmark-button {
  background: none;
  border: none;
  color: #ff4081;
  cursor: pointer;
  padding: 0.3rem;
  transition: transform 0.2s;
}

.bookmark-button:hover {
  transform: scale(1.1);
}

.bookmark-button.bookmarked {
  color: #ff4081;
}

@media (max-width: 768px) {
  .bookmark-grid {
    grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
    gap: 1rem;
  }
}
</style> 