# Nairobi Restaurant Discovery - Data Pipeline

## Project Overview
This project is a highly scalable, automated data pipeline designed to discover, acquire, process, and serve restaurant metadata, menus, and high-quality imagery for Nairobi, Kenya. 

Initiated as a zero-budget project, the system relies entirely on free-tier APIs, local machine learning models, and serverless infrastructure to aggregate data for up to 3,000 restaurants. The final product is a production-ready application with operational costs of exactly $0.00 per month.

---

## System Architecture

The pipeline functions as a continuous content discovery engine divided into five distinct layers, orchestrated safely in the background.

* **Discovery Layer:** Aggregates base restaurant metadata (ID, name, location) using the free tiers of the Google Places API and OpenStreetMap Overpass API.
* **Acquisition Layer:** Ethically scrapes targeted restaurant websites for menu PDFs and standard images using Puppeteer, incorporating strict rate-limit delays to avoid IP bans.
* **Processing & Enrichment Layer:** Utilises local YOLO models to classify food images and executes Tesseract.js for offline OCR on extracted menus. Missing images are enriched by querying OpenFoodFacts and Unsplash APIs.
* **Storage Layer:** Stores structured relational data in Supabase utilising PostgreSQL, while offloading all heavy media assets directly to Cloudinary.
* **Serving Layer:** Exposes the cleaned data via Supabase's auto-generated REST API to a Next.js frontend application hosted on Vercel.
* **Orchestration:** The entire workflow is managed by Apache Airflow using Directed Acyclic Graphs (DAGs) to enforce explicit execution order and ensure pipeline resilience. All tasks utilise UPSERT logic for idempotency.

---

## Technology Stack

| Category | Tool | Purpose |
| :--- | :--- | :--- |
| **Orchestration** | Apache Airflow | DAG-based scheduling & idempotency. |
| **Acquisition** | Node.js / Puppeteer | Scraping & data extraction. |
| **Enrichment** | YOLO / Tesseract | Local AI vision & OCR sidecar service. |
| **Database** | PostgreSQL | Relational storage. |
| **Frontend** | Nuxt 4 / Vue 3 | Public interface & UI. |

---

## Getting Started (Local Development)

### 1. Prerequisites
Ensure you have the following installed on your machine:
* Docker & Docker Compose
* Node.js (v18+)
* Python (3.10+)
* Git

### 2. Environment Configuration
Create a `.env` file in the root directory and populate it with your local database credentials and API keys:

```env
# Database Configuration
POSTGRES_USER=nairobi_admin
POSTGRES_PASSWORD=your_secure_password
POSTGRES_DB=restaurant_discovery
POSTGRES_PORT=5432

# API Keys (Add as you progress)
GOOGLE_PLACES_KEY=your_key
UNSPLASH_ACCESS_KEY=your_key


### Local Infrastructure
The system uses a custom Docker bridge network to shield the database.
```bash
# Initialize the 3-tier architecture
docker compose up -d
