from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.pago import PagoStatus

class PagoBase(BaseModel):
    reserva_id: int
    monto: float
    metodo_pago: Optional[str] = None
    estado: PagoStatus = PagoStatus.PENDIENTE
    transaction_id: Optional[str] = None

class PagoCreate(PagoBase):
    pass

class Pago(PagoBase):
    id: int
    usuario_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True