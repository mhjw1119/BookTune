import { ref } from 'vue';

const isGenerating = ref(localStorage.getItem('isGenerating') === 'true');

function startGenerating() {
  isGenerating.value = true;
  localStorage.setItem('isGenerating', 'true');
}
function stopGenerating() {
  isGenerating.value = false;
  localStorage.removeItem('isGenerating');
}

export function useGenerating() {
  return {
    isGenerating,
    startGenerating,
    stopGenerating,
  };
} 