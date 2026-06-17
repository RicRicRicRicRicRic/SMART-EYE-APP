<template>
  <div>
    <div class="row mb-4">
      <div class="col-12">
        <h1 class="text-dark dashboard-title">Dashboard Overview</h1>
        <p class="text-muted dashboard-subtitle">Welcome back, {{ userFullName }}! Here's a brief status lookup.</p>
      </div>
    </div>

    <div class="row mb-4">
      <div class="col-sm-6 col-lg-4">
        <div class="card text-white bg-info-coreui widget-card mb-3">
          <div class="card-body d-flex justify-content-between align-items-center">
            <div>
              <div class="text-value-lg">{{ stats.total }}</div>
              <div class="widget-label">Total Responders</div>
            </div>
            <div class="card-icon-big">👥</div>
          </div>
        </div>
      </div>

      <div class="col-sm-6 col-lg-4">
        <div class="card text-white bg-warning-coreui widget-card mb-3">
          <div class="card-body d-flex justify-content-between align-items-center">
            <div>
              <div class="text-value-lg">{{ stats.pending }}</div>
              <div class="widget-label">Pending Approval</div>
            </div>
            <div class="card-icon-big">⏳</div>
          </div>
        </div>
      </div>

      <div class="col-sm-6 col-lg-4">
        <div class="card text-white bg-success-coreui widget-card mb-3">
          <div class="card-body d-flex justify-content-between align-items-center">
            <div>
              <div class="text-value-lg">{{ stats.approved }}</div>
              <div class="widget-label">Approved Accounts</div>
            </div>
            <div class="card-icon-big">✅</div>
          </div>
        </div>
      </div>
    </div>

    <div class="card shadow-accent border-light mb-4">
      <div class="card-header d-flex align-items-center justify-content-between">
        <span class="header-text-main">Recent Registrations</span>
        <span class="badge bg-light-gray text-dark-gray">Latest 5 Entries</span>
      </div>
      <div class="card-body p-0">
        <div class="table-responsive" v-if="recentRegistrations.length > 0">
          <table class="table table-striped table-hover table-align-middle mb-0">
            <thead>
              <tr>
                <th class="ps-4">Responder Details</th>
                <th>Registration Date</th>
                <th class="text-center pe-4">Status</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in recentRegistrations" :key="item.responder_id">
                <td class="ps-4 py-3">
                  <div class="font-weight-semibold">{{ item.full_name }}</div>
                  <div class="text-muted sub-cell-text">{{ item.email }}</div>
                </td>
                <td class="py-3 text-secondary font-size-sm">
                  {{ new Date(item.created_at).toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' }) }}
                </td>
                <td class="text-center pe-4 py-3">
                  <StatusBadge :status="item.approval_status.toLowerCase()" />
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div v-else class="text-muted text-center py-5 my-0 empty-box">
          <span>📤 No new registry data found.</span>
        </div>
      </div>
    </div>

    <div class="d-flex flex-wrap gap-2 mt-2">
      <router-link to="/responders" class="btn btn-primary px-4 shadow-sm font-weight-semibold">
        Manage Responders &nbsp;&rarr;
      </router-link>
      <router-link to="/password-reset" class="btn btn-secondary px-4 shadow-sm font-weight-semibold">
        Password Requests &nbsp;&rarr;
      </router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import api from '@/services/api'
import StatusBadge from '@/components/common/StatusBadge.vue'

const authStore = useAuthStore()

const stats = ref({
  total: 0,
  pending: 0,
  approved: 0
})

const recentRegistrations = ref<any[]>([])

const userFullName = computed(() => authStore.admin?.full_name || 'Admin')

const fetchDashboardData = async () => {
  try {
    const statsRes = await api.get('/admin/responders/stats')
    stats.value = statsRes.data

    const respondersRes = await api.get('/admin/responders')
    const allResponders = respondersRes.data.responders || respondersRes.data
    recentRegistrations.value = allResponders
      .sort((a: any, b: any) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
      .slice(0, 5)
  } catch (error) {
    console.error('Failed to fetch dashboard data:', error)
  }
}

onMounted(fetchDashboardData)
</script>

<style scoped>
.dashboard-title {
  font-weight: 700;
  letter-spacing: -0.5px;
  font-size: 1.75rem;
  margin-bottom: 0.25rem;
}
.dashboard-subtitle {
  font-size: 0.95rem;
}
.row {
  display: flex;
  flex-wrap: wrap;
  margin-right: -15px;
  margin-left: -15px;
}
.col-12 { width: 100%; padding: 0 15px; }
.col-sm-6 { padding: 0 15px; flex: 0 0 50%; max-width: 50%; }
@media (min-width: 992px) {
  .col-lg-4 { flex: 0 0 33.333333%; max-width: 33.333333%; }
}
.card {
  position: relative;
  display: flex;
  flex-direction: column;
  background-color: #fff;
  border: 1px solid #d8dbe0;
  border-radius: 0.375rem;
}
.border-light {
  border-color: #e4e7ea !important;
}
.shadow-accent {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03) !important;
}
.widget-card {
  border: none;
  border-radius: 0.5rem;
  box-shadow: 0 3px 6px rgba(0,0,0,0.04);
}
.card-header {
  padding: 0.85rem 1.25rem;
  background-color: #fff;
  border-bottom: 1px solid #e4e7ea;
}
.header-text-main {
  font-weight: 600;
  color: #3c4b64;
  font-size: 0.95rem;
}
.card-body { flex: 1 1 auto; padding: 1.25rem; }
.p-0 { padding: 0 !important; }
.text-white { color: #fff !important; }
.bg-info-coreui { background-color: #2982cc !important; }
.bg-warning-coreui { background-color: #f6960b !important; }
.bg-success-coreui { background-color: #249b4e !important; }
.text-value-lg { font-size: 1.75rem; font-weight: 700; line-height: 1.2; }
.widget-label { font-size: 0.85rem; font-weight: 500; opacity: 0.85; margin-top: 0.2rem; }
.card-icon-big { font-size: 2.25rem; opacity: 0.25; }
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
  letter-spacing: 0.5px; 
}
.table td { padding: 0.75rem; border-top: 1px solid #e4e7ea; text-align: left; vertical-align: middle; }
.table-striped tbody tr:nth-of-type(odd) { background-color: rgba(0,0,0,.015); }
.table-hover tbody tr:hover { background-color: rgba(50,31,219,0.02); }
.ps-4 { padding-left: 1.25rem !important; }
.pe-4 { padding-right: 1.25rem !important; }
.py-3 { padding-top: 0.85rem !important; padding-bottom: 0.85rem !important; }
.font-weight-semibold { font-weight: 600; color: #3c4b64; font-size: 0.9rem; }
.sub-cell-text { font-size: 0.8rem; margin-top: 0.1rem; }
.text-secondary { color: #768192; }
.font-size-sm { font-size: 0.85rem; }
.text-center { text-align: center !important; }
.btn-primary { color: #fff; background-color: #321fdb; border-color: #321fdb; }
.btn-primary:hover { background-color: #2215ab; border-color: #1f139e; }
.btn-secondary { color: #4f5d73; background-color: #fff; border-color: #cbd5e1; }
.btn-secondary:hover { color: #2f3542; background-color: #f8f9fa; border-color: #94a3b8; }
.btn-secondary:focus { box-shadow: 0 0 0 0.2rem rgba(203,213,225,0.4); outline: none; }
.d-flex { display: flex !important; }
.flex-wrap { flex-wrap: wrap !important; }
.gap-2 { gap: 0.5rem !important; }
.justify-content-between { justify-content: space-between !important; }
.align-items-center { align-items: center !important; }
.bg-light-gray { background-color: #f0f3f5; }
.text-dark-gray { color: #4f5d73; font-size: 0.75rem; font-weight: 600; padding: 0.25rem 0.5rem; border-radius: 0.25rem; }
.empty-box { font-size: 0.9rem; background-color: #fafbfc; }
</style>