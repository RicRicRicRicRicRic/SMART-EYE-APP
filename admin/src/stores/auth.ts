/**
 * src/stores/auth.ts
 */
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/services/api'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('adminToken'))
  
  // Safely parse the persisted admin user metadata string object back into memory
  const savedAdmin = localStorage.getItem('adminUser')
  const admin = ref<any>(savedAdmin ? JSON.parse(savedAdmin) : null)
  
  const isAuthenticated = ref(!!token.value)
  const router = useRouter()

  const restoreAuth = async () => {
    if (!token.value || !localStorage.getItem('adminUser')) {
      token.value = null
      admin.value = null
      isAuthenticated.value = false
      localStorage.removeItem('adminToken')
      localStorage.removeItem('adminUser')
      return false
    }

    isAuthenticated.value = true
    return true
  }

  const login = async (email: string, password: string) => {
    try {
      const response = await api.post('/admin/login', { email, password })
      const { access_token, admin: adminData } = response.data

      token.value = access_token
      admin.value = adminData
      isAuthenticated.value = true

      // Synchronize both token credentials and object context schemas to LocalStorage
      localStorage.setItem('adminToken', access_token)
      localStorage.setItem('adminUser', JSON.stringify(adminData))

      router.push('/dashboard')
      return true
    } catch (error: any) {
      const message = error.response?.data?.detail || 'Invalid email or password'
      throw new Error(message)
    }
  }

  const logout = () => {
    token.value = null
    admin.value = null
    isAuthenticated.value = false
    localStorage.removeItem('adminToken')
    localStorage.removeItem('adminUser')
    router.push('/login')
  }

  return {
    token,
    admin,
    isAuthenticated,
    login,
    logout,
    restoreAuth
  }
})