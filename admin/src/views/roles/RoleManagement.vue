<template>
  <div>
    <div class="row mb-4">
      <div class="col-12">
        <h1 class="text-dark page-title-main">Role Management</h1>
        <p class="text-muted page-subtitle-sub">Configure user security roles, privilege rings, and dashboard admin assignments.</p>
      </div>
    </div>

    <div class="card shadow-card border-light">
      <div class="card-header">
        <span class="table-header-title">System Authorization Management Matrix</span>
      </div>
      <div class="card-body p-0">
        <div class="table-responsive">
          <table class="table table-striped table-hover table-align-middle mb-0">
            <thead>
              <tr>
                <th class="ps-4">System Identity Account Name</th>
                <th>Secure Communications Email</th>
                <th>Assigned Access Privilege Token</th>
                <th class="text-right pe-4">Administration Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="user in users" :key="user.responder_id" :class="{ 'table-active-row': isCurrentUser(user) }">
                <td class="ps-4 py-3">
                  <span class="font-weight-semibold">{{ user.full_name }}</span>
                  <span v-if="isCurrentUser(user)" class="badge bg-active-self ms-2">You</span>
                </td>
                <td class="text-secondary py-3">{{ user.email }}</td>
                <td class="py-3">
                  <span :class="['badge-pill', getRoleBadgeClass(user.responder_role)]">
                    {{ formatRole(user.responder_role) }}
                  </span>
                </td>
                <td class="text-right pe-4 py-3">
                  <button 
                    v-if="user.responder_role?.toUpperCase() === 'RESPONDER'"
                    class="btn btn-success btn-sm font-weight-semibold"
                    @click="promoteToAdmin(user)">
                    Promote to Admin
                  </button>
                  <button 
                    v-if="user.responder_role?.toUpperCase() === 'ADMIN' && canDemote"
                    class="btn btn-outline-danger btn-sm font-weight-semibold"
                    @click="demoteToResponder(user)">
                    Demote to Responder
                  </button>
                  <span v-if="user.responder_role?.toUpperCase() === 'SUPER_ADMIN'" class="text-muted font-size-xs italic-text pe-1">System Master Lock</span>
                  <span v-if="user.responder_role?.toUpperCase() === 'ADMIN' && !canDemote && !isCurrentUser(user)" class="text-muted font-size-xs italic-text pe-1">Requires Super-Admin</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import api from '@/services/api'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

interface Responder {
  responder_id: string
  full_name: string
  email: string
  responder_role: string
}

const users = ref<Responder[]>([])

const canDemote = computed(() => {
  return authStore.admin?.responder_role?.toUpperCase() === 'SUPER_ADMIN'
})

const fetchUsers = async () => {
  try {
    const response = await api.get('/admin/responders')
    users.value = response.data.responders || response.data || []
  } catch (error) {
    console.error('Failed to fetch users:', error)
  }
}

const isCurrentUser = (user: Responder) => {
  return user.responder_id === authStore.admin?.responder_id
}

const formatRole = (role: string) => {
  if (!role) return 'RESPONDER'
  return role.replace('_', ' ').toUpperCase()
}

const getRoleBadgeClass = (role: string) => {
  const norm = role?.toUpperCase() || 'RESPONDER'
  if (norm === 'SUPER_ADMIN') return 'badge-super-admin'
  if (norm === 'ADMIN') return 'badge-admin'
  return 'badge-responder'
}

const promoteToAdmin = async (user: Responder) => {
  if (!confirm(`Promote ${user.full_name} to Admin?`)) return
  try {
    await api.patch(`/admin/responders/${user.responder_id}/promote-to-admin`)
    alert('User promoted successfully')
    fetchUsers()
  } catch (error: any) {
    alert(error.response?.data?.detail || 'Failed to promote')
  }
}

