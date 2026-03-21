// Datos de ejemplo de canchas
const canchas = [
    {
        id: 1,
        nombre: "Cancha de Fútbol 7",
        deporte: "futbol",
        ciudad: "madrid",
        ubicacion: "Madrid Centro",
        precio: 50,
        imagen: "https://images.unsplash.com/photo-1459865264687-595d652de67e?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80",
        descripcion: "Cancha de césped artificial con iluminación LED",
        horario: "9:00 - 22:00"
    },
    {
        id: 2,
        nombre: "Pista de Tenis",
        deporte: "tenis",
        ciudad: "barcelona",
        ubicacion: "Barcelona Norte",
        precio: 35,
        imagen: "https://images.unsplash.com/photo-1595435934249-5df7ed86e1c0?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80",
        descripcion: "Pista de tenis de tierra batida",
        horario: "8:00 - 21:00"
    },
    {
        id: 3,
        nombre: "Cancha de Pádel",
        deporte: "padel",
        ciudad: "valencia",
        ubicacion: "Valencia Sur",
        precio: 25,
        imagen: "https://images.unsplash.com/photo-1626224583764-f87db24ac4ea?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80",
        descripcion: "Cancha de pádel cubierta con cristal",
        horario: "10:00 - 23:00"
    },
    {
        id: 4,
        nombre: "Cancha de Baloncesto",
        deporte: "baloncesto",
        ciudad: "madrid",
        ubicacion: "Madrid Este",
        precio: 40,
        imagen: "https://images.unsplash.com/photo-1504450758481-7338eba7524c?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80",
        descripcion: "Cancha cubierta con parquet",
        horario: "9:00 - 22:00"
    }
];

// Array para almacenar reservas
let reservas = [];

// Función para formatear teléfono mientras se escribe
function formatearTelefono(input) {
    let valor = input.value.replace(/\D/g, ''); // Eliminar no dígitos
    
    if (valor.length <= 10) {
        if (valor.length > 6) {
            valor = valor.replace(/^(\d{3})(\d{3})(\d{0,4})/, '$1-$2-$3');
        } else if (valor.length > 3) {
            valor = valor.replace(/^(\d{3})(\d{0,3})/, '$1-$2');
        }
    }
    
    input.value = valor;
}

// Función para cargar canchas
function cargarCanchas() {
    const grid = document.getElementById('canchas-grid');
    grid.innerHTML = '';
    
    canchas.forEach(cancha => {
        const card = `
            <div class="col-lg-3 col-md-6">
                <div class="card h-100">
                    <img src="${cancha.imagen}" class="card-img-top" alt="${cancha.nombre}">
                    <div class="card-body">
                        <h5 class="card-title">${cancha.nombre}</h5>
                        <p class="card-text">
                            <i class="fas fa-map-marker-alt"></i> ${cancha.ubicacion}<br>
                            <i class="fas fa-clock"></i> ${cancha.horario}<br>
                            <i class="fas fa-info-circle"></i> ${cancha.descripcion}
                        </p>
                        <div class="d-flex justify-content-between align-items-center">
                            <span class="precio">€${cancha.precio}/hora</span>
                            <span class="badge bg-success">${cancha.deporte}</span>
                        </div>
                    </div>
                    <div class="card-footer bg-white border-0">
                        <button class="btn btn-success w-100" onclick="abrirModalReserva(${cancha.id})">
                            <i class="fas fa-calendar-check me-2"></i>Reservar
                        </button>
                    </div>
                </div>
            </div>
        `;
        grid.innerHTML += card;
    });
}

// Función para abrir modal de reserva
function abrirModalReserva(canchaId) {
    const cancha = canchas.find(c => c.id === canchaId);
    document.getElementById('canchaNombre').value = cancha.nombre;
    
    // Guardar ID de cancha en un atributo data del modal
    const modal = document.getElementById('reservaModal');
    modal.setAttribute('data-cancha-id', canchaId);
    
    // Establecer fecha mínima como hoy
    const hoy = new Date().toISOString().split('T')[0];
    document.getElementById('fechaReserva').min = hoy;
    
    // Abrir modal
    const reservaModal = new bootstrap.Modal(document.getElementById('reservaModal'));
    reservaModal.show();
}

