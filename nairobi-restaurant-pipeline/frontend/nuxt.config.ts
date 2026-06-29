export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: false },
  css: ['~/assets/css/main.css'],
  vite: {
    plugins: [
      (await import('@tailwindcss/vite')).default(),
    ],
  },
  app: {
    head: {
      link: [
        {
          rel: 'preconnect',
          href: 'https://fonts.googleapis.com',
        },
        {
          rel: 'preconnect',
          href: 'https://fonts.gstatic.com',
          crossorigin: '',
        },
        {
          rel: 'stylesheet',
          href: 'https://fonts.googleapis.com/css2?family=Epilogue:wght@600;700&family=IBM+Plex+Mono:wght@700&family=IBM+Plex+Sans:wght@400;600;700&display=swap',
        },
        {
          rel: 'stylesheet',
          href: 'https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap',
        },
      ],
      style: [
        {
          children: "body { font-family: 'IBM Plex Sans', sans-serif; }",
        },
      ],
    },
  },
  runtimeConfig: {
    postgresHost: process.env.POSTGRES_HOST || 'localhost',
    postgresPort: process.env.POSTGRES_PORT || '5432',
    postgresUser: process.env.POSTGRES_USER || 'nairobi_admin',
    postgresPassword: process.env.POSTGRES_PASSWORD || 'local_dev_password_123',
    postgresDb: process.env.POSTGRES_DB || 'nairobi_pipeline',
  },
})