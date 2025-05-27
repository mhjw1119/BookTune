<template>
  <div v-if="$route.meta.layout !== 'none'" class="min-h-screen bg-gray-50">
    <!-- Header -->
    <header class="w-full flex items-center justify-between px-8 py-6 bg-white relative">
      <!-- 햄버거 버튼 (모바일) -->
      <button class="hamburger" @click="showMenu = !showMenu">
        <span :class="{ open: showMenu }"></span>
        <span :class="{ open: showMenu }"></span>
        <span :class="{ open: showMenu }"></span>
      </button>
      <!-- 메뉴 (데스크탑/모바일) -->
      <nav :class="['main-nav', { open: showMenu }]">
        <RouterLink :to="{ name: 'home'}" class="nav-link text-gray-800">Home</RouterLink>
        <RouterLink :to="{ name: 'BookList'}" class="nav-link text-gray-800">Book List</RouterLink>
        <RouterLink :to="{ name: 'threads'}" class="nav-link text-gray-800">Community</RouterLink>
      </nav>
      <div class="flex items-center gap-8 righttebvar">
        <div v-if="!isLoggedIn">
          <a href="#" class="nav-link text-gray-800" @click.prevent="openLoginPopup">Login</a>
          <span> | </span>
          <a href="#" class="nav-link text-gray-800" @click.prevent="openSignupPopup">Sign up</a>
        </div>
        <div v-else>
          <template v-if="nickname">
            <Generating v-if="isGenerating" style="display:inline-block; margin-right:8px;" />
            <a href="#" class="nav-link text-gray-800" :class="nicknameClass" @click.prevent="goProfile">
              {{ nickname }}
            </a>
            <span> | </span>
            <a href="#" class="nav-link text-gray-800" @click.prevent="logout">Logout</a>
          </template>
        </div>
      </div>
    </header>
    <div class="w-full border-t my-8" style="border-color: rgba(0,0,0,0.1);"></div>
    <!-- 로그인/회원가입 팝업 -->
    <LoginView v-if="isLoginPopupVisible" @close-popup="closeLoginPopup" @login-success="checkLogin" />
    <SignupView v-if="isSignupPopupVisible" @close-popup="closeSignupPopup" @signup-success="checkLogin" />
    <!-- 로고/검색바: 모든 페이지에서 항상 보이게 -->
    <div class="flex flex-col items-center text-center pt-12">
      <span class="logo text-gray-900">BookTune</span>
      <span class="my-custom-span text-gray-500 mt-1 mb-16 text-base tracking-wide ">음악과 함께 즐기는 독서</span>
      <form class="search-bar-container" @submit.prevent="onSearch">
        <span class="search-icon">
          <!-- Search icon (left) -->
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="w-5 h-5">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M21 21l-4.35-4.35m0 0A7.5 7.5 0 104.5 4.5a7.5 7.5 0 0012.15 12.15z" />
          </svg>
        </span>
        <input
          type="text"
          placeholder="책, 저자 검색..."
          class="search-input"
          v-model="searchKeyword"
        />
        <button class="search-btn" type="submit">
          <!-- 펼쳐진 책 아이콘 (오픈 북) -->
          <svg class="action-icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M12 19c-2.5-1.5-6-2-9-2V6c3 0 6.5.5 9 2m0 11c2.5-1.5 6-2 9-2V6c-3 0-6.5.5-9 2m0 11V8" />
          </svg>
        </button>
      </form>
      <!-- 구분선 -->
      <div class="w-[92%] border-t my-8" style="border-color: rgba(0,0,0,0.13);"></div>
    </div>
    <Notification />
    <RouterView />
  </div>
  <div v-else>
    <RouterView />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick, watch, computed } from 'vue';
