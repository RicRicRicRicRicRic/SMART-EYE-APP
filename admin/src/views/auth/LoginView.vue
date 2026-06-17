<template>
  <div class="c-app flex-row align-items-center login-bg">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-5 col-lg-4">
          <transition name="login-card-anim" appear>
            <div class="card p-4 shadow-lg border-0 login-card">
              <div class="card-body">
                <div class="brand-wrap text-center mb-4">
                  <h1 class="text-primary font-weight-bold tracking-tight">SMART-EYE</h1>
                  <p class="text-muted small-text">Admin Dashboard Sign In</p>
                </div>

                <form @submit.prevent="handleLogin">
                  <div class="form-group mb-3">
                    <label class="form-label" for="username">Email Address</label>
                    <div class="input-group">
                      <span class="input-group-text">📧</span>
                      <input
                        v-model="username"
                        type="email"
                        id="username"
                        class="form-control"
                        placeholder="name@domain.com"
                        required
                        :disabled="loading"
                      />
                    </div>
                  </div>

                  <div class="form-group mb-4">
                    <label class="form-label" for="password">Password</label>
                    <div class="input-group">
                      <span class="input-group-text">🔒</span>
                      <input
                        v-model="password"
                        type="password"
                        id="password"
                        class="form-control"
                        placeholder="••••••••"
                        required
                        :disabled="loading"
                      />
                    </div>
                  </div>

                  <div class="row">
                    <div class="col-12">
                      <button type="submit" class="btn btn-primary w-100 py-2 d-flex align-items-center justify-content-center shadow-accent" :disabled="loading">
                        <span v-if="loading" class="spinner-border me-2"></span>
                        <strong>{{ loading ? 'Authenticating...' : 'Sign In' }}</strong>
                      </button>
                    </div>
                  </div>

                  <transition name="fade">
                    <div v-if="error" class="alert alert-danger mt-3 mb-0" role="alert">
                      <div class="d-flex align-items-center">
                        <span class="me-2">⚠️</span>
                        <small>{{ error }}</small>
                      </div>
                    </div>
                  </transition>
                </form>
              </div>
              <div class="card-footer bg-transparent border-0 text-center text-muted pb-2">
                <small class="legal-text">© 2026 SMART-EYE Systems</small>
              </div>
            </div>
          </transition>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

const username = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

const handleLogin = async () => {
  loading.value = true
  error.value = ''

  try {
    await authStore.login(username.value, password.value)
  } catch (err: any) {
    if (err.response?.data?.detail) {
      const detail = err.response.data.detail
      error.value = typeof detail === 'object' ? (detail[0]?.msg || JSON.stringify(detail)) : detail
    } else if (err.message) {
      error.value = typeof err.message === 'object' ? JSON.stringify(err.message) : err.message
    } else {
      error.value = 'Invalid username or password'
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-bg {
  background-color: #ebedef;
  background-image: radial-gradient(circle at top left, #f4f5f7 0%, #ebedef 100%);
  min-height: 100vh;
  display: flex;
  align-items: center;
}
.container {
  width: 100%;
  padding-right: 15px;
  padding-left: 15px;
  margin-right: auto;
  margin-left: auto;
}
.row {
  display: flex;
  flex-wrap: wrap;
  margin-right: -15px;
  margin-left: -15px;
}
.justify-content-center { justify-content: center; }
.col-md-5 {
  flex: 0 0 41.666667%;
  max-width: 41.666667%;
}
@media (min-width: 992px) {
  .col-lg-4 {
    flex: 0 0 33.333333%;
    max-width: 33.333333%;
  }
}
.card {
  position: relative;
  display: flex;
  flex-direction: column;
  min-width: 0;
  word-wrap: break-word;
  background-color: #fff;
  border-radius: 0.5rem;
}
.login-card {
  border: 1px solid rgba(0, 0, 0, 0.05) !important;
}
.p-4 { padding: 1.5rem; }
.pb-2 { padding-bottom: 0.5rem !important; }
.shadow-lg { box-shadow: 0 1rem 3rem rgba(0, 0, 0, 0.1) !important; }
.text-primary { color: #321fdb; }
.font-weight-bold { font-weight: 700; }
.tracking-tight { letter-spacing: -0.5px; }
.text-muted { color: #768192; }
.small-text { font-size: 0.9rem; margin-top: 0.25rem; }
.mb-4 { margin-bottom: 1.5rem; }
.mb-3 { margin-bottom: 1rem; }
.mt-3 { margin-top: 1rem; }
.mb-0 { margin-bottom: 0 !important; }
.w-100 { width: 100%; }
.form-label {
  display: inline-block;
  margin-bottom: .4rem;
  color: #3c4b64;
  font-weight: 600;
  font-size: 0.85rem;
}
.input-group {
  position: relative;
  display: flex;
  flex-wrap: wrap;
  align-items: stretch;
  width: 100%;
}
.input-group-text {
  display: flex;
  align-items: center;
  padding: .45rem .75rem;
  font-size: .875rem;
  background-color: #f0f3f5;
  border: 1px solid #d8dbe0;
  border-radius: .375rem 0 0 .375rem;
  border-right: none;
}
.form-control {
  display: block;
  flex: 1 1 auto;
  width: 1%;
  padding: .45rem .75rem;
  font-size: .875rem;
  color: #4f5d73;
  background-color: #fff;
  border: 1px solid #d8dbe0;
  border-radius: 0 .375rem .375rem 0;
  transition: border-color .15s ease-in-out, box-shadow 0.15s ease-in-out;
}
.form-control:focus {
  outline: 0;
  border-color: #321fdb;
  box-shadow: 0 0 0 0.2rem rgba(50, 31, 219, 0.15);
}
.btn-primary {
  color: #fff;
  background-color: #321fdb;
  border-color: #321fdb;
  border-radius: 0.375rem;
  transition: all 0.15s ease-in-out;
}
.btn-primary:hover:not(:disabled) {
  background-color: #2215ab;
  border-color: #1f139e;
}
.btn-primary:focus {
  box-shadow: 0 0 0 0.2rem rgba(50, 31, 219, 0.35);
  outline: none;
}
.btn-primary:disabled {
  background-color: #a3a6fa;
  border-color: #a3a6fa;
  cursor: not-allowed;
}
.alert-danger {
  color: #e55353;
  background-color: #fde8e8;
  border: 1px solid #fbc4c4;
  padding: .6rem 1rem;
  border-radius: .375rem;
}
.spinner-border {
  display: inline-block;
  width: 1rem;
  height: 1rem;
  vertical-align: text-bottom;
  border: .15em solid currentColor;
  border-right-color: transparent;
  border-radius: 50%;
  animation: spinner .75s linear infinite;
}
.legal-text {
  font-size: 0.75rem;
  color: #a4b0be;
}
@keyframes spinner { to { transform: rotate(360deg); } }

/* Login Form Transitions */
.login-card-anim-enter-active {
  transition: all 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}
.login-card-anim-enter-from {
  opacity: 0;
  transform: translateY(25px) scale(0.97);
}
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.25s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
@media (max-width: 576px) {
  .col-md-5 { flex: 0 0 100%; max-width: 100%; }
}
</style>