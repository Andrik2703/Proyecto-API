from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum

class PagoStatus(str, enum.Enum):
    PENDIENTE = "pendiente"
    COMPLETADO = "completado"
    FALLIDO = "fallido"
    REEMBOLSADO = "reembolsado"

class Pago(Base):
    __tablename__ = "pagos"
    
    id = Column(Integer, primary_key=True, index=True)
    reserva_id = Column(Integer, ForeignKey("reservas.id"), unique=True, nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    monto = Column(Float, nullable=False)
    metodo_pago = Column(String(50))
    estado = Column(Enum(PagoStatus), default=PagoStatus.PENDIENTE)
    transaction_id = Column(String(100), unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    reserva = relationship("Reserva", back_populates="pago")
    usuario = relationship("Usuario", back_populates="pagos")
    
    def __repr__(self):
        return f"<Pago {self.id}: €{self.monto} ({self.estado})>"