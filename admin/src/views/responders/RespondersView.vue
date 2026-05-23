<!-- src/views/responders/RespondersView.vue -->
<template>
  <div>
    <div class="page-header">
      <h1>Responders Management</h1>
      <div class="header-actions">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Search responders..."
          class="search-input"
        />
        <button class="refresh-btn" @click="fetchResponders">
          ↻ Refresh
        </button>
      </div>
    </div>

    <!-- Stats Row -->
    <div class="stats-grid">
      <div class="stat-card">
        <h3>Total</h3>
        <p class="stat-number">{{ totalResponders }}</p>
      </div>
      <div class="stat-card pending">
        <h3>Pending</h3>
        <p class="stat-number">{{ pendingCount }}</p>
      </div>
      <div class="stat-card approved">
        <h3>Approved</h3>
        <p class="stat-number">{{ approvedCount }}</p>
      </div>
    </div>

    <!-- Responders Table -->
    <div class="table-container">
      <table class="responders-table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Phone</th>
            <th>Status</th>
            <th>Registered</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="responder in filteredResponders" :key="responder.id">
            <td>{{ responder.name }}</td>
            <td>{{ responder.email }}</td>
            <td>{{ responder.phone || 'N/A' }}</td>
            <td>
              <StatusBadge :status="responder.status" />
            </td>
            <td>{{ responder.registeredDate }}</td>
            <td>
              <div class="action-buttons">
                <button 
                  v-if="responder.status === 'pending'"
                  class="approve-btn"
                  @click="updateStatus(responder.id, 'approved')">
                  Approve
                </button>
                
                <button 
                  v-if="responder.status === 'pending' || responder.status === 'approved'"
                  class="reject-btn"
                  @click="updateStatus(responder.id, 'rejected')">
                  Reject
                </button>

                <button 
                  v-if="responder.status === 'approved'"
                  class="suspend-btn"
                  @click="updateStatus(responder.id, 'suspended')">
                  Suspend
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
import { ref, computed, onMounted } from 'vue'
import StatusBadge from '@/components/common/StatusBadge.vue'

// Sample Data (Replace with API call later)
const responders = ref([
  {
    id: 1,
    name: "Juan Dela Cruz",
    email: "juan.delacruz@email.com",
    phone: "09123456789",
    status: "pending",
    registeredDate: "2025-05-20"
  },
  {
    id: 2,
    name: "Maria Santos",
    email: "maria.santos@email.com",
    phone: "09234567890",
    status: "approved",
    registeredDate: "2025-05-19"
  },
  {
    id: 3,
    name: "Robert Lim",
    email: "robert.lim@email.com",
    phone: "09345678901",
    status: "pending",
    registeredDate: "2025-05-22"
  }
])

const searchQuery = ref('')

const filteredResponders = computed(() => {
  return responders.value.filter(r => 
    r.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    r.email.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

const totalResponders = computed(() => responders.value.length)
const pendingCount = computed(() => responders.value.filter(r => r.status === 'pending').length)
const approvedCount = computed(() => responders.value.filter(r => r.status === 'approved').length)

const updateStatus = (id: number, newStatus: string) => {
  const responder = responders.value.find(r => r.id === id)
  if (responder) {
    if (confirm(`Mark this responder as ${newStatus.toUpperCase()}?`)) {
      responder.status = newStatus
      // TODO: Call API to update in backend
      alert(`Responder status updated to ${newStatus}`)
    }
  }
}

const fetchResponders = () => {
  // TODO: Replace with real API call to Flask
  console.log('Fetching latest responders...')
}

onMounted(() => {
  fetchResponders()
})
</script>

<style scoped>
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.page-header h1 {
  margin: 0;
  color: #1e2937;
}

.header-actions {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.search-input {
  padding: 10px 14px;
  width: 320px;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  font-size: 1rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.08);
  text-align: center;
}

.stat-card.pending { border-left: 5px solid #f59e0b; }
.stat-card.approved { border-left: 5px solid #10b981; }

.stat-number {
  font-size: 2.2rem;
  font-weight: 700;
  margin: 0.5rem 0 0 0;
}

.table-container {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.responders-table {
  width: 100%;
  border-collapse: collapse;
}

.responders-table th,
.responders-table td {
  padding: 14px 16px;
  text-align: left;
  border-bottom: 1px solid #e2e8f0;
}

.responders-table th {
  background: #f8fafc;
  font-weight: 600;
  color: #475569;
}

.action-buttons {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.approve-btn {
  background: #10b981;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
}

.reject-btn, .suspend-btn {
  background: #ef4444;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
}
</style>