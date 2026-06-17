<!-- src/views/roles/RoleManagement.vue -->
<template>
  <div>
    <div class="page-header">
      <h1>Role Management</h1>
      <p class="subtitle">Manage user roles and permissions across the system</p>
    </div>

    <div class="table-container">
      <table class="role-table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Current Role</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.responder_id" :class="{ 'current-user': isCurrentUser(user) }">
            <td class="name-cell">
              <strong>{{ user.full_name }}</strong>
            </td>
            <td class="email-cell">{{ user.email }}</td>
            <td>
              <span :class="`role-badge ${user.responder_role?.toLowerCase() || 'responder'}`">
                {{ formatRole(user.responder_role) }}
              </span>
            </td>
            <td class="actions-cell">
              <button 
                v-if="user.responder_role?.toUpperCase() === 'RESPONDER'"
                class="promote-btn"
                @click="promoteToAdmin(user)">
                Promote to Admin
              </button>
              <button 
                v-if="user.responder_role?.toUpperCase() === 'ADMIN' && canDemote"
                class="demote-btn"
                @click="demoteToResponder(user)">
                Demote to Responder
              </button>
              <span v-if="isCurrentUser(user)" class="current-user-tag">
                (You)
              </span>
            </td>
          </tr>
        </tbody>
      </table>
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
  // Ensure we compare uppercase roles consistently
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
  if (!role) return 'Responder'
  return role.replace('_', ' ').toUpperCase()
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
.page-header {
  margin-bottom: 2rem;
}

.subtitle {
  color: #64748b;
  margin-top: 0.5rem;
}

.table-container {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

.role-table {
  width: 100%;
  border-collapse: collapse;
}

.role-table th,
.role-table td {
  padding: 16px 20px;
  text-align: left;
  border-bottom: 1px solid #e2e8f0;
}

.role-table th {
  background: #f8fafc;
  font-weight: 600;
  color: #475569;
}

.name-cell strong {
  font-size: 1.05rem;
}

.email-cell {
  color: #64748b;
  font-size: 0.95rem;
}

.role-badge {
  padding: 6px 14px;
  border-radius: 9999px;
  font-weight: 600;
  font-size: 0.9rem;
}

.role-badge.admin { background: #3b82f6; color: white; }
.role-badge.super_admin { background: #8b5cf6; color: white; }
.role-badge.responder { background: #64748b; color: white; }

.promote-btn {
  background: #10b981;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
}

.demote-btn {
  background: #ef4444;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
}

.current-user-tag {
  color: #3b82f6;
  font-size: 0.85rem;
  font-weight: 500;
}

.actions-cell {
  white-space: nowrap;
}
</style>