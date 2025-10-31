# tests/test_gestor_datos_medico.py
# -*- coding: utf-8 -*-
import csv

from Controlador import gestor_datos_medico as gestor


def test_crud_medicos_json(tmp_path):
    filepath = tmp_path / "medicos.json"

    medico = {
        "documento": "555",
        "nombres": "Laura",
        "apellidos": "Mora",
        "especialidad": "Cardiología",
        "telefono": "3125554444"
    }

    gestor.crear_medico(medico, str(filepath))
    lista = gestor.leer_todos_los_medicos(str(filepath))
    assert len(lista) == 1

    buscado = gestor.buscar_medico_por_documento("555", str(filepath))
    assert buscado["especialidad"] == "Cardiología"

    buscado["especialidad"] = "Dermatología"
    gestor.actualizar_medico(buscado, str(filepath))
    actualizado = gestor.buscar_medico_por_documento("555", str(filepath))
    assert actualizado["especialidad"] == "Dermatología"

    gestor.eliminar_medico("555", str(filepath))
    assert gestor.leer_todos_los_medicos(str(filepath)) == []


def test_crud_medicos_csv(tmp_path):
    filepath = tmp_path / "medicos.csv"
    campos = ["documento", "nombres", "apellidos", "especialidad", "telefono"]

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()

    medico = {
        "documento": "666",
        "nombres": "Carlos",
        "apellidos": "Ruiz",
        "especialidad": "Pediatría",
        "telefono": "3101239876"
    }

    gestor.crear_medico(medico, str(filepath))
    lista = gestor.leer_todos_los_medicos(str(filepath))
    assert lista[0]["especialidad"] == "Pediatría"
