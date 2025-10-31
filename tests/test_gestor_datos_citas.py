import csv
import pytest
from Controlador import gestor_datos_citas as gestor

# TEST CRUD CITAS JSON
def test_crud_citas_json(tmp_path):
    filepath = tmp_path / "citas.json"

    # Inicializar archivo
    gestor.inicializar_archivo(str(filepath))

    cita = {
        "id": 1,
        "documento_paciente": "12345678",
        "documento_medico": "87654321",
        "fecha": "2025-10-28",
        "hora": "08:00",
        "motivo": "Chequeo",
        "estado": "pendiente"
    }

    # CREAR: agregar cita
    datos = gestor.cargar_datos(str(filepath))
    datos.append(cita)
    gestor.guardar_datos(str(filepath), datos)

    # LEER
    citas = gestor.cargar_datos(str(filepath))
    assert len(citas) == 1
    assert citas[0]["id"] == 1

    # ACTUALIZAR
    for c in citas:
        if str(c["id"]) == "1":
            c["estado"] = "completada"
    gestor.guardar_datos(str(filepath), citas)

    citas = gestor.cargar_datos(str(filepath))
    assert citas[0]["estado"] == "completada"

    # ELIMINAR
    citas = [c for c in citas if str(c["id"]) != "1"]
    gestor.guardar_datos(str(filepath), citas)

    citas = gestor.cargar_datos(str(filepath))
    assert len(citas) == 0


# TEST CRUD CITAS CSV

def test_crud_citas_csv(tmp_path):
    filepath = tmp_path / "citas.csv"

    # Inicializar archivo
    gestor.inicializar_archivo(str(filepath))

    cita = {
        "id": 2,
        "documento_paciente": "23456789",
        "documento_medico": "98765432",
        "fecha": "2025-10-29",
        "hora": "09:00",
        "motivo": "Revisión",
        "estado": "pendiente"
    }

    # CREAR: agregar cita
    datos = gestor.cargar_datos(str(filepath))
    datos.append(cita)
    gestor.guardar_datos(str(filepath), datos)
    
    # LEER
    citas = gestor.cargar_datos(str(filepath))
    assert len(citas) == 1
    assert int(citas[0]["id"]) == 2 


    # ACTUALIZAR
    for c in citas:
        if str(c["id"]) == "2":
            c["estado"] = "completada"
    gestor.guardar_datos(str(filepath), citas)

    citas = gestor.cargar_datos(str(filepath))
    assert citas[0]["estado"] == "completada"

    # ELIMINAR
    citas = [c for c in citas if str(c["id"]) != "2"]
    gestor.guardar_datos(str(filepath), citas)

    citas = gestor.cargar_datos(str(filepath))
    assert len(citas) == 0
