from fastapi import status
from models.factories import EstudiantesFactory
from models.tables import Estudiantes

def test_get_estudiante(client, session):
    # 1. ARRANGE: Create a real record in the Postgres test DB with one line!
    breakpoint()
    estudiante = EstudiantesFactory()
    
    # 2. Take the user and password of endpoint data
    login_data = {"usuario": estudiante.no_control, "password": "test"}
    login_response = client.post("/v1/login/", json=login_data)

    # 3. Extract the token
    token = login_response.json().get("data", {}).get("token")
    
    # 4. ACT: Call the API endpoint
    auth_headers = {"Authorization": f"Bearer {token}"}
    estudiante_response = client.get(f"/v1/estudiantes/{estudiante.no_control}", headers=auth_headers)

    # 5. ASSERT: 
    # Check if the API responded successfully
    breakpoint()
    assert estudiante_response.status_code == status.HTTP_200_OK
    api_data = estudiante_response.json()

    # 6. DATABASE COMPARISON:
    # Fetch the record directly from Postgres to verify
    breakpoint()
    db_record = session.query(Estudiantes).filter(Estudiantes.id == estudiante.id).first()

    # Compare API response against the Database record
    assert api_data["no_control"] == db_record.no_control
    assert api_data["nombre"] == db_record.nombre
    assert api_data["apellidos"] == db_record.apellidos
    assert api_data["fecha_nacimiento"] == db_record.fecha_nacimiento.isoformat()
    assert api_data["edad"] == db_record.edad
    assert api_data["semestre"] == db_record.semestre
    assert api_data["carrera"] == db_record.carrera
    assert api_data["municipio"] == db_record.municipio
    assert api_data["correo_institucional"] == db_record.correo_institucional
    assert api_data["fecha_registro"] == db_record.fecha_registro.isoformat()
    assert api_data["is_active"] == db_record.is_active