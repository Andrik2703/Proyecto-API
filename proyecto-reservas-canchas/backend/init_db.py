#!/usr/bin/env python
"""
Script para inicializar la base de datos con datos de ejemplo.
Ejecutar: python init_db.py
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal, engine, Base
from app.core.security import get_password_hash
from app.models.usuario import Usuario, UserRole
from app.models.deporte import Deporte
from app.models.cancha import Cancha
from app.models.reserva import Reserva, ReservaStatus
from app.models.pago import Pago, PagoStatus

def init_db():
    """Inicializa la base de datos con datos de ejemplo"""
    print("🚀 Inicializando base de datos...")
    
    # PASO CRÍTICO: Crear todas las tablas
    print("📦 Creando tablas en la base de datos...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas creadas exitosamente")
    
    db = SessionLocal()
    
    try:
        # ============================================
        # 1. CREAR DEPORTES
        # ============================================
        print("\n📊 Creando deportes...")
        deportes_data = [
            {"nombre": "fútbol", "descripcion": "Fútbol 7 y 11", "icono": "fa-futbol"},
            {"nombre": "tenis", "descripcion": "Tenis individual y dobles", "icono": "fa-tennis-ball"},
            {"nombre": "pádel", "descripcion": "Pádel profesional", "icono": "fa-table-tennis"},
            {"nombre": "baloncesto", "descripcion": "Baloncesto 3x3 y 5x5", "icono": "fa-basketball-ball"}
        ]
        
        for d in deportes_data:
            existe = db.query(Deporte).filter(Deporte.nombre == d["nombre"]).first()
            if not existe:
                deporte = Deporte(**d)
                db.add(deporte)
                print(f"  ✅ {d['nombre']}")
            else:
                print(f"  ⏩ {d['nombre']} (ya existe)")
        
        db.commit()
        
        # Obtener IDs de deportes
        futbol = db.query(Deporte).filter(Deporte.nombre == "fútbol").first()
        tenis = db.query(Deporte).filter(Deporte.nombre == "tenis").first()
        padel = db.query(Deporte).filter(Deporte.nombre == "pádel").first()
        basket = db.query(Deporte).filter(Deporte.nombre == "baloncesto").first()
        
        # ============================================
        # 2. CREAR USUARIOS
        # ============================================
        print("\n👥 Creando usuarios...")
        usuarios_data = [
    {
        "email": "admin@sportreserva.com",
        "username": "admin",
        "nombre_completo": "Administrador del Sistema",
        "telefono": "229-133-9124",
        "hashed_password": get_password_hash("admin123"),  # Cambiar a "admin123"
        "role": UserRole.ADMIN
    },
    {
        "email": "cliente@test.com",
        "username": "cliente1",
        "nombre_completo": "Cliente de Prueba",
        "telefono": "229-133-5678",
        "hashed_password": get_password_hash("cliente123"),  # Cambiar a "cliente123"
        "role": UserRole.CLIENTE
    }
]
        for u in usuarios_data:
            existe = db.query(Usuario).filter(
                (Usuario.email == u["email"]) | (Usuario.username == u["username"])
            ).first()
            if not existe:
                usuario = Usuario(**u)
                db.add(usuario)
                print(f"  ✅ {u['email']}")
            else:
                print(f"  ⏩ {u['email']} (ya existe)")
        
        db.commit()
        
        # ============================================
        # 3. CREAR CANCHAS
        # ============================================
        print("\n🏟️ Creando canchas...")
        canchas_data = [
            {
                "nombre": "Cancha de Fútbol 7 - Madrid Centro",
                "deporte_id": futbol.id,
                "ciudad": "madrid",
                "ubicacion": "Calle del Deporte, 45",
                "precio_por_hora": 50.0,
                "descripcion": "Cancha de césped artificial con iluminación LED",
                "imagen_url": "https://images.unsplash.com/photo-1459865264687-595d652de67e?w=500",
                "horario_apertura": "09:00",
                "horario_cierre": "22:00"
            },
            {
                "nombre": "Pista de Tenis - Barcelona Norte",
                "deporte_id": tenis.id,
                "ciudad": "barcelona",
                "ubicacion": "Av. Tenis, 123",
                "precio_por_hora": 35.0,
                "descripcion": "Pista de tierra batida con mantenimiento profesional",
                "imagen_url": "https://images.unsplash.com/photo-1595435934249-5df7ed86e1c0?w=500",
                "horario_apertura": "08:00",
                "horario_cierre": "21:00"
            },
            {
                "nombre": "Cancha de Pádel - Valencia Sur",
                "deporte_id": padel.id,
                "ciudad": "valencia",
                "ubicacion": "Polígono Deportivo Sur",
                "precio_por_hora": 25.0,
                "descripcion": "Cancha cubierta con cristal templado",
                "imagen_url": "https://images.unsplash.com/photo-1626224583764-f87db24ac4ea?w=500",
                "horario_apertura": "10:00",
                "horario_cierre": "23:00"
            },
            {
                "nombre": "Cancha de Baloncesto - Madrid Este",
                "deporte_id": basket.id,
                "ciudad": "madrid",
                "ubicacion": "Calle del Basket, 78",
                "precio_por_hora": 40.0,
                "descripcion": "Cancha cubierta con parquet flotante",
                "imagen_url": "https://images.unsplash.com/photo-1504450758481-7338eba7524c?w=500",
                "horario_apertura": "09:00",
                "horario_cierre": "22:00"
            }
        ]
        
        for c in canchas_data:
            existe = db.query(Cancha).filter(Cancha.nombre == c["nombre"]).first()
            if not existe:
                cancha = Cancha(**c)
                db.add(cancha)
                print(f"  ✅ {c['nombre']}")
            else:
                print(f"  ⏩ {c['nombre']} (ya existe)")
        
        db.commit()
        
        # ============================================
        # RESUMEN
        # ============================================
        print("\n" + "="*50)
        print("✅ BASE DE DATOS INICIALIZADA CON ÉXITO")
        print("="*50)
        print(f"Deportes: {db.query(Deporte).count()}")
        print(f"Usuarios: {db.query(Usuario).count()}")
        print(f"Canchas: {db.query(Cancha).count()}")
        print("="*50)
        print("\n📝 Usuarios de prueba:")
        print("  Admin: admin@sportreserva.com / admin123")
        print("  Cliente: cliente@test.com / cliente123")
        print("="*50)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db()