// Función para guardar reserva
function guardarReserva() {
    const canchaId = document.getElementById('reservaModal').getAttribute('data-cancha-id');
    const cancha = canchas.find(c => c.id == canchaId);
    
    const reserva = {
        id: Date.now(),
        canchaId: canchaId,
        canchaNombre: cancha.nombre,
        fecha: document.getElementById('fechaReserva').value,
        horaInicio: document.getElementById('horaInicio').value,
        duracion: document.getElementById('duracion').value,
        nombre: document.getElementById('nombreReserva').value,
        telefono: document.getElementById('telefonoReserva').value,
        email: document.getElementById('emailReserva').value,
        precioTotal: cancha.precio * parseInt(document.getElementById('duracion').value)
    };
    
    // Validar campos
    if (!validarReserva(reserva)) {
        return;
    }
    
    reservas.push(reserva);
    guardarEnLocalStorage();
    
    // Mostrar mensaje de éxito
    alert('¡Reserva confirmada! Precio total: €' + reserva.precioTotal);
    
    // Cerrar modal
    const modal = bootstrap.Modal.getInstance(document.getElementById('reservaModal'));
    modal.hide();
    
    // Limpiar formulario
    document.getElementById('formReserva').reset();
    
    // Actualizar la vista de mis reservas
    mostrarMisReservas();
}

// Función de validación
function validarReserva(reserva) {
    if (!reserva.fecha || !reserva.horaInicio || !reserva.nombre || !reserva.telefono || !reserva.email) {
        alert('Por favor, complete todos los campos');
        return false;
    }
    
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(reserva.email)) {
        alert('Por favor, ingrese un email válido');
        return false;
    }
    
    // Validar teléfono con formato xxx-xxx-xxxx (10 dígitos)
    const telefonoRegex = /^\d{3}-\d{3}-\d{4}$/;
    if (!telefonoRegex.test(reserva.telefono)) {
        alert('Por favor, ingrese un teléfono válido con formato: 229-133-9124 (10 dígitos)');
        return false;
    }
    
    return true;
}

