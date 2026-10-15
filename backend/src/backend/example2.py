## 프로젝트 디렉토리 구조 (FastAPI)

app/            # src/backend
├── main.py
├── core/
│   └── security.py        # 비밀번호 해싱 및 보안 로직
├── db/
│   └── session.py         # DB 세션 연결
├── models/
│   └── user.py            # SQLAlchemy DB 모델
├── schemas/
│   └── user.py            # Pydantic 요청/응답 스키마
├── services/
│   └── user.py            # 비즈니스 로직 처리
└── api/
    └── v1/
        └── endpoints/
            └── auth.py    # Router (요청 처리 및 응답)

## ==============================
# 1. Backend (FastAPI)
# 1) models/user.py (DB 엔티티 정의)
## ============================

from sqlalchemy import Column, BigInteger, String, Boolean, DateTime, func
from db.session import Base

class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    
    # 약관 동의 정보
    terms_of_service = Column(Boolean, default=False, nullable=False)
    privacy_policy = Column(Boolean, default=False, nullable=False)
    marketing_opt_in = Column(Boolean, default=False, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

## ============================
# 2) schemas/user.py (요청/응답 DTO)  
## ============================  

from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class TermsAgreement(BaseModel):
    terms_of_service: bool = Field(..., description="서비스 이용약관 (필수)")
    privacy_policy: bool = Field(..., description="개인정보 처리방침 (필수)")
    marketing_opt_in: bool = Field(False, description="마케팅 정보 수신 (선택)")

class UserCreateRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, description="비밀번호 8자 이상")
    terms: TermsAgreement

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True
## ============================
# 3) core/security.py (비밀번호 암호화)  
## ============================

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)      
## ============================
# 4) services/user.py (비즈니스 로직 & DB CRUD)
## ============================

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status

from models.user import User
from schemas.user import UserCreateRequest
from core.security import hash_password

class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_email(self, email: str) -> User | None:
        result = await self.db.execute(select(User).filter(User.email == email))
        return result.scalars().first()

    async def create_user(self, user_in: UserCreateRequest) -> User:
        # 1. 필수 약관동의 검증
        if not user_in.terms.terms_of_service or not user_in.terms.privacy_policy:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="필수 약관에 동의하셔야 합니다."
            )

        # 2. 이메일 중복 검사
        existing_user = await self.get_user_by_email(user_in.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="이미 가입된 이메일입니다."
            )

        # 3. DB 모델 객체 생성 및 저장
        new_user = User(
            email=user_in.email,
            hashed_password=hash_password(user_in.password),
            terms_of_service=user_in.terms.terms_of_service,
            privacy_policy=user_in.terms.privacy_policy,
            marketing_opt_in=user_in.terms.marketing_opt_in
        )
        
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)
        return new_user
## ============================
# 5) api/v1/endpoints/auth.py (Router)  
## ============================
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_db  # AsyncSession Dependency
from schemas.user import UserCreateRequest, UserResponse
from services.user import UserService

router = APIRouter()

@router.post("/sign-up", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def sign_up(
    user_in: UserCreateRequest,
    db: AsyncSession = Depends(get_db)
):
    user_service = UserService(db)
    created_user = await user_service.create_user(user_in)
    return created_user 


# 2. Frontend (Next.js / React)
# [http://127.0.0.1:8000/api/v1/sign-up]
# (http://127.0.0.1:8000/api/v1/sign-up)으로 요청을 전송하는 프론트엔드 연동 예시 코드입니다.

"use client";

import { useState } from "react";
import axios from "axios";

export default function SignUpPage() {
  const [formData, setFormData] = useState({
    email: "",
    password: "",
    confirmPassword: "",
    terms: {
      terms_of_service: false,
      privacy_policy: false,
      marketing_opt_in: false,
    },
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (formData.password !== formData.confirmPassword) {
      alert("비밀번호가 일치하지 않습니다.");
      return;
    }

    try {
      const response = await axios.post("http://127.0.0.1:8000/api/v1/sign-up", {
        email: formData.email,
        password: formData.password,
        terms: formData.terms,
      });

      alert(`회원가입 성공! (ID: ${response.data.id})`);
    } catch (error: any) {
      console.error(error);
      const errorMessage = error.response?.data?.detail || "회원가입에 실패했습니다.";
      alert(errorMessage);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      {/* 이메일 / 비밀번호 / 약관동의 입력 필드 바인딩 */}
    </form>
  );
}