<template>
  <div
    class="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50"
    v-if="visible"
  >
    <div class="bg-[#fafbfc] w-full max-w-md mx-auto p-8 rounded-2xl shadow-lg relative">
      <!-- Close Button -->
      <button @click="$emit('close')" class="absolute top-4 right-4 text-gray-500 hover:text-black text-xl">&times;</button>

      <!-- Logo -->
      <h1 class="logo-font text-5xl font-bold text-gray-800 mb-10 text-center select-none">BookTune</h1>

      <!-- Login Form -->
      <form class="flex flex-col gap-4" @submit.prevent="handleLogin">
        <input 
          v-model="id"
          type="text"
          placeholder="id" 
          class="handwriting px-5 py-3 border-2 border-gray-400 rounded-lg text-lg focus:outline-none focus:border-blue-500 placeholder:text-gray-400"
          autocomplete="username"
        />
        <input 
          v-model="password"
          type="password" 
          placeholder="password" 
          class="handwriting px-5 py-3 border-2 border-gray-400 rounded-lg text-lg focus:outline-none focus:border-blue-500 placeholder:text-gray-400"
          autocomplete="current-password"
        />
        <button 
          type="submit"
          class="handwriting py-3 mt-2 border-2 border-gray-400 rounded-lg text-lg font-bold bg-gray-400 hover:bg-blue-50 transition"
        >
          login
        </button>
      </form>

      <!-- Remember ID -->
      <div class="flex items-center mt-4 mb-2">
        <input id="remember" type="checkbox" v-model="rememberId" class="accent-blue-600 w-5 h-5 rounded border-gray-400 mr-2">
        <label for="remember" class="text-lg text-gray-700 select-none">아이디 저장</label>
      </div>

      <!-- Social Login -->
      <div class="bg-white rounded-lg shadow-sm py-5 px-4 flex flex-col items-center mb-6">
        <div class="flex gap-4 mb-2">
          <button type="button" class="social-btn bg-yellow-300 hover:bg-yellow-400" aria-label="카카오 로그인">
            <img src="https://upload.wikimedia.org/wikipedia/commons/8/82/Kakao_icon.png" alt="Kakao" class="w-8 h-8">
          </button>
          <button type="button" class="social-btn bg-white border border-gray-300 hover:bg-gray-100" aria-label="구글 로그인">
            <img src="https://upload.wikimedia.org/wikipedia/commons/5/53/Google_%22G%22_Logo.svg" alt="Google" class="w-8 h-8">
          </button>
        </div>
        <p class="text-xs text-gray-500 text-center leading-tight mt-2">
          개인정보 보호를 위해 공용 PC에서 사용 시 SNS계정의 로그아웃<br />
          상태를 꼭 확인해 주세요.
        </p>
      </div>

      <!-- Signup -->
      <button 
        class="py-3 w-full border-2 border-gray-400 rounded-lg text-lg font-bold bg-white hover:bg-blue-50 transition"
        type="button"
      >
        회원가입
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  visible: Boolean,
})

const emit = defineEmits(['close'])

const id = ref('')
const password = ref('')
const rememberId = ref(true)

function handleLogin() {
  // 여기에 로그인 로직 추가
  alert(`ID: ${id.value}, PW: ${password.value}, Remember: ${rememberId.value}`)
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Indie+Flower&family=Nunito:wght@400;700&display=swap');

body {
  font-family: 'Nunito', sans-serif;
}

.logo-font {
  font-family: 'Indie Flower', cursive;
  letter-spacing: 0.02em;
}

.handwriting {
  font-family: 'Indie Flower', cursive;
}

.social-btn {
  @apply flex items-center justify-center w-12 h-12 rounded-full shadow transition hover:scale-105;
}
.social-btn:focus {
  outline: 2px solid #2563eb;
  outline-offset: 2px;
}
</style>
