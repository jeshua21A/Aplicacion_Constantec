from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from autenticacion.seguridad import get_current_user
from consultas.consulta_estudiante import guardar_encuesta_estudiante
from database.connection import get_db
from models.tables import EncuestaSatisfaccion
from paquetes import schemas

router = APIRouter()

@router.post("/", response_model=schemas.EncuestaSatisfaccionSalida)
def guardar_encuesta(
    data_encuesta: schemas.EncuestaSatisfaccionCreate,
    db: Session = Depends(get_db),
    auth_user: dict[str, Any] = Depends(get_current_user),
):
    encuesta = guardar_encuesta_estudiante(db, data_encuesta.id_estudiante, data_encuesta.calificacion, data_encuesta.sugerencia)
    return encuesta


@router.get("/verificar/{id_estudiante}")
def verificar_encuesta(id_estudiante: int, db: Session = Depends(get_db)):
    existe = db.query(EncuestaSatisfaccion).filter(EncuestaSatisfaccion.id_estudiante == id_estudiante).first()
    return {"completada": existe is not None}
