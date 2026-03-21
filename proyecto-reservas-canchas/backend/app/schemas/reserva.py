from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import date, datetime
from app.models.reserva import ReservaStatus

class ReservaBase(BaseModel):
    cancha_id: int
    fecha: date
    hora_inicio: str = Field(..., pattern="^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$")
    duracion_horas: int = Field(..., ge=1, le=3)
    notas: Optional[str] = None
    
    @validator('fecha')
    def validate_fecha(cls, v):
        if v < date.today():
            raise ValueError('No se puede reservar en fechas pasadas')
        return v

class ReservaCreate(ReservaBase):
    pass

class ReservaUpdate(BaseModel):
    fecha: Optional[date] = None
    hora_inicio: Optional[str] = None
    duracion_horas: Optional[int] = Field(None, ge=1, le=3)
    estado: Optional[ReservaStatus] = None
    notas: Optional[str] = None

class Reserva(ReservaBase):
    id: int
    usuario_id: int
    precio_total: float
    estado: ReservaStatus
    created_at: datetime
    updated_at: Optional[datetime] = None
    cancha_nombre: Optional[str] = None
    usuario_nombre: Optional[str] = None
    
    class Config:
        from_attributes = True