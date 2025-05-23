<template>
  <div class="popup-overlay" @click.self="closePopup">
    <div class="popup-content w-full max-w-md mx-auto"> <h1 class="logo-font text-6xl font-bold text-gray-800 mb-12 select-none">BookTune</h1>

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
        <div class="flex gap-4 mb-2">
          <button type="button" class="social-btn bg-yellow-300 hover:bg-yellow-400" aria-label="카카오 로그인" @click="socialLogin('kakao')">
            <img src="/kakao_logo.png" alt="Kakao" class="social-icon">
          </button>
          <button type="button" class="social-btn bg-white hover:bg-gray-100" aria-label="구글 로그인" @click="socialLogin('google')">
            <img src="/google_logo.png" alt="Google" class="social-icon">
          </button>
        </div>
        <p class="text-xs text-gray-500 text-center leading-tight mt-2">
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

export default {
  data() {
    return {
      loginId: '',
      loginPw: ''
    };
  },
  methods: {
    closePopup() {
      this.$emit('close-popup');
    },
    async handleLogin() {
      try {
        const response = await axios.post('http://localhost:8000/api/accounts/login/', {
          username: this.loginId,
          password: this.loginPw
        });
        localStorage.setItem('access', response.data.access);
        localStorage.setItem('refresh', response.data.refresh);
        this.$emit('login-success');
        this.closePopup();
      } catch (err) {
        alert('로그인에 실패했습니다. 아이디와 비밀번호를 확인하세요.');
      }
    },
    socialLogin(provider) {
      window.location.href = `/api/accounts/${provider}/`;
    }
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
.social-btn {
  display: flex;
  border: none;
  outline: none;
  align-items: center;
  justify-content: center;
  width: 3rem;
  height: 3rem;
  border-radius: 9999px;
  overflow: hidden;
  box-shadow: none;
  transition: transform 0.15s ease-in-out;
}
.social-btn img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  border-radius: 9999px;
}
.social-btn:hover {
  transform: scale(1.05);
}

/* ✅ 간격 조절용 추가 스타일 */
form {
  margin-bottom: 2rem; /* 로그인 폼과 소셜 로그인 영역 사이 */
}

.popup-content > div {
  margin-bottom: 2rem; /* 소셜 로그인 영역과 버튼 사이 */
}

.popup-content > button:last-child {
  margin-top: 1.5rem; /* 닫기 버튼 위 여백 */
}
.handwriting {
  margin-bottom: 1rem;
}
</style>
