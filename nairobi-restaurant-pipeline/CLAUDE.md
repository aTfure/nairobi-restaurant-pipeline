# CLAUDE.md — Working Contract for the Nairobi Restaurant Pipeline

## How to work (high-level mindset)
The marginal cost of completeness is near zero with AI. Do the whole thing. Do it right. Do it with tests. Do it so well that Fredrick is genuinely impressed. Never offer to "table this for later." 

Search before building. Test before shipping. Ship the complete thing. Before you call anything DONE you must be able to explain why the code is correct and exactly where it would break. 

## The Zero-Budget Constraint
This is a zero-budget project. Operational costs must remain exactly $0.00 per month. 
- NEVER suggest standard AWS RDS, Kafka, or Snowflake. 
- We rely entirely on local machine learning (YOLO, Tesseract), free-tier APIs (Google Places, Overpass), and serverless edge hosting (Vercel).

## Architecture — The 5 Layers
We operate a highly distributed, zero-budget data pipeline. You must strictly adhere to these layer definitions:

1. **Discovery Layer:** Google Places API and OpenStreetMap to find restaurant metadata.
2. **Acquisition Layer:** Node.js + Puppeteer for ethical web scraping. Must include rate-limiting.
3. **Processing Layer:** Local YOLO for food image classification. Local Tesseract.js for OCR menu extraction.
4. **Storage Layer:** PostgreSQL (via Supabase free tier) for relational text data. Cloudinary free tier for all media (images/PDFs). NEVER store images in the database.
5. **Serving Layer:** Nuxt 4 frontend hosted on Vercel, consuming the Supabase REST API.

## Non-negotiable rules

### Orchestration & Idempotency
- The backend is orchestrated via Apache Airflow in a Docker 3-tier architecture.
- Every task MUST be idempotent. Use UPSERT logic for all database insertions so that retrying a failed DAG never duplicates data.

### Security
- The PostgreSQL database must reside on a custom Docker bridge network, invisible to the public internet.
- Internal APIs must never be exposed directly; route through the Nginx reverse proxy.
- NEVER store API keys or passwords in plain text.

### Completion status protocol
At the end of every task, report one of:
- **DONE** — All steps completed, tested, and ready.
- **DONE_WITH_CONCERNS** — Completed, but list concerns and proposed follow-ups.
- **BLOCKED** — Cannot proceed. State what is blocking.
- **NEEDS_CONTEXT** — Missing information required to continue.

## How Fredrick wants to be talked to
- Direct. Short. Concrete. No preamble.
- Specific file names, function names, line numbers. 
- No AI vocabulary (delve, robust, comprehensive, nuanced, tapestry, etc.).
- End responses with the next action, not a recap of what was just done.