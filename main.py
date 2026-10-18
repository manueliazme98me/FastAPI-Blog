from contextlib import asynccontextmanager
from typing import Annotated

from fastapi.exception_handlers import (
    http_exception_handler, 
    request_validation_exception_handler
)

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette.exceptions import HTTPException as StarletteHTTPException

import models
from database import Base, engine, get_db
from routers import posts, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create the database tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Drop the database tables (optional, for testing purposes)
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)
    
    await engine.dispose()
    
    

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.mount("/media", StaticFiles(directory="media"), name="media")

templates = Jinja2Templates(directory="templates")

app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(posts.router, prefix="/api/posts", tags=["Posts"])

@app.get("/", include_in_schema=False, name="home")
@app.get("/posts", include_in_schema=False, name="posts")
async def home(request: Request, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(
        select(models.Post)
        .options(selectinload(models.Post.author))
        .order_by(models.Post.date_posted.desc())
    )
    posts = result.scalars().all()
    
    return templates.TemplateResponse(
        request, 
        "home.html",
        {"posts": posts, "title": "Home"}
    )


@app.exception_handler(StarletteHTTPException)
async def general_http_exception_handler(request: Request, exception: StarletteHTTPException):
    message = (
        exception.detail 
        if exception.detail 
        else "An error occurred."
    )
    
    if request.url.path.startswith("/api"):
        return await http_exception_handler(request, exception)
    
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": exception.status_code, 
            "title": exception.status_code,
            "message": message
        },
        status_code=exception.status_code
    )
    
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exception: RequestValidationError):  
    if request.url.path.startswith("/api"):
        return await request_validation_exception_handler(request, exception)

    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT, 
            "title": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "message": "Invalid request data. Please check your input and try again."
        },
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT
    )