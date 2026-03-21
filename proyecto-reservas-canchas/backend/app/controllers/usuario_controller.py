from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioUpdate

class UsuarioController:
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100):
        """Obtiene todos los usuarios (solo admin)"""
        return db.query(Usuario).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_by_id(db: Session, usuario_id: int):
        """Obtiene un usuario por ID"""
        user = db.query(Usuario).filter(Usuario.id == usuario_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return user
    
    @staticmethod
    def update(db: Session, usuario_id: int, user_data: UsuarioUpdate):
        """Actualiza un usuario"""
        user = UsuarioController.get_by_id(db, usuario_id)
        
        update_data = user_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)
        
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def delete(db: Session, usuario_id: int):
        """Desactiva un usuario"""
        user = UsuarioController.get_by_id(db, usuario_id)
        user.is_active = False
        db.commit()
        return {"message": "Usuario desactivado"}