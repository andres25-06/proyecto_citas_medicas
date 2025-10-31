# # tests/test_validar_campos.py
# import sys
# import os
# import tempfile
# import json
# import pytest
# from unittest.mock import patch

# # ---------------------------
# # Permitir importar Validaciones.py desde la raíz
# # ---------------------------
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# import Validaciones as validar_campos

# # ==============================
# # TESTS validar_texto
# # ==============================
# @patch("rich.prompt.Prompt.ask", return_value="Sergio")
# def test_validar_texto(mock_prompt):
#     resultado = validar_campos.validar_texto("Nombre")

# @patch("rich.prompt.Prompt.ask", side_effect=["", "ab", "Juan"])
# def test_validar_texto_reintentos(mock_prompt):
#     resultado = validar_campos.validar_texto("Nombre", 3, 10)
#     assert resultado == "Juan"

# # ==============================
# # TESTS validar_numero
# # ==============================
# @patch("rich.prompt.Prompt.ask", return_value="25")
# def test_validar_numero_valido(mock_prompt):
#     resultado = validar_campos.validar_numero("Edad", 18, 99)
#     assert resultado == 25

# @patch("rich.prompt.Prompt.ask", side_effect=["", "abc", "5", "20"])
# def test_validar_numero_reintentos(mock_prompt):
#     resultado = validar_campos.validar_numero("Edad", 10, 30)
#     assert resultado == 20

# # ==============================
# # TESTS validar_telefono
# # ==============================
# @patch("rich.prompt.Prompt.ask", side_effect=["", "123", "3124567890"])
# def test_validar_telefono(mock_prompt):
#     resultado = validar_campos.validar_telefono("Teléfono")
#     assert resultado == "3124567890"

# # ==============================
# # TESTS validar_cedula
# # ==============================

# @pytest.fixture
# def json_tempfile():
#     with tempfile.NamedTemporaryFile(mode="w+", suffix=".json", delete=False) as f:
#         # pre-carga con un registro duplicado
#         json.dump([{"documento": "654321"}], f)
#         f.flush()
#         yield f.name

# @patch("rich.prompt.Prompt.ask", side_effect=["", "abc", "123456", "654321"])
# def test_validar_cedula(json_tempfile, mock_prompt):
#     resultado = validar_campos.validar_cedula("Cédula", json_tempfile)
#     assert resultado == "123456"  # el primer valor válido no duplicado

# # ==============================
# # TESTS validar_hora
# # ==============================
# @patch("builtins.input", side_effect=["hola", "25:99", "08:30"])
# def test_validar_hora(mock_input):
#     resultado = validar_campos.validar_hora("hora de cita")
#     assert resultado == "08:30"
