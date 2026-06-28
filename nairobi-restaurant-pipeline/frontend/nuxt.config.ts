export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: false },
  runtimeConfig: {
    postgresHost: process.env.POSTGRES_HOST || 'localhost',
    postgresPort: process.env.POSTGRES_PORT || '5432',
    postgresUser: process.env.POSTGRES_USER || 'nairobi_admin',
    postgresPassword: process.env.POSTGRES_PASSWORD || 'local_dev_password_123',
    postgresDb: process.env.POSTGRES_DB || 'nairobi_pipeline',
  }
})