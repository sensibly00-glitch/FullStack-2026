# schema
from pydantic import BaseModel, EmailStr, Field

class TermsAgreement(BaseModel):
    terms_of_service: bool = Field(..., description="서비스 이용약관 동의 (필수)")
    privacy_policy: bool = Field(..., description="개인정보 처리방침 동의 (필수)")
    marketing_opt_in: bool = False  # 마케팅 정보 수신 동의 (선택)

class SignUpRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, description="비밀번호 (8자 이상)")
    terms: TermsAgreement

class SignUpResponse(BaseModel):
    message: str
    email: EmailStr

    ## main.py ======================================================               

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from schemas import SignUpRequest, SignUpResponse

app = FastAPI()

# Next.js 프론트엔드와의 통신을 위한 CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js 기본 포트
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/v1/sign-up", response_model=SignUpResponse, status_code=status.HTTP_201_CREATED)
async def sign_up(request: SignUpRequest):
    # 1. 필수 약관 동의 검증
    if not request.terms.terms_of_service or not request.terms.privacy_policy:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="필수 약관에 동의해야 합니다."
        )

    # 2. 비밀번호 암호화 및 DB 저장 로직 수행 (예: passlib, SQLAlchemy 등 활용)
    # hashed_password = hash_password(request.password)
    # db.save_user(email=request.email, password=hashed_password, terms=request.terms)

    return SignUpResponse(
        message="회원가입이 완료되었습니다.",
        email=request.email
    )

## ===========    2. Next.js (React) 프론트엔드 API 호출 예시

import { useState } from 'react';
import axios from 'axios';

export default function SignUpForm() {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: '',
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
      const response = await axios.post('http://127.0.0.1:8000/api/v1/sign-up', {
        email: formData.email,
        password: formData.password,
        terms: formData.terms,
      });

      alert(response.data.message);
    } catch (error: any) {
      console.error(error);
      alert(error.response?.data?.detail || "회원가입 중 오류가 발생했습니다.");
    }
  };

  return (
    // UI 컴포넌트 처리
    <form onSubmit={handleSubmit}>
      {/* 이메일, 비밀번호, 약관동의 체크박스 상태를 formData에 바인딩하여 사용 */}
    </form>
  );
}