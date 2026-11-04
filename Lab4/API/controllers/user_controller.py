from fastapi import APIRouter, HTTPException, status
from schemas.userSchema import UserResponseSchema

from services.mappers import map_user_to_schema

from program_list import list_user

router = APIRouter(tags=["Users"])

@router.get("/users", response_model=list[UserResponseSchema])
def get_users():
    list_user_schema = list[UserResponseSchema]()

    for user in list_user:
        list_user_schema.append(map_user_to_schema(user))

    return  list_user_schema

@router.get("/user/{user_id}", response_model=UserResponseSchema, status_code=status.HTTP_200_OK)
def get_user(user_id: int):
    for user in list_user:
        if user.id == user_id:
            user_return = user

    if not user_return:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")
    
    return map_user_to_schema(user)