<template>
  <div>
    <div class="row align-items-center mb-4">
      <div class="col-md-6">
        <h1 class="text-dark page-title-main">Responders Management</h1>
      </div>
      <div class="col-md-6 text-md-right header-controls d-flex justify-content-md-end align-items-center gap-2">
        <div class="search-input-wrapper">
          <span class="search-icon">🔍</span>
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search full name or email..."
            class="form-control search-field"
          />
        </div>
        <button class="btn btn-outline-primary btn-refresh-custom" @click="fetchResponders" :disabled="loading">
          {{ loading ? 'Updating...' : '↻ Refresh' }}
        </button>
      </div>
    </div>

    <div class="row mb-4">
      <div class="col-sm-4">
        <div class="card text-center bg-white shadow-card border-left-info py-3">
          <div class="text-muted small text-uppercase font-weight-bold tracking-wider">Total Responders</div>
          <div class="text-value-xl mt-1">{{ totalResponders }}</div>
        </div>
      </div>
      <div class="col-sm-4">
        <div class="card text-center bg-white shadow-card border-left-warning py-3">
          <div class="text-muted small text-uppercase font-weight-bold tracking-wider">Pending Approval</div>
          <div class="text-value-xl text-warning mt-1">{{ pendingCount }}</div>
        </div>
      </div>
      <div class="col-sm-4">
        <div class="card text-center bg-white shadow-card border-left-success py-3">
          <div class="text-muted small text-uppercase font-weight-bold tracking-wider">Approved Active</div>
          <div class="text-value-xl text-success mt-1">{{ approvedCount }}</div>
        </div>
      </div>
    </div>

    <div class="card shadow-card border-light">
      <div class="card-header">
        <span class="table-header-title">Responders Registry Database Table</span>
      </div>
      <div class="card-body p-0">
        <div class="table-responsive">
          <table class="table table-striped table-hover table-align-middle mb-0">
            <thead>
              <tr>
                <th class="ps-4">Name</th>
                <th>Email Address</th>
                <th>Phone Number</th>
                <th>Approval Status</th>
                <th>Registered Stamp</th>
                <th class="text-right pe-4">System Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="filteredResponders.length === 0">
                <td colspan="6" class="text-center py-5 text-muted empty-table-info">
                  No matching responders records discovered.
                </td>
              </tr>
              <tr v-for="responder in filteredResponders" :key="responder.responder_id">
                <td class="ps-4 font-weight-semibold py-3">{{ responder.full_name }}</td>
                <td class="text-secondary py-3">{{ responder.email }}</td>
                <td class="text-secondary py-3">{{ responder.contact_number || '—' }}</td>
                <td class="py-3">
                  <StatusBadge :status="responder.approval_status.toLowerCase()" />
                </td>
                <td class="text-muted font-size-sm py-3">
                  {{ new Date(responder.created_at).toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' }) }}
                </td>
                <td class="text-right pe-4 py-3">
                  <span v-if="isCurrentUser(responder)" class="badge-account">
                    Your Account
                  </span>
                  <div v-else class="btn-group-custom">
                    <button v-if="responder.approval_status === 'Pending'" 
                            class="btn btn-success btn-sm me-1 font-weight-semibold"
                            @click="updateStatus(responder.responder_id, { approval_status: 'Approved' })">
                      Approve
                    </button>
                    <button v-if="responder.approval_status === 'Pending' || responder.approval_status === 'Approved'" 
                            class="btn btn-danger btn-sm me-1 font-weight-semibold"
                            @click="updateStatus(responder.responder_id, { approval_status: 'Rejected' })">
                      Reject
                    </button>
                    <button v-if="responder.approval_status === 'Approved'" 
                            class="btn btn-warning btn-sm text-white font-weight-semibold"
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
.page-title-main { font-weight: 700; letter-spacing: -0.5px; font-size: 1.75rem; margin: 0; }
.row { display: flex; flex-wrap: wrap; margin-right: -15px; margin-left: -15px; }
.col-md-6 { flex: 0 0 50%; max-width: 50%; padding: 0 15px; }
.col-sm-4 { flex: 0 0 33.333333%; max-width: 33.333333%; padding: 0 15px; }
.card { position: relative; display: flex; flex-direction: column; background-color: #fff; border: 1px solid #d8dbe0; border-radius: 0.375rem; }
.border-light { border-color: #e4e7ea !important; }
.shadow-card { box-shadow: 0 3px 10px rgba(0, 0, 0, 0.02) !important; }
.card-header { padding: 0.85rem 1.25rem; background-color: #fff; border-bottom: 1px solid #e4e7ea; }
.table-header-title { font-weight: 600; color: #3c4b64; font-size: 0.95rem; }
.card-body { flex: 1 1 auto; padding: 1.25rem; }
.p-0 { padding: 0 !important; }
.py-3 { padding-top: 0.75rem !important; padding-bottom: 0.75rem !important; }
.border-left-info { border-left: 4px solid #2982cc !important; }
.border-left-warning { border-left: 4px solid #f9b115 !important; }
.border-left-success { border-left: 4px solid #2eb85c !important; }
.tracking-wider { letter-spacing: 0.5px; font-size: 0.75rem; }
.text-value-xl { font-size: 2rem; font-weight: 700; color: #2f3542; }
.text-warning { color: #f6960b !important; }
.text-success { color: #249b4e !important; }
.search-input-wrapper { position: relative; display: inline-block; }
.search-icon { position: absolute; left: 10px; top: 50%; transform: translateY(-50%); font-size: 0.85rem; color: #94a3b8; pointer-events: none; }
.search-field { display: block; padding: .4rem .75rem .4rem 2rem; font-size: .875rem; color: #4f5d73; background-color: #fff; border: 1px solid #cbd5e1; border-radius: .375rem; width: 260px; transition: border-color 0.15s, box-shadow 0.15s; }
.search-field:focus { outline: none; border-color: #321fdb; box-shadow: 0 0 0 0.2rem rgba(50,31,219,0.1); }
.gap-2 { gap: 0.5rem !important; }
.btn-outline-primary { color: #321fdb; border-color: #cbd5e1; background-color: #fff; font-weight: 600; }
.btn-outline-primary:hover:not(:disabled) { color: #fff; background-color: #321fdb; border-color: #321fdb; }
.btn-outline-primary:disabled { color: #94a3b8; cursor: not-allowed; }
.btn-success { color: #fff; background-color: #2eb85c; border-color: #2eb85c; }
.btn-success:hover { background-color: #228b44; }
.btn-danger { color: #fff; background-color: #e55353; border-color: #e55353; }
.btn-danger:hover { background-color: #d93737; }
.btn-warning { color: #fff; background-color: #f9b115; border-color: #f9b115; }
.btn-warning:hover { background-color: #e79e07; }
.text-white { color: #fff !important; }
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
.ps-4 { padding-left: 1.25rem !important; }
.pe-4 { padding-right: 1.25rem !important; }
.font-weight-semibold { font-weight: 600; color: #3c4b64; font-size: 0.9rem; }
.text-secondary { color: #4f5d73; font-size: 0.875rem; }
.font-size-sm { font-size: 0.85rem; }
.text-right { text-align: right !important; }
.badge-account { color: #321fdb; font-weight: 600; font-style: italic; font-size: 0.85rem; padding-right: 0.25rem; }
.btn-group-custom { display: inline-flex; gap: 2px; }
.me-1 { margin-right: 0.25rem !important; }
.empty-table-info { font-size: 0.9rem; background-color: #fafbfc; }
@media(max-width: 768px) {
  .col-md-6 { flex: 0 0 100%; max-width: 100%; }
  .header-controls { margin-top: 1rem; width: 100%; justify-content: flex-start !important; }
  .search-field { width: 100%; }
  .search-input-wrapper { flex-grow: 1; }
}
</style>