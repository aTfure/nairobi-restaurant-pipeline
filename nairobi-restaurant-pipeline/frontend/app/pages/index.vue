<script setup lang="ts">
const { data: allRestaurants, pending, error } = await useFetch('/api/restaurants')

const activeFilter = ref<'all' | 'has-address' | 'no-address'>('all')
const PAGE_SIZE = 12

const filtered = computed(() => {
  if (!allRestaurants.value) return []
  return allRestaurants.value.filter((r: any) => {
    if (activeFilter.value === 'has-address') return r.address?.trim()
    if (activeFilter.value === 'no-address') return !r.address?.trim()
    return true
  })
})

const currentPage = ref(1)
const totalPages = computed(() => Math.ceil(filtered.value.length / PAGE_SIZE))

const paginated = computed(() => {
  const start = (currentPage.value - 1) * PAGE_SIZE
  return filtered.value.slice(start, start + PAGE_SIZE)
})

watch(activeFilter, () => { currentPage.value = 1 })

function setFilter(f: 'all' | 'has-address' | 'no-address') {
  activeFilter.value = f
}
</script>

<template>
  <main class="page">
    <section class="hero">
      <p class="eyebrow">Westlands, Nairobi</p>
      <h1>Restaurant Explorer</h1>
      <p class="sub">
        {{ allRestaurants?.length ?? 283 }} restaurants discovered via OpenStreetMap pipeline
      </p>
    </section>

    <div class="stats-row">
      <div class="stat">
        <div class="stat-label">Total</div>
        <div class="stat-value">{{ allRestaurants?.length ?? 283 }}</div>
      </div>
      <div class="stat">
        <div class="stat-label">Showing</div>
        <div class="stat-value">{{ filtered.length }}</div>
      </div>
      <div class="stat">
        <div class="stat-label">Sources</div>
        <div class="stat-value">OSM</div>
      </div>
      <div class="stat">
        <div class="stat-label">Area</div>
        <div class="stat-value">Westlands</div>
      </div>
    </div>

    <div class="filters">
      <button
        v-for="f in [
          { key: 'all', label: 'All' },
          { key: 'has-address', label: 'Has address' },
          { key: 'no-address', label: 'No address' },
        ]"
        :key="f.key"
        class="filter-btn"
        :class="{ active: activeFilter === f.key }"
        @click="setFilter(f.key as any)"
      >
        {{ f.label }}
      </button>
    </div>

    <div v-if="pending" class="state">Loading restaurants…</div>
    <div v-else-if="error" class="state error">Unable to load restaurants.</div>
    <template v-else>
      <div class="grid">
        <RestaurantCard
          v-for="r in paginated"
          :key="r.id"
          :restaurant="r"
        />
      </div>

      <div v-if="totalPages > 1" class="pagination">
        <button
          class="page-btn"
          :disabled="currentPage === 1"
          @click="currentPage--"
        >‹</button>
        <span class="page-info">Page {{ currentPage }} of {{ totalPages }}</span>
        <button
          class="page-btn"
          :disabled="currentPage === totalPages"
          @click="currentPage++"
        >›</button>
      </div>
    </template>
  </main>
</template>

<style scoped>
.page {
  max-width: 1080px;
  margin: 0 auto;
  padding: 2rem 1rem 3rem;
  font-family: Inter, system-ui, sans-serif;
}
.eyebrow {
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #64748b;
  margin-bottom: 0.25rem;
}
.hero h1 { font-size: 2rem; font-weight: 600; margin: 0 0 0.25rem; }
.sub { color: #64748b; margin-bottom: 1.5rem; }

.stats-row {
  display: flex;
  gap: 10px;
  margin-bottom: 1rem;
}
.stat {
  background: #f1f5f9;
  border-radius: 8px;
  padding: 0.75rem 1rem;
  flex: 1;
}
.stat-label { font-size: 11px; color: #64748b; text-transform: uppercase; letter-spacing: 0.07em; margin-bottom: 0.2rem; }
.stat-value { font-size: 20px; font-weight: 600; color: #0f172a; }

.filters {
  display: flex;
  gap: 8px;
  margin-bottom: 1.25rem;
}
.filter-btn {
  padding: 0.45rem 1rem;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  background: white;
  color: #475569;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.15s;
}
.filter-btn:hover { background: #f8fafc; }
.filter-btn.active {
  background: #eff6ff;
  border-color: #93c5fd;
  color: #1d4ed8;
}

.grid {
  display: grid;
  gap: 1rem;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
}

.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  margin-top: 1.5rem;
}
.page-btn {
  padding: 0.45rem 0.9rem;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  background: white;
  color: #475569;
  font-size: 16px;
  cursor: pointer;
}
.page-btn:disabled { opacity: 0.35; cursor: default; }
.page-btn:not(:disabled):hover { background: #f8fafc; }
.page-info { font-size: 13px; color: #64748b; }

.state { padding: 3rem; text-align: center; color: #64748b; }
.error { color: #dc2626; }
</style>