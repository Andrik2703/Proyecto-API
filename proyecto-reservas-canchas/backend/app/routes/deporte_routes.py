from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.controllers.deporte_controller import DeporteController
from app.schemas.deporte import Deporte, DeporteCreate, DeporteUpdate
from app.core.dependencies import get_current_admin
from app.models.usuario import Usuario

router = APIRouter(prefix="/deportes", tags=["Deportes"])

@router.get("/", response_model=list[Deporte])
async def get_deportes(db: Session = Depends(get_db)):
    """
    Obtiene todos los deportes disponibles.
    """
    return DeporteController.get_all(db)

@router.get("/{deporte_id}", response_model=Deporte)
async def get_deporte(deporte_id: int, db: Session = Depends(get_db)):
    """
    Obtiene un deporte específico por ID.
    """
    return DeporteController.get_by_id(db, deporte_id)

@router.post("/", response_model=Deporte, status_code=status.HTTP_201_CREATED)
async def create_deporte(
    deporte_data: DeporteCreate,
    db: Session = Depends(get_db),
    admin: Usuario = Depends(get_current_admin)
):
    """
    Crea un nuevo deporte (solo admin).
    """
    return DeporteController.create(db, deporte_data)

@router.put("/{deporte_id}", response_model=Deporte)
async def update_deporte(
    deporte_id: int,
    deporte_data: DeporteUpdate,
    db: Session = Depends(get_db),
    admin: Usuario = Depends(get_current_admin)
):
    """
    Actualiza un deporte existente (solo admin).
    """
    return DeporteController.update(db, deporte_id, deporte_data)

@router.delete("/{deporte_id}")
async def delete_deporte(
    deporte_id: int,
    db: Session = Depends(get_db),
    admin: Usuario = Depends(get_current_admin)
):
    """
    Elimina un deporte (solo admin).
    """
    return DeporteController.delete(db, deporte_id)