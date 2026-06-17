<template>
  <div class="c-app">
    <aside class="c-sidebar" :class="{ 'c-sidebar-show': sidebarShow }">
      <div class="c-sidebar-brand">
        <CIcon :icon="cilViewStream" class="logo-icon-svg" />
        <span class="logo-text">SMART-EYE</span>
      </div>
      
      <nav class="c-sidebar-nav">
        <router-link to="/dashboard" class="c-sidebar-nav-link">
          <CIcon :icon="cilSpeedometer" class="c-sidebar-nav-icon" /> Dashboard
        </router-link>
        
        <router-link to="/responders" class="c-sidebar-nav-link">
          <CIcon :icon="cilPeople" class="c-sidebar-nav-icon" /> Responders
        </router-link>
        
        <router-link to="/password-reset" class="c-sidebar-nav-link">
          <CIcon :icon="cilLockLocked" class="c-sidebar-nav-icon" /> Password Reset
        </router-link>

        <router-link to="/role-management" class="c-sidebar-nav-link">
          <CIcon :icon="cilShieldAlt" class="c-sidebar-nav-icon" /> Role Management
        </router-link>
      </nav>
    </aside>

    <div class="c-wrapper">
      <header class="c-header">
        <button class="c-header-toggler" @click="sidebarShow = !sidebarShow" aria-label="Toggle Sidebar">
          ☰
        </button>
        
        <span class="c-header-brand-title">{{ currentPageTitle }}</span>
        
        <ul class="c-header-nav">
          <li class="c-header-nav-item">
            <span class="user-welcome">Welcome, <strong>{{ userFullName }}</strong></span>
          </li>
          <li class="c-header-nav-item">
            <button @click="logout" class="btn btn-outline-danger btn-sm header-logout-btn">
              Logout
            </button>
          </li>
        </ul>
      </header>

      <div class="c-body">
        <main class="c-main">
          <div class="container-fluid px-4">
            <router-view v-slot="{ Component }">
              <transition name="fade-slide" mode="out-in">
                <component :is="Component" />
              </transition>
            </router-view>
          </div>
        </main>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

// 1. Import CoreUI Icon Vue Component
import { CIcon } from '@coreui/icons-vue'

// 2. Import specific icons needed for this view
import { 
  cilSpeedometer, 
  cilPeople, 
  cilLockLocked, // <-- Replace cilKey with this
  cilShieldAlt,
  cilViewStream
} from '@coreui/icons'

const authStore = useAuthStore()
const router = useRouter()
const route = useRoute()

const sidebarShow = ref(true)

const userFullName = computed(() => {
  return authStore.admin?.full_name || 'Admin'
})

const currentPageTitle = computed(() => {
  switch (route.path) {
    case '/dashboard': return 'Dashboard'
    case '/responders': return 'Responders Management'
    case '/password-reset': return 'Password Reset Requests'
    case '/role-management': return 'Role Management'
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
.c-app {
  display: flex;
  flex-direction: row;
  min-height: 100vh;
  background-color: #f4f5f7;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
}

.c-sidebar {
  width: 260px;
  background: #1e222b;
  color: #fff;
  display: flex;
  flex-direction: column;
  transition: transform 0.25s cubic-bezier(0.4, 0, 0.2, 1), margin-left 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  z-index: 1030;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.05);
}

.c-sidebar-brand {
  height: 60px;
  display: flex;
  align-items: center;
  padding: 0 1.5rem;
  font-size: 1.25rem;
  font-weight: 700;
  background: rgba(0, 0, 0, 0.15);
  gap: 10px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

/* Styled CoreUI SVG logo icon */
.logo-icon-svg {
  width: 24px;
  height: 24px;
  color: #4638e0;
}

.logo-text {
  color: #4638e0;
  letter-spacing: 0.5px;
}

.c-sidebar-nav {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 0.75rem 0;
}

.c-sidebar-nav-link {
  display: flex;
  align-items: center;
  padding: 0.85rem 1.5rem;
  color: rgba(255, 255, 255, 0.65);
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: 500;
  transition: background-color 0.2s, color 0.2s;
}

.c-sidebar-nav-link:hover {
  color: #fff;
  background: rgba(255, 255, 255, 0.04);
}

.c-sidebar-nav-link.router-link-active {
  color: #fff;
  background: #321fdb;
  font-weight: 600;
}

/* Updated styling to control CoreUI SVG sizing perfectly inside nav */
.c-sidebar-nav-icon {
  width: 18px;
  height: 18px;
  margin-right: 1rem;
}

.c-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.c-header {
  height: 60px;
  background: #fff;
  border-bottom: 1px solid #d8dbe0;
  display: flex;
  align-items: center;
  padding: 0 1.5rem;
  justify-content: space-between;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
}

.c-header-toggler {
  background: transparent;
  border: none;
  font-size: 1.3rem;
  cursor: pointer;
  color: #4f5d73;
  padding: 0.25rem;
  border-radius: 0.25rem;
  transition: background-color 0.15s;
}

.c-header-toggler:hover {
  background-color: #f0f3f5;
}

.c-header-brand-title {
  font-size: 1.15rem;
  font-weight: 600;
  color: #3c4b64;
  margin-left: 1.25rem;
  margin-right: auto;
}

.c-header-nav {
  display: flex;
  align-items: center;
  list-style: none;
  margin: 0;
  padding: 0;
  gap: 1.5rem;
}

.user-welcome {
  color: #4f5d73;
  font-size: 0.9rem;
}

.c-body {
  flex: 1;
}

.c-main {
  padding-top: 2rem;
  padding-bottom: 2rem;
}

.container-fluid {
  width: 100%;
  margin-right: auto;
  margin-left: auto;
}

.px-4 {
  padding-right: 1.5rem !important;
  padding-left: 1.5rem !important;
}

.btn {
  font-weight: 500;
  text-align: center;
  vertical-align: middle;
  user-select: none;
  border: 1px solid transparent;
  padding: 0.45rem 0.85rem;
  font-size: 0.875rem;
  border-radius: 0.375rem;
  cursor: pointer;
  transition: color 0.15s ease-in-out, background-color 0.15s ease-in-out, border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
}

.btn-outline-danger {
  color: #e55353;
  border-color: #e55353;
  background: transparent;
}

.btn-outline-danger:hover {
  color: #fff;
  background-color: #e55353;
}

.btn-outline-danger:focus {
  box-shadow: 0 0 0 0.2rem rgba(229, 83, 83, 0.3);
  outline: none;
}

.btn-sm {
  padding: 0.3rem 0.6rem;
  font-size: 0.8rem;
  border-radius: 0.25rem;
}

.header-logout-btn {
  font-weight: 600;
}

/* Page Animations */
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: opacity 0.2s cubic-bezier(0.4, 0, 0.2, 1), transform 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateY(8px);
}

.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}

@media (max-width: 768px) {
  .c-sidebar {
    position: fixed;
    height: 100vh;
    transform: translateX(-100%);
  }
  .c-sidebar.c-sidebar-show {
    transform: translateX(0);
  }
}
</style>