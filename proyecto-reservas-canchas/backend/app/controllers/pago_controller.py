from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.pago import Pago, PagoStatus
from app.models.reserva import Reserva
from app.schemas.pago import PagoCreate
from datetime import datetime

class PagoController:
    @staticmethod
    def get_by_reserva(db: Session, reserva_id: int):
        """Obtiene el pago de una reserva"""
        return db.query(Pago).filter(Pago.reserva_id == reserva_id).first()
    
    @staticmethod
    def create(db: Session, pago_data: PagoCreate, usuario_id: int):
        """Crea un nuevo pago"""
        # Verificar que la reserva existe
        reserva = db.query(Reserva).filter(Reserva.id == pago_data.reserva_id).first()
        if not reserva:
            raise HTTPException(status_code=404, detail="Reserva no encontrada")
        
        # Verificar que la reserva pertenece al usuario
        if reserva.usuario_id != usuario_id:
            raise HTTPException(status_code=403, detail="No autorizado")
        
        # Verificar que no haya pago previo
        existing = db.query(Pago).filter(Pago.reserva_id == pago_data.reserva_id).first()
        if existing:
            raise HTTPException(status_code=400, detail="La reserva ya tiene un pago asociado")
        
        # Crear pago
        transaction_id = f"TXN{reserva.id}{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        db_pago = Pago(
            **pago_data.model_dump(),
            usuario_id=usuario_id,
            transaction_id=transaction_id,
            estado=PagoStatus.COMPLETADO
        )
        
        db.add(db_pago)
        db.commit()
        db.refresh(db_pago)
        
        return db_pago