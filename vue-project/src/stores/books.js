import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useBookStore = defineStore('book', () => {
  const books = ref([])
  const API_URL = 'http://127.0.0.1:8000'

  const getBooks = function () {
    axios({
      method: 'get',
      url: `${API_URL}/api/books/`
    })
    .then( res => {
      books.value = res.data
      console.log(books.value)
    })
    .catch( err => console.log(err))
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

  return { books, API_URL, getBooks, searchBooks, genreBooks }
}, { persist: true })