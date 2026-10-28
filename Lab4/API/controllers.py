from fastapi import APIRouter, HTTPException, status

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/", response_model=list[UserResponse])
def get_users():
    return UserModel.get_all()

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    user = UserModel.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")
    return user

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate):
    return UserModel.create(payload.name, payload.email)