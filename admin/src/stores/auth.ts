/**
 * src/stores/auth.ts
 */
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/services/api'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('adminToken'))
  const admin = ref<any>(null)
  const isAuthenticated = ref(!!token.value)

  const router = useRouter()

  const login = async (email: string, password: string) => {
    try {
      console.log('Attempting login with:', { email }) // Debug log

      const response = await api.post('/admin/login', {  
        email,
        password
      })

      console.log('Login successful:', response.data) // Debug log

      const { access_token, admin: adminData } = response.data

      token.value = access_token
      admin.value = adminData
      isAuthenticated.value = true

      localStorage.setItem('adminToken', access_token)

      return true
    } catch (error: any) {
      console.error('Full Login Error:', error)
      console.error('Response Data:', error.response?.data)
      console.error('Status Code:', error.response?.status)

      const detail = error.response?.data?.detail
      let message = 'Invalid email or password'

      if (detail) {
        message = detail
      } else if (error.response?.status === 403) {
        message = "You don't have admin privileges or your account is not approved"
      } else if (error.response?.status === 401) {
        message = "Invalid email or password"
      }

      throw new Error(message)
    }
  }

  const logout = () => {
    token.value = null
    admin.value = null
    isAuthenticated.value = false
    localStorage.removeItem('adminToken')
    router.push('/login')
  }

  const checkAuth = async () => {
    if (!token.value) return false

    try {
      const response = await api.get('/admin/me')  
      admin.value = response.data
      isAuthenticated.value = true
      return true
    } catch {
      logout()
      return false
    }
  }

  return {
    token,
    admin,
    isAuthenticated,
    login,
    logout,
    checkAuth
  }
})