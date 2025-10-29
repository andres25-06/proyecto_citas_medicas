# -- coding: utf-8 --
import pytest
import builtins
from unittest.mock import patch, MagicMock
from Vista import vista_paciente


@pytest.fixture
def mock_paciente(monkeypatch):
    """Mock del módulo Modelo.paciente"""
    mock = MagicMock()
    monkeypatch.setattr(vista_paciente, "paciente", mock)
    return mock


@pytest.fixture
def archivo_csv(tmp_path):
    """Archivo temporal de prueba"""
    return tmp_path / "pacientes.csv"


# ======================================================
# 🔹 TEST: solicitar_tipo_documento
# ======================================================
def test_solicitar_tipo_documento(monkeypatch):
    """Debe retornar el tipo de documento correcto"""
    with patch("Vista.vista_paciente.selector_interactivo", return_value=1):
        tipo = vista_paciente.solicitar_tipo_documento()
        assert tipo == "T.I"  # Segunda opción del diccionario


# ======================================================
# 🔹 TEST: elegir_almacenamiento
# ======================================================
@pytest.mark.parametrize("opcion, esperado", [
    (0, "pacientes.csv"),
    (1, "pacientes.json"),
])
def test_elegir_almacenamiento(monkeypatch, opcion, esperado):
    """Debe retornar la ruta del archivo según selección"""
    with patch("Vista.vista_paciente.selector_interactivo", return_value=opcion):
        ruta = vista_paciente.elegir_almacenamiento()
        assert ruta.endswith(esperado)


# ======================================================
# 🔹 TEST: menu_crear_paciente
# ======================================================
def test_menu_crear_paciente(mock_paciente, archivo_csv, monkeypatch):
    """Debe crear un paciente correctamente"""
    # Mock de validaciones y entradas
    monkeypatch.setattr(vista_paciente.validar_campos, "validar_cedula", lambda x, y: "123")
    monkeypatch.setattr(vista_paciente.validar_campos, "validar_texto", lambda x: "Juan")
    monkeypatch.setattr(vista_paciente.validar_campos, "validar_telefono", lambda x: "3100000000")
    monkeypatch.setattr(vista_paciente.entrada_datos, "validar_datos_relacion_obligatorios", lambda d, c, t: True)
    monkeypatch.setattr(vista_paciente, "solicitar_tipo_documento", lambda: "C.C")
    monkeypatch.setattr(builtins, "input", lambda *args, **kwargs: "")  # Simula Enter

    mock_paciente.crear_paciente.return_value = {"id": "1", "documento": "123"}

    vista_paciente.menu_crear_paciente(str(archivo_csv))

    mock_paciente.crear_paciente.assert_called_once()


# ======================================================
# 🔹 TEST: menu_leer_pacientes
# ======================================================
def test_menu_leer_pacientes_con_datos(mock_paciente, archivo_csv, monkeypatch):
    """Debe mostrar pacientes en una tabla"""
    mock_paciente.leer_todos_los_pacientes.return_value = [
        {"id": "1", "tipo_documento": "C.C", "documento": "123", "nombres": "Juan", "apellidos": "Pérez", "direccion": "Calle 1", "telefono": "310"}
    ]
    monkeypatch.setattr(builtins, "input", lambda *a, **kw: "")
    vista_paciente.menu_leer_pacientes(str(archivo_csv))
    mock_paciente.leer_todos_los_pacientes.assert_called_once()


def test_menu_leer_pacientes_vacio(mock_paciente, archivo_csv, monkeypatch):
    """Debe mostrar mensaje cuando no hay pacientes"""
    mock_paciente.leer_todos_los_pacientes.return_value = []
    monkeypatch.setattr(builtins, "input", lambda *a, **kw: "")
    vista_paciente.menu_leer_pacientes(str(archivo_csv))
    mock_paciente.leer_todos_los_pacientes.assert_called_once()


# ======================================================
# 🔹 TEST: menu_actualizar_paciente
# ======================================================
def test_menu_actualizar_paciente(mock_paciente, archivo_csv, monkeypatch):
    """Debe actualizar un paciente existente"""
    mock_paciente.buscar_paciente_por_documento.return_value = {
        "documento": "123", "nombres": "Juan", "apellidos": "Pérez", "direccion": "Calle 1", "telefono": "310"
    }
    mock_paciente.actualizar_paciente.return_value = True
    monkeypatch.setattr(vista_paciente, "solicitar_tipo_documento", lambda permitir_vacio=True: None)
    monkeypatch.setattr(vista_paciente.Prompt, "ask", lambda *a, **kw: "Juan")
    monkeypatch.setattr(vista_paciente.IntPrompt, "ask", lambda *a, **kw: 310)
    monkeypatch.setattr(builtins, "input", lambda *a, **kw: "")

    vista_paciente.menu_actualizar_paciente(str(archivo_csv))
    mock_paciente.actualizar_paciente.assert_called_once()


# ======================================================
# 🔹 TEST: menu_eliminar_paciente
# ======================================================
def test_menu_eliminar_paciente_confirmado(mock_paciente, archivo_csv, monkeypatch):
    """Debe eliminar paciente si se confirma"""
    mock_paciente.buscar_paciente_por_documento.return_value = {
        "nombres": "Juan", "apellidos": "Pérez"
    }
    mock_paciente.eliminar_paciente.return_value = True
    monkeypatch.setattr(vista_paciente.Confirm, "ask", lambda *a, **kw: True)
    monkeypatch.setattr(vista_paciente.IntPrompt, "ask", lambda *a, **kw: 123)
    monkeypatch.setattr(builtins, "input", lambda *a, **kw: "")

    vista_paciente.menu_eliminar_paciente(str(archivo_csv))
    mock_paciente.eliminar_paciente.assert_called_once()


def test_menu_eliminar_paciente_cancelado(mock_paciente, archivo_csv, monkeypatch):
    """Debe cancelar si no se confirma"""
    mock_paciente.buscar_paciente_por_documento.return_value = {
        "nombres": "Juan", "apellidos": "Pérez"
    }
    monkeypatch.setattr(vista_paciente.Confirm, "ask", lambda *a, **kw: False)
    monkeypatch.setattr(vista_paciente.IntPrompt, "ask", lambda *a, **kw: 123)
    monkeypatch.setattr(builtins, "input", lambda *a, **kw: "")

    vista_paciente.menu_eliminar_paciente(str(archivo_csv))
    mock_paciente.buscar_paciente_por_documento.assert_called_once()
    mock_paciente.eliminar_paciente.assert_not_called()
