<template>
  <div class="callback-container">
    <p>카카오 로그인 처리 중입니다...</p>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()

onMounted(async () => {
  const code = new URL(window.location.href).searchParams.get('code')

  if (code) {
    try {
      const response = await axios.post('http://localhost:8000/api/auth/social/kakao/', {
        code,
        redirect_uri: `${window.location.origin}/auth/kakao/callback`
      })

      localStorage.setItem('access', response.data.access)
      localStorage.setItem('refresh', response.data.refresh)
      router.push('/')
    } catch (error) {
      console.error('카카오 로그인 실패:', error.response?.data || error)
      alert('카카오 로그인 실패')
      router.push('/login')
    }
  }
})
</script>

<style scoped>
.callback-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f5f5;
}

p {
  font-size: 1.2rem;
  color: #666;
}
</style> 