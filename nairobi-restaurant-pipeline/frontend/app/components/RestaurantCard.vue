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
  <article class="bg-surface-container-lowest border border-surface-variant rounded-lg overflow-hidden flex flex-col hover:border-primary transition-colors cursor-pointer group">
    <div class="h-32 bg-cover bg-center w-full relative" style="background-image: url('https://lh3.googleusercontent.com/aida-public/AB6AXuDztkxZP3P4uD3fVef0ihQIJoCk8n-D90DPgOUBFGiLVeqpIEfSPEKeBjd_D8UodhSR0gCaEO2ClqhzmoFxVK6Q4mjbMxEv4cJUKkxzO8hnpmI5VGgp6x7Hr8-JL2xGnbPrNGGV7LlVzUqAsqgiTF7XiEU42-GdEMe-knCgzk7RN7GSqWofxqpHM80PDNOkue9teQQdic_zxld67LEGFgutlHboQvHtkTIPHNqz4lV4U3X6mbKtcwJTmVvJVGeqNSAvLexcEhSdYfeb')">
      <div class="absolute top-2 right-2 bg-secondary-container text-on-secondary-container font-label-caps text-label-caps px-2 py-1 rounded">{{ restaurant.source || 'OSM' }}</div>
    </div>

    <div class="p-[1.1rem] flex flex-col gap-2">
      <div class="flex justify-between items-start">
        <h3 class="font-headline-md text-[18px] leading-tight text-on-background group-hover:text-primary transition-colors">{{ restaurant.name }}</h3>
        <span class="bg-secondary-fixed-dim text-on-secondary-fixed-variant font-label-caps text-label-caps px-2 py-0.5 rounded-full flex items-center gap-1">
          <span class="material-symbols-outlined" style="font-size: 12px;">check_circle</span> Stable
        </span>
      </div>

      <div class="flex flex-col gap-1 mt-1">
        <div class="font-body-base text-body-base text-on-surface-variant flex items-center gap-2">
          <span class="material-symbols-outlined" style="font-size: 16px;">storefront</span>
          <span>{{ restaurant.address || 'Address pending' }}</span>
        </div>
        <div class="font-label-caps text-label-caps text-on-surface-variant flex items-center gap-2 mt-2">
          <span class="material-symbols-outlined" style="font-size: 14px;">my_location</span>
          {{ restaurant.lat.toFixed(4) }}, {{ restaurant.lng.toFixed(4) }}
        </div>
      </div>

      <div class="mt-3 flex flex-col gap-1">
        <div class="flex justify-between font-label-caps text-label-caps text-on-surface-variant">
          <span>Extraction Confidence</span>
          <span>94%</span>
        </div>
        <div class="h-1.5 w-full bg-surface-container-high rounded-full overflow-hidden">
          <div class="h-full bg-secondary" style="width: 94%;"></div>
        </div>
      </div>
    </div>
  </article>
</template>
