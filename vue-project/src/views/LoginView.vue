<template>
  <div class="popup-overlay" @click.self="closePopup">
    <div class="popup-content w-full max-w-md mx-auto"> <h1 class="logo-font text-6xl font-bold text-gray-800 mb-12 select-none">BookTune</h1>

      <form class="w-full flex flex-col gap-4">
        <input
          type="text"
          placeholder="id"
          class="handwriting w-full px-5 py-3 border-2 border-gray-400 rounded-lg text-lg focus:outline-none focus:border-blue-500 transition placeholder:text-gray-400"
          autocomplete="username"
        />
        <input
          type="password"
          placeholder="password"
          class="handwriting w-full px-5 py-3 border-2 border-gray-400 rounded-lg text-lg focus:outline-none focus:border-blue-500 transition placeholder:text-gray-400"
          autocomplete="current-password"
        />
        <button
          type="submit"
          class="handwriting w-full py-3 mt-2 border-2 border-gray-400 rounded-lg text-lg font-bold bg-gray-400 hover:bg-blue-50 transition"
        >
          login
        </button>
      </form>

      <div class="flex items-center w-full mt-4 mb-2">
        <input id="remember" type="checkbox" class="accent-blue-600 w-5 h-5 rounded border-gray-400 mr-2" checked>
        <label for="remember" class="text-lg text-gray-700 select-none">아이디 저장</label>
      </div>

      <div class="w-full bg-white rounded-lg shadow-sm py-5 px-4 flex flex-col items-center mb-6">
        <div class="flex gap-4 mb-2">
          <button type="button" class="social-btn bg-yellow-300 hover:bg-yellow-400" aria-label="카카오 로그인">
            <img src="https://upload.wikimedia.org/wikipedia/commons/8/82/Kakao_icon.png" alt="Kakao" class="w-8 h-8">
          </button>
          <button type="button" class="social-btn bg-white border border-gray-300 hover:bg-gray-100" aria-label="구글 로그인">
            <img src="https://upload.wikimedia.org/wikipedia/commons/5/53/Google_%22G%22_Logo.svg" alt="Google" class="w-8 h-8">
          </button>
        </div>
        <p class="text-xs text-gray-500 text-center leading-tight mt-2">
          개인정보 보호를 위해 공용 PC에서 사용 시 SNS계정의 로그아웃<br>
          상태를 꼭 확인해 주세요.
        </p>
      </div>

      <button
        class="w-full py-3 border-2 border-gray-400 rounded-lg text-lg font-bold bg-white hover:bg-blue-50 transition"
        type="button"
      >
        signup
      </button>
      <button @click="closePopup" class="w-full py-3 mt-4 border-2 border-gray-400 rounded-lg text-lg font-bold bg-white hover:bg-gray-100 transition">close</button>
    </div>
  </div>
</template>

<script>
export default {
  methods: {
    closePopup() {
      this.$emit('close-popup');
    }
  }
};
</script>

<style scoped>
/* 폰트 임포트는 여기에 배치 */
@import url('https://fonts.googleapis.com/css2?family=Indie+Flower&family=Nunito:wght@400;700&display=swap');

/* 팝업 오버레이 스타일 (이전과 동일) */
.popup-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5); /* 반투명 검정 배경 */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

/* 팝업 내용 컨테이너 스타일 */
.popup-content {
  background: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  text-align: center;
  /* max-width는 Tailwind 클래스 `max-w-md`로 대체되므로, 여기서는 기본 max-width를 제거하거나 조정합니다. */
  /* max-width: 448px; /* max-w-md와 동일한 28rem */
  width: 40%; /* 작은 화면을 위한 반응형 */
}

/* 제공해주신 HTML의 커스텀 CSS를 여기에 추가 */
.logo-font {
  font-family: 'Indie Flower', cursive;
  letter-spacing: 0.02em;
}
.handwriting {
  font-family: 'Indie Flower', cursive;
}
.social-btn {
  /* @apply는 <style scoped> 내에서 직접 사용할 수 없습니다. Tailwind 클래스를 직접 나열해야 합니다. */
  display: flex;
  align-items: center;
  justify-content: center;
  width: 4rem; /* w-12 */
  height: 4rem; /* h-12 */
  border-radius: 9999px; /* rounded-full */
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06); /* shadow */
  transition: transform 0.15s ease-in-out; /* transition (hover:scale-105의 트랜지션) */
}
.social-btn:hover {
  transform: scale(1.05); /* hover:scale-105 */
}
.social-btn:focus {
  outline: 2px solid #2563eb; /* outline-blue-600 */
  outline-offset: 2px;
}

/* 닫기 버튼에 기본 스타일을 좀 더 명확히 주기 위해 추가 */
.popup-content > button:last-child {
  /* 마지막 버튼(닫기)에 mt-4를 적용했습니다. */
  margin-top: 1rem; /* mt-4 */
}
</style>