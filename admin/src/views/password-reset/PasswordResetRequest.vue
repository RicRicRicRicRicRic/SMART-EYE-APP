<template>
  <div>
    <div class="row mb-4">
      <div class="col-12">
        <h1 class="text-dark page-title-main">Password Reset Requests</h1>
        <p class="text-muted page-subtitle-sub">Process security credentials requests submitted by deployed responders.</p>
      </div>
    </div>

    <div class="row mb-4">
      <div class="col-sm-6 col-md-4">
        <div class="card text-center bg-white shadow-card border-left-primary py-3">
          <div class="text-muted small text-uppercase font-weight-bold tracking-wider">Total System Requests</div>
          <div class="text-value-xl mt-1">{{ totalRequests }}</div>
        </div>
      </div>
      <div class="col-sm-6 col-md-4">
        <div class="card text-center bg-white shadow-card border-left-warning py-3">
          <div class="text-muted small text-uppercase font-weight-bold tracking-wider">Awaiting Attention</div>
          <div class="text-value-xl text-warning mt-1">{{ pendingRequests }}</div>
        </div>
      </div>
    </div>

    <div class="card shadow-card border-light">
      <div class="card-header d-flex align-items-center">
        <span class="table-header-title">Request Authorization Dashboard Queue</span>
      </div>
      <div class="card-body p-0">
        <div class="table-responsive">
          <table class="table table-hover table-striped table-align-middle mb-0">
            <thead>
              <tr>
                <th class="ps-4">Full Name</th>
                <th>Email Address</th>
                <th>Request Date</th>
                <th>Expires At</th>
                <th>Status Stamp</th>
                <th class="text-right pe-4">Administrative Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="resetRequests.length === 0">
                <td colspan="6" class="text-center py-5 text-muted empty-table-info">
                  No active password reset requests discovered in queue.
                </td>
              </tr>
              <tr v-for="req in resetRequests" :key="req.ResetModel?.request_id || req.request_id">
                <td class="ps-4 font-weight-semibold py-3">{{ req.full_name }}</td>
                <td class="text-secondary py-3">{{ req.email }}</td>
                <td class="text-muted font-size-sm py-3">
                  {{ formatDate(req.ResetModel?.request_date || req.request_date) }}
                </td>
                <td class="text-muted font-size-sm py-3">
                  {{ formatDate(req.ResetModel?.expires_at || req.expires_at) }}
                </td>
                <td class="py-3">
                  <span :class="getStatusBadgeClass(req.ResetModel?.status || req.status)">
                    {{ req.ResetModel?.status || req.status || 'Unknown' }}
                  </span>
                </td>
                <td class="text-right pe-4 py-3">
                  <div v-if="(req.ResetModel?.status || req.status) === 'pending'" class="d-flex justify-content-end gap-2">
                    <button 
                      class="btn btn-success btn-sm font-weight-semibold px-3"
                      @click="approveReset(req.ResetModel?.request_id || req.request_id!)"
                      :disabled="processingId === (req.ResetModel?.request_id || req.request_id)"
                    >
                      {{ processingId === (req.ResetModel?.request_id || req.request_id) ? 'Processing...' : 'Authorize Reset' }}
                    </button>
                    <button 
                      class="btn btn-danger btn-sm font-weight-semibold px-3"
                      @click="rejectReset(req.ResetModel?.request_id || req.request_id!)"
                      :disabled="processingId === (req.ResetModel?.request_id || req.request_id)"
                    >
                      {{ processingId === (req.ResetModel?.request_id || req.request_id) ? 'Cancelling...' : 'Reject' }}
                    </button>
                  </div>
                  <span v-else class="text-muted font-size-xs font-style-italic">
                    Processed
                  </span>
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
import api from '@/services/api'

interface ResetRequestItem {
  ResetModel?: {
    request_id: string
    responder_id: string
    status: string
    request_date: string | null
    expires_at: string | null
  }
  full_name: string
  email: string
  request_id?: string
  status?: string
  request_date?: string | null
  expires_at?: string | null
}

const resetRequests = ref<ResetRequestItem[]>([])
const processingId = ref<string | null>(null)

const fetchRequests = async () => {
  try {
    const response = await api.get('/admin/password-reset/requests')
    resetRequests.value = response.data
  } catch (error) {
    console.error('Failed to load password reset requests:', error)
  }
}

const approveReset = async (requestId: string) => {
  if (!confirm('Are you sure you want to authorize this reset? A temporary password will be sent automatically.')) return
  
  processingId.value = requestId
  try {
    await api.post(`/admin/password-reset/approve/${requestId}`)
    alert('Password reset completed and notification dispatched successfully.')
    await fetchRequests()
  } catch (error: any) {
    console.error(error)
    alert(error.response?.data?.detail || 'Failed to complete password reset.')
  } finally {
    processingId.value = null
  }
}

