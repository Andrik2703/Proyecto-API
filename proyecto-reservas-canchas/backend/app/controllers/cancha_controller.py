from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.cancha import Cancha
from app.models.deporte import Deporte
from app.schemas.cancha import CanchaCreate, CanchaUpdate
from typing import Optional

class CanchaController:
    @staticmethod
    def get_all(db: Session, deporte: Optional[str] = None, ciudad: Optional[str] = None):
        """Obtiene todas las canchas con filtros opcionales"""
        query = db.query(Cancha).filter(Cancha.is_active == True)
        
        if deporte:
            query = query.join(Deporte).filter(Deporte.nombre == deporte)
        
        if ciudad:
            query = query.filter(Cancha.ciudad == ciudad)
        
        # Agregar información del deporte
        canchas = query.all()
        for cancha in canchas:
            cancha.deporte = cancha.deporte.nombre if cancha.deporte else None
        
        return canchas
    
    @staticmethod
    def get_by_id(db: Session, cancha_id: int):
        """Obtiene una cancha por ID"""
        cancha = db.query(Cancha).filter(Cancha.id == cancha_id).first()
        if not cancha:
            raise HTTPException(status_code=404, detail="Cancha no encontrada")
        
        cancha.deporte = cancha.deporte.nombre if cancha.deporte else None
        return cancha
    
    @staticmethod
    def create(db: Session, cancha_data: CanchaCreate):
        """Crea una nueva cancha"""
        # Verificar que el deporte existe
        deporte = db.query(Deporte).filter(Deporte.id == cancha_data.deporte_id).first()
        if not deporte:
            raise HTTPException(status_code=400, detail="Deporte no válido")
        
        db_cancha = Cancha(**cancha_data.model_dump())
        db.add(db_cancha)
        db.commit()
        db.refresh(db_cancha)
        
        db_cancha.deporte = deporte.nombre
        return db_cancha
    
    @staticmethod
    def update(db: Session, cancha_id: int, cancha_data: CanchaUpdate):
        """Actualiza una cancha"""
        cancha = CanchaController.get_by_id(db, cancha_id)
        
        update_data = cancha_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(cancha, field, value)
        
        db.commit()
        db.refresh(cancha)
        return cancha
    
    @staticmethod
    def delete(db: Session, cancha_id: int):
        """Desactiva una cancha (soft delete)"""
        cancha = CanchaController.get_by_id(db, cancha_id)
        cancha.is_active = False
        db.commit()
        return {"message": "Cancha desactivada exitosamente"}