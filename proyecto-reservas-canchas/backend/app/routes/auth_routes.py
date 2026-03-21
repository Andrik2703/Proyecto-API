from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.controllers.auth_controller import AuthController
from app.schemas.usuario import UsuarioCreate, UsuarioInDB, Token

router = APIRouter(prefix="/auth", tags=["Autenticación"])

@router.post("/register", response_model=UsuarioInDB, status_code=status.HTTP_201_CREATED)
async def register(user_data: UsuarioCreate, db: Session = Depends(get_db)):
    """
    Registra un nuevo usuario en el sistema.
    
    - **email**: Email válido
    - **username**: Nombre de usuario único
    - **nombre_completo**: Nombre completo
    - **telefono**: Opcional, formato 229-133-9124
    - **password**: Mínimo 6 caracteres
    """
    return AuthController.register(db, user_data)

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Inicia sesión y obtiene un token JWT.
    
    - **username**: Email o nombre de usuario
    - **password**: Contraseña
    """
    return AuthController.login(db, form_data.username, form_data.password)

@router.get("/health")
async def health_check():
    """
    Endpoint de verificación de salud de la API.
    """
    return {
        "status": "ok",
        "message": "API SportReserva funcionando correctamente",
        "timestamp": datetime.now().isoformat()
    }