const rejectReset = async (requestId: string) => {
  if (!confirm('Are you sure you want to reject this password reset request? This action cannot be undone.')) return
  
  processingId.value = requestId
  try {
    await api.post(`/admin/password-reset/reject/${requestId}`)
    alert('Password reset request has been rejected and cancelled.')
    await fetchRequests()
  } catch (error: any) {
    console.error(error)
    alert(error.response?.data?.detail || 'Failed to reject request.')
  } finally {
    processingId.value = null
  }
}

const totalRequests = computed(() => resetRequests.value.length)
const pendingRequests = computed(() => resetRequests.value.filter(r => 
  (r.ResetModel?.status || r.status) === 'pending'
).length)

const getStatusBadgeClass = (status: string | undefined): string => {
  switch (status?.toLowerCase()) {
    case 'pending': return 'badge bg-warning text-dark px-2.5 py-1 rounded font-size-xs tracking-wide text-uppercase font-weight-bold'
    case 'completed': return 'badge bg-success text-white px-2.5 py-1 rounded font-size-xs tracking-wide text-uppercase font-weight-bold'
    case 'cancelled': return 'badge bg-danger text-white px-2.5 py-1 rounded font-size-xs tracking-wide text-uppercase font-weight-bold'
    default: return 'badge bg-secondary text-white px-2.5 py-1 rounded font-size-xs tracking-wide text-uppercase font-weight-bold'
  }
}

const formatDate = (dateString: string | null | undefined): string => {
  if (!dateString) return '—'
  return new Date(dateString).toLocaleDateString(undefined, {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(fetchRequests)
</script>

<style scoped>
.page-title-main { font-weight: 700; letter-spacing: -0.5px; font-size: 1.75rem; margin: 0; }
.page-subtitle-sub { font-size: 0.9rem; margin-top: 0.25rem; margin-bottom: 0; }
.row { display: flex; flex-wrap: wrap; margin-right: -15px; margin-left: -15px; }
.col-12 { flex: 0 0 100%; max-width: 100%; padding: 0 15px; }
.col-sm-6 { padding: 0 15px; }
@media (min-width: 576px) {
  .col-sm-6 { flex: 0 0 50%; max-width: 50%; }
}
@media (min-width: 768px) {
  .col-md-4 { flex: 0 0 33.333333%; max-width: 33.333333%; }
}
.card { position: relative; display: flex; flex-direction: column; background-color: #fff; border: 1px solid #d8dbe0; border-radius: 0.375rem; }
.border-light { border-color: #e4e7ea !important; }
.shadow-card { box-shadow: 0 3px 10px rgba(0, 0, 0, 0.02) !important; }
.card-header { padding: 0.85rem 1.25rem; background-color: #fff; border-bottom: 1px solid #e4e7ea; }
.table-header-title { font-weight: 600; color: #3c4b64; font-size: 0.95rem; }
.card-body { flex: 1 1 auto; padding: 1.25rem; }
.p-0 { padding: 0 !important; }
.py-3 { padding-top: 0.75rem !important; padding-bottom: 0.75rem !important; }
.border-left-primary { border-left: 4px solid #321fdb !important; }
.border-left-warning { border-left: 4px solid #f9b115 !important; }
.tracking-wider { letter-spacing: 0.5px; font-size: 0.75rem; }
.text-value-xl { font-size: 2rem; font-weight: 700; color: #2f3542; }
.text-warning { color: #f6960b !important; }
.btn-success { color: #fff; background-color: #2eb85c; border-color: #2eb85c; margin-right: 0.5rem;}
.btn-success:hover { background-color: #228b44; border-color: #1f7e3e; }
.btn-success:focus { box-shadow: 0 0 0 0.2rem rgba(46,184,92,0.3); outline: none; }
.btn-success:disabled { background-color: #8cdba3; border-color: #8cdba3; cursor: not-allowed; }
.btn-danger { color: #fff; background-color: #e55353; border-color: #e55353; }
.btn-danger:hover { background-color: #d63939; border-color: #ca3030; }
.btn-danger:focus { box-shadow: 0 0 0 0.2rem rgba(229,83,83,0.3); outline: none; }
.btn-danger:disabled { background-color: #f5a8a8; border-color: #f5a8a8; cursor: not-allowed; }
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
.font-size-xs { font-size: 0.8rem; }
.font-style-italic { font-style: italic; }
.text-right { text-align: right !important; }
.empty-table-info { font-size: 0.9rem; background-color: #fafbfc; }
.bg-warning { background-color: #f9b115 !important; }
.bg-success { background-color: #2eb85c !important; }
.bg-danger { background-color: #e55353 !important; }
.px-2\.5 { padding-left: 0.6rem !important; padding-right: 0.6rem !important; }
.py-1 { padding-top: 0.25rem !important; padding-bottom: 0.25rem !important; }
.rounded { border-radius: 0.2rem !important; }
.tracking-wide { letter-spacing: 0.5px; }
.text-uppercase { text-transform: uppercase; }
.font-weight-bold { font-weight: 700; }
.gap-2 { gap: 0.5rem; }
</style>