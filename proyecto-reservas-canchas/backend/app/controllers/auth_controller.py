from datetime import timedelta
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, Token
from app.core.security import get_password_hash, verify_password, create_access_token
from app.core.config import settings

class AuthController:
    @staticmethod
    def register(db: Session, user_data: UsuarioCreate):
        """Registra un nuevo usuario"""
        # Verificar si ya existe
        existing_user = db.query(Usuario).filter(
            (Usuario.email == user_data.email) | (Usuario.username == user_data.username)
        ).first()
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email o username ya registrado"
            )
        
        # Crear usuario
        hashed_password = get_password_hash(user_data.password)
        db_user = Usuario(
            email=user_data.email,
            username=user_data.username,
            nombre_completo=user_data.nombre_completo,
            telefono=user_data.telefono,
            hashed_password=hashed_password
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        return db_user
    
    @staticmethod
    def login(db: Session, username: str, password: str):
        """Autentica un usuario y devuelve token JWT"""
        # Buscar por username o email
        user = db.query(Usuario).filter(
            (Usuario.username == username) | (Usuario.email == username)
        ).first()
        
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales incorrectas",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Usuario inactivo"
            )
        
        # Crear token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username},
            expires_delta=access_token_expires
        )
        
        return Token(
            access_token=access_token,
            token_type="bearer",
            user={
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "nombre_completo": user.nombre_completo,
                "role": user.role
            }
        )