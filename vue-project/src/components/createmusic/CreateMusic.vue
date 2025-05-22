<template>
  <main class="hand-drawn-box p-8 md:p-12 w-[95vw] max-w-xl mx-auto">
    <label for="music-desc" class="block mb-6 text-2xl md:text-3xl font-noto text-gray-900 leading-snug">
      원하는 <span class="font-pacifico text-black text-2xl md:text-3xl align-middle">ai</span> 음악을 설명해주세요.
    </label>
    <textarea
      id="music-desc"
      v-model="musicDescription"
      rows="6"
      placeholder="예: 밝고 신나는 분위기의 일렉트로닉 음악을 원해요."
      class="hand-drawn-textarea w-full mb-8"
      aria-label="원하는 ai 음악 설명 입력"
      :disabled="isLoading"
    ></textarea>
    <div class="flex justify-center">
      <button
        @click="handleSubmit"
        class="hand-drawn px-8 py-2"
        type="button"
        :disabled="isLoading"
      >
        {{ isLoading ? 'Loading...' : 'done' }}
      </button>
    </div>
  </main>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';

const musicDescription = ref('');
const isLoading = ref(false);
const emit = defineEmits(['submit', 'error']);

const handleSubmit = async () => {
  if (!musicDescription.value.trim()) {
    alert('음악에 대한 설명을 입력해주세요!');
    return;
  }

  try {
    isLoading.value = true;
    const response = await axios({
      method: 'post',
      url: '/api/recommend/',
      data: {
        prompt: musicDescription.value.trim()
      },
      headers: {
        'Content-Type': 'application/json'
      }
    });
    emit('submit', response.data);
  } catch (error) {
    console.error('음악 추천 요청 실패:', error);
    emit('error', error.response?.data || '음악 추천을 가져오는데 실패했습니다.');
    alert('음악 추천을 가져오는데 실패했습니다. 다시 시도해주세요.');
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
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

/* Disabled state styles */
.hand-drawn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.hand-drawn-textarea:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style> 