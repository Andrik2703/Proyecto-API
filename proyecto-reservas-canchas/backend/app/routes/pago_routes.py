from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.controllers.pago_controller import PagoController
from app.schemas.pago import Pago, PagoCreate
from app.core.dependencies import get_current_user
from app.models.usuario import Usuario

router = APIRouter(prefix="/pagos", tags=["Pagos"])

@router.get("/reserva/{reserva_id}", response_model=Pago)
async def get_pago_by_reserva(
    reserva_id: int,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtiene el pago asociado a una reserva.
    """
    return PagoController.get_by_reserva(db, reserva_id)

@router.post("/", response_model=Pago, status_code=status.HTTP_201_CREATED)
async def create_pago(
    pago_data: PagoCreate,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Registra un pago para una reserva.
    """
    return PagoController.create(db, pago_data, current_user.id)