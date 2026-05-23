<!-- src/views/password-reset/PasswordResetRequest.vue -->
<template>
  <div>
    <div class="page-header">
      <h1>Password Reset Requests</h1>
      <p class="subtitle">Manage and process password reset requests from responders</p>
    </div>

    <!-- Stats -->
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

    <!-- Table -->
    <div class="table-container">
      <table class="reset-table">
        <thead>
          <tr>
            <th>Responder Name</th>
            <th>Email</th>
            <th>Request Date</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="request in filteredRequests" :key="request.id">
            <td>{{ request.name }}</td>
            <td>{{ request.email }}</td>
            <td>{{ request.requestDate }}</td>
            <td>
              <StatusBadge :status="request.status" />
            </td>
            <td>
              <div class="action-group">
                <button 
                  v-if="request.status === 'pending'"
                  class="reset-btn"
                  @click="resetPassword(request)">
                  Reset Password
                </button>
                
                <button 
                  v-if="request.status === 'pending'"
                  class="dismiss-btn"
                  @click="dismissRequest(request.id)">
                  Dismiss
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import StatusBadge from '@/components/common/StatusBadge.vue'

// Sample Data
const resetRequests = ref([
  {
    id: 1,
    name: "Juan Dela Cruz",
    email: "juan.delacruz@email.com",
    requestDate: "2025-05-22 14:30",
    status: "pending"
  },
  {
    id: 2,
    name: "Maria Santos",
    email: "maria.santos@email.com",
    requestDate: "2025-05-22 11:15",
    status: "pending"
  },
  {
    id: 3,
    name: "Robert Lim",
    email: "robert.lim@email.com",
    requestDate: "2025-05-21 09:45",
    status: "completed"
  }
])

const searchQuery = ref('')

const filteredRequests = computed(() => {
  return resetRequests.value.filter(req =>
    req.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    req.email.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

const totalRequests = computed(() => resetRequests.value.length)
const pendingRequests = computed(() => 
  resetRequests.value.filter(r => r.status === 'pending').length
)

const resetPassword = (request: any) => {
  if (confirm(`Send new password to ${request.email}?`)) {
    // TODO: Call Flask API to generate and send new password
    alert(`✅ New password has been generated and sent to ${request.email}`)
    
    // Mark as completed
    const req = resetRequests.value.find(r => r.id === request.id)
    if (req) req.status = 'completed'
  }
}

const dismissRequest = (id: number) => {
  if (confirm('Dismiss this request?')) {
    const index = resetRequests.value.findIndex(r => r.id === id)
    if (index !== -1) resetRequests.value.splice(index, 1)
  }
}
</script>

<style scoped>
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