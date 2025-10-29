# tests/test_gestor_datos_pacientes.py
# -*- coding: utf-8 -*-
import pytest
import csv
import json
from Controlador import gestor_datos_pacientes as gestor


def test_crud_pacientes_json(tmp_path):
    filepath = tmp_path / "pacientes.json"

    # Crear paciente
    paciente = {
        "documento": "111",
        "nombres": "Juan",
        "apellidos": "Pérez",
        "direccion": "Calle 1",
        "telefono": "3001234567"
    }
    gestor.crear_paciente(paciente, str(filepath))

    # Leer todos
    lista = gestor.leer_todos_los_pacientes(str(filepath))
    assert len(lista) == 1

    # Buscar
    encontrado = gestor.buscar_paciente_por_documento("111", str(filepath))
    assert encontrado["nombres"] == "Juan"

    # Actualizar
    encontrado["direccion"] = "Calle 2"
    gestor.actualizar_paciente(encontrado, str(filepath))
    actualizado = gestor.buscar_paciente_por_documento("111", str(filepath))
    assert actualizado["direccion"] == "Calle 2"

    # Eliminar
    gestor.eliminar_paciente("111", str(filepath))
    assert gestor.leer_todos_los_pacientes(str(filepath)) == []


def test_crud_pacientes_csv(tmp_path):
    filepath = tmp_path / "pacientes.csv"
    campos = ["documento", "nombres", "apellidos", "direccion", "telefono"]

    # Crear CSV vacío
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()

    paciente = {
        "documento": "222",
        "nombres": "Ana",
        "apellidos": "López",
        "direccion": "Calle 3",
        "telefono": "3019998877"
    }
    gestor.crear_paciente(paciente, str(filepath))

    lista = gestor.leer_todos_los_pacientes(str(filepath))
    assert lista[0]["nombres"] == "Ana"
