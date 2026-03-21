"""initial migration

Revision ID: 001
Revises: 
Create Date: 2024-01-01

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Crear tipo ENUM para roles de usuario
    op.execute("CREATE TYPE userrole AS ENUM ('admin', 'cliente')")
    
    # Crear tabla deportes
    op.create_table('deportes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nombre', sa.String(length=50), nullable=False),
        sa.Column('descripcion', sa.Text(), nullable=True),
        sa.Column('icono', sa.String(length=50), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('nombre')
    )
    
    # Crear tabla usuarios
    op.create_table('usuarios',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=100), nullable=False),
        sa.Column('username', sa.String(length=50), nullable=False),
        sa.Column('nombre_completo', sa.String(length=100), nullable=False),
        sa.Column('telefono', sa.String(length=20), nullable=True),
        sa.Column('hashed_password', sa.String(length=200), nullable=False),
        sa.Column('role', sa.Enum('ADMIN', 'CLIENTE', name='userrole'), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True, server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_usuarios_email'), 'usuarios', ['email'], unique=True)
    op.create_index(op.f('ix_usuarios_id'), 'usuarios', ['id'], unique=False)
    op.create_index(op.f('ix_usuarios_username'), 'usuarios', ['username'], unique=True)
    
    # Crear tabla canchas
    op.create_table('canchas',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nombre', sa.String(length=100), nullable=False),
        sa.Column('deporte_id', sa.Integer(), nullable=False),
        sa.Column('ciudad', sa.String(length=50), nullable=False),
        sa.Column('ubicacion', sa.String(length=200), nullable=False),
        sa.Column('precio_por_hora', sa.Float(), nullable=False),
        sa.Column('descripcion', sa.Text(), nullable=True),
        sa.Column('imagen_url', sa.String(length=500), nullable=True),
        sa.Column('horario_apertura', sa.String(length=5), nullable=True),
        sa.Column('horario_cierre', sa.String(length=5), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True, server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['deporte_id'], ['deportes.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_canchas_id'), 'canchas', ['id'], unique=False)
    
    # Crear tabla reservas
    op.create_table('reservas',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('usuario_id', sa.Integer(), nullable=False),
        sa.Column('cancha_id', sa.Integer(), nullable=False),
        sa.Column('fecha', sa.DateTime(), nullable=False),
        sa.Column('hora_inicio', sa.String(length=5), nullable=False),
        sa.Column('duracion_horas', sa.Integer(), nullable=False),
        sa.Column('precio_total', sa.Float(), nullable=False),
        sa.Column('estado', sa.Enum('PENDIENTE', 'CONFIRMADA', 'CANCELADA', 'COMPLETADA', name='reservastatus'), nullable=True),
        sa.Column('notas', sa.String(length=500), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['cancha_id'], ['canchas.id'], ),
        sa.ForeignKeyConstraint(['usuario_id'], ['usuarios.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_reservas_id'), 'reservas', ['id'], unique=False)
    
    # Agregar check constraint para fecha no pasada
    op.execute(
        "ALTER TABLE reservas ADD CONSTRAINT reserva_fecha_no_pasado CHECK (fecha >= CURRENT_DATE)"
    )
    
    # Crear tabla pagos
    op.create_table('pagos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('reserva_id', sa.Integer(), nullable=False),
        sa.Column('usuario_id', sa.Integer(), nullable=False),
        sa.Column('monto', sa.Float(), nullable=False),
        sa.Column('metodo_pago', sa.String(length=50), nullable=True),
        sa.Column('estado', sa.Enum('PENDIENTE', 'COMPLETADO', 'FALLIDO', 'REEMBOLSADO', name='pagostatus'), nullable=True),
        sa.Column('transaction_id', sa.String(length=100), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['reserva_id'], ['reservas.id'], ),
        sa.ForeignKeyConstraint(['usuario_id'], ['usuarios.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('reserva_id'),
        sa.UniqueConstraint('transaction_id')
    )
    op.create_index(op.f('ix_pagos_id'), 'pagos', ['id'], unique=False)

def downgrade():
    op.drop_table('pagos')
    op.drop_table('reservas')
    op.drop_table('canchas')
    op.drop_table('usuarios')
    op.drop_table('deportes')
    
    # Eliminar tipos ENUM
    op.execute('DROP TYPE userrole')
    op.execute('DROP TYPE reservastatus')
    op.execute('DROP TYPE pagostatus')