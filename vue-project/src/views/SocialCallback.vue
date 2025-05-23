<template>
  <div class="social-callback">
    <div class="loading-container">
      <div class="loading-spinner"></div>
      <p>소셜 로그인 처리 중...</p>
    </div>
  </div>
</template>

<script>
import { onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from 'axios'

export default {
  name: 'SocialCallback',
  setup() {
    const router = useRouter()
    const route = useRoute()

    const handleSocialCallback = async () => {
      try {
        // URL에서 인증 코드 추출
        const code = route.query.code
        const provider = route.params.provider // 'google', 'kakao' 등

        if (!code) {
          throw new Error('인증 코드가 없습니다.')
        }

        // 백엔드로 인증 코드 전송
        const response = await axios.post('/api/auth/social/callback', {
          code,
          provider
        })

        // 토큰 저장
        const { access_token, refresh_token } = response.data
        localStorage.setItem('access_token', access_token)
        localStorage.setItem('refresh_token', refresh_token)

        // 메인 페이지로 리다이렉트
        router.push('/')
      } catch (error) {
        console.error('소셜 로그인 처리 중 오류 발생:', error)
        router.push('/login?error=social_login_failed')
      }
    }

    onMounted(() => {
      handleSocialCallback()
    })

    return {}
  }
}
</script>

<style scoped>
.social-callback {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f5f5;
}

.loading-container {
  text-align: center;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 5px solid #f3f3f3;
  border-top: 5px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

p {
  color: #666;
  font-size: 1.1em;
}
</style> 