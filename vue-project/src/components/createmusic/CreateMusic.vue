<template>
  <main class="modal-content music-modal-content">
    <label for="music-desc" class="block mb-6 text-2xl font-indie text-gray-900 leading-snug">
      원하는 <span class="font-pacifico text-blue-400 text-2xl align-middle"></span> AI 음악을 설명해주세요.
    </label>
    <textarea
      id="music-desc"
      v-model="prompt"
      rows="6"
      placeholder="음악 생성을 위한 프롬프트를 입력하세요...
ex) 차분하면서 피아노 선율이 돋보이는 음악을 만들어줘."
      class="edit-textarea w-full mb-8"
      aria-label="원하는 ai 음악 설명 입력"
      :disabled="isGenerating"
      style="max-width: 100%; box-sizing: border-box;"
    ></textarea>
    <div class="flex justify-center">
      <button
        @click="handleGenerateMusic"
        class="save-btn px-8 py-2"
        type="button"
        :disabled="isGenerating"
        style="max-width: 100%;"
      >
        {{ isGenerating ? '음악 생성 중...' : '음악 생성하기' }}
      </button>
    </div>
    <div v-if="generatedMusic" class="mt-8">
      <h3 class="text-xl font-bold mb-4 font-indie">생성된 음악</h3>
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
@import url('https://fonts.googleapis.com/css2?family=Indie+Flower&family=Noto+Sans+KR:wght@400;700&family=Pacifico&display=swap');

.font-indie {
  font-family: sans-serif;
  font-size: 1.5rem;
  font-weight: bold;
  text-align: center;
}
.font-pacifico {
  font-family: sans-serif;
}

.music-modal-content {
  background: #fff;
  padding: 2rem;
  border-radius: 1rem;
  width: 90vw;
  max-width: 480px;
  box-shadow: 0 4px 24px rgba(0,0,0,0.08);
  border: 1px solid #eee;
  margin: 3rem auto 0 auto;
}

.edit-textarea {
  width: 100%;
  min-height: 120px;
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 0.5rem;
  margin-bottom: 1rem;
  resize: none;
  font-size: 1.05rem;
  font-family: 'Noto Sans KR', 'Indie Flower', cursive;
  transition: box-shadow 0.2s, border 0.2s;
}
.edit-textarea:focus {
  outline: none;
  border-color: #61bef8;
  box-shadow: 0 0 0 2px #61bef855;
}
.edit-textarea:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.save-btn {
  background: #61bef8;
  color: white;
  border: none;
  padding: 0.8rem 2.2rem;
  border-radius: 0.5rem;
  cursor: pointer;
  font-weight: bold;
  font-size: 1.1rem;
  font-family: sans-serif;
  transition: background 0.2s, box-shadow 0.2s, transform 0.1s;
  box-shadow: 0 2px 8px rgba(0,0,0,0.10);
}
.save-btn:hover:not(:disabled) {
  background: #0078c8;
  box-shadow: 0 4px 16px rgba(97,190,248,0.13);
  transform: translateY(-2px) scale(1.03);
}
.save-btn:active:not(:disabled) {
  background: #005fa3;
  transform: scale(0.98);
}
.save-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

h3 {
  font-family: 'Indie Flower', cursive;
}
</style> 
