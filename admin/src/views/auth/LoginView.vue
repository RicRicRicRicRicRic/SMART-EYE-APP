<!-- src/views/auth/LoginView.vue -->
<template>
  <div class="login-container">
    <div class="login-card">
      <!-- Logo / Header -->
      <div class="login-header">
        <h1>SMART-EYE</h1>
        <p>Admin Dashboard</p>
      </div>

      <!-- Login Form -->
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="username">Username or Email</label>
          <input
            v-model="username"
            type="text"
            id="username"
            placeholder="Enter your username or email"
            required
          />
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <input
            v-model="password"
            type="password"
            id="password"
            placeholder="Enter your password"
            required
          />
        </div>

        <button type="submit" class="login-btn" :disabled="loading">
          {{ loading ? 'Logging in...' : 'Login' }}
        </button>
      </form>

      <div class="login-footer">
        <p>© 2025 SMART-EYE Thesis Project</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const username = ref('')
const password = ref('')
const loading = ref(false)

const handleLogin = async () => {
  loading.value = true

  // Simulate API call delay
  await new Promise(resolve => setTimeout(resolve, 800))

  // TODO: Replace this with real API call to your Flask backend later
  if (username.value && password.value) {
    localStorage.setItem('adminToken', 'fake-jwt-token')
    router.push('/dashboard')
  } else {
    alert('Please enter username and password')
  }

  loading.value = false
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #1e3a8a, #3b82f6);
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.login-card {
  background: white;
  padding: 2.5rem 2rem;
  border-radius: 16px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
  width: 100%;
  max-width: 420px;
  text-align: center;
}

.login-header h1 {
  color: #1e40af;
  font-size: 2.2rem;
  margin: 0 0 0.5rem 0;
  font-weight: 700;
}

.login-header p {
  color: #64748b;
  margin: 0 0 2rem 0;
  font-size: 1.1rem;
}

.form-group {
  margin-bottom: 1.2rem;
  text-align: left;
}

label {
  display: block;
  margin-bottom: 6px;
  font-weight: 500;
  color: #374151;
}

input {
  width: 100%;
  padding: 12px 14px;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 1rem;
  transition: border 0.3s;
}

input:focus {
  outline: none;
  border-color: #3b82f6;
}

.login-btn {
  width: 100%;
  padding: 14px;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  margin-top: 1rem;
  transition: background 0.3s;
}

.login-btn:hover {
  background: #2563eb;
}

.login-btn:disabled {
  background: #93c5fd;
  cursor: not-allowed;
}

.login-footer {
  margin-top: 2rem;
  color: #94a3b8;
  font-size: 0.9rem;
}
</style>