import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import BookListView from '@/views/BookListView.vue'
import BookSearchView from '@/views/BookSearchView.vue'
import BookDetailView from '@/views/BookDetailView.vue'
import ProfileView from '@/views/ProfileView.vue'

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
      path: '/profile',
      name: 'profile',
      component: ProfileView,
    }
  ],
})

export default router
