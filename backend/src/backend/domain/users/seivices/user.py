from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status

from backend.domain.users.models.user import User
from backend.domain.users.schemas.user import UserCreate
from backend.core.security import hash_password

class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_email(self, email: str) -> User | None:
        result = await self.db.execute(select(User).filter(User.email == email))
        return result.scalars().first()

    async def create_user(self, user_in: UserCreate) -> User:
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