# tests/test_vista_cita.py
# -- coding: utf-8 --
"""
Pytest para la Vista del Módulo de Citas.
Simula interacciones y valida el flujo general de las funciones.
"""
import pytest

from Vista import vista_cita



# Utilidades
@pytest.fixture(autouse=True)
def no_clear(monkeypatch):
    """Evita limpiar la consola en los tests."""
    monkeypatch.setattr(vista_cita, "limpiar", lambda: None)


@pytest.fixture
def mock_console(monkeypatch):
    """Evita que Rich imprima realmente en consola."""
    class DummyConsole:
        def print(self, *args, **kwargs):
            pass
        def input(self, prompt=""):
            return ""
    dummy = DummyConsole()
    monkeypatch.setattr(vista_cita, "console", dummy)
    return dummy



#  Pruebas de funciones auxiliares
def test_leer_datos_archivo_json(tmp_path):
    """Debe leer correctamente un archivo JSON válido."""
    archivo = tmp_path / "citas.json"
    data = [{"id": "1", "paciente": "Juan"}]
    archivo.write_text('[{"id": "1", "paciente": "Juan"}]', encoding="utf-8")

    resultado = vista_cita.leer_datos_archivo(str(archivo))
    assert resultado == data


def test_leer_datos_archivo_csv(tmp_path):
    """Debe leer correctamente un archivo CSV."""
    archivo = tmp_path / "citas.csv"
    archivo.write_text("id,paciente\n1,Ana\n", encoding="utf-8")

    resultado = vista_cita.leer_datos_archivo(str(archivo))
    assert resultado[0]["paciente"] == "Ana"


def test_leer_datos_archivo_vacio(tmp_path):
    """Si el archivo está vacío o malformado, debe devolver lista vacía."""
    archivo = tmp_path / "vacio.json"
    archivo.write_text("", encoding="utf-8")

    resultado = vista_cita.leer_datos_archivo(str(archivo))
    assert resultado == []


def test_estado_cita_devuelve_valido(monkeypatch, mock_console):
    """Simula seleccionar una opción de estado."""
    # Simulamos que el usuario presiona Enter al seleccionar la primera opción
    monkeypatch.setattr(vista_cita, "selector_interactivo", lambda t, o: 0)

    estado = vista_cita.estado_cita()
    assert estado in ["Completada", "Pendiente", "Cancelada"]


def test_estado_cita_permitir_vacio(monkeypatch, mock_console):
    """Debe permitir no cambiar el estado."""
    # Primer índice: opción "No cambiar"
    monkeypatch.setattr(vista_cita, "selector_interactivo", lambda t, o: 0)
    estado = vista_cita.estado_cita(permitir_vacio=True)
    assert estado is None


# test Prueba del calendario y selección de fecha
# def test_calendario_y_fecha(monkeypatch, mock_console):
#     """Simula la selección de una fecha."""
#     # Selector de fecha que retorna una fecha fija
#     monkeypatch.setattr(vista_cita, "seleccionar_fecha", lambda: "2025-12-25")
#     mock_console.input = lambda prompt="": "10:00"
#     resultado = vista_cita.calendario()
#     assert "2025-12-25" in resultado
#     assert "10:00" in resultado



#test Prueba de obtener_nombre_completo_por_documento
# def test_obtener_nombre_completo_por_documento(tmp_path):
#     """Debe devolver el nombre completo si encuentra el documento."""
#     archivo = tmp_path / "pacientes.json"
#     archivo.write_text('[{"documento": "123", "nombres": "Juan", "apellidos": "Pérez"}]', encoding="utf-8")

#     nombre = vista_cita.obtener_nombre_completo_por_documento(str(archivo), "123", "paciente")
#     assert "Juan Pérez" in nombre


def test_obtener_nombre_completo_no_encontrado(tmp_path):
    """Si no encuentra el documento, devuelve mensaje de no encontrado."""
    archivo = tmp_path / "pacientes.json"
    archivo.write_text('[]', encoding="utf-8")
    nombre = vista_cita.obtener_nombre_completo_por_documento(str(archivo), "999", "paciente")
    assert "(no encontrado)" in nombre



#  test de menu_cancelar_cita
def test_menu_cancelar_cita(monkeypatch, mock_console, tmp_path):
    """Simula cancelar cita con confirmación afirmativa."""
    filepath = tmp_path / "citas.json"

    # Parchear prompt.ask para que devuelva "12345" como documento
    monkeypatch.setattr("rich.prompt.Prompt.ask", lambda _: "12345")
    # Parchear Confirm.ask para confirmación afirmativa (True)
    monkeypatch.setattr("rich.prompt.Confirm.ask", lambda *a, **kw: True)
    # Parchear la función que elimina la cita para simular éxito
    monkeypatch.setattr(vista_cita.cita, "eliminar_cita_por_documento", lambda f, d: True)
    # Parchear input para evitar error de pytest reading stdin
    monkeypatch.setattr("builtins.input", lambda _: "")

    vista_cita.menu_cancelar_cita(str(filepath))


def test_menu_cancelar_cita_cancelada(monkeypatch, mock_console, tmp_path):
    """Simula cancelar cita con respuesta negativa."""
    filepath = tmp_path / "citas.json"

    monkeypatch.setattr("rich.prompt.Prompt.ask", lambda _: "12345")
    monkeypatch.setattr("rich.prompt.Confirm.ask", lambda *a, **kw: False)
    monkeypatch.setattr("builtins.input", lambda _: "")

    vista_cita.menu_cancelar_cita(str(filepath))

