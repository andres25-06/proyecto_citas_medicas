# tests/test_modelo_paciente.py
# -*- coding: utf-8 -*-
import csv
import pytest
from Modelo import paciente


def test_crud_paciente_completo(tmp_path):
    filepath_json = tmp_path / "pacientes.json"
    filepath_csv = tmp_path / "pacientes.csv"
    
    # ---------- CREAR PACIENTES ----------
    pacientes = [
        {"tipo_documento": "C.C", "documento": 101, "nombres": "María", "apellidos": "Gómez", "direccion": "Calle 10", "telefono": 3005551234},
        {"tipo_documento": "C.C", "documento": 102, "nombres": "Luis", "apellidos": "Torres", "direccion": "Calle 11", "telefono": 3017778899}
    ]

    for p in pacientes:
        creado = paciente.crear_paciente(
            str(filepath_json),
            p["tipo_documento"],
            p["documento"],
            p["nombres"],
            p["apellidos"],
            p["direccion"],
            p["telefono"]
        )
        assert creado is not None
        # Verificar que todos los valores son strings
        for key in ["id", "tipo_documento", "documento", "nombres", "apellidos", "direccion", "telefono"]:
            assert isinstance(creado[key], str)

    # Intentar crear paciente con documento duplicado
    duplicado = paciente.crear_paciente(
        str(filepath_json),
        "C.C", 101, "María", "Gómez", "Calle 10", 3005551234
    )
    assert duplicado is None

    # ---------- LEER Y BUSCAR ----------
    lista = paciente.leer_todos_los_pacientes(str(filepath_json))
    assert len(lista) == 2

    encontrado = paciente.buscar_paciente_por_documento(str(filepath_json), "101")
    assert encontrado["nombres"] == "María"

    no_encontrado = paciente.buscar_paciente_por_documento(str(filepath_json), "999")
    assert no_encontrado is None

    # ---------- ACTUALIZAR ----------
    actualizado = paciente.actualizar_paciente(str(filepath_json), "101", {"direccion": "Avenida 5", "telefono": 3111111111})
    assert actualizado["direccion"] == "Avenida 5"
    assert actualizado["telefono"] == "3111111111"  # convertido a string

    # Actualizar paciente inexistente
    actualizado_none = paciente.actualizar_paciente(str(filepath_json), "999", {"direccion": "X"})
    assert actualizado_none is None

    # ---------- ELIMINAR ----------
    eliminado = paciente.eliminar_paciente(str(filepath_json), "101")
    assert eliminado is True
    # Eliminar paciente inexistente
    eliminado_none = paciente.eliminar_paciente(str(filepath_json), "999")
    assert eliminado_none is False

    # Verificar que quedó solo un paciente
    lista_final = paciente.leer_todos_los_pacientes(str(filepath_json))
    assert len(lista_final) == 1
    assert lista_final[0]["documento"] == "102"

    # ---------- TEST CSV ----------
    campos = ["id", "tipo_documento", "documento", "nombres", "apellidos", "direccion", "telefono"]
    with open(filepath_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()

    # Crear paciente CSV
    p_csv = pacientes[0]
    paciente.crear_paciente(
        str(filepath_csv),
        p_csv["tipo_documento"],
        p_csv["documento"],
        p_csv["nombres"],
        p_csv["apellidos"],
        p_csv["direccion"],
        p_csv["telefono"]
    )
    lista_csv = paciente.leer_todos_los_pacientes(str(filepath_csv))
    assert lista_csv[0]["nombres"] == p_csv["nombres"]
