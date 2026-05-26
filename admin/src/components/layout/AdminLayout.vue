<!-- src/components/layout/AdminLayout.vue -->
<template>
  <div class="admin-layout">
    <!-- Top Navbar -->
    <nav class="navbar">
      <div class="navbar-left">
        <div class="logo">
          <span class="logo-icon">👁️</span>
          <span class="logo-text">SMART-EYE</span>
        </div>
        <h2 class="page-title">{{ currentPageTitle }}</h2>
      </div>
      
      <div class="navbar-right">
        <div class="user-info">
          <span class="username">
            Welcome! {{ userFullName }}
          </span>
        </div>
        <button @click="logout" class="logout-btn">
          Logout
        </button>
      </div>
    </nav>

    <div class="main-container">
      <aside class="sidebar">
        <div class="sidebar-header">
          <h3>Admin Panel</h3>
        </div>
        
        <nav class="sidebar-nav">
          <router-link to="/dashboard" class="nav-item">
            <span class="nav-icon">📊</span>
            <span>Dashboard</span>
          </router-link>
          
          <router-link to="/responders" class="nav-item">
            <span class="nav-icon">👥</span>
            <span>Responders</span>
          </router-link>
          
          <router-link to="/password-reset" class="nav-item">
            <span class="nav-icon">🔑</span>
            <span>Password Reset</span>
          </router-link>
        </nav>
      </aside>

      <main class="content">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const router = useRouter()
const route = useRoute()

const userFullName = computed(() => {
  return authStore.admin?.full_name || 'Admin'
})

const currentPageTitle = computed(() => {
  switch (route.path) {
    case '/dashboard': return 'Dashboard'
    case '/responders': return 'Responders Management'
    case '/password-reset': return 'Password Reset Requests'
    default: return 'Admin Panel'
  }
})

const logout = () => {
  if (confirm('Are you sure you want to logout?')) {
    authStore.logout()
  }
}
</script>

<style scoped>
.admin-layout {
  min-height: 100vh;
  background: #f8fafc;
}

.navbar {
  background: #1e2937;
  color: white;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  position: sticky;
  top: 0;
  z-index: 100;
}

.navbar-left {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.logo {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 1.5rem;
  font-weight: 700;
}

.logo-text {
  color: #60a5fa;
}

.page-title {
  margin: 0;
  font-size: 1.35rem;
  font-weight: 500;
  color: #e2e8f0;
}

.navbar-right {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.logout-btn {
  background: #ef4444;
  color: white;
  border: none;
  padding: 8px 18px;
  border-radius: 6px;
  cursor: pointer;
}

.main-container {
  display: flex;
  min-height: calc(100vh - 73px);
}

.sidebar {
  width: 280px;
  background: white;
  border-right: 1px solid #e2e8f0;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.08);
  padding: 1.5rem 1rem;
  position: fixed;           
  top: 73px;                 
  bottom: 0;
  overflow-y: auto;
  z-index: 90;
}

.sidebar-header {
  padding: 0 1rem 1.5rem;
  border-bottom: 1px solid #e2e8f0;
  margin-bottom: 1rem;
}

.sidebar-nav {
  display: flex;
  flex-direction: column;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  color: #475569;
  text-decoration: none;
  border-radius: 10px;
  margin-bottom: 4px;
  transition: all 0.2s ease;
  font-weight: 500;
}

.nav-item:hover {
  background: #f1f5f9;
  color: #1e40af;
}

.nav-item.router-link-active {
  background: #3b82f6;
  color: white;
}

.content {
  flex: 1;
  padding: 2rem;
  margin-left: 280px;       
  background: #f8fafc;
  min-height: calc(100vh - 73px);
}
</style>