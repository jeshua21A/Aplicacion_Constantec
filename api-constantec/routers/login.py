import logging

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from autenticacion.seguridad import create_access_token, verify_password
from comun.response import Response as CommonResponse
from consultas.consulta_administrador import obtener_administrador_por_id
from consultas.consulta_estudiante import obtener_estudiante_por_no_control
from database.connection import get_db
from paquetes import schemas

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/", response_model=CommonResponse)
async def login_for_access_token(login_request: schemas.LoginRequest, response: Response, db: Session = Depends(get_db)):
    usuario = None
    tipo = None

    """
    Authenticates a user with username and password and returns a JWT.
    Client should send credentials as 'application/x-www-form-urlencoded'.
    """
    try:
        if login_request.usuario.isdigit():
            usuario = obtener_estudiante_por_no_control(db, login_request.usuario)
            tipo = "estudiante" if usuario else None
        else:
            usuario = obtener_administrador_por_id(db, login_request.usuario)
            tipo = "admin" if usuario else None

        if usuario is None:
            raise HTTPException(detail="Usuario no encontrado", status_code=status.HTTP_404_NOT_FOUND)

        logging.debug(usuario.password)
        if not verify_password(login_request.password, usuario.password):
            raise HTTPException(detail="Password incorrecto", status_code=status.HTTP_401_UNAUTHORIZED)

    except Exception as ex:
        raise ex

    # 3. Los usuarios son autenticados con JWT
    access_token_payload = {
        "sub": login_request.usuario,
        "tipo": tipo,
    }
    access_token = create_access_token(jwt_payload=access_token_payload)

    response.set_cookie(key="access_token", value=access_token, httponly=True, path="/")

    # Devolvemos la respuesta, comprobando si es un administrador
    return CommonResponse(data={"token": access_token, "id_estudiante": usuario.id, "tipo": tipo}, success=True, message="autenticacion exitosa", error_code=None)