const demoteToResponder = async (user: Responder) => {
  if (!confirm(`Demote ${user.full_name} to Responder?`)) return
  try {
    await api.patch(`/admin/responders/${user.responder_id}/demote-to-responder`)
    alert('User demoted successfully')
    fetchUsers()
  } catch (error: any) {
    alert(error.response?.data?.detail || 'Failed to demote')
  }
}

onMounted(fetchUsers)
</script>

<style scoped>
.page-title-main { font-weight: 700; letter-spacing: -0.5px; font-size: 1.75rem; margin-bottom: 0.25rem; }
.page-subtitle-sub { font-size: 0.95rem; }
.row { display: flex; flex-wrap: wrap; margin-right: -15px; margin-left: -15px; }
.col-12 { width: 100%; padding: 0 15px; }
.card { position: relative; display: flex; flex-direction: column; background-color: #fff; border: 1px solid #d8dbe0; border-radius: 0.375rem; }
.border-light { border-color: #e4e7ea !important; }
.shadow-card { box-shadow: 0 3px 10px rgba(0, 0, 0, 0.02) !important; }
.card-header { padding: 0.85rem 1.25rem; background-color: #fff; border-bottom: 1px solid #e4e7ea; }
.table-header-title { font-weight: 600; color: #3c4b64; font-size: 0.95rem; }
.card-body { flex: 1 1 auto; padding: 1.25rem; }
.p-0 { padding: 0 !important; }
.py-3 { padding-top: 0.75rem !important; padding-bottom: 0.75rem !important; }
.table-responsive { display: block; width: 100%; overflow-x: auto; }
.table { width: 100%; margin-bottom: 0; border-collapse: collapse; }
.table th { 
  padding: 0.75rem; 
  background-color: #f8f9fa; 
  color: #4f5d73; 
  font-weight: 600; 
  font-size: 0.8rem; 
  text-transform: uppercase; 
  border-bottom: 1px solid #d8dbe0; 
}
.table td { padding: 0.75rem; border-top: 1px solid #e4e7ea; text-align: left; vertical-align: middle; }
.table-hover tbody tr:hover { background-color: rgba(50,31,219,0.015); }
.table-striped tbody tr:nth-of-type(odd) { background-color: rgba(0,0,0,.01); }
.table-active-row { background-color: rgba(50, 31, 219, 0.02) !important; }
.ps-4 { padding-left: 1.25rem !important; }
.pe-4 { padding-right: 1.25rem !important; }
.ms-2 { margin-left: 0.5rem !important; }
.font-weight-semibold { font-weight: 600; color: #3c4b64; font-size: 0.9rem; }
.text-secondary { color: #4f5d73; font-size: 0.875rem; }
.font-size-xs { font-size: 0.8rem; }
.text-right { text-align: right !important; }
.italic-text { font-style: italic; }
.badge { display: inline-block; padding: 0.25em 0.4em; font-size: 75%; font-weight: 700; line-height: 1; text-align: center; white-space: nowrap; vertical-align: baseline; border-radius: 0.25rem; }
.bg-active-self { background-color: #321fdb; color: #fff; }
.btn-success { color: #fff; background-color: #2eb85c; border-color: #2eb85c; }
.btn-success:hover { background-color: #228b44; border-color: #1f7e3e; }
.btn-outline-danger { color: #e55353; border-color: #fbc4c4; background-color: transparent; }
.btn-outline-danger:hover { color: #fff; background-color: #e55353; border-color: #e55353; }

/* CoreUI Badge Pills */
.badge-pill {
  display: inline-block;
  padding: .3em .7em;
  font-size: 75%;
  font-weight: 700;
  line-height: 1;
  text-align: center;
  white-space: nowrap;
  vertical-align: baseline;
  border-radius: 10rem;
  color: #fff;
  letter-spacing: 0.3px;
}
.badge-admin { background-color: #321fdb; }
.badge-super-admin { background-color: #6f42c1; }
.badge-responder { background-color: #768192; }
</style>