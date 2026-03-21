from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.controllers.reserva_controller import ReservaController
from app.schemas.reserva import Reserva, ReservaCreate
from app.core.dependencies import get_current_user
from app.models.usuario import Usuario

router = APIRouter(prefix="/reservas", tags=["Reservas"])

@router.get("/", response_model=list[Reserva])
async def get_mis_reservas(
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtiene todas las reservas del usuario autenticado.
    """
    return ReservaController.get_user_reservas(db, current_user.id)

@router.get("/{reserva_id}", response_model=Reserva)
async def get_reserva(
    reserva_id: int,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtiene una reserva específica del usuario autenticado.
    """
    return ReservaController.get_by_id(db, reserva_id, current_user.id)

@router.post("/", response_model=Reserva, status_code=status.HTTP_201_CREATED)
async def create_reserva(
    reserva_data: ReservaCreate,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Crea una nueva reserva para el usuario autenticado.
    
    Reglas:
    - No se puede reservar en fechas pasadas
    - La cancha debe estar disponible en el horario solicitado
    - La duración debe ser entre 1 y 3 horas
    """
    return ReservaController.create(db, reserva_data, current_user.id)

@router.post("/{reserva_id}/cancelar")
async def cancelar_reserva(
    reserva_id: int,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Cancela una reserva existente del usuario autenticado.
    Solo se pueden cancelar reservas futuras.
    """
    return ReservaController.cancel(db, reserva_id, current_user.id)