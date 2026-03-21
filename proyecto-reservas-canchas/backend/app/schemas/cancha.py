from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class CanchaBase(BaseModel):
    nombre: str
    deporte_id: int
    ciudad: str
    ubicacion: str
    precio_por_hora: float = Field(..., gt=0)
    descripcion: Optional[str] = None
    imagen_url: Optional[str] = None
    horario_apertura: Optional[str] = None
    horario_cierre: Optional[str] = None

class CanchaCreate(CanchaBase):
    pass

class CanchaUpdate(BaseModel):
    nombre: Optional[str] = None
    deporte_id: Optional[int] = None
    ciudad: Optional[str] = None
    ubicacion: Optional[str] = None
    precio_por_hora: Optional[float] = Field(None, gt=0)
    descripcion: Optional[str] = None
    imagen_url: Optional[str] = None
    horario_apertura: Optional[str] = None
    horario_cierre: Optional[str] = None

class Cancha(CanchaBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    deporte: Optional[dict] = None
    
    class Config:
        from_attributes = True