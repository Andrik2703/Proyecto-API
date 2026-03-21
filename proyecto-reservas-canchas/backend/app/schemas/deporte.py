from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DeporteBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    icono: Optional[str] = None

class DeporteCreate(DeporteBase):
    pass

class DeporteUpdate(DeporteBase):
    pass

class Deporte(DeporteBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True