import { useUserStore } from '@/stores/user'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/Register.vue')
  },
  {
    path: '/question/:id',
    name: 'QuestionDetail',
    component: () => import('@/views/QuestionDetail.vue')
  },
  {
    path: '/ask',
    name: 'Ask',
    component: () => import('@/views/Ask.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/hot',
    name: 'Hot',
    component: () => import('@/views/Hot.vue')
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('@/views/Profile.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/ai',
    name: 'AI',
    component: () => import('@/views/AI.vue')
  }
]

export default routes

export const setupRouterGuard = (router) => {
  router.beforeEach((to, from, next) => {
    const userStore = useUserStore()
    if (to.meta?.requiresAuth && !userStore.isLoggedIn()) {
      next('/login')
    } else {
      next()
    }
  })
}