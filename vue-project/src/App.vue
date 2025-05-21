<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <header class="w-full flex items-center justify-between px-8 py-6 bg-white shadow-sm fixed top-0 left-0 right-0 z-10">
      <div class="flex items-center gap-8">
        <a href="#" class="nav-link text-gray-800">Home</a>
      </div>
      <div class="flex items-center gap-8">
        <a href="#" class="nav-link text-gray-800">Sign up / Login</a>
      </div>
    </header>

    <!-- Main: 로고를 화면 정중앙에 -->
    <main class="flex flex-col justify-center items-center h-screen text-center">
      <!-- 헤더 높이만큼 padding 줌 (py-6 = 약 24px) -->
    <div class="flex-1 flex flex-col items-center">
      <span class="logo text-gray-900">BookTune</span>
      <span class="text-gray-500 mt-1 text-base tracking-wide">음악과 함께 즐기는 독서</span>
      <!-- Search Bar -->
  <div class="w-full flex justify-center mt-12">
    <input
      type="text"
      placeholder="책, 저자, 음악 검색..."
      class="flex-1 max-w-lg px-5 h-12 rounded-l-lg border border-gray-300 shadow-sm focus:outline-none focus:ring-2 focus:ring-green-200 text-lg bg-white transition"
    />
    <button class="flex items-center justify-center w-12 h-12 bg-gray-400 text-white shadow-md hover:bg-green-400 focus:outline-none focus:ring-2 focus:ring-green-300 focus:ring-opacity-50 transition duration-150 ease-in-out rounded-r-lg -ml-px">
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-6 h-6">
        <path stroke-linecap="round" stroke-linejoin="round" d="M9 19V6l12-3v13m-12 3H2.25M9 19c0 1.096-.45 2-1.006 2S6 20.096 6 19s.45-2 1.006-2S9 17.904 9 19zm0 0c0 1.096-.45 2-1.006 2s-1.006-.904-1.006-2S7.994 17 9 17zm12-3c0 1.096-.45 2-1.006 2s-1.006-.904-1.006-2S19.994 12 21 12zm0 0V6.75V4.5H21"/>
      </svg>
    </button>
  </div>
    </div>

    <!-- 검색색 바바
  <div class="w-full flex justify-center mt-12">
    <input
      v-model="searchQuery"
      type="text"
      placeholder="책, 저자, 음악 검색..."
      class="flex-1 max-w-lg px-5 h-12 rounded-l-lg border border-gray-300 shadow-sm focus:outline-none focus:ring-2 focus:ring-green-200 text-lg bg-white transition"
    />
    <button
      @click="handleSearch"
      class="flex items-center justify-center w-12 h-12 bg-gray-400 text-white shadow-md hover:bg-green-400 focus:outline-none focus:ring-2 focus:ring-green-300 focus:ring-opacity-50 transition duration-150 ease-in-out rounded-r-lg -ml-px"
    >
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-6 h-6">
        <path stroke-linecap="round" stroke-linejoin="round" d="M9 19V6l12-3v13m-12 3H2.25M9 19c0 1.096-.45 2-1.006 2S6 20.096 6 19s.45-2 1.006-2S9 17.904 9 19zm0 0c0 1.096-.45 2-1.006 2s-1.006-.904-1.006-2S7.994 17 9 17zm12-3c0 1.096-.45 2-1.006 2s-1.006-.904-1.006-2S19.994 12 21 12zm0 0V6.75V4.5H21"/>
      </svg>
    </button>
  </div> -->


  </main>
  </div>

  <RouterView />

</template>



<script>
export default {
  name: "App",
};

import { RouterView } from 'vue-router'

</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Indie+Flower&family=Noto+Sans+KR:wght@400;700&display=swap');

body {
  font-family: 'Noto Sans KR', sans-serif;
  background: #f7f8fa;
}
.logo {
  font-family: 'Indie Flower', cursive;
  font-size: 6rem; /* 헤더에 맞게 크기 조절을 고려해보세요. 현재 6rem은 매우 큽니다. */
  letter-spacing: 0.05em;
}
.section-title {
  font-family: 'Indie Flower', cursive;
  font-size: 3rem;
  letter-spacing: 0.03em;
  font-weight: bold;
}
.nav-link {
  font-family: 'Indie Flower', cursive;
  font-size: 2rem; /* 헤더에 맞게 크기 조절을 고려해보세요. */
  transition: color 0.2s;
  font-weight: bold;
}
.nav-link:hover {
  color: #6366f1;
}
</style>