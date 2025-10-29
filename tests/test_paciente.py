# tests/test_modelo_paciente.py
# -*- coding: utf-8 -*-
import pytest
import csv
import json
from Modelo import paciente


def test_crud_paciente_json(tmp_path):
    filepath = tmp_path / "pacientes.json"

    # Crear paciente
    nuevo_paciente = {
        "documento": "101",
        "nombres": "María",
        "apellidos": "Gómez",
        "direccion": "Calle 10",
        "telefono": "3005551234"
    }

    paciente.crear_paciente(nuevo_paciente, str(filepath))

    # Leer todos
    lista = paciente.leer_todos_los_pacientes(str(filepath))
    assert len(lista) == 1

    # Buscar
    encontrado = paciente.buscar_paciente_por_documento("101", str(filepath))
    assert encontrado["nombres"] == "María"

    # Actualizar
    encontrado["direccion"] = "Avenida 5"
    paciente.actualizar_paciente(encontrado, str(filepath))
    actualizado = paciente.buscar_paciente_por_documento("101", str(filepath))
    assert actualizado["direccion"] == "Avenida 5"

    # Eliminar
    paciente.eliminar_paciente("101", str(filepath))
    assert paciente.leer_todos_los_pacientes(str(filepath)) == []


def test_crud_paciente_csv(tmp_path):
    filepath = tmp_path / "pacientes.csv"
    campos = ["documento", "nombres", "apellidos", "direccion", "telefono"]

    # Inicializar archivo CSV vacío
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()

    nuevo_paciente = {
        "documento": "202",
        "nombres": "Luis",
        "apellidos": "Torres",
        "direccion": "Calle 11",
        "telefono": "3017778899"
    }

    paciente.crear_paciente(nuevo_paciente, str(filepath))
    lista = paciente.leer_todos_los_pacientes(str(filepath))
    assert lista[0]["nombres"] == "Luis"
