import os
import pytest
import json
import csv
from Validaciones import entrada_datos as val

def test_validar_documento_unico_true():
    registros = [{"documento": "999"}, {"documento": "888"}]
    resultado = val.validar_documento_unico("777", registros, "Paciente")
    assert resultado is True  # Documento no repetido


def test_validar_documento_unico_false():
    registros = [{"documento": "123"}, {"documento": "456"}]
    resultado = val.validar_documento_unico("123", registros, "Paciente")
    assert resultado is False  # Documento ya existe


def test_validar_datos_relacion_obligatorios_true():
    datos = {"documento": "111", "nombre": "Juan", "edad": "30"}
    campos = ["documento", "nombre"]
    resultado = val.validar_datos_relacion_obligatorios(datos, campos, "Paciente")
    assert resultado is True  # Todos los campos están


def test_validar_datos_relacion_obligatorios_false():
    datos = {"documento": "", "nombre": "Juan"}
    campos = ["documento", "nombre"]
    resultado = val.validar_datos_relacion_obligatorios(datos, campos, "Paciente")
    assert resultado is False  # Falta documento


def test_validar_existencia_relacion_lista(tmp_path):
    lista = [{"documento": "123"}]
    assert val.validar_existencia_relacion("123", lista, "Paciente") is True
    assert val.validar_existencia_relacion("999", lista, "Paciente") is False


def test_validar_existencia_relacion_json(tmp_path):
    # Crear archivo JSON temporal
    data_dir = tmp_path / "Data"
    data_dir.mkdir()
    archivo_json = data_dir / "paciente.json"

    datos = [{"documento": "555"}]
    with open(archivo_json, "w", encoding="utf-8") as f:
        json.dump(datos, f)

    # Cambiar directorio de trabajo temporalmente
    os.chdir(tmp_path)
    assert val.validar_existencia_relacion("555", [], "Paciente") is True
    assert val.validar_existencia_relacion("999", [], "Paciente") is False


def test_validar_existencia_relacion_csv(tmp_path):
    # Crear archivo CSV temporal
    data_dir = tmp_path / "Data"
    data_dir.mkdir()
    archivo_csv = data_dir / "paciente.csv"

    with open(archivo_csv, "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["documento", "nombre"])
        writer.writeheader()
        writer.writerow({"documento": "777", "nombre": "Ana"})

    os.chdir(tmp_path)
    assert val.validar_existencia_relacion("777", [], "Paciente") is True
    assert val.validar_existencia_relacion("999", [], "Paciente") is False
