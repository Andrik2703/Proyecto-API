from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Enum, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum

class ReservaStatus(str, enum.Enum):
    PENDIENTE = "pendiente"
    CONFIRMADA = "confirmada"
    CANCELADA = "cancelada"
    COMPLETADA = "completada"

class Reserva(Base):
    __tablename__ = "reservas"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    cancha_id = Column(Integer, ForeignKey("canchas.id"), nullable=False)
    fecha = Column(DateTime, nullable=False)
    hora_inicio = Column(String(5), nullable=False)
    duracion_horas = Column(Integer, nullable=False)
    precio_total = Column(Float, nullable=False)
    estado = Column(Enum(ReservaStatus), default=ReservaStatus.PENDIENTE)
    notas = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    usuario = relationship("Usuario", back_populates="reservas")
    cancha = relationship("Cancha", back_populates="reservas")
    pago = relationship("Pago", back_populates="reserva", uselist=False)
    
    # Reglas de integridad
    __table_args__ = (
        CheckConstraint('fecha >= CURRENT_DATE', name='reserva_fecha_no_pasado'),
    )
    
    def __repr__(self):
        return f"<Reserva {self.id}: {self.fecha} {self.hora_inicio}>"