<!-- src/components/layout/AdminLayout.vue -->
<template>
  <div class="admin-layout">
    <nav class="navbar">
      <div class="navbar-left">
        <h2>SMART-EYE Admin</h2>
      </div>
      <div class="navbar-right">
        <span>Welcome, Admin</span>
        <button @click="logout" class="logout-btn">Logout</button>
      </div>
    </nav>

    <div class="main-container">
      <aside class="sidebar">
        <router-link to="/dashboard" class="nav-item">
          📊 Dashboard
        </router-link>
        <router-link to="/responders" class="nav-item">
          👥 Responders
        </router-link>
        <router-link to="/password-reset" class="nav-item">
          🔑 Password Reset
        </router-link>
      </aside>

      <main class="content">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const logout = () => {
  localStorage.removeItem('adminToken')
  router.push('/login')
}
</script>

<style scoped>
.admin-layout {
  min-height: 100vh;
  background: #f4f6f9;
}

.navbar {
  background: #1e2937;
  color: white;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.navbar-left h2 {
  margin: 0;
  font-size: 1.4rem;
}

.navbar-right {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.logout-btn {
  background: #ef4444;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
}

.main-container {
  display: flex;
  min-height: calc(100vh - 64px);
}

.sidebar {
  width: 260px;
  background: white;
  padding: 2rem 1rem;
  box-shadow: 2px 0 5px rgba(0,0,0,0.05);
  border-right: 1px solid #e5e7eb;
}

.nav-item {
  display: block;
  padding: 12px 16px;
  margin: 6px 0;
  color: #374151;
  text-decoration: none;
  border-radius: 8px;
  transition: all 0.2s;
}

.nav-item:hover,
.nav-item.router-link-active {
  background: #3b82f6;
  color: white;
}

.content {
  flex: 1;
  padding: 2rem;
  overflow-y: auto;
}
</style>