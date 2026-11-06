from pydantic import BaseModel, Field
from typing import Literal

class BaseDescriptionSchema(BaseModel):
    titre: str

class DescriptionTexteSchema(BaseDescriptionSchema):
    type: Literal["texte"] = "texte"
    description: str

class DescriptionImageSchema(BaseDescriptionSchema):
    type: Literal["image"] = "image"
    filepath: str
    binary_content: bytes

DescriptionUnion = DescriptionTexteSchema | DescriptionImageSchema

class DescriptionCreateSchema(BaseModel):
    type_description: Literal["texte", "image"]
    titre: str
    contenu: str
    binary_content: bytes | None = Field(default=None, description="Contenu binaire optionnel encodé en Base64 en JSON")

class DescriptionUpdateSchema(DescriptionCreateSchema):
    pass