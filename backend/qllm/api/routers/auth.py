from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from qllm.api.deps import get_db
from qllm.api.middlewares.jwt import (
    create_access_token,
    get_current_active_user,
    get_password_hash,
    verify_password,
)
from qllm.api.schemas.auth import Token, User, UserCreate, UserLogin
from qllm.core.config import settings

from ...models.model import User as UserModel

router = auth_router = APIRouter()


@router.post("/signup", response_model=User)
async def signup(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    # Kiểm tra email đã tồn tại
    result = await db.execute(
        select(UserModel).where(UserModel.email == user_data.email)
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    # Tạo user mới
    password_hash = get_password_hash(user_data.password)
    db_user = UserModel(
        email=user_data.email,
        password_hash=password_hash,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


@router.post("/login", response_model=Token)
async def login(user_data: UserLogin, db: AsyncSession = Depends(get_db)):
    # Tìm user bằng email
    result = await db.execute(
        select(UserModel).where(UserModel.email == user_data.email)
    )
    user = result.scalar_one_or_none()

    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email hoặc mật khẩu không chính xác",
        )

    # Tạo access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# @router.post("/login/email", response_model=Token)
# async def login_with_email(
#     user_data: UserLogin,
#     db: AsyncSession = Depends(get_db)
# ):
#     # Tìm user bằng email
#     result = await db.execute(
#         select(UserModel).where(UserModel.email == user_data.email)
#     )
#     user = result.scalar_one_or_none()

#     if not user or not verify_password(user_data.password, user.password_hash):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Email hoặc mật khẩu không chính xác",
#             headers={"WWW-Authenticate": "Bearer"},
#         )

#     # Tạo access token
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.email}, expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("Authorization")
    return {"message": "Successfully logged out"}


@router.get("/users/me", response_model=User)
async def read_users_me(
    current_user: Annotated[UserModel, Depends(get_current_active_user)]
):
    return current_user
