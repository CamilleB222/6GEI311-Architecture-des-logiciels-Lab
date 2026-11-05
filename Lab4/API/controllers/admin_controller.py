from fastapi import APIRouter, HTTPException, status, Depends
from schemas.userSchema import AdminResponseSchema

from program_list import list_admin
from services.mappers import map_user_to_schema
from dependencies import verify_custom_token

router = APIRouter(tags=["Admins"], dependencies=[Depends(verify_custom_token)])

@router.get("/admins", response_model=list[AdminResponseSchema])
def get_users():
    list_admin_schemat = list[AdminResponseSchema]()

    for admin in list_admin:
        list_admin_schemat.append(map_user_to_schema(admin))

    return list_admin

@router.get("/admin/{admin_id}", response_model=AdminResponseSchema, status_code=status.HTTP_200_OK)
def get_user(admin_id: int):
    admin_return : AdminResponseSchema | None = None
    
    for admin in list_admin:
        if admin.id == admin_id:
            admin_return = admin

    if not admin_return:
        raise HTTPException(status_code=404, detail="Administrateur introuvable")
    
    return map_user_to_schema(admin_return)