// NUEVA FUNCIÓN: Mostrar mis reservas
function mostrarMisReservas() {
    const container = document.getElementById('reservas-container');
    const sinReservas = document.getElementById('sin-reservas');
    
    if (reservas.length === 0) {
        container.innerHTML = '';
        sinReservas.classList.remove('d-none');
        return;
    }
    
    sinReservas.classList.add('d-none');
    container.innerHTML = '';
    
    reservas.forEach(reserva => {
        // Formatear fecha
        const fecha = new Date(reserva.fecha);
        const fechaFormateada = fecha.toLocaleDateString('es-ES', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
        
        const card = `
            <div class="col-md-6 mb-4">
                <div class="card h-100 border-success">
                    <div class="card-header bg-success text-white d-flex justify-content-between align-items-center">
                        <h5 class="mb-0">${reserva.canchaNombre}</h5>
                        <span class="badge bg-light text-success">Confirmada</span>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            <div class="col-6">
                                <p class="mb-2">
                                    <i class="fas fa-calendar text-success me-2"></i>
                                    <strong>Fecha:</strong><br>
                                    ${fechaFormateada}
                                </p>
                                <p class="mb-2">
                                    <i class="fas fa-clock text-success me-2"></i>
                                    <strong>Hora:</strong><br>
                                    ${reserva.horaInicio} (${reserva.duracion} hora${reserva.duracion > 1 ? 's' : ''})
                                </p>
                            </div>
                            <div class="col-6">
                                <p class="mb-2">
                                    <i class="fas fa-user text-success me-2"></i>
                                    <strong>Reservado por:</strong><br>
                                    ${reserva.nombre}
                                </p>
                                <p class="mb-2">
                                    <i class="fas fa-phone text-success me-2"></i>
                                    <strong>Teléfono:</strong><br>
                                    ${reserva.telefono}
                                </p>
                            </div>
                        </div>
                        <hr>
                        <div class="d-flex justify-content-between align-items-center">
                            <div>
                                <i class="fas fa-envelope text-success me-2"></i>
                                ${reserva.email}
                            </div>
                            <h5 class="text-success mb-0">€${reserva.precioTotal}</h5>
                        </div>
                    </div>
                    <div class="card-footer bg-white">
                        <button class="btn btn-outline-danger btn-sm" onclick="cancelarReserva(${reserva.id})">
                            <i class="fas fa-times me-1"></i>Cancelar Reserva
                        </button>
                    </div>
                </div>
            </div>
        `;
        container.innerHTML += card;
    });
}

// Función para cancelar reserva
function cancelarReserva(id) {
    if (confirm('¿Estás seguro de que deseas cancelar esta reserva?')) {
        reservas = reservas.filter(r => r.id !== id);
        guardarEnLocalStorage();
        mostrarMisReservas();
        alert('Reserva cancelada exitosamente');
    }
}

// Guardar en localStorage
function guardarEnLocalStorage() {
    localStorage.setItem('reservas', JSON.stringify(reservas));
}

// Cargar reservas del localStorage
function cargarReservas() {
    const reservasGuardadas = localStorage.getItem('reservas');
    if (reservasGuardadas) {
        reservas = JSON.parse(reservasGuardadas);
    }
}

// Event listeners para filtros
document.getElementById('filtroDeporte').addEventListener('change', filtrarCanchas);
document.getElementById('filtroCiudad').addEventListener('change', filtrarCanchas);
document.getElementById('filtroFecha').addEventListener('change', filtrarCanchas);

function filtrarCanchas() {
    const deporte = document.getElementById('filtroDeporte').value;
    const ciudad = document.getElementById('filtroCiudad').value;
    const fecha = document.getElementById('filtroFecha').value;
    
    const canchasFiltradas = canchas.filter(cancha => {
        let cumpleDeporte = !deporte || cancha.deporte === deporte;
        let cumpleCiudad = !ciudad || cancha.ciudad === ciudad;
        return cumpleDeporte && cumpleCiudad;
    });
    
    mostrarCanchasFiltradas(canchasFiltradas);
}

function mostrarCanchasFiltradas(canchasFiltradas) {
    const grid = document.getElementById('canchas-grid');
    grid.innerHTML = '';
    
    if (canchasFiltradas.length === 0) {
        grid.innerHTML = '<div class="col-12 text-center"><p class="lead">No hay canchas disponibles con esos filtros</p></div>';
        return;
    }
    
    canchasFiltradas.forEach(cancha => {
        const card = `
            <div class="col-lg-3 col-md-6">
                <div class="card h-100">
                    <img src="${cancha.imagen}" class="card-img-top" alt="${cancha.nombre}">
                    <div class="card-body">
                        <h5 class="card-title">${cancha.nombre}</h5>
                        <p class="card-text">
                            <i class="fas fa-map-marker-alt"></i> ${cancha.ubicacion}<br>
                            <i class="fas fa-clock"></i> ${cancha.horario}<br>
                            <i class="fas fa-info-circle"></i> ${cancha.descripcion}
                        </p>
                        <div class="d-flex justify-content-between align-items-center">
                            <span class="precio">€${cancha.precio}/hora</span>
                            <span class="badge bg-success">${cancha.deporte}</span>
                        </div>
                    </div>
                    <div class="card-footer bg-white border-0">
                        <button class="btn btn-success w-100" onclick="abrirModalReserva(${cancha.id})">
                            <i class="fas fa-calendar-check me-2"></i>Reservar
                        </button>
                    </div>
                </div>
            </div>
        `;
        grid.innerHTML += card;
    });
}

// Inicialización
document.addEventListener('DOMContentLoaded', function() {
    cargarReservas();
    cargarCanchas();
    mostrarMisReservas(); // Mostrar reservas al cargar la página
    
    // Establecer fecha actual como valor por defecto en el filtro
    const hoy = new Date().toISOString().split('T')[0];
    document.getElementById('filtroFecha').value = hoy;
});