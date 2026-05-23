/**
 * src/router/index.ts
 */
import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

// Layout
import AdminLayout from '@/components/layout/AdminLayout.vue'

// Views
import LoginView from '@/views/auth/LoginView.vue'
import DashboardView from '@/views/dashboard/DashboardView.vue'
import RespondersView from '@/views/responders/RespondersView.vue'
import PasswordResetRequest from '@/views/password-reset/PasswordResetRequest.vue'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginView,
    meta: { requiresAuth: false }
  },
  {
    path: '/dashboard',
    component: AdminLayout,
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'Dashboard',
        component: DashboardView
      }
    ]
  },
  {
    path: '/responders',
    component: AdminLayout,
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'Responders',
        component: RespondersView
      }
    ]
  },
  {
    path: '/password-reset',
    component: AdminLayout,
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'PasswordReset',
        component: PasswordResetRequest
      }
    ]
  },
  // Catch-all route
  {
    path: '/:pathMatch(.*)*',
    redirect: '/dashboard'
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

// Navigation Guard using Pinia Auth Store
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()

  // Wait for auth check if needed
  if (!authStore.isAuthenticated && authStore.token) {
    await authStore.checkAuth()
  }

  const isAuthenticated = authStore.isAuthenticated

  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
  } 
  else if (to.path === '/login' && isAuthenticated) {
    next('/dashboard')
  } 
  else {
    next()
  }
})

export default router