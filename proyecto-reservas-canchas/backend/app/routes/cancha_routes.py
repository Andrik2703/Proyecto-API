from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import Optional, List
from app.core.database import get_db
from app.controllers.cancha_controller import CanchaController
from app.schemas.cancha import Cancha, CanchaCreate, CanchaUpdate
from app.core.dependencies import get_current_admin
from app.models.usuario import Usuario

router = APIRouter(prefix="/canchas", tags=["Canchas"])

@router.get("/", response_model=List[Cancha])
async def get_canchas(
    deporte: Optional[str] = Query(None, description="Filtrar por deporte"),
    ciudad: Optional[str] = Query(None, description="Filtrar por ciudad"),
    db: Session = Depends(get_db)
):
    """
    Obtiene todas las canchas activas.
    
    Filtros opcionales:
    - **deporte**: fútbol, tenis, pádel, baloncesto
    - **ciudad**: madrid, barcelona, valencia
    """
    return CanchaController.get_all(db, deporte, ciudad)

@router.get("/{cancha_id}", response_model=Cancha)
async def get_cancha(cancha_id: int, db: Session = Depends(get_db)):
    """
    Obtiene una cancha específica por su ID.
    """
    return CanchaController.get_by_id(db, cancha_id)

@router.post("/", response_model=Cancha, status_code=status.HTTP_201_CREATED)
async def create_cancha(
    cancha_data: CanchaCreate,
    db: Session = Depends(get_db),
    admin: Usuario = Depends(get_current_admin)
):
    """
    Crea una nueva cancha (solo admin).
    """
    return CanchaController.create(db, cancha_data)

@router.put("/{cancha_id}", response_model=Cancha)
async def update_cancha(
    cancha_id: int,
    cancha_data: CanchaUpdate,
    db: Session = Depends(get_db),
    admin: Usuario = Depends(get_current_admin)
):
    """
    Actualiza una cancha existente (solo admin).
    """
    return CanchaController.update(db, cancha_id, cancha_data)

@router.delete("/{cancha_id}")
async def delete_cancha(
    cancha_id: int,
    db: Session = Depends(get_db),
    admin: Usuario = Depends(get_current_admin)
):
    """
    Desactiva una cancha (soft delete) - solo admin.
    """
    return CanchaController.delete(db, cancha_id)