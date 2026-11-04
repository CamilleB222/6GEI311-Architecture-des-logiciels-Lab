from pydantic import BaseModel
from typing import Literal

class BaseDescriptionSchema(BaseModel):
    titre: str

class DescriptionTexteSchema(BaseDescriptionSchema):
    type: Literal["texte"] = "texte"
    description: str

class DescriptionImageSchema(BaseDescriptionSchema):
    type: Literal["image"] = "image"
    filepath: str

DescriptionUnion = DescriptionTexteSchema | DescriptionImageSchema

class DescriptionCreateSchema(BaseModel):
    titre: str
    type_description: Literal["texte", "image"]
    contenu: str