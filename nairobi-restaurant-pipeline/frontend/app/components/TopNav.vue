<template>
  <header class="bg-surface w-full h-16 border-b border-surface-variant flex justify-between items-center px-margin-desktop sticky top-0 z-10">
    <div class="flex items-center gap-8 flex-1">
      <span class="font-display-lg text-display-lg text-primary" style="font-size: 24px; line-height: 1;">GastroData</span>
      <div class="relative max-w-md w-full ml-4">
        <span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-on-surface-variant">search</span>
        <input class="w-full bg-surface-container-lowest border border-surface-variant rounded-full py-2 pl-10 pr-4 font-body-base text-body-base text-on-surface focus:outline-none focus:border-primary transition-colors" placeholder="Search by name or address..." type="text" />
      </div>
    </div>

    <nav class="flex items-center gap-6 hidden lg:flex">
      <a class="text-on-surface-variant font-body-base hover:bg-surface-container-low transition-colors px-2 py-1 rounded" href="#">Dashboard</a>
      <a class="text-on-surface-variant font-body-base hover:bg-surface-container-low transition-colors px-2 py-1 rounded" href="#">Metrics</a>
    </nav>

    <div class="flex items-center gap-4 ml-8">
      <span class="material-symbols-outlined text-on-surface-variant cursor-pointer active:scale-95 transition-transform">notifications</span>
      <span class="material-symbols-outlined text-on-surface-variant cursor-pointer active:scale-95 transition-transform">settings</span>
      <button class="text-on-surface-variant font-body-bold px-3 py-1.5 border border-surface-variant rounded-lg hover:bg-surface-container-low transition-colors">Export</button>
      <button class="bg-primary text-on-primary font-body-bold px-4 py-1.5 rounded-lg active:scale-95 transition-transform">Execute Pipeline</button>
      <img alt="User Avatar" class="w-8 h-8 rounded-full object-cover border border-surface-variant ml-2" src="https://lh3.googleusercontent.com/aida-public/AB6AXuD1RNrPsBhuzNul-4ERabPrTd1RuPoQjAXZBYdgTHHYIunSe090wZ36O9UWG5lQRP_wx_zWrZwaHF4HdX9z4YaMysE9Y5QDhtdX02RHn4RO1_jzuHUBNq_OXqcfGKdSZN9A74drVjXZpbovAVSD4jcIdCG4pZxE5DQfKZw5axjOSbY4-G2oa37B_CzuwQigX4atYbR3M3OThhQUA_wsxMxIlc8oVozbhPNwAIhyJ7u3yX3bnJoZDfR7wdSw5vHFebaTkDtwsbu_yn_n" />
    </div>
  </header>
</template>
