# -*- coding: utf-8 -*-
from Controlador import gestor_datos_medico as medico


def test_crud_medico_json(tmp_path):
    filepath = tmp_path / "medicos.json"

    # Crear lista de médicos
    medicos = [
        {
            "id": "1",
            "tipo_documento": "CC",
            "documento": 1023456789,
            "nombres": "Laura",
            "apellidos": "Pérez Gómez",
            "direccion": "Calle 10 #5-23",
            "especialidad": "Cardiología",
            "telefono": 3124567890,
            "estado": "Activo",
            "consultorio": "201A",
            "hospital": "Clínica Central"
        }
    ]

    # Guardar datos
    medico.guardar_datos(str(filepath), medicos)

    # Leer datos y validar creación
    datos = medico.cargar_datos(str(filepath))
    assert len(datos) == 1
    assert datos[0]["nombres"] == "Laura"

    # Actualizar especialidad
    datos[0]["especialidad"] = "Dermatología"
    medico.guardar_datos(str(filepath), datos)
    actualizado = medico.cargar_datos(str(filepath))
    assert actualizado[0]["especialidad"] == "Dermatología"

    # Eliminar (dejar lista vacía)
    actualizado.pop(0)
    medico.guardar_datos(str(filepath), actualizado)
    final = medico.cargar_datos(str(filepath))
    assert final == []
"""
def test_crear medico"""


