import { defineStore } from 'pinia'

export const useThemeStore = defineStore('theme', {
  state: () => ({
    isDarkMode: false
  }),
  
  actions: {
    toggleTheme() {
      this.isDarkMode = !this.isDarkMode
      localStorage.setItem('theme', this.isDarkMode ? 'dark' : 'light')
      this.updateTheme()
    },
    
    initTheme() {
      const savedTheme = localStorage.getItem('theme')
      this.isDarkMode = savedTheme === 'dark'
      this.updateTheme()
    },
    
    updateTheme() {
      document.documentElement.classList.toggle('dark-mode', this.isDarkMode)
    }
  }
}) 