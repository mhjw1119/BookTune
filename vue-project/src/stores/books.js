import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useBookStore = defineStore('book', () => {
  const books = ref([])
  const recommendedBooks = ref([])
  const loading = ref(false)
  const error = ref(null)
  const API_URL = 'http://127.0.0.1:8000'

  const getBooks = async function () {
    try {
      const response = await axios({
        method: 'get',
        url: `${API_URL}/api/books/`
      })
      books.value = response.data
      return response.data
    } catch (error) {
      console.error('Error fetching books:', error)
      throw error
    }
  }

  const searchBooks = async function (query) {
    try {
      const response = await axios({
        method: 'get',
        url: `${API_URL}/api/books/`,
        params: { search: query }
      })
      return response.data
    } catch (error) {
      console.error('Error searching books:', error)
      throw error
    }
  }

  const genreBooks = async function (genre) {
    try {
      const response = await axios({
        method: 'get',
        url: `${API_URL}/api/books/`,
        params: { genre }
      })
      return response.data
    } catch (error) {
      console.error('Error filtering books by genre:', error)
      throw error
    }
  }

  const toggleLike = async (isbn) => {
    const access = localStorage.getItem('access')
    const res = await axios.post(
      `${API_URL}/api/books/${isbn}/likes/`,
      {},
      { headers: { Authorization: `Bearer ${access}` } }
    )
    return res.data // { status: 'liked' or 'unliked' }
  }

  const createThread = async (isbn, formData) => {
    try {
      const access = localStorage.getItem('access')
      if (!access) {
        throw new Error('Please login to create a thread')
      }

      // 토큰 유효성 검사
      const tokenParts = access.split('.')
      if (tokenParts.length !== 3) {
        throw new Error('Invalid token format')
      }

      // bookId를 isbn으로 사용
      const response = await axios.post(
        `${API_URL}/api/books/${isbn}/threads/create/`,
        formData,
        { 
          headers: { 
            Authorization: `Bearer ${access}`,
            'Content-Type': 'multipart/form-data'
          } 
        }
      )
      return response.data
    } catch (error) {
      console.error('Error creating thread:', error)
      if (error.response) {
        if (error.response.status === 401) {
          throw new Error('Your session has expired. Please login again.')
        }
        if (error.response.status === 404) {
          throw new Error('Book not found. Please check if the book ID is correct.')
        }
        throw new Error(error.response.data.message || 'Failed to create thread')
      }
      throw error
    }
  }

  const getBookThreads = async (bookId) => {
    try {
      const access = localStorage.getItem('access')
      const response = await axios.get(
        `${API_URL}/api/books/${bookId}/threads/`,
        {
          headers: { 
            Authorization: `Bearer ${access}`
          }
        }
      )
      return response.data
    } catch (error) {
      console.error('Error fetching book threads:', error)
      throw error
    }
  }

  const likeThread = async (threadId) => {
    try {
      const access = localStorage.getItem('access')
      const response = await axios.post(
        `${API_URL}/api/books/threads/${threadId}/like/`,
        {},
        {
          headers: { 
            Authorization: `Bearer ${access}`
          }
        }
      )
      return response.data
    } catch (error) {
      console.error('Error liking thread:', error)
      throw error
    }
  }

  const getRecommendedBooks = async () => {
    loading.value = true
    error.value = null
    try {
      const access = localStorage.getItem('access')
      if (!access) {
        throw new Error('로그인이 필요합니다.')
      }
      
      const response = await axios.get(
        `${API_URL}/api/books/recommendations/`,
        {
          headers: {
            Authorization: `Bearer ${access}`
          }
        }
      )
      recommendedBooks.value = response.data
    } catch (err) {
      error.value = err.response?.data?.message || '추천 도서를 불러오는데 실패했습니다.'
      console.error('Error fetching recommended books:', err)
    } finally {
      loading.value = false
    }
  }

  return { 
    books, 
    recommendedBooks,
    loading,
    error,
    API_URL, 
    getBooks, 
    searchBooks, 
    genreBooks, 
    toggleLike,
    createThread,
    getBookThreads,
    likeThread,
    getRecommendedBooks
  }
}, { persist: true })