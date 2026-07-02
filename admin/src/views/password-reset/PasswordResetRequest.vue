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
                <th class="ps-4">Responder Profile Name</th>
                <th>Secure Email</th>
                <th>Contact Phone</th>
                <th>Created Stamp</th>
                <th>Current Status</th>
                <th class="text-right pe-4">Actions Grid</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="filteredRequests.length === 0">
                <td colspan="6" class="text-center py-5 text-muted empty-row-text">
                  ✨ No active credentials requests require processing.
                </td>
              </tr>
              <tr v-for="req in filteredRequests" :key="req.request_id">
                <td class="ps-4 font-weight-semibold py-3">{{ req.full_name }}</td>
                <td class="text-secondary py-3">{{ req.email }}</td>
                <td class="text-secondary py-3">{{ req.contact_number || '—' }}</td>
                <td class="text-muted font-size-sm py-3">
                  {{ req.created_at ? new Date(req.created_at).toLocaleString() : '—' }}
                </td>
                <td class="py-3">
                  <StatusBadge :status="req.status" />
                </td>
                <td class="text-right pe-4 py-3">
                  <div class="btn-group-custom" v-if="req.status === 'pending'">
                    <button 
                      class="btn btn-success btn-sm me-2 d-flex align-items-center"
                      @click="resetPassword(req)"
                      :disabled="loadingIds.includes(req.request_id)">
                      <span v-if="loadingIds.includes(req.request_id)" class="spinner-inline me-1"></span>
                      {{ loadingIds.includes(req.request_id) ? 'Syncing...' : 'Reset & Email' }}
                    </button>
                    
                    <button 
                      class="btn btn-outline-secondary btn-sm"
                      @click="dismissRequest(req.request_id)">
                      Dismiss
                    </button>
                  </div>
                  <span v-else class="text-muted italic-text font-size-xs">Archived/Processed</span>
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
import StatusBadge from '@/components/common/StatusBadge.vue'
import api from '@/services/api'

const resetRequests = ref<any[]>([])
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
.page-title-main { font-weight: 700; letter-spacing: -0.5px; font-size: 1.75rem; margin-bottom: 0.25rem; }
.page-subtitle-sub { font-size: 0.95rem; }
.row { display: flex; flex-wrap: wrap; margin-right: -15px; margin-left: -15px; }
.col-12 { width: 100%; padding: 0 15px; }
.col-sm-6 { flex: 0 0 50%; max-width: 50%; padding: 0 15px; }
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
.text-right { text-align: right !important; }
.btn-success { color: #fff; background-color: #2eb85c; border-color: #2eb85c; }
.btn-success:hover { background-color: #228b44; border-color: #1f7e3e; }
.btn-success:focus { box-shadow: 0 0 0 0.2rem rgba(46,184,92,0.3); outline: none; }
.btn-outline-secondary { color: #64748b; border-color: #cbd5e1; background-color: transparent; }
.btn-outline-secondary:hover { color: #334155; background-color: #f1f5f9; border-color: #94a3b8; }
.me-2 { margin-right: 0.5rem !important; }
.btn-group-custom { display: inline-flex; }
.italic-text { font-style: italic; }
.empty-row-text { font-size: 0.9rem; background-color: #fafbfc; }
.spinner-inline {
  display: inline-block;
  width: 0.85rem;
  height: 0.85rem;
  border: 2px solid currentColor;
  border-right-color: transparent;
  border-radius: 50%;
  animation: spinner .75s linear infinite;
}
@keyframes spinner { to { transform: rotate(360deg); } }
</style>