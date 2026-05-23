<!-- src/components/common/StatusBadge.vue -->
<template>
  <span class="status-badge" :class="statusClass">
    {{ statusText }}
  </span>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  status: string
}>()

const statusClass = computed(() => {
  switch (props.status.toLowerCase()) {
    case 'approved':
      return 'approved'
    case 'pending':
      return 'pending'
    case 'rejected':
      return 'rejected'
    case 'suspended':
      return 'suspended'
    default:
      return 'pending'
  }
})

const statusText = computed(() => {
  return props.status.charAt(0).toUpperCase() + props.status.slice(1)
})
</script>

<style scoped>
.status-badge {
  padding: 6px 12px;
  border-radius: 9999px;
  font-size: 0.85rem;
  font-weight: 600;
  text-transform: capitalize;
}

.approved {
  background: #d1fae5;
  color: #10b981;
}

.pending {
  background: #fef3c7;
  color: #d97706;
}

.rejected,
.suspended {
  background: #fee2e2;
  color: #ef4444;
}
</style>