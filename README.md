# Personal Inbox

A full-stack personal knowledge inbox for saving web resources, extracting their content, and automatically generating concise summaries and topic tags with Google Gemini.

The application is built with FastAPI, React, PostgreSQL, Docker, Alembic, JWT authentication, background processing, and GitHub Actions CI.

## Features

* Save web resources with a title and URL.
* Automatically fetch and extract webpage content.
* Generate an AI summary and 3–5 topic tags.
* Track resource processing status.
* Preserve extracted content when AI analysis fails.
* Edit and delete saved resources.
* Search saved resources by text.
* Filter saved resources by tag.
* Authenticate users with username/password and JWT access tokens.
* Run the complete application locally with Docker Compose.
* Automatically validate backend, frontend, and database migrations with GitHub Actions.

## Tech Stack

### Backend

* Python 3.10
* FastAPI
* SQLAlchemy
* PostgreSQL 16
* Alembic
* Pydantic
* Pydantic Settings
* JWT authentication
* Google Gemini API

### Frontend

* React
* TypeScript
* Vite
* CSS
* Nginx for the production container

### Infrastructure

* Docker
* Docker Compose
* GitHub Actions

### Architecture

Browser
    |
    v
React + TypeScript
    |
    | HTTP / JSON
    v
FastAPI backend
    |
    +-------------------+-------------------+
    |                   |                   |
    v                   v                   v
Authentication       Item API          Background
+ JWT                + Search           Processing
                                            |
                                +-----------+-----------+
                                |                       |
                                v                       v
                       Webpage extraction        Gemini analysis
                                                        |
                                                 +------+------+
                                                 |             |
                                                 v             v
                                              Summary        Tags


PostgreSQL


The frontend is built as a static React application and served through Nginx.

The FastAPI backend handles authentication, resource management, search, webpage extraction, AI analysis, and database persistence.

## Resource Processing

Saving a resource creates the database record and schedules background processing.


Create resource
      ↓
Store title + URL
      ↓
processing_status = processing
      ↓
Fetch and extract webpage
      ↓
Store extracted content
      ↓
Send content to Gemini
      ↓
Generate structured summary + tags
      ↓
Store analysis
      ↓
processing_status = completed


Processing failures are recorded explicitly.

For extraction failures:


processing_status = failed
processing_error = "Failed to fetch and extract content."


For AI analysis failures:


processing_status = failed
processing_error = "Failed to analyze content."


Extracted content is retained when AI analysis fails.

## AI Analysis

Google Gemini is used to generate a concise summary and 3–5 useful tags from saved webpage content.

The model is configurable through an environment variable:


GEMINI_MODEL=gemini-3.5-flash-lite


The backend requests structured JSON output using the `AIAnalysis` Pydantic schema.

The AI service is tested with mocked Gemini responses, so the automated test suite does not consume Gemini API quota.

## Authentication

The application uses JWT-based authentication.

The authentication flow is:


Username + password
        ↓
POST /auth/login
        ↓
JWT access token
        ↓
Authorization: Bearer <token>
        ↓
Protected API endpoints


User passwords are stored as hashes rather than plaintext values.

## Database

PostgreSQL 16 is used for persistent application data.

The database contains:

* `users`
* `items`

Items store their URL, extracted content, AI-generated summary and tags, processing state, processing errors, and owning user.

## Database Migrations

Alembic manages schema changes.

The current migration chain is:

99106d571ac3
create initial users and items tables
        ↓
0b1b680b0b80
add content
        ↓
5c6c14588067
add processing error
        ↓
2bbc85f58c9d
add user_id
        ↓
142052e2b2d3
add AI summary and tags
        ↓
4a06948bdfb4
add item processing status


The migration chain has been verified against a fresh PostgreSQL database from an empty schema through the current Alembic head.

## Local Development

### Prerequisites

* Docker Desktop
* Git
* Python 3.10+
* Node.js 22+
* npm

### Environment variables

Create a `.env` file in the repository root.

Example:

DATABASE_URL=postgresql://postgres:postgres@127.0.0.1:5433/personal_inbox
JWT_SECRET=replace-with-a-long-random-secret
GEMINI_API_KEY=your-gemini-api-key
GEMINI_MODEL=gemini-3.5-flash-lite

Never commit real credentials or API keys.

### Run with Docker Compose

From the repository root:

docker compose up --build


The local services are available at:


Frontend: http://localhost:5173
Backend:  http://localhost:8000
Swagger:  http://localhost:8000/docs


PostgreSQL is exposed locally on port `5433`.

### Stop the application

docker compose down

## Backend Development

Install the Python dependencies:

pip install -r requirements.txt

Run the backend test suite:

python -m pytest -q

Run database migrations:

alembic upgrade head

Check for migration drift:

alembic check

## Frontend Development

From the `frontend` directory:

npm install
npm run dev

Run linting:

npm run lint

Build the production frontend:

npm run build


## Docker

The repository contains separate Docker configurations for the backend and frontend.

### Backend

The backend container:

* installs Python dependencies;
* runs `alembic upgrade head` when the container starts;
* starts FastAPI with Uvicorn.

### Frontend

The frontend container:

* installs frontend dependencies;
* builds the React application;
* serves the production build through Nginx.

### Compose

Docker Compose orchestrates:

PostgreSQL
    +
FastAPI backend
    +
React frontend

## Testing and CI

GitHub Actions runs automatically on pushes and pull requests targeting `main`.

### Backend CI

The backend job:

1. Starts PostgreSQL 16.
2. Installs Python dependencies.
3. Applies all Alembic migrations.
4. Runs the backend test suite.
5. Runs `alembic check`.

### Frontend CI

The frontend job:

1. Installs Node.js dependencies.
2. Runs ESLint.
3. Builds the production frontend.

Gemini is not called by CI. AI tests use mocked responses.

The current backend test suite contains 50 tests, and the latest CI run passed both backend and frontend jobs.

## Project Structure

personal-inbox/
├── .github/
│   └── workflows/
│       └── ci.yml
├── alembic/
│   ├── versions/
│   └── env.py
├── app/
│   ├── repositories/
│   ├── routers/
│   ├── schemas/
│   ├── services/
│   ├── config.py
│   ├── dependencies.py
│   ├── main.py
│   └── models.py
├── frontend/
│   ├── public/
│   ├── src/
│   ├── Dockerfile
│   └── package.json
├── .dockerignore
├── Dockerfile
├── compose.yaml
├── requirements.txt
└── README.md

## API

The FastAPI backend provides endpoints for:

* user registration;
* user login;
* listing saved resources;
* creating resources;
* retrieving individual resources;
* updating resources;
* deleting resources;
* triggering resource processing;
* searching resources by text;
* filtering resources by tag.

Interactive API documentation is available at:

http://localhost:8000/docs

## Error Handling

Resource processing distinguishes between content extraction and AI analysis failures.

This allows the application to preserve useful extracted data even when external AI processing is unavailable.

The processing state can be:

pending
processing
completed
failed

Processing errors are stored on the item for visibility and debugging.

## Security

Do not commit:

* `.env` files
* Gemini API keys
* JWT secrets
* database passwords
* local database backups

Production credentials should be provided through environment variables or the hosting provider's secret-management system.

## Status

The application currently includes:

* Full-stack React + FastAPI application
* JWT authentication
* PostgreSQL persistence
* Alembic migrations
* Web content extraction
* Gemini-powered summaries and tags
* Background item processing
* Search and tag filtering
* Dockerized local environment
* GitHub Actions CI
* Automated backend and frontend validation

The next step is deployment of the application and managed PostgreSQL database.

## License

This project does not currently specify an open-source license.
