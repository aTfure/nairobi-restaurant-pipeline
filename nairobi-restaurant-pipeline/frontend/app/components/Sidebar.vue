<template>
  <aside class="bg-surface-container-lowest w-64 h-full fixed left-0 top-0 border-r border-surface-variant flex flex-col py-stack-lg gap-stack-md z-20">
    <div class="px-4 mb-4">
      <h1 class="font-headline-md text-headline-md text-on-surface">Technical Gastronomy</h1>
      <p class="font-label-caps text-label-caps text-on-surface-variant mt-1">Extraction Engine v2.4</p>
    </div>

    <nav class="flex-1 flex flex-col gap-1 px-2">
      <a class="bg-secondary-container text-on-secondary-container font-body-bold rounded-lg px-4 py-3 flex items-center gap-3 transition-colors" href="#">
        <span class="material-symbols-outlined">restaurant</span>
        Portfolio
      </a>
      <a class="text-on-surface-variant font-body-base px-4 py-3 flex items-center gap-3 hover:bg-surface-container-high transition-colors rounded-lg" href="#">
        <span class="material-symbols-outlined">analytics</span>
        Health
      </a>
      <a class="text-on-surface-variant font-body-base px-4 py-3 flex items-center gap-3 hover:bg-surface-container-high transition-colors rounded-lg" href="#">
        <span class="material-symbols-outlined">database</span>
        Logs
      </a>
    </nav>

    <div class="px-4 mt-auto">
      <button class="w-full bg-primary text-on-primary font-body-bold rounded-lg py-3 flex justify-center items-center gap-2 hover:opacity-90 transition-opacity">
        <span class="material-symbols-outlined">add</span>
        New Pipeline
      </button>
    </div>

    <div class="px-2 border-t border-surface-variant pt-4 mt-4">
      <a class="text-on-surface-variant font-body-base px-4 py-2 flex items-center gap-3 hover:bg-surface-container-high transition-colors rounded-lg" href="#">
        <span class="material-symbols-outlined">menu_book</span>
        Documentation
      </a>
      <a class="text-on-surface-variant font-body-base px-4 py-2 flex items-center gap-3 hover:bg-surface-container-high transition-colors rounded-lg" href="#">
        <span class="material-symbols-outlined">contact_support</span>
        Support
      </a>
    </div>
  </aside>
</template>
