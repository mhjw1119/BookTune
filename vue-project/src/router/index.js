import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import BookListView from '@/views/BookListView.vue'
import BookSearchView from '@/views/BookSearchView.vue'
import BookDetailView from '@/views/BookDetailView.vue'
import ProfileView from '@/views/ProfileView.vue'
import CreateMusicView from '@/views/CreateMusicView.vue'
import GoogleCallback from '@/views/GoogleCallback.vue'
import KakaoCallback from '@/views/KakaoCallback.vue'
import ThreadListView from '@/views/ThreadListView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/books',
      name: 'BookList',
      component: BookListView,
    },
    {
      path: '/api/books',
      name: 'BookSearch',
      component: BookSearchView,
    },
    {
      path: '/books/:isbn',
      name: 'BookDetail',
      component: BookDetailView,
      props: true
    },
    {
      path: '/profile/:userId?',
      name: 'profile',
      component: ProfileView,
      meta: { layout: 'none' }
    },
    {
      path: '/liked',
      name: 'liked_books',
      component: ProfileView,
      meta: { layout: 'none' }
    },
    {
      path: '/create-music',
      name: 'createMusic',
      component: CreateMusicView
    },
    {
      path: '/auth/google/callback',
      name: 'GoogleCallback',
      component: GoogleCallback
    },
    {
      path: '/auth/kakao/callback',
      name: 'KakaoCallback',
      component: KakaoCallback
    },
    // {
    //   path: '/community',
    //   name: 'Community',
    //   component: CommunityView
    // },
    {
      path: '/books/threads',
      name: 'threads',
      component: ThreadListView,
      meta: { requiresAuth: true }
    },
  ],
})

export default router
