

# 1. 회원가입 요청 데이터 검증 스키마
# 클라이언트가 회원가입 요청 시 보낸 데이터를 검증하는 Pydantic 스키마입니다.

from pydantic import BaseModel, EmailStr, Field
# from datetime import datetime


# BaseModel을 상속받는 순간, 이 클래스는 데이터 검증 기능을 갖추게 됩니다.
# Pydantic은 타입 힌트를 기반으로 데이터의 유효성을 검사하고, 잘못된 데이터가 들어오면 자동으로 에러를 발생시킵니다.
# 회원가입 요청 데이터 검증 스키마를 정의합니다.
# ... 은 필수값을 표시
class UserCreate(BaseModel):
    email: EmailStr  = Field(...,description="사용자 이메일 주소", example="user@example.com")
    password: str = Field(..., min_length=8, description="사용자 비밀번호", example="securepassword123")

    # 약관 동의 필드
    # ... 의 의미: 필수 입력 필드임을 나타냅니다.
    terms_agreed: bool = Field(..., description="약관 동의 여부", example=True) 
    privacy_agreed: bool = Field(..., description="개인정보 처리방침 동의 여부", example=True)
    marketing_agreed: bool = Field(False, description="마케팅 수신 동의 여부", example=False)

class UserLogin(BaseModel):
    email: EmailStr  = Field(...,description="사용자 이메일 주소", example="user@example.com")
    password: str = Field(..., min_length=8, description="사용자 비밀번호", example="securepassword123")


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    # created_at: datetime

# Pydantic V2에서 SQLAlchemy 객체(DB 모델)를 Pydantic Schema 모델로 자동 변환하기 위해 사용하는 설정
# class Config:
#     from_attributes = True    
class ConfigDict:
    from_attributes = True        