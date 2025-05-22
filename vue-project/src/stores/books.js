import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useBookStore = defineStore('book', () => {
  const books = ref([])
  const API_URL = 'http://127.0.0.1:8000'

  // axios 인스턴스 생성
  const axiosInstance = axios.create({
    baseURL: API_URL,
    headers: {
      'Content-Type': 'application/json',
    },
  })

  // 요청 인터셉터 추가
  axiosInstance.interceptors.request.use(
    (config) => {
      const token = localStorage.getItem('access_token')
      if (token) {
        config.headers.Authorization = `Bearer ${token}`
      }
      return config
    },
    (error) => {
      return Promise.reject(error)
    }
  )

  const getBooks = async function () {
    try {
      // 토큰 없이도 요청 가능하도록 일반 axios 사용
      const response = await axios.get(`${API_URL}/api/books/`)
      books.value = response.data
      return response.data
    } catch (error) {
      console.error('Error fetching books:', error)
      throw error
    }
  }

  return { books, API_URL, getBooks }
}, { persist: true })