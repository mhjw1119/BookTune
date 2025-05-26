<template>
  <main class="hand-drawn-box px-16 py-20 md:px-24 md:py-28 w-[90vw] max-w-lg mx-auto">
    <label for="music-desc" class="block mb-6 text-2xl md:text-3xl font-noto text-gray-900 leading-snug">
      원하는 <span class="font-pacifico text-black text-2xl md:text-3xl align-middle">ai</span> 음악을 설명해주세요.
    </label>
    <textarea
      id="music-desc"
      v-model="prompt"
      rows="6"
      placeholder="음악 생성을 위한 프롬프트를 입력하세요..."
      class="hand-drawn-textarea w-full mb-8"
      aria-label="원하는 ai 음악 설명 입력"
      :disabled="isGenerating"
      style="max-width: 100%; box-sizing: border-box;"
    ></textarea>
    <div class="flex justify-center">
      <button
        @click="handleGenerateMusic"
        class="hand-drawn px-8 py-2"
        type="button"
        :disabled="isGenerating"
        style="max-width: 100%;"
      >
        {{ isGenerating ? '음악 생성 중...' : '음악 생성하기' }}
      </button>
    </div>
    <div v-if="generatedMusic" class="mt-8">
      <h3 class="text-xl font-bold mb-4">생성된 음악</h3>
      <audio :src="generatedMusic.audio_url" controls class="w-full"></audio>
    </div>
  </main>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useBookStore } from '@/stores/books';
import { useGenerating } from '@/composables/useGenerating';

const { startGenerating } = useGenerating();

const props = defineProps({
  bookId: {
    type: [String, Number],
    required: true
  }
});

const emit = defineEmits(['close', 'generate']);

const store = useBookStore();
const prompt = ref('');
const isGenerating = ref(false);
const generatedMusic = ref(null);

const handleGenerateMusic = async () => {
  console.log('음악 생성 버튼 클릭');
  if (!prompt.value.trim()) {
    alert('프롬프트를 입력해주세요.');
    return;
  }

  try {
    console.log('음악 생성 요청 시작');
    startGenerating(); // 생성중 애니메이션 시작
    isGenerating.value = true;
    const response = await axios.post(
      `${store.API_URL}/api/songs/generate/`,
      JSON.stringify({
        prompt: prompt.value.trim(),
        book_id: props.bookId
      }),
      {
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('access')}`
        }
      }
    );

    console.log('음악 생성 응답:', response.data);

    if (response.data.status === 'processing') {
      alert('음악 생성이 시작되었습니다. 잠시만 기다려주세요.');
      generatedMusic.value = response.data;
      prompt.value = '';  // 입력 필드 초기화
      console.log('generate 이벤트 발생');
      emit('generate', response.data);  // generate 이벤트 발생
      console.log('close 이벤트 발생');
      emit('close');  // 팝업 닫기
    } else {
      throw new Error('음악 생성 요청 실패');
    }
  } catch (error) {
    console.error('음악 생성 실패:', error);
    alert(error.response?.data?.error || '음악 생성에 실패했습니다. 다시 시도해주세요.');
  } finally {
    isGenerating.value = false;
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Pacifico&family=Noto+Sans+KR:wght@400;700&display=swap');

.hand-drawn-box {
  border: 5px solid #10b981;
  border-radius: 1.5rem;
  box-shadow: 0 2px 0 #10b981;
  background: #fff;
}

.font-pacifico {
  font-family: 'Pacifico', cursive;
}

.font-noto {
  font-family: 'Noto Sans KR', sans-serif;
}

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

.hand-drawn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.hand-drawn-textarea:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style> 
