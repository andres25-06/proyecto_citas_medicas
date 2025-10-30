# tests/test_modelo_medico.py
# -*- coding: utf-8 -*-
import csv

from Modelo import medico


def test_crud_medico_json(tmp_path):
    filepath = tmp_path / "medicos.json"

    nuevo_medico = {
        "documento": "303",
        "nombres": "Pedro",
        "apellidos": "Jiménez",
        "especialidad": "Oftalmología",
        "telefono": "3128884567"
    }

    medico.crear_medico(nuevo_medico, str(filepath))

    lista = medico.leer_todos_los_medicos(str(filepath))
    assert len(lista) == 1

    encontrado = medico.buscar_medico_por_documento("303", str(filepath))
    assert encontrado["especialidad"] == "Oftalmología"

    encontrado["especialidad"] = "Neurología"
    medico.actualizar_medico(encontrado, str(filepath))
    actualizado = medico.buscar_medico_por_documento("303", str(filepath))
    assert actualizado["especialidad"] == "Neurología"

    medico.eliminar_medico("303", str(filepath))
    assert medico.leer_todos_los_medicos(str(filepath)) == []


def test_crud_medico_csv(tmp_path):
    filepath = tmp_path / "medicos.csv"
    campos = ["documento", "nombres", "apellidos", "especialidad", "telefono"]

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()

    nuevo_medico = {
        "documento": "404",
        "nombres": "Claudia",
        "apellidos": "Morales",
        "especialidad": "Dermatología",
        "telefono": "3101112233"
    }

    medico.crear_medico(nuevo_medico, str(filepath))
    lista = medico.leer_todos_los_medicos(str(filepath))
    assert lista[0]["nombres"] == "Claudia"
