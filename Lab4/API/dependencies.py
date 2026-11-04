from fastapi import Header, HTTPException, status
from program_list import dict_user_connect

from dossier_modeles import Admin

async def verify_custom_token(x_token: str = Header(..., alias="X-Token")):
    if x_token not in dict_user_connect :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Header 'X-Token' invalide ou absent."
        )
    
    return x_token

async def verify_custom_token_admin(x_token: str = Header(..., alias="X-Token")):
    if x_token not in dict_user_connect :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Header 'X-Token' invalide ou absent."
        )

    if not isinstance(dict_user_connect[x_token] ,Admin):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Header 'X-Token' non admin."
            )
    
    return x_token