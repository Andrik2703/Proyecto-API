# 🚀 Documentación de Proyecto: API Backend & Infraestructura

## 1. Información General
* **Nombre del Proyecto:** [proyecto-reservas-canchas]
* **Integrantes:** * [Andrik_Bryan]
    * [Conde_Leal]
* **Repositorio (GitHub/GitLab):** https://github.com/Andrik2703/Proyecto-API.git
* **Fecha de Entrega:** [28/03/2026]

---

## 2. Arquitectura y Stack Tecnológico
* **Detalla las herramientas utilizadas para construir y desplegar la solución:**

* **Lenguaje de Programación: Python 3.11+**

* **Framework: FastAPI / Uvicorn**

* **Gestor de Base de Datos: SQLite (archivo sportreserva) con SQLAlchemy + Alembic**

* **Ubicación de la DB: Local (archivo en backend/)**

### Diagrama de Flujo (Texto)
`[Cliente/Postman] --(Petición HTTP)--> [Servidor Uvicorn (FastAPI)] --(SQLAlchemy ORM)--> [Base de Datos SQLite]`

---

## 3. Configuración de Infraestructura (Docker)
* **Nota: El proyecto actualmente corre de forma nativa con entorno virtual Python, no con Docker.**

* **Entorno Virtual: Python venv**

* **Puerto Expuesto: 8000**

* **Comando de ejecución:**
* **cd backend**
* **venv\Scripts\activate**
* **python -m uvicorn app.main:app --reload**

### Variables de Entorno (.env)
*Copia aquí las llaves (nombres) que utiliza tu proyecto para funcionar (no incluyas contraseñas reales):*
* **DB_URL=sqlite:///./sportreserva.db**
* **SECRET_KEY=tu_clave_secreta**
* **ALGORITHM=HS256**
* **ACCESS_TOKEN_EXPIRE_MINUTES=30**
---

## 4. Documentación de Endpoints
**Nota: Los endpoints deben agregarse en app/routers/. Se sugiere crear un router de health check para evidenciar funcionamiento.**

Método	Ruta	Descripción	Cuerpo (JSON) / Params	Respuesta (200 OK)
GET	/	Raíz de la API	N/A	{"message": "Bienvenido a la API de Reservas de Canchas", "status": "running"}
GET	/health	Verifica salud de API y DB	N/A	{"status": "healthy", "database": "connected"}
GET	/docs	Documentación Swagger	N/A	Interfaz Swagger UI

---

## 5. Evidencias de Funcionamiento
*(Instrucciones: Pega aquí las capturas de pantalla de tu terminal o herramientas)*


### A. Contenedores en Ejecución
> [Pega aquí captura de `docker ps` o Docker Desktop donde se vea el contenedor activo]

### B. Conexión a Base de Datos
> [Pega aquí captura de los logs de la consola donde se confirme la conexión exitosa a la DB]

### C. Prueba de Endpoint (Postman/Thunder Client)
> [Pega aquí captura de una petición exitosa a uno de tus endpoints]

---

## 6. Reflexión y Autoevaluación

⚡ Retos del Proyecto
Mayor dificultad técnica: Configurar correctamente el entorno virtual y que Uvicorn detectara la aplicación FastAPI. Inicialmente hubo problemas con la estructura de importaciones y la activación del venv en Windows.

Solución aplicada: Se verificó la estructura del proyecto, se usó la ruta correcta (app.main:app) y se confirmó que el archivo app/main.py existiera con la instancia app = FastAPI(). Se ejecutó pip install -r requirements.txt dentro del venv.

🎓 Experiencia en la Clase de Backend
Análisis Personal: Lo que más se me ha dificultado es comprender la diferencia entre los principios SOLID aplicados en código real y cómo estructurar un proyecto limpio desde cero.

Causa del Bloqueo: Me cuesta trabajo visualizar cómo dividir responsabilidades en capas (routers, services, models) sin que se vuelva confuso. Además, la configuración de entornos virtuales y variables de entorno fue nueva para mí.

Sugerencia de Mejora: Sería de gran ayuda tener más ejemplos de proyectos completos (tipo "template") que sigan buenas prácticas, para poder usarlos como referencia. También explicaciones más visuales de cómo interactúan las capas (diagramas de flujo).
---

## 7. Estado Final del Proyecto
Estatus: El proyecto corre localmente en entorno virtual con FastAPI y SQLite. El servidor se levanta correctamente en http://127.0.0.1:8000. Queda pendiente agregar más endpoints de negocio y migrar a Docker para despliegue.