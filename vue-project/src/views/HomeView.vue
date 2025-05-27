<template>
  <div class="w-full max-w-6xl mx-auto mt-12 px-6 pb-16">
    <!-- 탭 버튼 -->
    <div class="tab-bar">
      <button
        @click="activeTab = 'best'"
        :class="['tab-btn', { active: activeTab === 'best' } ]"
      >
        Best
      </button>
      <button
        @click="activeTab = 'recommend'"
        :class="['tab-btn', { active: activeTab === 'recommend' } ]"
      >
        Recommend
      </button>
    </div>
    
    <!-- 컴포넌트 표시 영역 -->
    <section class="bg-white rounded-xl shadow-md p-8 flex flex-col">
      <Transition name="fade" mode="out-in">
        <BestBookView v-if="activeTab === 'best'" />
        <RecommendBook v-else />
      </Transition>
    </section>
  </div>
</template>

<script setup>
import BestBookView from '@/views/BestBookView.vue'
import RecommendBook from '@/components/RecommendBook.vue'
import { useBookStore } from '@/stores/books'
import { onMounted, ref } from 'vue'

const store = useBookStore()
const activeTab = ref('best')

onMounted(async () => {
  await store.getBooks()
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Indie+Flower&display=swap');

.tab-bar {
  display: flex;
  justify-content: center;
  gap: 2rem;
  /* border-bottom: 1px solid #e5e7eb; */
  margin-bottom: -1rem;
  position: relative;
  margin-top: 1.2rem;
}

.tab-btn {
  margin-top: 1rem;
  font-family: 'Indie Flower', cursive;
  font-size: 2.5rem;
  font-weight: bold;
  color: #bdbdbd;
  background: none;
  border: none;
  outline: none;
  cursor: pointer;
  padding: 0 1.5rem 0.5rem 1.5rem;
  position: relative;
  transition: color 0.2s;
}

.tab-btn.active {
  color: #222;
}

.tab-btn.active::after {
  content: '';
  display: block;
  margin: 0 auto;
  margin-top: 0.2rem;
  width: 60%;
  height: 2px;
  background: #949596;
  border-radius: 1px;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
