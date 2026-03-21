# 🏟️ Modelado del Dominio - SportReserva

## 📋 Descripción del Dominio

SportReserva es un sistema de reservas de canchas deportivas que permite a los usuarios buscar, reservar y pagar por el uso de instalaciones deportivas. El sistema gestiona usuarios, canchas, deportes, reservas y pagos.

## 🎯 Problema que Resuelve

Facilita la reserva de espacios deportivos, evitando conflictos de horarios y permitiendo a los usuarios gestionar sus reservas de manera eficiente desde cualquier dispositivo.

## 👥 Usuarios Objetivo

- **Clientes**: Personas que desean reservar canchas para practicar deportes
- **Administradores**: Gestionan el catálogo de canchas y supervisan reservas

## 📊 Entidades Principales (5+)

### 1. **Usuario**
- **Descripción**: Representa a las personas que utilizan el sistema
- **Atributos**: 
  - `id` (PK): Identificador único
  - `email`: Correo electrónico (único)
  - `username`: Nombre de usuario (único)
  - `nombre_completo`: Nombre completo
  - `telefono`: Número de contacto (formato: 229-133-9124)
  - `hashed_password`: Contraseña cifrada
  - `role`: Rol (admin/cliente)
  - `is_active`: Estado de la cuenta
  - `created_at`: Fecha de registro
  - `updated_at`: Última actualización

### 2. **Deporte**
- **Descripción**: Catálogo de deportes disponibles
- **Atributos**:
  - `id` (PK): Identificador único
  - `nombre`: Nombre del deporte (fútbol, tenis, etc.) - único
  - `descripcion`: Descripción del deporte
  - `icono`: Clase de FontAwesome para el icono
  - `created_at`, `updated_at`: Timestamps

### 3. **Cancha**
- **Descripción**: Instalaciones deportivas disponibles para reserva
- **Atributos**:
  - `id` (PK): Identificador único
  - `nombre`: Nombre de la cancha
  - `deporte_id` (FK): Deporte que se practica
  - `ciudad`: Ubicación (madrid, barcelona, valencia)
  - `ubicacion`: Dirección específica
  - `precio_por_hora`: Costo por hora (mayor a 0)
  - `descripcion`: Características
  - `imagen_url`: URL de la imagen
  - `horario_apertura`: Hora de apertura (HH:MM)
  - `horario_cierre`: Hora de cierre (HH:MM)
  - `is_active`: Disponibilidad
  - `created_at`, `updated_at`: Timestamps

### 4. **Reserva** (Entidad principal del negocio)
- **Descripción**: Núcleo del sistema, conecta usuarios con canchas
- **Atributos**:
  - `id` (PK): Identificador único
  - `usuario_id` (FK): Usuario que reserva
  - `cancha_id` (FK): Cancha reservada
  - `fecha`: Día de la reserva
  - `hora_inicio`: Hora de inicio (HH:MM)
  - `duracion_horas`: Duración (1-3 horas)
  - `precio_total`: Precio calculado (precio_hora × duración)
  - `estado`: pendiente/confirmada/cancelada/completada
  - `notas`: Comentarios adicionales
  - `created_at`, `updated_at`: Timestamps

### 5. **Pago** (Entidad de detalle)
- **Descripción**: Transacciones asociadas a reservas
- **Atributos**:
  - `id` (PK): Identificador único
  - `reserva_id` (FK - único): Reserva asociada
  - `usuario_id` (FK): Usuario que paga
  - `monto`: Cantidad pagada
  - `metodo_pago`: tarjeta/efectivo/transferencia
  - `estado`: pendiente/completado/fallido/reembolsado
  - `transaction_id`: ID único de transacción
  - `created_at`, `updated_at`: Timestamps

## 🔗 Relaciones

| Relación | Tipo | Descripción |
|----------|------|-------------|
| Usuario → Reserva | 1:N | Un usuario puede tener múltiples reservas |
| Cancha → Reserva | 1:N | Una cancha puede tener múltiples reservas (diferentes horarios) |
| Deporte → Cancha | 1:N | Un deporte puede tener múltiples canchas |
| Reserva → Pago | 1:1 | Cada reserva tiene un único pago asociado |

## 🛡️ Reglas de Integridad

### Unique Constraints
```sql
- UNIQUE(usuarios.email)
- UNIQUE(usuarios.username)
- UNIQUE(deportes.nombre)
- UNIQUE(pagos.transaction_id)
- UNIQUE(pagos.reserva_id)  -- Relación 1:1


Check Constraints
sql
- CHECK (canchas.precio_por_hora > 0)
- CHECK (reservas.duracion_horas BETWEEN 1 AND 3)
- CHECK (reservas.fecha >= CURRENT_DATE)  -- No reservas en pasado
Not Null
Todos los campos principales son obligatorios

Foreign Keys siempre referencian registros existentes

Default Values
is_active = true para usuarios y canchas

estado = 'pendiente' para nuevas reservas

created_at = CURRENT_TIMESTAMP para todos los registros

📈 Decisiones Clave de Diseño
1. Soft Delete vs Hard Delete
Usuarios y canchas usan soft delete (is_active)

Reservas y pagos mantienen historial completo (nunca se eliminan)

2. Timestamps en Todas las Tablas
created_at: Auditoría de creación

updated_at: Seguimiento de modificaciones

3. Enums para Estados

UserRole = ["admin", "cliente"]
ReservaStatus = ["pendiente", "confirmada", "cancelada", "completada"]
PagoStatus = ["pendiente", "completado", "fallido", "reembolsado"]
4. Índices para Optimización
Índices en todas las claves primarias

Índices en campos de búsqueda: email, username, ciudad, fecha

5. Cálculo Automático
precio_total se calcula en backend: cancha.precio_por_hora * duracion_horas

💡 Supuestos Asumidos
Horarios: Formato 24h (HH:MM), ej: "18:00"

Duración: Mínimo 1 hora, máximo 3 horas por reserva

Anticipación: Las reservas se hacen con al menos 1 día de anticipación

Zona horaria: Todo en UTC, el frontend maneja conversión

Teléfono: Formato estándar "229-133-9124" (10 dígitos)

Pagos: Se procesan externamente, solo registramos el resultado

Cancelaciones: Solo el propietario puede cancelar su reserva

Estados: Flujo unidireccional (pendiente → confirmada → completada/cancelada)

✅ Validaciones de Negocio Implementadas
No se pueden crear reservas en fechas pasadas

No puede haber dos reservas en la misma cancha a la misma hora

El email debe ser único por usuario

El username debe ser único

La hora de inicio debe estar dentro del horario de la cancha

El precio por hora debe ser positivo

La duración debe ser entre 1 y 3 horas

Solo usuarios autenticados pueden reservar

Solo el dueño de la reserva puede cancelarla

📊 Normalización
Base de datos en 3FN (Tercera Forma Normal):

✅ Sin dependencias transitivas

✅ Sin redundancia de datos

✅ Claves foráneas correctamente definidas

✅ Tablas independientes para catálogos (deportes)