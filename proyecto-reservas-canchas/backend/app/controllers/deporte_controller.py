from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.deporte import Deporte
from app.schemas.deporte import DeporteCreate, DeporteUpdate

class DeporteController:
    @staticmethod
    def get_all(db: Session):
        """Obtiene todos los deportes"""
        return db.query(Deporte).all()
    
    @staticmethod
    def get_by_id(db: Session, deporte_id: int):
        """Obtiene un deporte por ID"""
        deporte = db.query(Deporte).filter(Deporte.id == deporte_id).first()
        if not deporte:
            raise HTTPException(status_code=404, detail="Deporte no encontrado")
        return deporte
    
    @staticmethod
    def create(db: Session, deporte_data: DeporteCreate):
        """Crea un nuevo deporte"""
        # Verificar si ya existe
        existing = db.query(Deporte).filter(Deporte.nombre == deporte_data.nombre).first()
        if existing:
            raise HTTPException(status_code=400, detail="Ya existe un deporte con ese nombre")
        
        db_deporte = Deporte(**deporte_data.model_dump())
        db.add(db_deporte)
        db.commit()
        db.refresh(db_deporte)
        return db_deporte
    
    @staticmethod
    def update(db: Session, deporte_id: int, deporte_data: DeporteUpdate):
        """Actualiza un deporte"""
        deporte = DeporteController.get_by_id(db, deporte_id)
        
        update_data = deporte_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(deporte, field, value)
        
        db.commit()
        db.refresh(deporte)
        return deporte
    
    @staticmethod
    def delete(db: Session, deporte_id: int):
        """Elimina un deporte"""
        deporte = DeporteController.get_by_id(db, deporte_id)
        db.delete(deporte)
        db.commit()
        return {"message": "Deporte eliminado"}