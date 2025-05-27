<template>
  <div class="w-full max-w-5xl flex justify-start mt-10">
    <button class="btn-book-action" @click="showPopup">
      <i class="fas fa-music"></i> AI 음악 생성
    </button>
    <CreateMusicView 
      v-if="isPopupVisible" 
      :book-id="bookId"
      @close-popup="closePopup"
      @generate="handleGenerate" 
    />
  </div>
</template>

<script setup>
import { ref } from 'vue';
import CreateMusicView from '@/views/CreateMusicView.vue';

const props = defineProps({
  bookId: {
    type: [String, Number],
    required: true
  }
});

const emit = defineEmits(['generate']);
const isPopupVisible = ref(false);

const showPopup = () => {
  isPopupVisible.value = true;
};

const closePopup = () => {
  isPopupVisible.value = false;
};

const handleGenerate = (data) => {
  emit('generate', data);
};
</script>

<style scoped>
.btn-book-action {
  font-family: 'Gowun Dodum', 'Inter', sans-serif;
  font-size: 1.1rem;
  font-weight: 600;
  background-color: #f6f1e9;
  color: #333;
  padding: 12px 20px;
  border-radius: 10px;
  border: 1px solid #ddd;
  display: inline-flex;
  align-items: center;
  gap: 10px;
  transition: background-color 0.3s ease, transform 0.1s ease;
  box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}

.btn-book-action:hover {
  background-color: #e5ded2;
  transform: translateY(-1px);
}
</style>