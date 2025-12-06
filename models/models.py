from sqlalchemy import Table, Column, Integer, String, ForeignKey, DateTime, MetaData
from sqlalchemy.sql import func
from db.database import metadata

# Use the metadata from database.py
programa_estudio = Table(
    "programa_estudio", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("nombre", String(150), nullable=False),
    Column("numero_cuatrimestres", Integer, nullable=False)
)

cuatrimestre = Table(
    "cuatrimestre", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("numero", Integer, nullable=False),
    Column("programa_id", Integer, ForeignKey("programa_estudio.id"), nullable=False)
)

asignatura = Table(
    "asignatura", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("nombre", String(150), nullable=False),
    Column("cuatrimestre_id", Integer, ForeignKey("cuatrimestre.id"), nullable=False),
    Column("codigo", String(50))
)

docente = Table(
    "docente", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("nombre", String(150), nullable=False),
    Column("correo", String(200))
)

docente_asignatura = Table(
    "docente_asignatura", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("docente_id", Integer, ForeignKey("docente.id"), nullable=False),
    Column("asignatura_id", Integer, ForeignKey("asignatura.id"), nullable=False)
)

alumno = Table(
    "alumno", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("nombre", String(150), nullable=False),
    Column("matricula", String(20), nullable=False),
    Column("cuatrimestre", Integer, nullable=False),
    Column("correo", String(200))
)

alumno_asignatura = Table(
    "alumno_asignatura", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("alumno_id", Integer, ForeignKey("alumno.id"), nullable=False),
    Column("asignatura_id", Integer, ForeignKey("asignatura.id"), nullable=False)
)

grupo = Table(
    "grupo", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("nombre", String(50), nullable=False),
    Column("asignatura_id", Integer, ForeignKey("asignatura.id"), nullable=False),
    Column("docente_id", Integer, ForeignKey("docente.id"), nullable=False),
    Column("cuatrimestre_id", Integer, ForeignKey("cuatrimestre.id"), nullable=False),
    Column("capacidad", Integer, nullable=False, default=25)
)

grupo_alumno = Table(
    "grupo_alumno", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("grupo_id", Integer, ForeignKey("grupo.id"), nullable=False),
    Column("alumno_id", Integer, ForeignKey("alumno.id"), nullable=False),
    Column("fecha_matricula", DateTime, server_default=func.now)
)
