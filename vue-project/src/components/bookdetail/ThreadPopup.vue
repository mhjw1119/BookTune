<template>
  <div v-if="isVisible" class="popup-overlay">
    <div class="popup-content">
      <div class="popup-header">
        <h2>Create Thread</h2>
        <button class="close-button" @click="closePopup">&times;</button>
      </div>
      <div class="popup-body">
        <div class="form-group">
          <label>Content</label>
          <textarea 
            v-model="content" 
            class="content-input"
            placeholder="Write your thoughts about this book..."
            rows="5"
          ></textarea>
        </div>
        <div class="form-group">
          <label>Song</label>
          <div class="file-upload-container" @click="triggerFileInput">
            <input 
              type="file" 
              ref="fileInput"
              @change="handleFileChange"
              accept="audio/*"
              class="file-input"
            />
            <div class="upload-text">Click to upload audio file</div>
            <div class="file-info" v-if="selectedFile">
              <span class="file-name">{{ selectedFile.name }}</span>
              <button class="remove-file" @click.stop="removeFile">&times;</button>
            </div>
            <div class="file-preview" v-if="audioUrl">
              <audio controls :src="audioUrl"></audio>
            </div>
          </div>
        </div>
      </div>
      <div class="popup-footer">
        <button class="cancel-button" @click="closePopup">Cancel</button>
        <button 
          class="submit-button" 
          @click="submitThread"
          :disabled="!isFormValid || isSubmitting"
        >
          {{ isSubmitting ? 'Creating...' : 'Create Thread' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useBookStore } from '@/stores/books';

const props = defineProps({
  isVisible: {
    type: Boolean,
    required: true
  },
  bookId: {
    type: [String, Number],
    required: true
  },
  bookTitle: {
    type: String,
    required: true
  },
  isbn: {
    type: String,
    required: true
  }
});

const emit = defineEmits(['close', 'thread-created']);

const store = useBookStore();
const content = ref('');
const isSubmitting = ref(false);
const selectedFile = ref(null);
const audioUrl = ref(null);
const fileInput = ref(null);

const isFormValid = computed(() => {
  return content.value.trim() && selectedFile.value;
});

const triggerFileInput = () => {
  fileInput.value.click();
};

const handleFileChange = (event) => {
  const file = event.target.files[0];
  if (file && file.type.startsWith('audio/')) {
    selectedFile.value = file;
    audioUrl.value = URL.createObjectURL(file);
  } else {
    alert('Please select an audio file');
    if (fileInput.value) {
      fileInput.value.value = '';
    }
  }
};

const removeFile = (event) => {
  event.stopPropagation();
  selectedFile.value = null;
  if (audioUrl.value) {
    URL.revokeObjectURL(audioUrl.value);
    audioUrl.value = null;
  }
  if (fileInput.value) {
    fileInput.value.value = '';
  }
};

const closePopup = () => {
  content.value = '';
  removeFile(new Event('click'));
  emit('close');
};

const submitThread = async () => {
  if (!isFormValid.value || isSubmitting.value) return;

  try {
    isSubmitting.value = true;
    
    const formData = new FormData();
    formData.append('content', content.value);
    if (selectedFile.value) {
      formData.append('audio_file', selectedFile.value);
    }

    const result = await store.createThread(props.isbn, formData);
    
    console.log('Thread created successfully:', result);
    emit('thread-created', result);
    closePopup();
  } catch (error) {
    console.error('Error creating thread:', error);
    alert(error.message || 'Failed to create thread. Please try again.');
  } finally {
    isSubmitting.value = false;
  }
};
</script>

<style scoped>
.popup-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.popup-content {
  background: white;
  border-radius: 1rem;
  width: 90%;
  max-width: 600px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.popup-header {
  padding: 1.5rem;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.popup-header h2 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1f2937;
}

.close-button {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #6b7280;
  cursor: pointer;
  padding: 0.5rem;
}

.popup-body {
  padding: 1.5rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #333;
}

.content-input {
  width: 100%;
  max-width: 500px;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-family: 'Noto Sans KR', sans-serif;
  font-size: 1rem;
  resize: none;
}

input.content-input {
  height: 2.5rem;
}

textarea.content-input {
  resize: none;
  min-height: 100px;
}

.popup-footer {
  padding: 1.5rem;
  border-top: 1px solid #e5e7eb;
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}

.cancel-button, .submit-button {
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.cancel-button {
  background: #f3f4f6;
  color: #374151;
  border: 1px solid #d1d5db;
}

.submit-button {
  background: #4f46e5;
  color: white;
  border: none;
}

.submit-button:disabled {
  background: #9ca3af;
  cursor: not-allowed;
}

.submit-button:not(:disabled):hover {
  background: #4338ca;
}

.cancel-button:hover {
  background: #e5e7eb;
}

.file-upload-container {
  border: 2px dashed #d1d5db;
  border-radius: 0.5rem;
  padding: 1rem;
  text-align: center;
  background: #f9fafb;
  cursor: pointer;
  transition: all 0.2s;
}

.file-input {
  display: none;
}

.upload-text {
  color: #6b7280;
  font-size: 0.875rem;
  margin-bottom: 0.5rem;
}

.file-info {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.file-name {
  font-size: 0.875rem;
  color: #374151;
}

.remove-file {
  background: none;
  border: none;
  color: #ef4444;
  cursor: pointer;
  font-size: 1.25rem;
  padding: 0.25rem;
}

.file-preview {
  margin-top: 1rem;
}

.file-preview audio {
  width: 100%;
  border-radius: 0.5rem;
}

.file-upload-container:hover {
  border-color: #4f46e5;
  background: #f3f4f6;
}
</style> 