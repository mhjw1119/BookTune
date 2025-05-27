<template>
  <div class="popup-overlay" @click.self="closePopup">
    <div class="popup-content w-full max-w-md mx-auto">
      <h1 class="logo-font text-6xl font-bold text-gray-800 mb-12 select-none">BookTune</h1>

      <form class="w-full flex flex-col gap-4 mb-8" @submit.prevent="handleLogin">
        <input
          type="text"
          placeholder="id"
          class="handwriting w-full px-5 py-3 border-2 border-gray-400 rounded-lg text-lg focus:outline-none focus:border-blue-500 transition placeholder:text-gray-400"
          autocomplete="username"
          v-model="loginId"
        />
        <input
          type="password"
          placeholder="password"
          class="handwriting mb-4 w-full px-5 py-3 border-2 border-gray-400 rounded-lg text-lg focus:outline-none focus:border-blue-500 transition placeholder:text-gray-400"
          autocomplete="current-password"
          v-model="loginPw"
        />
        <button
          type="submit"
          class="handwriting w-full py-3 mt-2 border-2 border-gray-400 rounded-lg text-lg font-bold bg-gray-400 hover:bg-blue-50 transition"
        >
          login
        </button>
      </form>

      <div class="w-full bg-white rounded-lg py-5 px-4 flex flex-col items-center mb-10">
        <div class="social-login-buttons w-full">
          <button type="button" class="social-button google" @click="handleGoogleLogin">
            <img src="/google_logo.png" alt="google" />
            <span>구글 계정으로 로그인</span>
          </button>
          <button type="button" class="social-button kakao" @click="handleKakaoLogin">
            <img src="/kakao_logo.png" alt="kakao" />
            <span>카카오톡 계정으로 로그인</span>
          </button>
        </div>
        <p class="text-xs text-gray-500 text-center leading-tight mt-4">
          개인정보 보호를 위해 공용 PC에서 사용 시 SNS계정의 로그아웃<br>
          상태를 꼭 확인해 주세요.
        </p>
      </div>

      <button @click="closePopup" class="mt-6 w-full py-3 mt-4 border-2 border-gray-400 rounded-lg text-lg font-bold bg-white hover:bg-gray-100 transition">close</button>
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
/* 폰트 임포트 */
@import url('https://fonts.googleapis.com/css2?family=Indie+Flower&family=Nunito:wght@400;700&display=swap');

/* 팝업 오버레이 스타일 */
.popup-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

/* 팝업 내용 */
.popup-content {
  background: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  text-align: center;
  width: 20%;
  height: 50%;
}

/* 폰트 스타일 */
.logo-font {
  font-family: 'Indie Flower', cursive;
  letter-spacing: 0.02em;
}
.handwriting {
  font-family: 'Indie Flower', cursive;
}

/* 소셜 로그인 버튼 스타일 */
.social-login-buttons {
  display: flex;
  flex-direction: column;
  gap: 12px;
  width: 100%;
}

.social-button {
  display: flex;
  align-items: center;
  width: 100%;
  padding: 12px;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.social-button img {
  width: 24px;
  height: 24px;
  margin-right: 12px;
}

.social-button span {
  flex: 1;
  text-align: center;
}

.social-button.google {
  background-color: white;
  color: #757575;
  border: 1px solid #ddd;
}

.social-button.google:hover {
  background-color: #f8f8f8;
}

.social-button.kakao {
  background-color: #FEE500;
  color: #000000;
}

.social-button.kakao:hover {
  background-color: #FDD835;
}

/* 간격 조절용 추가 스타일 */
form {
  margin-bottom: 2rem;
}

.popup-content > div {
  margin-bottom: 2rem;
}

.popup-content > button:last-child {
  margin-top: 1.5rem;
}

.handwriting {
  margin-bottom: 1rem;
}
</style>