import { RouterView, RouterLink, useRoute } from 'vue-router';
import { useRouter } from 'vue-router';
import LoginView from './views/LoginView.vue';
import SignupView from './views/SignUpView.vue';
import axios from 'axios';
import { useBookStore } from '@/stores/books';
import { websocketService } from './utils/websocket';
import Notification from './components/Notification.vue';
import Generating from './components/notification/Generating.vue';
import { useGenerating } from '@/composables/useGenerating';

const isLoginPopupVisible = ref(false);
const isSignupPopupVisible = ref(false);
const searchKeyword = ref('');
const isLoggedIn = ref(false);
const store = useBookStore();
const nickname = ref('');
const router = useRouter();
const route = useRoute();

// 생성중 상태 composable 사용
const { isGenerating, stopGenerating } = useGenerating();

const showMenu = ref(false)

function openLoginPopup() {
  isLoginPopupVisible.value = true;
}
function closeLoginPopup() {
  isLoginPopupVisible.value = false;
  checkLogin();
}
function openSignupPopup() {
  isSignupPopupVisible.value = true;
}
function closeSignupPopup() {
  isSignupPopupVisible.value = false;
  checkLogin();
}
function onSearch() {
  if (searchKeyword.value.trim()) {
    router.push({ name: 'BookSearch', query: { q: searchKeyword.value.trim() } });
    searchKeyword.value = '';
  }
}
async function checkLogin() {
  try {
    const access = localStorage.getItem('access');
    if (access) {
      isLoggedIn.value = true;
      await nextTick();
      const profile = await getProfile();
      nickname.value = profile.nickname;
    } else {
      isLoggedIn.value = false;
      nickname.value = '';
    }
  } catch (error) {
    console.error('Login check failed:', error);
    isLoggedIn.value = false;
    nickname.value = '';
  }
}
async function goProfile() {
  try {
    const profile = await getProfile();
    router.push({ name: 'profile', params: { userId: profile.id } });
  } catch (error) {
    console.error('프로필 정보를 가져오는데 실패했습니다:', error);
  }
}
function logout() {
  localStorage.removeItem('access');
  isLoggedIn.value = false;
  nickname.value = '';
  router.push({ name: 'home' });
}

onMounted(async () => {
  await checkLogin();
  websocketService.connect();
  websocketService.addListener('song_notification', stopGenerating);
});

onUnmounted(() => {
  websocketService.disconnect();
});

watch(
  () => route.fullPath,
  async () => {
    await checkLogin();
  }
);

const getProfile = async function () {
  try {
    const access = localStorage.getItem('access');
    if (!access) {
      throw new Error('No access token found');
    }
    
    const response = await axios({
      method: 'get',
      url: `${store.API_URL}/api/auth/profile/`,
      headers: { Authorization: `Bearer ${access}` } 
    });
    
    if (!response.data) {
      throw new Error('No profile data received');
    }
    
    return response.data;
  } catch (error) {
    console.error('Profile fetch failed:', error);
    localStorage.removeItem('access'); // 토큰이 유효하지 않은 경우 제거
    throw error;
  }
};

const isKorean = (text) => {
  return /[ㄱ-ㅎ|ㅏ-ㅣ|가-힣]/.test(text);
};

const nicknameClass = computed(() => {
  return {
    'nicknamestyle': true,
    'korean-font': isKorean(nickname.value),
    'english-font': !isKorean(nickname.value)
  };
});
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Indie+Flower&family=Noto+Sans+KR:wght@400;700&family=Pacifico&family=Gaegu:wght@400;700&display=swap');
@import url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_2107-2@1.0/Cafe24Ssurround.woff2');

header {
  position: fixed;
  margin-top: 2rem;
  margin-left: 2rem;
  margin-right: 1rem;
  margin-bottom: 1rem;
  top: 0;
  left: 0;
  width: 100%;
  background-color: white;
  z-index: 9999;
  font-family: 'Indie Flower', cursive;
  margin: 0;
  padding: 1rem 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); /* 선택사항: 그림자 */
}

