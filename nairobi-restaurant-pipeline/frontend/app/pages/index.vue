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
  <div class="w-full">
    <section class="flex flex-col gap-2">
      <div class="flex items-center gap-2 text-on-surface-variant font-label-caps text-label-caps">
        <span class="material-symbols-outlined" style="font-size: 16px;">location_on</span>
        WESTLANDS, NAIROBI
      </div>
      <h2 class="font-display-lg text-display-lg text-on-background">Restaurant Explorer</h2>
      <p class="font-body-base text-body-base text-on-surface-variant max-w-2xl">
        {{ allRestaurants?.length ?? 283 }} restaurants discovered via OpenStreetMap pipeline. Displaying live extraction telemetry and confidence scores for verified geographic entities.
      </p>
    </section>

    <section class="grid grid-cols-1 md:grid-cols-4 gap-gutter mt-4">
      <div class="bg-surface-container-lowest border border-surface-variant rounded-lg p-stack-md flex flex-col gap-1">
        <span class="font-label-caps text-label-caps text-on-surface-variant uppercase">Total Restaurants</span>
        <span class="font-stat-lg text-stat-lg text-on-background">{{ allRestaurants?.length ?? 283 }}</span>
      </div>
      <div class="bg-surface-container-lowest border border-surface-variant rounded-lg p-stack-md flex flex-col gap-1">
        <span class="font-label-caps text-label-caps text-on-surface-variant uppercase">Showing</span>
        <span class="font-stat-lg text-stat-lg text-on-background">{{ filtered.length }}</span>
      </div>
      <div class="bg-surface-container-lowest border border-surface-variant rounded-lg p-stack-md flex flex-col gap-1">
        <span class="font-label-caps text-label-caps text-on-surface-variant uppercase">Avg Confidence</span>
        <span class="font-stat-lg text-stat-lg text-secondary flex items-center gap-2">88% <span class="material-symbols-outlined" style="font-size: 20px;">trending_up</span></span>
      </div>
      <div class="bg-surface-container-lowest border border-surface-variant rounded-lg p-stack-md flex flex-col gap-1">
        <span class="font-label-caps text-label-caps text-on-surface-variant uppercase">Coverage Area</span>
        <span class="font-stat-lg text-stat-lg text-on-background truncate">Westlands</span>
      </div>
    </section>

    <section class="flex flex-wrap gap-2 items-center mt-2">
      <button
        v-for="f in [
          { key: 'all', label: 'All' },
          { key: 'has-address', label: 'Verified' },
          { key: 'no-address', label: 'Pending' },
        ]"
        :key="f.key"
        class="px-4 py-2 rounded-lg transition-colors"
        :class="activeFilter === f.key
          ? 'bg-primary-container text-on-primary-container font-body-bold'
          : 'bg-surface-container-lowest border border-surface-variant text-on-surface-variant font-body-base hover:bg-surface-container-low'"
        @click="setFilter(f.key as any)"
      >
        {{ f.label }}
      </button>
      <button class="bg-surface-container-lowest border border-error-container text-error font-body-base px-4 py-2 rounded-lg hover:bg-error-container transition-colors flex items-center gap-2">
        <span class="material-symbols-outlined" style="font-size: 16px;">warning</span> Sync Issues
      </button>
    </section>

    <div v-if="pending" class="py-16 text-center text-on-surface-variant">Loading restaurants…</div>
    <div v-else-if="error" class="py-16 text-center text-error">Unable to load restaurants.</div>
    <template v-else>
      <section class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-gutter mt-2">
        <RestaurantCard
          v-for="r in paginated"
          :key="r.id"
          :restaurant="r"
        />
      </section>

      <div v-if="totalPages > 1" class="flex items-center justify-center gap-3 mt-6">
        <button class="px-3 py-2 rounded-lg border border-surface-variant bg-surface-container-lowest text-on-surface-variant disabled:opacity-35" :disabled="currentPage === 1" @click="currentPage--">‹</button>
        <span class="text-sm text-on-surface-variant">Page {{ currentPage }} of {{ totalPages }}</span>
        <button class="px-3 py-2 rounded-lg border border-surface-variant bg-surface-container-lowest text-on-surface-variant disabled:opacity-35" :disabled="currentPage === totalPages" @click="currentPage++">›</button>
      </div>
    </template>

    <section class="mt-8 bg-surface-container-low border border-outline-variant rounded-lg p-stack-lg flex flex-col md:flex-row gap-6 items-center justify-between">
      <div class="flex-1">
        <h3 class="font-headline-md text-[20px] text-on-background mb-1">Add a Missing Entity</h3>
        <p class="font-body-base text-body-base text-on-surface-variant">Manually inject a new restaurant record into the crowdsourced verification pipeline.</p>
      </div>
      <div class="flex flex-col sm:flex-row gap-3 w-full md:w-auto">
        <input class="bg-surface-container-lowest border border-surface-variant rounded-lg px-4 py-2 font-body-base text-body-base text-on-surface focus:outline-none focus:border-primary transition-colors min-w-[200px]" placeholder="Restaurant Name" type="text" />
        <input class="bg-surface-container-lowest border border-surface-variant rounded-lg px-4 py-2 font-body-base text-body-base text-on-surface focus:outline-none focus:border-primary transition-colors min-w-[200px]" placeholder="Address / Location" type="text" />
        <button class="bg-primary text-on-primary font-body-bold px-6 py-2 rounded-lg hover:opacity-90 transition-opacity whitespace-nowrap">Inject Record</button>
      </div>
    </section>
  </div>
</template>
