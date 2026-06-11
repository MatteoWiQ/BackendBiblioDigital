from pydantic import BaseModel, EmailStr
from typing import Optional
# ESQUEMAS PARA USUARIOS
class UserBase(BaseModel):
    email: EmailStr 

class UserCreate(UserBase):
    password: str
    rol: Optional[str] = "Usuario" 

class UserResponse(UserBase):
    id: int
    rol: str

   
    class Config:
        from_attributes = True 
# ESQUEMAS PARA LIBROS

from pydantic import BaseModel

class BookBase(BaseModel):
    titulo: str
    autor: str
    descripcion: str
    url_pdf: str
    categoria: Optional[str] = None 
    precio: Optional[float] = 0.0

class BookCreate(BookBase):
    pass

class BookResponse(BookBase):
    id: int

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    rol: Optional[str] = None