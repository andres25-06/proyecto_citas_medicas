# -- coding: utf-8 --
import builtins
from unittest.mock import MagicMock, patch

import pytest

from Vista import vista_medico


@pytest.fixture
def mock_medico(monkeypatch):
    """Mock del módulo Modelo.medico"""
    mock = MagicMock()
    monkeypatch.setattr(vista_medico, "medico", mock)
    return mock


@pytest.fixture
def archivo_csv(tmp_path):
    """Archivo temporal para pruebas"""
    return tmp_path / "medicos.csv"


# ======================================================
# 🔹 TEST: elegir_almacenamiento
# ======================================================
@pytest.mark.parametrize("opcion, esperado", [
    (0, "medicos.csv"),
    (1, "medicos.json"),
])
def test_elegir_almacenamiento(monkeypatch, opcion, esperado):
    """Debe retornar la ruta del archivo correcto"""
    with patch("Vista.vista_medico.selector_interactivo", return_value=opcion):
        ruta = vista_medico.elegir_almacenamiento()
        assert ruta.endswith(esperado)


# ======================================================
# 🔹 TEST: solicitar_tipo_documento
# ======================================================
def test_solicitar_tipo_documento(monkeypatch):
    """Debe retornar el tipo de documento seleccionado"""
    with patch("Vista.vista_medico.selector_interactivo", return_value=2):
        tipo = vista_medico.solicitar_tipo_documento()
        assert tipo == "R.C"  # Tercera opción


# # ======================================================
# # 🔹 TEST: solicitar_especialidad_medica
# # ======================================================
# def test_solicitar_especialidad(monkeypatch):
#     """Debe retornar la especialidad seleccionada"""
#     with patch("Vista.vista_medico.selector_interactivo", return_value=4):
#         esp = vista_medico.solicitar_especialidad_medica()
#         assert esp == "Medicina Interna"


# ======================================================
# 🔹 TEST: estado_medico
# ======================================================
def test_estado_medico(monkeypatch):
    """Debe retornar el estado 'Activo'"""
    with patch("Vista.vista_medico.selector_interactivo", return_value=0):
        estado = vista_medico.estado_medico()
        assert estado == "Activo"


# ======================================================
# 🔹 TEST: menu_crear_medico
# ======================================================
def test_menu_crear_medico(mock_medico, archivo_csv, monkeypatch):
    """Debe crear un médico correctamente"""
    # Mock entradas y validaciones
    monkeypatch.setattr(vista_medico, "solicitar_tipo_documento", lambda: "C.C")
    monkeypatch.setattr(vista_medico.validar_campos, "validar_cedula", lambda x, y: "111")
    monkeypatch.setattr(vista_medico.validar_campos, "validar_texto", lambda x: "Juan")
    monkeypatch.setattr(vista_medico.validar_campos, "validar_telefono", lambda x: "3100000")
    monkeypatch.setattr(vista_medico.validar_campos, "validar_numero", lambda x: "101")
    monkeypatch.setattr(vista_medico, "solicitar_especialidad_medica", lambda: "Cardiología")
    monkeypatch.setattr(vista_medico, "estado_medico", lambda: "Activo")
    monkeypatch.setattr(vista_medico.entrada_datos, "validar_datos_relacion_obligatorios", lambda d, c, t: True)
    monkeypatch.setattr(builtins, "input", lambda *a, **kw: "")

    mock_medico.crear_medico.return_value = {"id": "1", "documento": "111"}

    vista_medico.menu_crear_medico(str(archivo_csv))
    mock_medico.crear_medico.assert_called_once()


# ======================================================
# 🔹 TEST: menu_leer_medicos
# ======================================================
def test_menu_leer_medicos_con_datos(mock_medico, archivo_csv, monkeypatch):
    """Debe mostrar médicos cuando hay registros"""
    mock_medico.leer_todos_los_medicos.return_value = [
        {"id": "1", "nombres": "Juan", "apellidos": "Pérez", "especialidad": "Cardiología", "telefono": "310", "estado": "Activo", "consultorio": "101"}
    ]
    monkeypatch.setattr(builtins, "input", lambda *a, **kw: "")
    vista_medico.menu_leer_medicos(str(archivo_csv))
    mock_medico.leer_todos_los_medicos.assert_called_once()


def test_menu_leer_medicos_vacio(mock_medico, archivo_csv, monkeypatch):
    """Debe mostrar mensaje si no hay médicos"""
    mock_medico.leer_todos_los_medicos.return_value = []
    monkeypatch.setattr(builtins, "input", lambda *a, **kw: "")
    vista_medico.menu_leer_medicos(str(archivo_csv))
    mock_medico.leer_todos_los_medicos.assert_called_once()


# ======================================================
# 🔹 TEST: menu_actualizar_medico
# ======================================================
def test_menu_actualizar_medico(mock_medico, archivo_csv, monkeypatch):
    """Debe actualizar un médico existente"""
    mock_medico.buscar_medico_por_documento.return_value = {
        "documento": "111", "nombres": "Juan", "especialidad": "Cardiología", "telefono": "310"
    }
    mock_medico.actualizar_medico.return_value = True

    monkeypatch.setattr(vista_medico.Prompt, "ask", lambda *a, **kw: "Pedro")
    monkeypatch.setattr(vista_medico.IntPrompt, "ask", lambda *a, **kw: 312)
    monkeypatch.setattr(builtins, "input", lambda *a, **kw: "")

    vista_medico.menu_actualizar_medico(str(archivo_csv))
    mock_medico.actualizar_medico.assert_called_once()


# ======================================================
# 🔹 TEST: menu_eliminar_medico
# ======================================================
def test_menu_eliminar_medico_confirmado(mock_medico, archivo_csv, monkeypatch):
    """Debe eliminar médico si se confirma"""
    mock_medico.buscar_medico_por_documento.return_value = {"nombres": "Juan", "apellidos": "Pérez"}
    mock_medico.eliminar_medico.return_value = True
    monkeypatch.setattr(vista_medico.Confirm, "ask", lambda *a, **kw: True)
    monkeypatch.setattr(vista_medico.IntPrompt, "ask", lambda *a, **kw: 111)
    monkeypatch.setattr(builtins, "input", lambda *a, **kw: "")

    vista_medico.menu_eliminar_medico(str(archivo_csv))
    mock_medico.eliminar_medico.assert_called_once()


def test_menu_eliminar_medico_cancelado(mock_medico, archivo_csv, monkeypatch):
    """Debe cancelar si el usuario no confirma"""
    mock_medico.buscar_medico_por_documento.return_value = {"nombres": "Juan", "apellidos": "Pérez"}
    monkeypatch.setattr(vista_medico.Confirm, "ask", lambda *a, **kw: False)
    monkeypatch.setattr(vista_medico.IntPrompt, "ask", lambda *a, **kw: 111)
    monkeypatch.setattr(builtins, "input", lambda *a, **kw: "")

    vista_medico.menu_eliminar_medico(str(archivo_csv))
    mock_medico.eliminar_medico.assert_not_called()
