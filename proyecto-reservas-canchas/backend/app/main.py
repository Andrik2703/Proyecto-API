"""
SportReserva API - Main Application
Sistema de reservas de canchas deportivas
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
import os

from app.core.database import engine, Base
from app.routes import (
    auth_router,
    usuario_router,
    deporte_router,
    cancha_router,
    reserva_router,
    pago_router
)

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Inicializar app
app = FastAPI(
    title="SportReserva API",
    description="""
    API para sistema de reservas de canchas deportivas.
    
    ## Características
    * Gestión de usuarios y autenticación JWT
    * Catálogo de deportes y canchas
    * Sistema de reservas con validación de disponibilidad
    * Pagos y gestión de estados
    
    ## Documentación
    * Swagger UI: /api/docs
    * ReDoc: /api/redoc
    """,
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    contact={
        "name": "SportReserva Support",
        "email": "soporte@sportreserva.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    }
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(auth_router)
app.include_router(usuario_router)
app.include_router(deporte_router)
app.include_router(cancha_router)
app.include_router(reserva_router)
app.include_router(pago_router)

@app.get("/")
async def root():
    """
    Endpoint raíz - Información de la API
    """
    return {
        "name": "SportReserva API",
        "version": "2.0.0",
        "status": "operational",
        "timestamp": datetime.now().isoformat(),
        "documentation": {
            "swagger": "/api/docs",
            "redoc": "/api/redoc"
        },
        "endpoints": {
            "auth": "/auth",
            "usuarios": "/usuarios",
            "deportes": "/deportes",
            "canchas": "/canchas",
            "reservas": "/reservas",
            "pagos": "/pagos"
        }
    }

@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "environment": os.getenv("ENVIRONMENT", "development"),
        "database": "connected"  # Podrías verificar la BD aquí
    }

@app.get("/api")
async def api_info():
    """
    Información de la API
    """
    return {
        "message": "SportReserva API",
        "version": "2.0.0",
        "docs": "/api/docs"
    }

# Manejo de errores global
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not Found",
            "message": "El recurso solicitado no existe",
            "path": request.url.path
        }
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "Error interno del servidor",
            "path": request.url.path
        }
    )