import os
import json
import csv
import tempfile
from Vista import vista_cita

# --- Pruebas de funciones auxiliares --- #

def test_cargar_datos_json(tmp_path):
    data = [{"id": 1, "motivo": "Dolor de cabeza"}]
    file_path = tmp_path / "citas.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f)

    result = vista_cita.cargar_datos(str(file_path))
    assert result == data


def test_cargar_datos_csv(tmp_path):
    file_path = tmp_path / "citas.csv"
    with open(file_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "motivo"])
        writer.writeheader()
        writer.writerow({"id": "1", "motivo": "Chequeo"})

    result = vista_cita.cargar_datos(str(file_path))
    assert isinstance(result, list)
    assert result[0]["motivo"] == "Chequeo"


def test_leer_datos_archivo_json_valido(tmp_path):
    data = [{"id": 1, "motivo": "Consulta"}]
    file_path = tmp_path / "test.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f)

    result = vista_cita.leer_datos_archivo(str(file_path))
    assert result == data


def test_leer_datos_archivo_json_invalido(tmp_path):
    file_path = tmp_path / "test.json"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("archivo inválido")

    result = vista_cita.leer_datos_archivo(str(file_path))
    assert result == []


def test_leer_datos_archivo_csv(tmp_path):
    file_path = tmp_path / "test.csv"
    with open(file_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "estado"])
        writer.writeheader()
        writer.writerow({"id": "1", "estado": "Pendiente"})

    result = vista_cita.leer_datos_archivo(str(file_path))
    assert result[0]["estado"] == "Pendiente"


# --- Pruebas de búsqueda --- #

def test_buscar_cita_por_documento_encontrada():
    citas = [
        {"id": 1, "documento_paciente": "123", "motivo": "Revisión"},
        {"id": 2, "documento_paciente": "456", "motivo": "Control"}
    ]
    resultado = vista_cita.buscar_cita_por_documento(citas, "123")
    assert len(resultado) == 1
    assert resultado[0]["motivo"] == "Revisión"


def test_buscar_cita_por_documento_no_encontrada():
    citas = [{"id": 1, "documento_paciente": "999"}]
    resultado = vista_cita.buscar_cita_por_documento(citas, "000")
    assert resultado == []


# --- Pruebas de obtener nombre por documento --- #

def test_obtener_nombre_por_documento_json(tmp_path):
    data = [{"documento": "123", "nombres": "Ana", "apellidos": "Pérez"}]
    file_path = tmp_path / "pacientes.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f)

    result = vista_cita.obtener_nombre_por_documento(str(file_path), "123")
    assert result == "Ana Pérez"


def test_obtener_nombre_por_documento_csv(tmp_path):
    file_path = tmp_path / "pacientes.csv"
    with open(file_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["documento", "nombres", "apellidos"])
        writer.writeheader()
        writer.writerow({"documento": "456", "nombres": "Carlos", "apellidos": "Lopez"})

    result = vista_cita.obtener_nombre_por_documento(str(file_path), "456")
    assert result == "Carlos Lopez"


def test_obtener_nombre_por_documento_no_existe(tmp_path):
    file_path = tmp_path / "pacientes.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump([], f)

    result = vista_cita.obtener_nombre_por_documento(str(file_path), "000")
    assert result == "No encontrado"
