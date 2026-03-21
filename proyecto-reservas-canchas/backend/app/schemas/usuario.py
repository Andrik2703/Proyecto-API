from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime
from app.models.usuario import UserRole

class UsuarioBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    nombre_completo: str = Field(..., min_length=3, max_length=100)
    telefono: Optional[str] = None

class UsuarioCreate(UsuarioBase):
    password: str = Field(..., min_length=6)
    
    @validator('telefono')
    def validate_telefono(cls, v):
        if v and not v.replace('-', '').isdigit():
            raise ValueError('El teléfono debe contener solo dígitos y guiones')
        return v

class UsuarioUpdate(BaseModel):
    nombre_completo: Optional[str] = None
    telefono: Optional[str] = None

class UsuarioInDB(UsuarioBase):
    id: int
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: Optional[dict] = None

class TokenData(BaseModel):
    username: Optional[str] = None