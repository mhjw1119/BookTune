
// vite.config.js
import { fileURLToPath, URL } from 'node:url' // <<<<< 이 줄을 추가 또는 수정해주세요!


import vueDevTools from 'vite-plugin-vue-devtools'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite' // <<<<< 이 줄이 중요합니다!

export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
    tailwindcss(), // <<<<< 이 줄도 중요합니다!
  ],
    resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
})
