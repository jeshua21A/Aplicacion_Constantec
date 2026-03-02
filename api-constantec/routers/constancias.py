from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from autenticacion.seguridad import get_current_user
from database.connection import get_db
from models.tables import Constancias
from paquetes import schemas

router = APIRouter()

@router.get("/constancias", response_model=list[schemas.ConstanciaSalida])
def listar_constancias(db: Session = Depends(get_db), auth_user: dict[str, Any] = Depends(get_current_user)):
    return db.query(Constancias).all()


@router.get("/{id_constancia}", response_model=schemas.ConstanciaSalida)
def buscar_constancia(id_constancia: str, db: Session = Depends(get_db), auth_user: dict[str, Any] = Depends(get_current_user)):
    constancia = db.query(Constancias).filter(Constancias.id == id_constancia).first()
    if not constancia:
        raise HTTPException(detail="Constancia no encontrada", status_code=404)
    return constancia
