# Personal Inbox

A full-stack personal knowledge inbox for saving web resources, extracting their content, and automatically generating summaries and topic tags with Google Gemini. Built with FastAPI, React, and PostgreSQL, featuring JWT authentication, database migrations, background processing, automated tests, and Docker support.

## Features

- User registration and login with JWT authentication
- Save web resources by title and URL
- Automatic webpage content extraction
- AI-generated summary and 3–5 topic tags (Google Gemini)
- Resource processing status tracking (pending / processing / completed / failed)
- Search by text and filter by tag
- Edit and delete saved resources
- PostgreSQL database with Alembic migrations
- Pytest backend test suite with 50 passing tests
- Docker and Docker Compose setup
- GitHub Actions CI (backend, frontend, and migration checks)
- Swagger / OpenAPI interactive documentation

## Tech Stack

**Backend:** Python 3.10, FastAPI, SQLAlchemy, Alembic, Pydantic, JWT, Google Gemini API

**Frontend:** React, TypeScript, Vite

**Infrastructure:** PostgreSQL 16, Docker / Docker Compose, GitHub Actions, Nginx (production build)


## Project Structure

```
app/
├── repositories/  # Database operations
├── routers/       # API endpoints
├── schemas/       # Request/response schemas
├── services/       # Application logic
├── config.py
├── dependencies.py
└── main.py         # Application entry point

frontend/           # React + TypeScript app
alembic/            # Database migrations
.github/workflows/  # CI pipeline
Dockerfile
compose.yaml
requirements.txt
```

## Local Setup

```bash
# clone and set up environment
git clone https://github.com/knasstya/personal-inbox.git
cd personal-inbox
cp .env.example .env   # add DATABASE_URL, JWT_SECRET, GEMINI_API_KEY

# run with Docker Compose
docker compose up --build
```

- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- Swagger UI: http://localhost:8000/docs

## Testing & CI

GitHub Actions runs on every push and pull request to `main`, applying Alembic migrations, running the 50-test backend suite, linting and building the frontend. Gemini is not called in CI — AI logic is tested with mocked responses.

## Status

Not deployed yet due to free-tier infrastructure limits. Deployment is the next planned step.
