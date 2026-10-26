# FastAPI Blog

A full-stack blog application built with FastAPI, SQLAlchemy, PostgreSQL, and Jinja2 templates. The project combines a modern REST API with server-rendered HTML pages, giving users a streamlined way to register, authenticate, create posts, reset passwords, and manage profile content in one application.

## Overview

This project is designed for a production-style blog workflow with a clean separation between backend logic, database models, API routes, and UI templates. It supports both machine-readable API consumption and a traditional web experience for end users.

The application includes:

- User registration and authentication
- JWT-based access control
- Blog post creation, listing, and editing
- Author-oriented post management
- Password reset via email
- Profile image upload and storage
- Secure configuration via environment variables
- Async database access using SQLAlchemy

## Tech Stack

- Python 3.14+
- FastAPI
- SQLAlchemy 2 async ORM
- PostgreSQL
- Pydantic + Pydantic Settings
- Jinja2 templates
- JWT authentication
- Alembic migration tooling
- Pillow for image processing
- Uvicorn / FastAPI development server

## Architecture

The application follows a simple layered structure:

- `main.py` initializes the FastAPI application and route registration
- `routers/` contains user and post endpoints
- `models.py` defines the database schema
- `schemas.py` contains request and response models
- `database.py` manages async database sessions
- `auth.py` handles token creation and user identity checks
- `templates/` renders browser-facing pages
- `static/` serves CSS, JavaScript, and other front-end assets
- `media/` stores uploaded user media such as profile photos

## Project Structure

```text
.
├── alembic/                  # Database migration history and configuration
├── media/                   # Uploaded media and profile images
├── routers/                 # API and page route modules
├── static/                  # Front-end assets (CSS, JS, images)
├── templates/               # Jinja2 HTML templates for the blog UI
├── tests/                   # Basic smoke tests
├── .env                     # Local environment variables
├── alembic.ini              # Alembic config
├── auth.py                  # JWT and auth helpers
├── config.py                # Application settings loaded from environment
├── database.py              # Async engine and session provider
├── Dockerfile               # Container build configuration
├── email_utils.py           # Email delivery utilities
├── image_utils.py           # Profile image validation and processing
├── main.py                  # FastAPI application entry point
├── models.py                # SQLAlchemy models
├── populate_db.py           # Seed/sample data script
├── pyproject.toml           # Project dependencies and metadata
├── README.md                # Project documentation
├── schemas.py               # Pydantic model definitions
└── src/fastapi_blog/        # package namespace for the project
```

## Features

### Authentication and user management

- Email-based user registration
- Login flow with secure password verification
- JWT access token issuance
- Authenticated access checks for protected endpoints
- Password reset and change workflows
- Users can view and manage profile-related content

### Blog functionality

- Create new blog posts
- Browse post lists in the home view
- Open individual post pages
- Display posts by author
- Restrict updates/deletes to the post owner
- Pagination support for large collections

### Media and UI

- Profile image uploads with resizing and validation
- Static asset delivery for CSS, JS, and media
- Jinja2 templates for server-rendered pages
- Responsive browser user interface
- Security headers applied at the application middleware layer

## Prerequisites

Before running the application, ensure the following are available:

- Python 3.14 or newer
- PostgreSQL database instance
- SMTP-capable mail service or local testing provider such as Mailtrap
- Optional: `uv` for dependency and environment management

## Local Development Setup

### 1. Clone the repository

```bash
git clone https://github.com/manueliazme98me/FastAPI-Blog.git
cd FastAPI-Blog
```

### 2. Create environment variables

Create a `.env` file in the project root with the values required by `config.py`:

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

> Keep the `.env` file private and never commit secrets to version control.

### 3. Install dependencies

Using `uv` (recommended):

```bash
uv sync
```

Or using `pip`:

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -e .
```

### 4. Run the application

Start the development server:

```bash
uv run fastapi dev main.py
```

Alternatively, run it with Uvicorn directly:

```bash
uv run uvicorn main:app --reload
```

The app becomes available at:

- Application: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Database Setup and Migrations

This project uses Alembic for schema management and database evolution.

Apply the migrations to a configured PostgreSQL database:

```bash
uv run alembic upgrade head
```

If you are starting from a blank database, confirm that `DATABASE_URL` points to the correct PostgreSQL instance before running migrations.

## Docker Deployment

A Dockerfile is included for containerized deployment. It builds the application with `uv` and runs it with FastAPI on port 8080 by default.

Build the image:

```bash
docker build -t fastapi-blog .
```

Run the container:

```bash
docker run -p 8080:8080 --env-file .env fastapi-blog
```

## API Overview

The backend exposes two main route groups:

- `/api/users` for authentication, profile operations, and user data
- `/api/posts` for creating and reading blog content

### Core user endpoints

- `POST /api/users` — register a new user
- `POST /api/users/token` — authenticate and obtain a JWT
- `GET /api/users/me` — fetch the current authenticated user
- `POST /api/users/forgot-password` — request a password reset email
- `POST /api/users/reset-password` — complete password reset using a token
- `GET /api/users/{user_id}` — fetch public user data
- `GET /api/users/{user_id}/posts` — list posts for a specific user

### Core post endpoints

- `GET /api/posts` — list posts
- `POST /api/posts` — create a post
- `GET /api/posts/{post_id}` — fetch a specific post
- `PUT /api/posts/{post_id}` — update a post
- `DELETE /api/posts/{post_id}` — delete a post

## Security Notes

- Password hashes are generated with a secure hashing strategy.
- JWTs are used for authenticated access.
- Sensitive settings are kept in environment variables rather than hard-coded values.
- Security headers are added at the HTTP middleware layer.
- Uploaded profile images are processed to reduce risk and enforce size constraints.

## Testing

Run the test suite with:

```bash
pytest
```

The current tests validate that the app loads correctly and that the primary routes are registered as expected.

## Contributing

Contributions are welcome. To maintain quality and consistency:

1. Keep the code modular and readable.
2. Add or update tests for changed behavior.
3. Document new endpoints or configuration values.
4. Validate the project before opening a pull request.

## License

This repository does not currently include a license file. If you intend to use or distribute the project publicly, confirm the licensing terms before deployment or redistribution.
