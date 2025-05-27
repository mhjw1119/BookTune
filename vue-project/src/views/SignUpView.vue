<template>
  <div class="popup-overlay" @click.self="$emit('close-popup')">
    <div class="popup-content">
      <form class="w-full bg-white rounded-xl shadow-lg px-10 py-10">
        <h1 class="logo-font text-4xl handwritten font-bold text-gray-800 select-none text-center mb-8">BookTune</h1>

        <div class="form-row">
          <label for="ID">ID :</label>
          <input id="ID" type="text" class="input-box" v-model="signupForm.ID" required />
        </div>

        <div class="form-row">
          <label for="nickname">Nickname :</label>
          <input id="nickname" type="text" class="input-box" v-model="signupForm.nickname" required />
        </div>

        <div class="form-row">
          <label for="password">Password :</label>
          <input id="password" type="password" class="input-box" v-model="signupForm.password" required />
        </div>

        <div class="form-row">
          <label for="confirmPassword">Confirm Password :</label>
          <input id="confirmPassword" type="password" class="input-box" v-model="signupForm.confirmPassword" required />
        </div>

        <div class="form-row">
          <label for="email">Email :</label>
          <input id="email" type="email" class="input-box" v-model="signupForm.email" required />
        </div>

        <div class="flex justify-center mt-8 space-x-4">
          <button type="submit" @click.prevent="handleSignup" class="form-button">Sign Up</button>
          <button @click="$emit('close-popup')" class="form-button alt">Close</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      signupForm: {
        ID: '',
        nickname: '',
        password: '',
        confirmPassword: '',
        email: '',
      },
    };
  },
  methods: {
    async handleSignup() {
      if (this.signupForm.password !== this.signupForm.confirmPassword) {
        alert('비밀번호가 일치하지 않습니다.');
        return;
      }
      try {
        const res = await axios.post('http://localhost:8000/api/auth/signup/', {
          username: this.signupForm.ID,
          password: this.signupForm.password,
          password2: this.signupForm.confirmPassword,
          nickname: this.signupForm.nickname,
          email: this.signupForm.email
        });
        alert('회원가입이 완료되었습니다!');
        this.$emit('close-popup');
      } catch (error) {
        if (error.response && error.response.data) {
          alert('회원가입 실패: 올바른 정보를 입력해주세요');
        } else {
          alert('회원가입 중 오류가 발생했습니다.');
        }
      }
    },
  },
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Indie+Flower&family=Nunito:wght@400;700&display=swap');

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

.popup-content {
  background: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  width: 100%;
  max-width: 780px;
}

.logo-font {
  font-family: 'Indie Flower', cursive;
}

.handwritten {
  font-family: 'Indie Flower', cursive;
}

.form-row {
  display: flex;
  align-items: center;
  margin-bottom: 1.5rem;
}

.form-row label {
  width: 160px;
  text-align: right;
  margin-right: 1rem;
  font-family: 'Indie Flower', cursive;
  font-size: 1.1rem;
  color: #333;
}

.input-box {
  flex: 1;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  padding: 0.5rem 1rem;
  font-size: 1rem;
  transition: border 0.2s;
}

.input-box:focus {
  outline: none;
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

.form-button {
  font-family: 'Indie Flower', cursive;
  font-size: 1.2rem;
  font-weight: bold;
  padding: 0.5rem 2rem;
  border: 2px solid #333;
  border-radius: 0.5rem;
  background-color: white;
  transition: all 0.2s ease-in-out;
  margin-right: 1rem;
}

.form-button:hover {
  background-color: #f3f4f6;
}

.form-button.alt {
  border-color: #aaa;
}
</style>
