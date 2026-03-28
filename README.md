# Proyecto-API

# 🏟️ API de Reservas de Canchas Deportivas

> Backend para la gestión de reservas de canchas deportivas, desarrollado con FastAPI y SQLite.

---

## 📋 Tabla de Contenidos

- [Descripción General](#descripción-general)
- [Tecnologías Utilizadas](#tecnologías-utilizadas)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Requisitos Previos](#requisitos-previos)
- [Instalación y Configuración](#instalación-y-configuración)
- [Ejecución del Servidor](#ejecución-del-servidor)
- [Endpoints de la API](#endpoints-de-la-api)
- [Base de Datos y Migraciones](#base-de-datos-y-migraciones)
- [Principios SOLID Aplicados](#principios-solid-aplicados)
- [Evidencias de Funcionamiento](#evidencias-de-funcionamiento)
- [Contribuciones](#contribuciones)
- [Licencia](#licencia)

---

## 🎯 Descripción General

Este proyecto es una **API RESTful** para la gestión de reservas de canchas deportivas. Permite a los usuarios:

- ✅ Registrar y autenticarse en el sistema
- ✅ Visualizar canchas disponibles
- ✅ Crear, consultar y cancelar reservas
- ✅ Administrar horarios y disponibilidad

El backend está construido siguiendo los **principios SOLID**, garantizando un código limpio, mantenible y escalable.

---

## 🛠️ Tecnologías Utilizadas

| Categoría | Tecnología | Versión |
|-----------|------------|---------|
| **Lenguaje** | Python | 3.11+ |
| **Framework** | FastAPI | 0.115+ |
| **Servidor** | Uvicorn | 0.30+ |
| **ORM** | SQLAlchemy | 2.0+ |
| **Migraciones** | Alembic | 1.13+ |
| **Base de Datos** | SQLite | 3.x |
| **Validación** | Pydantic | 2.0+ |
| **Autenticación** | JWT / python-jose | - |
| **Gestor de Paquetes** | pip / venv | - |

---

## 📁 Estructura del Proyecto
proyecto-reservas-canchas/
├── backend/ # Backend principal
│ ├── alembic/ # Migraciones de base de datos
│ │ ├── versions/ # Archivos de migración
│ │ └── alembic.ini # Configuración de Alembic
│ ├── app/ # Código fuente de la aplicación
│ │ ├── models/ # Modelos SQLAlchemy
│ │ ├── schemas/ # Esquemas Pydantic (validación)
│ │ ├── routers/ # Endpoints de la API
│ │ ├── services/ # Lógica de negocio
│ │ ├── dependencies/ # Dependencias inyectables
│ │ ├── database.py # Configuración de BD
│ │ ├── config.py # Configuración general
│ │ └── main.py # Punto de entrada de FastAPI
│ ├── venv/ # Entorno virtual
│ ├── .env # Variables de entorno
│ ├── .env.example # Ejemplo de variables
│ ├── requirements.txt # Dependencias del proyecto
│ └── sportreserva.db # Base de datos SQLite
├── frontend/ # Frontend (React/Vue - pendiente)
├── docs/ # Documentación adicional
├── .gitignore # Archivos ignorados por Git
└── LICENSE # Licencia del proyecto


---

## ⚙️ Requisitos Previos

Asegúrate de tener instalado:

- **Python 3.11 o superior** ([Descargar](https://www.python.org/downloads/))
- **Git** ([Descargar](https://git-scm.com/))
- **Visual Studio Code** (recomendado) u otro editor

---

## 🚀 Instalación y Configuración

### 1. Clonar el repositorio

```bash
git clone https://github.com/Andrik2703/Proyecto-API.git
cd Proyecto-API/backend

📍 Endpoints de la API
Método	Ruta	Descripción	Autenticación
GET	/	Raíz de la API	No
GET	/health	Health check	No
GET	/docs	Documentación Swagger UI	No
GET	/redoc	Documentación ReDoc	No
POST	/auth/register	Registro de usuario	No
POST	/auth/login	Inicio de sesión (JWT)	No
GET	/api/canchas	Listar todas las canchas	Sí
GET	/api/canchas/{id}	Detalle de una cancha	Sí
POST	/api/reservas	Crear una reserva	Sí
GET	/api/reservas	Listar reservas del usuario	Sí
DELETE	/api/reservas/{id}	Cancelar una reserva	Sí

🧱 Principios SOLID Aplicados
Principio	Aplicación en el Proyecto
S (SRP)	Cada clase tiene una única responsabilidad: EmailValidator valida, SMTPSender envía, ReservaService maneja lógica de reservas
O (OCP)	Nuevos proveedores de email o formatos se agregan sin modificar código existente
L (LSP)	Todas las implementaciones de MessageService son intercambiables
I (ISP)	Interfaces pequeñas y específicas (MessageService, MessageFormatter, Validator)
D (DIP)	Módulos de alto nivel dependen de abstracciones, no de implementaciones concretas

🤝 Contribuciones
Las contribuciones son bienvenidas. Para contribuir:

Fork el repositorio

Crea una rama (git checkout -b feature/nueva-funcionalidad)

Commit tus cambios (git commit -m 'Agrega nueva funcionalidad')

Push a la rama (git push origin feature/nueva-funcionalidad)

Abre un Pull Request

📄 Licencia
Este proyecto está bajo la licencia MIT. Consulta el archivo LICENSE para más detalles.

👥 Autores
Nombre	Contacto
Andrik Bryan	GitHub
Conde Leal	GitHub
🙏 Agradecimientos
Documentación oficial de FastAPI

Guía de buenas prácticas de SQLAlchemy

Comunidad de Python por las herramientas y bibliotecas
