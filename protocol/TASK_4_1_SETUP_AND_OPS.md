# Task 4.1 — Installation, Configuration, and Operations

This document describes how to run the **Semantic Duplication Detection** service locally and in production.

## Components delivered for 4.1

- `backend/semantic_dedupe/` FastAPI service
- PostgreSQL schema with `pgvector`
- Embedding model: `sentence-transformers/all-MiniLM-L6-v2` (384-dim)
- API endpoint to check duplicates: `POST /v1/dedupe/check`
- API endpoint to upsert indexed claims: `POST /v1/dedupe/upsert-claim`
- Backfill script to embed existing claims: `python -m semantic_dedupe.backfill`

## Prereqs

- Python 3.11+ (3.10 works; prefer 3.11)
- PostgreSQL 15+ (14 ok)
- `pgvector` extension installed
- (Optional) Docker + docker-compose

## Environment variables

Create `.env`:

```
DEDUPE_DB_DSN=postgresql+psycopg://user:pass@localhost:5432/verisphere
DEDUPE_BIND=0.0.0.0
DEDUPE_PORT=8080
DEDUPE_MODEL_NAME=sentence-transformers/all-MiniLM-L6-v2
DEDUPE_MAX_TEXT_BYTES=4096
DEDUPE_DEFAULT_TOP_K=10
DEDUPE_DEFAULT_THRESHOLD=0.80
```

## Database setup (pgvector)

1) Install pgvector (example for Ubuntu):
- Use your distro package if available, or build from source.
- Verify in psql:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

2) Apply schema:

```sql
-- See file: backend/semantic_dedupe/sql/001_init.sql
```

## Run locally (venv)

From repo root:

```bash
cd backend/semantic_dedupe
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
uvicorn semantic_dedupe.api:app --host 0.0.0.0 --port 8080
```

## Backfill embeddings

If you already have claims indexed from 3.6, run:

```bash
cd backend/semantic_dedupe
source .venv/bin/activate
python -m semantic_dedupe.backfill --batch-size 256
```

## API usage

### Check duplicates

```bash
curl -s http://localhost:8080/v1/dedupe/check \
  -H 'content-type: application/json' \
  -d '{"text":"Drug X is safe","top_k":10,"threshold":0.8}'
```

### Upsert claim (called by your indexer)

```bash
curl -s http://localhost:8080/v1/dedupe/upsert-claim \
  -H 'content-type: application/json' \
  -d '{"claim_post_id":"123","text":"Drug X is safe","normalized_text":"drug x is safe"}'
```

## Deployment notes

- This service is stateless; scale horizontally.
- Model downloads on first boot; bake into image for faster deploy.
- Put a reverse proxy in front (nginx / cloud LB).
- Apply request rate limits and timeouts.

## Suggested SLOs

- p95 `/check` under 300ms for typical corpora (10k–100k claims) with vector index.
- Error budget: keep 5xx under 0.5%.

## Monitoring

Log:
- request id
- normalized text length
- corpus size
- top match similarity
- latency

Export:
- request counts
- latency histograms
- error rate

## Tuning similarity search

If using `ivfflat`, you may need:
- `lists` during index creation
- `SET ivfflat.probes = ...` per session

If using `hnsw`, tune:
- `m`
- `ef_construction`
- `ef_search`

