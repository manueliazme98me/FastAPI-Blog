# FastAPI Blog

A modern blog platform built with FastAPI, SQLAlchemy, and PostgreSQL. The application combines a REST API with server-rendered HTML pages, allowing users to register, authenticate, publish posts, manage profiles, and reset passwords securely.

## Overview

This project is designed as a full-stack blog application with a clean separation between API routes, templates, and backend services. It provides both developer-friendly API endpoints and a user-facing web experience powered by Jinja2 templates.

Key capabilities include:

- User registration and authentication
- JWT-based access control
- Blog post creation, listing, updating, and deletion
- User-specific post pages
- Password reset flow with email delivery
- Profile image handling and media serving
- Structured configuration using environment variables
- Async SQLAlchemy database access

## Tech Stack

- Python 3.14+
- FastAPI
- SQLAlchemy 2 async ORM
- PostgreSQL
- Pydantic + Pydantic Settings
- Jinja2 templates
- JWT authentication
- Alembic migrations
- Pillow for image processing

## Project Structure

```text
.
├── alembic/                  # Database migration files
├── media/                   # Uploaded media and profile image storage
├── routers/                 # API route modules
├── src/fastapi_blog/        # Package entry point
├── static/                  # CSS, JS, and static assets
├── templates/               # HTML templates for the frontend
├── tests/                   # Application import and route checks
├── .env                     # Local environment configuration
├── alembic.ini              # Alembic configuration
├── auth.py                  # Authentication and token helpers
├── config.py                # Application settings
├── database.py              # Database engine/session setup
├── email_utils.py           # Mail delivery helpers
├── image_utils.py           # Image resizing and validation
├── main.py                  # FastAPI application entry point
├── models.py                # SQLAlchemy models
├── schemas.py               # Pydantic request/response schemas
├── pyproject.toml           # Dependency and project metadata
├── README.md                # Project documentation
└── populate_db.py           # Seed or sample data utilities
```

## Features

### Authentication

- Secure user registration with validation
- Login via email and password
- JWT access token generation
- Protected routes for authenticated users
- Password change and reset workflows

### Blog functionality

- Create, read, update, and delete posts
- Paginated post listing
- User-specific post views
- Author ownership checks for modification operations

### Media and UI

- Profile image upload processing
- Static file serving for media and frontend assets
- Jinja templates for page rendering
- Responsive front-end styling and utilities

## Prerequisites

Before starting, make sure you have:

- Python 3.14 or newer
- PostgreSQL database running locally or remotely
- A mail provider or SMTP testing service such as Mailtrap for password reset emails
- Optional: `uv` for dependency management

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/manueliazme98me/FastAPI-Blog.git
cd FastAPI-Blog
```

### 2. Configure environment variables

Create a `.env` file in the project root with the following values:

```env
DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/fastapi_blog
SECRET_KEY=change-me-to-a-long-random-secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
POSTS_PER_PAGE=5
RESET_TOKEN_EXPIRE_MINUTES=60
MAIL_SERVER=sandbox.smtp.mailtrap.io
MAIL_PORT=2525
MAIL_USERNAME=your-mailtrap-username
MAIL_PASSWORD=your-mailtrap-password
MAIL_FROM=noreply@yourdomain.com
MAIL_USE_TLS=true
FRONTEND_URL=http://localhost:8000
```

> Keep your `.env` file private and never commit credentials to version control.

### 3. Install dependencies

Using `uv` (recommended):

```bash
uv sync
```

Or using `pip`:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .
```

### 4. Run the application

Development mode:

```bash
uv run fastapi dev main.py
```

Or with Uvicorn directly:

```bash
uv run uvicorn main:app --reload
```

The application will be available at:

- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Database Setup

This project uses Alembic for schema management. To initialize or apply migrations:

```bash
uv run alembic upgrade head
```

If you are working on a fresh database, make sure the `DATABASE_URL` points to a valid PostgreSQL instance before running migrations.

## Running Tests

```bash
pytest
```

The current test suite checks that the application loads correctly and that key page routes are registered.

## API Highlights

The app exposes two major route groups:

- `/api/users` for authentication, profile actions, and user-related data
- `/api/posts` for post listing, creation, and author-controlled updates

Authentication endpoints include:

- `POST /api/users/token` for login
- `GET /api/users/me` for the current authenticated user
- `POST /api/users/forgot-password`
- `POST /api/users/reset-password`

## Security Notes

- Password hashes are generated with a secure password hashing strategy.
- JWT tokens are used for session authentication.
- Sensitive configuration is loaded from environment variables.
- Security headers are applied in the application middleware.

## Contributing

Contributions are welcome. If you plan to extend the project, please keep the code organized, document new features clearly, and validate any behavior with tests before submitting a pull request.

## License

This project does not currently declare a license file. If you are using it in a public or production environment, confirm the licensing terms before deployment or redistribution.
