from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from autenticacion.seguridad import get_current_user
from consultas.consulta_estudiante import obtener_estudiante_por_no_control
from database.connection import get_db
from models.tables import Estudiantes
from paquetes import schemas

router = APIRouter()

@router.get("/{no_control}", response_model=schemas.EstudiantesSalida)
def buscar_perfil(no_control: str, db: Session = Depends(get_db), auth_user: dict[str, Any] = Depends(get_current_user)):
    estudiante = obtener_estudiante_por_no_control(db, no_control)
    if not estudiante:
        raise HTTPException(detail="Estudiante no encontrado", status_code=404)

    if estudiante.no_control != auth_user.get("sub"):
        raise HTTPException(detail="Numero de control no coincide con el estudiante", status_code=404)

    return estudiante


@router.get("/todos_estudiantes", response_model=list[schemas.EstudiantesSalida])
def listar_estudiantes(db: Session = Depends(get_db), auth_user: dict[str, Any] = Depends(get_current_user)):
    current_no_control = auth_user.get("sub")

    estudiantes = db.query(Estudiantes).filter(Estudiantes.no_control == current_no_control).all()

    if not estudiantes:
        raise HTTPException(detail="Estudiantes no encontrados", status_code=404)

    return estudiantes
