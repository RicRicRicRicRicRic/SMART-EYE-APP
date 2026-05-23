<!-- src/views/dashboard/DashboardView.vue -->
<template>
  <div>
    <div class="dashboard-header">
      <h1>Dashboard Overview</h1>
      <p class="welcome-text">Welcome back, Admin! Here's what's happening today.</p>
    </div>

    <!-- Stats Cards -->
    <div class="stats-grid">
      <div class="stat-card total">
        <div class="stat-icon">👥</div>
        <div class="stat-info">
          <h3>Total Responders</h3>
          <p class="stat-number">{{ totalResponders }}</p>
        </div>
      </div>

      <div class="stat-card pending">
        <div class="stat-icon">⏳</div>
        <div class="stat-info">
          <h3>Pending Approval</h3>
          <p class="stat-number">{{ pendingCount }}</p>
        </div>
      </div>

      <div class="stat-card approved">
        <div class="stat-icon">✅</div>
        <div class="stat-info">
          <h3>Approved</h3>
          <p class="stat-number">{{ approvedCount }}</p>
        </div>
      </div>

      <div class="stat-card active">
        <div class="stat-icon">🟢</div>
        <div class="stat-info">
          <h3>Active Now</h3>
          <p class="stat-number">{{ activeNow }}</p>
        </div>
      </div>
    </div>

    <!-- Recent Activity -->
    <div class="recent-activity">
      <h2>Recent Registrations</h2>
      <div class="activity-list">
        <div v-for="item in recentRegistrations" :key="item.id" class="activity-item">
          <div class="activity-info">
            <strong>{{ item.name }}</strong>
            <span>{{ item.email }}</span>
          </div>
          <div class="activity-time">
            {{ item.timeAgo }}
          </div>
          <StatusBadge :status="item.status" />
        </div>
      </div>
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
import { ref, onMounted } from 'vue'
import StatusBadge from '@/components/common/StatusBadge.vue'

// Sample Data - Will be replaced with real API data later
const totalResponders = ref(48)
const pendingCount = ref(12)
const approvedCount = ref(34)
const activeNow = ref(8)

const recentRegistrations = ref([
  {
    id: 1,
    name: "Carlos Mendoza",
    email: "carlos.m@email.com",
    status: "pending",
    timeAgo: "2 hours ago"
  },
  {
    id: 2,
    name: "Andrea Villanueva",
    email: "andrea.v@email.com",
    status: "approved",
    timeAgo: "5 hours ago"
  },
  {
    id: 3,
    name: "Miguel Santos",
    email: "miguel.s@email.com",
    status: "pending",
    timeAgo: "Yesterday"
  }
])

onMounted(() => {
  // TODO: Fetch real data from Flask backend here
  console.log('Dashboard data loaded')
})
</script>

<style scoped>
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