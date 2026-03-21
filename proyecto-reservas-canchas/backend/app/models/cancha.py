from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Cancha(Base):
    __tablename__ = "canchas"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    deporte_id = Column(Integer, ForeignKey("deportes.id"), nullable=False)
    ciudad = Column(String(50), nullable=False)
    ubicacion = Column(String(200), nullable=False)
    precio_por_hora = Column(Float, nullable=False)
    descripcion = Column(Text)
    imagen_url = Column(String(500))
    horario_apertura = Column(String(5))
    horario_cierre = Column(String(5))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    deporte = relationship("Deporte", back_populates="canchas")
    reservas = relationship("Reserva", back_populates="cancha")
    
    def __repr__(self):
        return f"<Cancha {self.nombre} ({self.ciudad})>"