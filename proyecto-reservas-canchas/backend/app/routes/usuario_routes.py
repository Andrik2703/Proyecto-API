from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.controllers.usuario_controller import UsuarioController
from app.schemas.usuario import UsuarioInDB, UsuarioUpdate
from app.core.dependencies import get_current_user, get_current_admin
from app.models.usuario import Usuario

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

@router.get("/me", response_model=UsuarioInDB)
async def get_current_user_info(current_user: Usuario = Depends(get_current_user)):
    """
    Obtiene información del usuario autenticado.
    """
    return current_user

@router.put("/me", response_model=UsuarioInDB)
async def update_current_user(
    user_data: UsuarioUpdate,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Actualiza información del usuario autenticado.
    """
    return UsuarioController.update(db, current_user.id, user_data)

@router.get("/", response_model=list[UsuarioInDB])
async def get_all_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    admin: Usuario = Depends(get_current_admin)
):
    """
    Obtiene todos los usuarios (solo admin).
    """
    return UsuarioController.get_all(db, skip, limit)

@router.get("/{usuario_id}", response_model=UsuarioInDB)
async def get_user(
    usuario_id: int,
    db: Session = Depends(get_db),
    admin: Usuario = Depends(get_current_admin)
):
    """
    Obtiene un usuario por ID (solo admin).
    """
    return UsuarioController.get_by_id(db, usuario_id)