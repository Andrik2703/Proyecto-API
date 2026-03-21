from datetime import datetime, date
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.reserva import Reserva, ReservaStatus
from app.models.cancha import Cancha
from app.schemas.reserva import ReservaCreate, ReservaUpdate

class ReservaController:
    @staticmethod
    def get_user_reservas(db: Session, usuario_id: int):
        """Obtiene todas las reservas de un usuario"""
        reservas = db.query(Reserva).filter(
            Reserva.usuario_id == usuario_id
        ).order_by(Reserva.fecha.desc()).all()
        
        # Enriquecer con datos de cancha
        for r in reservas:
            cancha = db.query(Cancha).filter(Cancha.id == r.cancha_id).first()
            r.cancha_nombre = cancha.nombre if cancha else "Cancha"
            r.usuario_nombre = r.usuario.nombre_completo if r.usuario else "Usuario"
        
        return reservas
    
    @staticmethod
    def get_by_id(db: Session, reserva_id: int, usuario_id: int = None):
        """Obtiene una reserva por ID"""
        query = db.query(Reserva).filter(Reserva.id == reserva_id)
        
        if usuario_id:
            query = query.filter(Reserva.usuario_id == usuario_id)
        
        reserva = query.first()
        if not reserva:
            raise HTTPException(status_code=404, detail="Reserva no encontrada")
        
        # Enriquecer
        cancha = db.query(Cancha).filter(Cancha.id == reserva.cancha_id).first()
        reserva.cancha_nombre = cancha.nombre if cancha else "Cancha"
        
        return reserva
    
    @staticmethod
    def check_disponibilidad(db: Session, cancha_id: int, fecha: date, hora_inicio: str, duracion: int):
        """Verifica si una cancha está disponible en fecha/hora"""
        # Verificar fecha pasada
        if fecha < date.today():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se puede reservar en fechas pasadas"
            )
        
        # Verificar horario de la cancha
        cancha = db.query(Cancha).filter(Cancha.id == cancha_id).first()
        if cancha and cancha.horario_apertura and cancha.horario_cierre:
            hora_fin = f"{int(hora_inicio.split(':')[0]) + duracion}:{hora_inicio.split(':')[1]}"
            if hora_inicio < cancha.horario_apertura or hora_fin > cancha.horario_cierre:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Horario fuera del rango de operación ({cancha.horario_apertura} - {cancha.horario_cierre})"
                )
        
        # Verificar conflictos con otras reservas
        conflictos = db.query(Reserva).filter(
            and_(
                Reserva.cancha_id == cancha_id,
                Reserva.fecha == fecha,
                Reserva.estado.in_([ReservaStatus.CONFIRMADA, ReservaStatus.PENDIENTE])
            )
        ).all()
        
        for reserva in conflictos:
            reserva_inicio = int(reserva.hora_inicio.split(':')[0])
            reserva_fin = reserva_inicio + reserva.duracion_horas
            nueva_inicio = int(hora_inicio.split(':')[0])
            nueva_fin = nueva_inicio + duracion
            
            if not (nueva_fin <= reserva_inicio or nueva_inicio >= reserva_fin):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="La cancha no está disponible en ese horario"
                )
    
    @staticmethod
    def create(db: Session, reserva_data: ReservaCreate, usuario_id: int):
        """Crea una nueva reserva"""
        # Verificar disponibilidad
        ReservaController.check_disponibilidad(
            db,
            reserva_data.cancha_id,
            reserva_data.fecha,
            reserva_data.hora_inicio,
            reserva_data.duracion_horas
        )
        
        # Calcular precio
        cancha = db.query(Cancha).filter(Cancha.id == reserva_data.cancha_id).first()
        if not cancha:
            raise HTTPException(status_code=404, detail="Cancha no encontrada")
        
        precio_total = cancha.precio_por_hora * reserva_data.duracion_horas
        
        # Crear reserva
        db_reserva = Reserva(
            usuario_id=usuario_id,
            cancha_id=reserva_data.cancha_id,
            fecha=reserva_data.fecha,
            hora_inicio=reserva_data.hora_inicio,
            duracion_horas=reserva_data.duracion_horas,
            precio_total=precio_total,
            notas=reserva_data.notas,
            estado=ReservaStatus.CONFIRMADA
        )
        
        db.add(db_reserva)
        db.commit()
        db.refresh(db_reserva)
        
        # Enriquecer respuesta
        db_reserva.cancha_nombre = cancha.nombre
        
        return db_reserva
    
    @staticmethod
    def cancel(db: Session, reserva_id: int, usuario_id: int):
        """Cancela una reserva"""
        reserva = ReservaController.get_by_id(db, reserva_id, usuario_id)
        
        if reserva.estado == ReservaStatus.CANCELADA:
            raise HTTPException(status_code=400, detail="La reserva ya está cancelada")
        
        if reserva.estado == ReservaStatus.COMPLETADA:
            raise HTTPException(status_code=400, detail="No se puede cancelar una reserva completada")
        
        # Verificar que la fecha no haya pasado
        if reserva.fecha.date() < date.today():
            raise HTTPException(status_code=400, detail="No se puede cancelar una reserva pasada")
        
        reserva.estado = ReservaStatus.CANCELADA
        db.commit()
        
        return {"message": "Reserva cancelada exitosamente", "id": reserva_id}