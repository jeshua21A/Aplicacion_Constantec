import os
import shutil

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.orm import Session

from comun.response import Response as CommonResponse
from database.connection import get_db
from models.tables import ComprobantesPago, Estudiantes

router = APIRouter()

# Carpeta donde se guardarán los PDFs
UPLOAD_DIR = "/app/uploads/comprobantes"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/factura", response_model=CommonResponse)
async def guardar_comprobante(no_control: str = Form(...), archivo: UploadFile = File(...), db: Session = Depends(get_db)):
    # 1. Verificar que el estudiante existe
    estudiante = db.query(Estudiantes).filter(Estudiantes.no_control == no_control).first()
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

    # 3. Validar si el archivo exite
    if not os.path.exists(UPLOAD_DIR):
        try:
            os.makedirs(UPLOAD_DIR, exist_ok=True)
        except Exception as ex:
            raise HTTPException(status_code=500, detail=f"No se pudo crear el directorio: {ex}")

    # 3. Crear nombre de archivo único (ej: 20130123_comprobante.pdf)
    extesion_archivo = (archivo.filename or "").split(".")[-1]
    nombre_archivo = f"{no_control}_comprobante.{extesion_archivo}"
    ruta_archivo = f"{UPLOAD_DIR}/{nombre_archivo}"

    # 4. Guardar el archivo físicamente
    try:
        with open(ruta_archivo, "wb") as buffer:
            shutil.copyfileobj(archivo.file, buffer)
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Error al escribir el archivo: {str(ex)}")
    finally:
        archivo.file.close()

    # 5. Guardar en la base de datos
    nuevo_comprobante = ComprobantesPago(factura=nombre_archivo, id_estado_comprobante=2, id_estudiante=estudiante.id)

    db.add(nuevo_comprobante)
    db.commit()
    db.refresh(nuevo_comprobante)

    return CommonResponse(
        data={"id": nuevo_comprobante.id, "archivo": nombre_archivo, "estado": nuevo_comprobante.id_estado_comprobante},
        success=True,
        message="Comprobante guardado exitosamente",
        error_code=None,
    )


@router.get("/{no_control}")
def obtener_estado_pago(no_control: str, db: Session = Depends(get_db)):
    estudiante = db.query(Estudiantes).filter(Estudiantes.no_control == no_control).first()

    if estudiante is None:
        return {"estado": 1, "mensaje": "Estudiante no encontrado"}

    # Buscamos el último comprobante subido
    stmt = select(ComprobantesPago).where(ComprobantesPago.id_estudiante == estudiante.id).order_by(ComprobantesPago.id.desc())
    comprobante = db.execute(stmt).scalars().first()

    if comprobante is None:
        return {"estado": 1, "mensaje": "No se encontraron comprobantes"}

    return {"estado": comprobante.id_estado_comprobante, "motivo_rechazo": comprobante.motivo_rechazo, "archivoNombre": comprobante.factura}
