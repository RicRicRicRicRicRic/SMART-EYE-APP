<template>
  <div>
    <div class="dashboard-header">
      <h1>Dashboard Overview</h1>
      <p class="welcome-text">Welcome back, {{ userFullName }}! Here's what's happening today.</p>
    </div>

    <div class="stats-grid">
      <div class="stat-card total">
        <div class="stat-icon">👥</div>
        <div class="stat-info">
          <h3>Total Responders</h3>
          <p class="stat-number">{{ stats.total }}</p>
        </div>
      </div>

      <div class="stat-card pending">
        <div class="stat-icon">⏳</div>
        <div class="stat-info">
          <h3>Pending Approval</h3>
          <p class="stat-number">{{ stats.pending }}</p>
        </div>
      </div>

      <div class="stat-card approved">
        <div class="stat-icon">✅</div>
        <div class="stat-info">
          <h3>Approved</h3>
          <p class="stat-number">{{ stats.approved }}</p>
        </div>
      </div>
    </div>

    <div class="recent-activity">
      <h2>Recent Registrations</h2>
      <div class="activity-list" v-if="recentRegistrations.length > 0">
        <div v-for="item in recentRegistrations" :key="item.responder_id" class="activity-item">
          <div class="activity-info">
            <strong>{{ item.full_name }}</strong>
            <span class="email">{{ item.email }}</span>
          </div>
          <div class="activity-time">
            {{ new Date(item.created_at).toLocaleDateString() }}
          </div>
          <StatusBadge :status="item.approval_status.toLowerCase()" />
        </div>
      </div>
      <p v-else class="no-data">No recent registrations yet.</p>
    </div>

    <div class="quick-actions">
      <router-link to="/responders" class="action-btn primary">
        Manage All Responders →
      </router-link>
      <router-link to="/password-reset" class="action-btn">
        View Password Reset Requests →
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
    // Get stats
    const statsRes = await api.get('/admin/responders/stats')
    stats.value = statsRes.data

    // Get recent responders
    const respondersRes = await api.get('/admin/responders')
    // Sort by created_at descending and take latest 5
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
.email{
 margin-left: 10px
}

.no-data {
  color: #94a3b8;
  font-style: italic;
  text-align: center;
  padding: 2rem;
}

.dashboard-header {
  margin-bottom: 2rem;
}

.welcome-text {
  color: #64748b;
  font-size: 1.1rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.stat-card {
  background: white;
  padding: 1.8rem;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  display: flex;
  align-items: center;
  gap: 1.2rem;
}

.stat-icon {
  font-size: 2.5rem;
}

.stat-number {
  font-size: 2.4rem;
  font-weight: 700;
  margin: 0.3rem 0 0 0;
}

.pending .stat-number { color: #f59e0b; }
.approved .stat-number { color: #10b981; }
.active .stat-number { color: #22c55e; }

.recent-activity {
  background: white;
  padding: 1.8rem;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  margin-bottom: 2rem;
}

.activity-list {
  margin-top: 1rem;
}

.activity-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 0;
  border-bottom: 1px solid #e2e8f0;
}

.activity-item:last-child {
  border-bottom: none;
}

.activity-info span {
  color: #64748b;
  font-size: 0.95rem;
}

.activity-time {
  color: #94a3b8;
  font-size: 0.9rem;
}

.quick-actions {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
}

.action-btn {
  padding: 14px 24px;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s;
}

.primary {
  background: #3b82f6;
  color: white;
}

.action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0,0,0,0.15);
}
</style>