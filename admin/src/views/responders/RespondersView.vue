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
        <button class="refresh-btn" @click="fetchResponders" :disabled="loading">
          ↻ Refresh
        </button>
      </div>
    </div>

    <!-- Stats -->
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

    <!-- Table -->
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
          <tr v-for="responder in filteredResponders" :key="responder.responder_id">
            <td>{{ responder.full_name }}</td>
            <td>{{ responder.email }}</td>
            <td>{{ responder.contact_number || 'N/A' }}</td>
            <td>
              <StatusBadge :status="responder.approval_status.toLowerCase()" />
            </td>
            <td>{{ new Date(responder.created_at).toLocaleDateString() }}</td>
            <td>
              <!-- Show "Your Account" if it's the logged-in user -->
              <span v-if="isCurrentUser(responder)" class="your-account">
                Your Account
              </span>
              <!-- Otherwise show action buttons -->
              <div v-else class="action-buttons">
                <button v-if="responder.approval_status === 'Pending'" 
                        class="approve-btn"
                        @click="updateStatus(responder.responder_id, { approval_status: 'Approved' })">
                  Approve
                </button>
                <button v-if="responder.approval_status === 'Pending' || responder.approval_status === 'Approved'" 
                        class="reject-btn"
                        @click="updateStatus(responder.responder_id, { approval_status: 'Rejected' })">
                  Reject
                </button>
                <button v-if="responder.approval_status === 'Approved'" 
                        class="suspend-btn"
                        @click="updateStatus(responder.responder_id, { is_active: 'suspended' })">
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
import { responderService, type Responder } from '@/services/responderService'
import { useAuthStore } from '@/stores/auth'
import StatusBadge from '@/components/common/StatusBadge.vue'

const authStore = useAuthStore()

const responders = ref<Responder[]>([])
const loading = ref(false)
const searchQuery = ref('')

const fetchResponders = async () => {
  loading.value = true
  try {
    const data = await responderService.getAll()
    responders.value = Array.isArray(data) ? data : data.responders || []
  } catch (error) {
    console.error('Failed to fetch responders:', error)
    alert('Failed to load responders')
  } finally {
    loading.value = false
  }
}

const isCurrentUser = (responder: Responder) => {
  return responder.responder_id === authStore.admin?.responder_id
}

const updateStatus = async (responderId: string, data: any) => {
  if (!confirm('Are you sure you want to update this responder?')) return

  try {
    await responderService.updateStatus(responderId, data)
    await fetchResponders()
    alert('Status updated successfully')
  } catch (error) {
    alert('Failed to update status')
  }
}

const filteredResponders = computed(() => {
  return responders.value.filter(r =>
    r.full_name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    r.email.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

const totalResponders = computed(() => responders.value.length)
const pendingCount = computed(() => responders.value.filter(r => r.approval_status === 'Pending').length)
const approvedCount = computed(() => responders.value.filter(r => r.approval_status === 'Approved').length)

onMounted(fetchResponders)
</script>

<style scoped>
.your-account {
  color: #3b82f6;
  font-weight: 600;
  font-style: italic;
}

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