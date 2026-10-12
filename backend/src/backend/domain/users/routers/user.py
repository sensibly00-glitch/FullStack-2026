from fastapi import APIRouter, status
from backend.domain.users.schemas.user import UserCreate, UserResponse, UserLogin

# router = APIRouter(prefix="/auth", tags=["AUTH"])
router = APIRouter()

# 회원가입
@router.post("/sign-up", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signUp(body: UserCreate):
    # 비즈니스 로직 호출
    # 회원 가입 API
    # - 클라이언트
    return "회원가입 API 입니다."

# 로그인
@router.get("/sign-in")
def signIn(body: UserLogin):
    #
    return "로그인 API 입니다."