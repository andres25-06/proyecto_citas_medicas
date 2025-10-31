import builtins
import json
import os
import pytest
from unittest.mock import patch, mock_open
from datetime import datetime

import Validaciones as val  # Importar módulo de validación


# ======================================================
# TEST validar_texto
# ======================================================
@patch("Validaciones.Prompt.ask")
def test_validar_texto_valido(mock_ask):
    mock_ask.return_value = "Sergio"
    resultado = val.validar_texto("Nombre", 3, 10)
    assert resultado == "Sergio"


@patch("Validaciones.Prompt.ask", side_effect=["", "ab", "Juan"])
def test_validar_texto_reintentos(mock_ask):
    resultado = val.validar_texto("Nombre", 3, 10)
    assert resultado == "Juan"


# ======================================================
# TEST validar_numero
# ======================================================
@patch("Validaciones.Prompt.ask", return_value="25")
def test_validar_numero_valido(mock_ask):
    resultado = val.validar_numero("Edad", 18, 99)
    assert resultado == 25


@patch("Validaciones.Prompt.ask", side_effect=["", "abc", "5", "20"])
def test_validar_numero_reintentos(mock_ask):
    resultado = val.validar_numero("Edad", minimo=10, maximo=30)
    assert resultado == 20


# ======================================================
# TEST validar_telefono
# ======================================================
@patch("Validaciones.Prompt.ask", side_effect=["", "123", "3124567890"])
def test_validar_telefono(mock_ask):
    resultado = val.validar_telefono("Teléfono")
    assert resultado == "3124567890"


# ======================================================
# TEST validar_cedula
# ======================================================
@pytest.fixture
def json_tempfile(tmp_path):
    """Crea un archivo JSON temporal con un registro existente."""
    data = [{"documento": "123456"}]
    path = tmp_path / "registros.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    return str(path)


@patch("Validaciones.Prompt.ask", side_effect=["", "abc", "123456", "654321"])
def test_validar_cedula(json_tempfile, mock_ask):
    resultado = val.validar_cedula("Cédula", filepath=json_tempfile)
    assert resultado == "654321"


# ======================================================
# TEST validar_hora
# ======================================================
@patch("builtins.input", side_effect=["hola", "25:99", "08:30"])
def test_validar_hora(mock_input):
    resultado = val.validar_hora("hora de cita")
    assert resultado == "08:30"
