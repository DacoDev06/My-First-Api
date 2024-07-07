from pydantic import BaseModel, Field
from typing import Optional


class Movie(BaseModel):
    id: Optional[int] = None
    name: str = Field(min_length=4,max_length=1000)
    rating: float = Field(default=0,le=10,ge = 0)
    category: str = Field(default="Category")

    class Config: 
        json_schema_extra = {
            "example": {
                "id": 0,
                "name": "Nombre Pelicula",
                "rating":1.2,
                "category":"Categoria de la pelicula"
            }
        }