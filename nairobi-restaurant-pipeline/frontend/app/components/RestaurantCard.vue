<script setup lang="ts">
defineProps<{
  restaurant: {
    id: string | number
    name: string
    city?: string | null
    address?: string | null
    lat: number
    lng: number
    source?: string | null
  }
}>()
</script>

<template>
  <article class="card">
    <div class="card-header">
      <span class="card-name">{{ restaurant.name }}</span>
      <span class="badge">{{ restaurant.source ?? 'OSM' }}</span>
    </div>
    <div class="card-meta">
      <div v-if="restaurant.city" class="card-row">
        <span class="icon">🏙</span>{{ restaurant.city }}
      </div>
      <div class="card-row">
        <span class="icon">📍</span>
        <span v-if="restaurant.address">{{ restaurant.address }}</span>
        <span v-else class="no-address">No address recorded</span>
      </div>
      <div class="card-row coords">
        {{ restaurant.lat.toFixed(4) }}, {{ restaurant.lng.toFixed(4) }}
      </div>
    </div>
  </article>
</template>

<style scoped>
.card {
  background: white;
  border: 0.5px solid #e2e8f0;
  border-radius: 12px;
  padding: 1rem 1.1rem;
  display: flex;
  flex-direction: column;
  gap: 8px;
  transition: border-color 0.15s;
}
.card:hover { border-color: #94a3b8; }
.card-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 8px;
}
.card-name {
  font-size: 14px;
  font-weight: 600;
  color: #0f172a;
  line-height: 1.3;
}
.badge {
  font-size: 11px;
  padding: 2px 8px;
  border-radius: 20px;
  background: #dcfce7;
  color: #166534;
  white-space: nowrap;
  flex-shrink: 0;
}
.card-meta { display: flex; flex-direction: column; gap: 4px; }
.card-row {
  display: flex;
  align-items: flex-start;
  gap: 6px;
  font-size: 13px;
  color: #475569;
}
.icon { font-size: 12px; margin-top: 1px; flex-shrink: 0; }
.no-address { color: #94a3b8; font-style: italic; }
.coords { font-size: 12px; color: #94a3b8; padding-left: 18px; }
</style>