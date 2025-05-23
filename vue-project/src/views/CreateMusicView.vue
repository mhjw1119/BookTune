<template>
  <div class="popup-overlay" @click.self="$emit('close-popup')">
    <CreateMusic 
      @submit="handleSubmit"
      @error="handleError"
    />
  </div>
</template>

<script setup>
import CreateMusic from '@/components/createmusic/CreateMusic.vue';

const emit = defineEmits(['close-popup']);

const handleSubmit = (data) => {
  console.log('음악 추천 결과:', data);
  // TODO: 추천 결과 처리 로직 추가
  alert('음악이 성공적으로 생성되었습니다!');
  emit('close-popup');
};

const handleError = (error) => {
  console.error('에러 발생:', error);
};
</script>

<style scoped>
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

body {
  background: #f7f8fa;
}

.font-pacifico {
  font-family: 'Pacifico', cursive;
}

.font-noto {
  font-family: 'Noto Sans KR', sans-serif;
}

/* Custom hand-drawn effect for the button */
.hand-drawn {
  border: 3px solid #222;
  border-radius: 0.75rem;
  box-shadow: 2px 2px 0 #222;
  font-family: 'Pacifico', cursive;
  font-size: 1.25rem;
  background: #fff;
  transition: background 0.2s, box-shadow 0.2s;
}

.hand-drawn:active {
  background: #e5e7eb;
  box-shadow: 1px 1px 0 #222;
}

/* Custom hand-drawn effect for textarea */
.hand-drawn-textarea {
  border: 4px solid #222;
  border-radius: 1rem;
  box-shadow: 2px 2px 0 #222;
  background: #fff;
  resize: none;
  font-size: 1.1rem;
  font-family: 'Noto Sans KR', sans-serif;
  padding: 1rem;
  transition: box-shadow 0.2s;
}

.hand-drawn-textarea:focus {
  outline: none;
  box-shadow: 0 0 0 2px #10b981;
}

/* Custom hand-drawn effect for the main box */
.hand-drawn-box {
  border: 5px solid #10b981;
  border-radius: 1.5rem;
  box-shadow: 0 2px 0 #10b981;
  background: #fff;
}
</style>