# ClimateLens

**Climate Change Data Visualisation Hub** — a web platform to search, explore and forecast open climate data in one place.

Team project for the Information Retrieval course at Riga Technical University (RTU).

## Features

- **Hybrid search**: keyword (full-text) and semantic search over climate reports, ranked by relevance
- **Visualisation**: interactive charts and a world map of climate indicators, from 1880 to today
- **Comparison**: compare countries side by side on any indicator
- **Forecasting**: LSTM-based predictions for the next 10 years

## Tech stack

| Layer | Technologies |
|---|---|
| Frontend | Next.js (TypeScript) |
| Backend | Python, FastAPI |
| Database | PostgreSQL 16 + pgvector |
| ML | PyTorch (LSTM), sentence-transformers |
| DevOps | Docker, GitHub Actions, AWS (EC2, RDS, S3, ECR) |

## Project structure

```
ClimateLens/
├── backend/
│   ├── api/          # FastAPI app: routes and Pydantic schemas
│   ├── database/     # SQLAlchemy models, Alembic migrations, DB connection
│   ├── etl/          # Data pipeline: sources → S3 → PostgreSQL
│   ├── indexation/   # Chunking, full-text index, embeddings
│   ├── search/       # Keyword, semantic and hybrid search
│   └── tools/        # Shared code (config, logging)
├── frontend/         # Next.js web app
├── ml/               # Forecasting models
├── .github/          # CI/CD workflows
└── docker-compose.yaml
```

## Getting started

### Prerequisites

- Docker and Docker Compose
- Git

### Setup

1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd ClimateLens
   ```
2. Create your environment file from the template, then fill in the values:
   ```bash
   cp .env.example .env
   ```
3. Start the database:
   ```bash
   docker compose up -d db
   ```
4. Check that it is running (status should be `healthy`):
   ```bash
   docker compose ps
   ```

### Services

| Service | URL |
|---|---|
| Frontend | http://localhost:3000 |
| API | http://localhost:8080 |
| PostgreSQL | localhost:5432 |

## Contributing

- One branch per feature: `feature/<short-name>`
- Open a pull request to `main`; at least one teammate reviews it before merging
- Never commit `.env` or any secret