body {
  font-family: 'Noto Sans KR', sans-serif;
  background: #f7f8fa;
}

a {
  color: inherit;
  text-decoration: none;
}

.router-link-active {
  color: inherit;
}

.search-bar-container {
  display: flex;
  align-items: center;
  width: 100%;
  max-width: 700px;
  margin: 2.5rem auto 2.5rem auto;
  background: #fff;
  box-shadow: 0 2px 16px 0 rgba(0,0,0,0.10);
  padding: 0.5rem 1.5rem;
  border-radius: 9999px ;
  gap: 0.75rem;
  border: 2px solid #e0e0e0;
  margin-bottom: 60px;
}

.search-icon {
  color: #9ca3af;
  display: flex;
  align-items: center;
  margin-right: 0.5rem;
}

.search-input {
  
  flex: 1;
  border: none;
  outline: none;
  background: transparent;
  font-size: 1.1rem;
  padding: 0.8rem 0;
}

.search-btn {
  background: transparent;
  border: none;
  outline: none;
  cursor: pointer;
  padding: 0;
}

.action-icon {
  width: 3rem;
  height: 3rem;
  color: #444;
  opacity: 0.7;
  cursor: pointer;
  transition: opacity 0.2s;
}
.action-icon:hover {
  opacity: 1;
}

.logo {
  font-family: 'Indie Flower', cursive;
  font-size: 6rem;
  letter-spacing: 0.05em;
  margin-top: 10rem;
  margin-bottom: -1rem;
  font-weight: bold;
}

.my-custom-span {
    font-family: 'Cafe24 Ssurround', sans-serif;

    display: block;
    margin-bottom: 5px;
    font-size: 1.5rem;
  }

.section-title {
  font-family: 'Indie Flower', cursive;
  font-size: 3rem;
  letter-spacing: 0.03em;
  font-weight: bold;
}
.nav-link {
  font-family: 'Indie Flower', cursive;
  font-size: 2rem;
  transition: color 0.2s;
  font-weight: bold;
  color: #000000;
  margin-right: 1.5rem;
  margin-left: 1.5rem;
}

.nav-link:last-child {
  margin-right: 4rem;  /* 마지막 nav-link에 더 큰 오른쪽 여백 추가 */
}

.nav-link:hover {
  color: #6366f1;
}
.nav-link:active {
  color: #6366f1;
}
.nicknamestyle {
  font-size: 2rem;
  transition: color 0.2s;
  font-weight: bold;
  color: #000000;
}

.korean-font {
  font-family: 'Gaegu', cursive;
}

.english-font {
  font-family: 'Indie Flower', cursive;
}

.hamburger {
  display: none;
  flex-direction: column;
  justify-content: center;
  width: 40px;
  height: 40px;
  background: none;
  border: none;
  cursor: pointer;
  z-index: 20;
  margin-right: 1rem;
}
.hamburger span {
  display: block;
  height: 4px;
  width: 28px;
  background: #222;
  margin: 5px 0;
  border-radius: 2px;
  transition: 0.3s;
}
.hamburger span.open:nth-child(1) { transform: translateY(9px) rotate(45deg);}
.hamburger span.open:nth-child(2) { opacity: 0;}
.hamburger span.open:nth-child(3) { transform: translateY(-9px) rotate(-45deg);}

.main-nav {
  display: flex;
  gap: 2rem;
  align-items: center;
}
@media (max-width: 900px) {
  .main-nav {
    display: none;
    position: absolute;
    top: 70px;
    left: 0;
    right: 0;
    background: #fff;
    flex-direction: column;
    gap: 1.5rem;
    padding: 2rem 0;
    box-shadow: 0 4px 24px rgba(0,0,0,0.08);
    z-index: 10;
  }
  .main-nav.open {
    display: flex;
  }
  .hamburger {
    display: flex;
  }
  .righttebvar{
    margin-right: 10px;
    padding-right: 2rem;
  }
}
</style>
