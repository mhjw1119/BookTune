<template>
  <div
    class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
    style="position: fixed !important; z-index: 99999 !important; width: 100vw !important; height: 100vh !important; left: 0 !important; top: 0 !important;"
    @click.self="handleClose"
  >
    <div class="bg-white rounded-lg shadow-lg p-8 md:p-12 w-[95vw] max-w-xl mx-auto">
      <div class="flex justify-between items-center mb-6">
      </div>
      <CreateMusic 
        :book-id="bookId" 
        @close="handleClose"
        @generate="handleGenerate" 
      />
    </div>
  </div>
</template>

<script setup>
console.log('CreateMusicView 렌더링됨');
import CreateMusic from '@/components/createmusic/CreateMusic.vue';

const props = defineProps({
  bookId: {
    type: [String, Number],
    required: true
  }
});

const emit = defineEmits(['close-popup', 'generate']);

const handleClose = () => {
  console.log('CreateMusicView: 팝업 닫기');
  emit('close-popup');
};

const handleGenerate = (data) => {
  console.log('CreateMusicView: 음악 생성 이벤트 수신:', data);
  emit('generate', data);
};

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
</style>