<template>
  <div class="callback-container">
    <div v-if="loading" class="loading">
      <p>카카오 로그인 처리 중입니다...</p>
    </div>
    <div v-else-if="error" class="error">
      <p>{{ error }}</p>
      <button @click="goToLogin" class="retry-button">로그인 페이지로 돌아가기</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const loading = ref(true)
const error = ref(null)

const goToLogin = () => {
  router.push('/login')
}

onMounted(async () => {
  const code = new URL(window.location.href).searchParams.get('code')
  console.log('🔵 Received code:', code)

  if (!code) {
    error.value = '인증 코드를 받지 못했습니다.'
    loading.value = false
    return
  }

  try {
    console.log('🔵 Sending request to backend...')
    const response = await axios.post('http://localhost:8000/api/auth/social/kakao/', {
      code,
      redirect_uri: `${window.location.origin}/auth/kakao/callback`
    })

    console.log('✅ Login successful:', response.data)
    localStorage.setItem('access', response.data.access)
    localStorage.setItem('refresh', response.data.refresh)
    router.push('/')
  } catch (error) {
    console.error('❌ 카카오 로그인 실패:', error.response?.data || error)
    if (error.response?.data?.details) {
      try {
        const details = JSON.parse(error.response.data.details)
        error.value = `카카오 로그인 실패: ${details.error_description || details.error}`
      } catch (e) {
        error.value = error.response?.data?.error || '카카오 로그인에 실패했습니다.'
      }
    } else {
      error.value = error.response?.data?.error || '카카오 로그인에 실패했습니다.'
    }
    loading.value = false
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

.loading, .error {
  text-align: center;
  padding: 2rem;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.error {
  color: #dc2626;
}

.retry-button {
  margin-top: 1rem;
  padding: 0.5rem 1rem;
  background-color: #3b82f6;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.retry-button:hover {
  background-color: #2563eb;
}
</style> 