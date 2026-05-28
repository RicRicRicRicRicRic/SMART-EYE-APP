<!-- src/views/password-reset/PasswordResetRequest.vue -->
<template>
  <div>
    <div class="page-header">
      <h1>Password Reset Requests</h1>
      <p class="subtitle">Manage and process password reset requests from responders</p>
    </div>

    <div class="stats-row">
      <div class="stat-box">
        <h3>Total Requests</h3>
        <p class="big-number">{{ totalRequests }}</p>
      </div>
      <div class="stat-box pending">
        <h3>Pending</h3>
        <p class="big-number">{{ pendingRequests }}</p>
      </div>
    </div>

    <div class="table-container">
      <table class="reset-table">
        <thead>
          <tr>
            <th>Responder Name</th>
            <th>Email</th>
            <th>Phone</th>
            <th>Request Date</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="req in filteredRequests" :key="req.request_id">
            <td>{{ req.full_name }}</td>
            <td>{{ req.email }}</td>
            <td>{{ req.contact_number || 'N/A' }}</td>
            <td>{{ new Date(req.request_date).toLocaleString() }}</td>
            <td>
              <StatusBadge :status="req.status" />
            </td>
            <td>
              <div class="action-group" v-if="req.status === 'pending'">
                <button 
                  class="reset-btn"
                  @click="resetPassword(req)"
                  :disabled="loadingIds.includes(req.request_id)">
                  {{ loadingIds.includes(req.request_id) ? 'Sending...' : 'Reset & Send Email' }}
                </button>
                
                <button 
                  class="dismiss-btn"
                  @click="dismissRequest(req.request_id)">
                  Dismiss
                </button>
              </div>
              <span v-else class="no-actions">No actions available</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import StatusBadge from '@/components/common/StatusBadge.vue'
import api from '@/services/api'

const resetRequests = ref<any[]>([])
const searchQuery = ref('')
const loadingIds = ref<string[]>([])

const fetchResetRequests = async () => {
  try {
    const response = await api.get('/admin/password-reset/requests')
    resetRequests.value = response.data
  } catch (error) {
    console.error(error)
  }
}

const resetPassword = async (req: any) => {
  if (!confirm(`Reset password for ${req.full_name} and send via email?`)) return

  loadingIds.value.push(req.request_id)

  try {
    const result = await api.post('/admin/password-reset', { 
      email: req.email 
    })

    alert(`✅ Password reset successful!\n\n` +
          `Name: ${req.full_name}\n` +
          `Email: ${req.email}\n` +
          `New Password: ${result.data.new_password}\n\n` +
          `Password has been sent to their email.`)

    await fetchResetRequests()
  } catch (error: any) {
    alert(error.response?.data?.detail || 'Failed to reset password')
  } finally {
    loadingIds.value = loadingIds.value.filter(id => id !== req.request_id)
  }
}

const dismissRequest = async (request_id: string) => {
  if (!confirm('Dismiss this request?')) return

  try {
    await api.patch(`/admin/password-reset/${request_id}/dismiss`)
    await fetchResetRequests()
  } catch (error) {
    alert('Failed to dismiss request')
  }
}

const filteredRequests = computed(() => resetRequests.value)

const totalRequests = computed(() => resetRequests.value.length)
const pendingRequests = computed(() => 
  resetRequests.value.filter(r => r.status === 'pending').length
)

onMounted(fetchResetRequests)
</script>



<style scoped>
.no-actions {
  color: #94a3b8;
  font-style: italic;
}

.page-header {
  margin-bottom: 2rem;
}

.subtitle {
  color: #64748b;
  margin-top: 0.5rem;
}

.stats-row {
  display: flex;
  gap: 2rem;
  margin-bottom: 2rem;
}

.stat-box {
  background: white;
  padding: 1.5rem 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  min-width: 200px;
}

.big-number {
  font-size: 2.8rem;
  font-weight: 700;
  margin: 0.5rem 0 0 0;
}

.pending .big-number {
  color: #f59e0b;
}

.table-container {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

.reset-table {
  width: 100%;
  border-collapse: collapse;
}

.reset-table th,
.reset-table td {
  padding: 16px;
  text-align: left;
  border-bottom: 1px solid #e2e8f0;
}

.reset-table th {
  background: #f8fafc;
  font-weight: 600;
  color: #475569;
}

.action-group {
  display: flex;
  gap: 10px;
}

.reset-btn {
  background: #3b82f6;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
}

.dismiss-btn {
  background: #64748b;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
}
</style>