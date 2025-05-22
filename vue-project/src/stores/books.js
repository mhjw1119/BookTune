import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useBookStore = defineStore('book', () => {
  const books = ref([])
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

  return { books, API_URL, getBooks }
}, { persist: true })