import pg from 'pg'

export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig(event)

  const client = new pg.Client({
    host: config.postgresHost,
    port: Number(config.postgresPort),
    user: config.postgresUser,
    password: config.postgresPassword,
    database: config.postgresDb,
  })

  await client.connect()

  try {
    const { rows } = await client.query(`
      SELECT id, name, city, address, lat, lng, source, created_at
      FROM restaurants
      ORDER BY name
      LIMIT 500
    `)
    return rows
  } finally {
    await client.end()
  }
})