<template>
  <div class="min-h-screen bg-background text-on-background flex">
    <Sidebar />

    <div class="ml-64 flex-1 flex flex-col">
      <TopNav />
      <main class="p-margin-desktop flex-1 flex flex-col gap-stack-lg max-w-7xl mx-auto w-full">
        <slot />
      </main>
    </div>
  </div>
</template>
