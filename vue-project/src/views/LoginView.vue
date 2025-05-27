<template>
  <div class="popup-overlay" @click.self="closePopup">
    <div class="popup-content">
      <h1 class="logo">BookTune</h1>
      <p class="subtitle">음악과 함께 즐기는 독서</p>

      <form class="login-form" @submit.prevent="handleLogin">
        <div class="input-group">
          <input
            type="text"
            placeholder="아이디"
            class="input-field"
            autocomplete="username"
            v-model="loginId"
          />
        </div>
        <div class="input-group">
          <input
            type="password"
            placeholder="비밀번호"
            class="input-field"
            autocomplete="current-password"
            v-model="loginPw"
          />
        </div>
        <button type="submit" class="login-button">
          로그인
        </button>
      </form>

      <div class="social-login">
        <div class="divider">
          <span>또는</span>
        </div>
        <div class="social-buttons">
          <button type="button" class="social-button google" @click="handleGoogleLogin">
            <img src="/google_logo.png" alt="google" />
            <span>구글 계정으로 로그인</span>
          </button>
          <button type="button" class="social-button kakao" @click="handleKakaoLogin">
            <img src="/kakao_logo.png" alt="kakao" />
            <span>카카오톡 계정으로 로그인</span>
          </button>
        </div>
        <p class="privacy-notice">
          개인정보 보호를 위해 공용 PC에서 사용 시<br>
          SNS계정의 로그아웃 상태를 꼭 확인해 주세요.
        </p>
      </div>

      <button @click="closePopup" class="close-button">
        닫기
      </button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

const CLIENT_ID = import.meta.env.VITE_GOOGLE_CLIENT_ID;
const KAKAO_JS_KEY = import.meta.env.VITE_KAKAO_JS_KEY;

export default {
  data() {
    return {
      loginId: '',
      loginPw: ''
    };
  },
  mounted() {
    // 카카오 SDK 스크립트 로드
    if (!document.getElementById('kakao-sdk')) {
      const script = document.createElement('script');
      script.id = 'kakao-sdk';
      script.src = 'https://developers.kakao.com/sdk/js/kakao.js';
      script.onload = () => {
        if (window.Kakao && !window.Kakao.isInitialized()) {
          window.Kakao.init(KAKAO_JS_KEY);
          window.Kakao.Auth.setAccessToken(null); // 기존 토큰 초기화
          console.log('✅ Kakao SDK Initialized:', window.Kakao.isInitialized());
        }
      };
      document.head.appendChild(script);
    }
  },
  methods: {
    closePopup() {
      this.$emit('close-popup');
    },
    async handleLogin() {
      try {
        const response = await axios.post('http://localhost:8000/api/auth/login/', {
          username: this.loginId,
          password: this.loginPw
        });
        localStorage.setItem('access', response.data.access);
        localStorage.setItem('refresh', response.data.refresh);
        await this.$emit('login-success');
        this.closePopup();
        window.location.reload();
      } catch (err) {
        alert('로그인에 실패했습니다. 아이디와 비밀번호를 확인하세요.');
      }
    },
    handleGoogleLogin() {
      const redirectUri = `${window.location.origin}/auth/google/callback`;
      const oauthUrl = `https://accounts.google.com/o/oauth2/v2/auth?client_id=${CLIENT_ID}&redirect_uri=${redirectUri}&response_type=code&scope=email profile`;
      window.location.href = oauthUrl;
    },
    handleKakaoLogin() {
      if (window.Kakao) {
        window.Kakao.Auth.authorize({
          redirectUri: `${window.location.origin}/auth/kakao/callback`,
          throughTalk: false
        });
      } else {
        console.error('❌ Kakao SDK not available');
      }
    },
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap');

.popup-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(4px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.popup-content {
  background: white;
  padding: 2.5rem;
  border-radius: 20px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 420px;
  margin: 1rem;
}

.logo {
  /* font-family: 'Noto Sans KR', sans-serif; */
  font-family: 'Indie Flower', cursive;
  font-size: 4rem;
  font-weight: 700;
  color: #1a1a1a;
  text-align: center;
  margin-bottom: 0.5rem;
}

.subtitle {
  font-family: 'Noto Sans KR', sans-serif;
  font-size: 1rem;
  color: #666;
  text-align: center;
  margin-bottom: 2rem;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 2rem;
}

.input-group {
  position: relative;
}

.input-field {
  width: 90%;
  padding: 1rem 1.25rem;
  border: 1.5px solid #e0e0e0;
  border-radius: 12px;
  font-size: 1rem;
  color: #1a1a1a;
  background: #f8f9fa;
  transition: all 0.2s ease;
}

.input-field:focus {
  outline: none;
  border-color: #4a90e2;
  background: white;
  box-shadow: 0 0 0 4px rgba(74, 144, 226, 0.1);
}

.input-field::placeholder {
  color: #999;
}

.login-button {
  width: 100%;
  padding: 1rem;
  border: none;
  border-radius: 12px;
  background: #4a90e2;
  color: white;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.login-button:hover {
  background: #357abd;
  transform: translateY(-1px);
}

.login-button:active {
  transform: translateY(0);
}

.social-login {
  margin: 2rem 0;
}

.divider {
  display: flex;
  align-items: center;
  text-align: center;
  margin: 1.5rem 0;
}

.divider::before,
.divider::after {
  content: '';
  flex: 1;
  border-bottom: 1px solid #e0e0e0;
}

.divider span {
  padding: 0 1rem;
  color: #666;
  font-size: 0.875rem;
}

.social-buttons {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.social-button {
  display: flex;
  align-items: center;
  width: 100%;
  padding: 0.875rem 1.25rem;
  border: 1.5px solid #e0e0e0;
  border-radius: 12px;
  background: white;
  font-size: 0.9375rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.social-button img {
  width: 24px;
  height: 24px;
  margin-right: 0.75rem;
}

.social-button span {
  flex: 1;
  text-align: center;
}

.social-button.google {
  color: #757575;
}

.social-button.google:hover {
  background: #f8f9fa;
  border-color: #d0d0d0;
}

.social-button.kakao {
  background: #FEE500;
  border-color: #FEE500;
  color: #000000;
}

.social-button.kakao:hover {
  background: #FDD835;
  border-color: #FDD835;
}

.privacy-notice {
  margin-top: 1.5rem;
  text-align: center;
  font-size: 0.75rem;
  color: #666;
  line-height: 1.5;
}

.close-button {
  width: 100%;
  padding: 0.875rem;
  border: 1.5px solid #e0e0e0;
  border-radius: 12px;
  background: white;
  color: #666;
  font-size: 0.9375rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.close-button:hover {
  background: #f8f9fa;
  border-color: #d0d0d0;
}

@media (max-width: 480px) {
  .popup-content {
    margin: 1rem;
    padding: 1.5rem;
  }

  .logo {
    font-size: 2rem;
  }

  .subtitle {
    font-size: 0.875rem;
  }
}
</style>
