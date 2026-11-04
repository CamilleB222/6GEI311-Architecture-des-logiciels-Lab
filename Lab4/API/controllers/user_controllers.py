from fastapi import APIRouter, HTTPException, status

router = APIRouter(tags=["Users"])

@router.get("/users", response_model=list[UserResponse])
def get_users():
    return UserModel.get_all()

@router.get("/user/{user_id}", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def get_user(user_id: int):
    user = UserModel.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")
    return user