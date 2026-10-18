from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

import models
from database import get_db
from schemas import PostResponse, UserResponse, UserCreate, UserUpdate

router = APIRouter()
templates = Jinja2Templates(directory="templates")



@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_user(user: UserCreate, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(
        select(models.User).where(models.User.username == user.username)
    )
    existing_user = result.scalars().first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists."
        )
    
    result = await db.execute(
        select(models.User).where(models.User.email == user.email)
    )
    existing_email = result.scalars().first()
    
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists."
        )
        
    new_user = models.User(
        username=user.username,
        email=user.email,
        image_file=user.image_file
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(
        select(models.User).where(models.User.id == user_id)
    )
    user = result.scalars().first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )
    
    return user


@router.get("/{user_id}/posts", include_in_schema=False, name="user_posts")
async def user_posts_page(
    request: Request,
    user_id: int,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    result = await db.execute(
        select(models.User).where(models.User.id == user_id)
    )
    user = result.scalars().first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )

    # count_result = await db.execute(
    #     select(func.count())
    #     .where(models.Post.user_id == user_id)
    # )
    # total = count_result.scalar() or 0
    
    result = await db.execute(
        select(models.Post)
        .options(selectinload(models.Post.author))
        .where(models.Post.user_id == user_id)
        .order_by(models.Post.date_posted.desc())
    )
    posts = result.scalars().all()

    if not posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No posts found for this user."
        )
    
    return templates.TemplateResponse(
        request, 
        "user_posts.html", 
        {
            "posts": posts, 
            "user": user, 
            "title": f"{user.username}'s Posts"
        }
    )


@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user_update: UserUpdate, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(
        select(models.User).where(models.User.id == user_id)
    )
    user = result.scalars().first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )
    
    if user_update.username and user_update.username != user.username:
        result = await db.execute(
            select(models.User).where(models.User.username == user_update.username)
        )
        existing_user = result.scalars().first()
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists."
            )
            
    if user_update.email is not None and user_update.email != user.email:
        result = await db.execute(
            select(models.User).where(models.User.email == user_update.email)
        )
        existing_email = result.scalars().first()
        
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists."
            )
    
    if user_update.username is not None:
        user.username = user_update.username
    if user_update.email is not None:   
        user.email = user_update.email
    if user_update.image_file is not None:
        user.image_file = user_update.image_file
    
    db.commit() 
    db.refresh(user)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(
        select(models.User).where(models.User.id == user_id)
    )
    user = result.scalars().first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )

    db.delete(user)
    db.commit()
    
  