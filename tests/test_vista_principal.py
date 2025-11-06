# tests/test_vista_principal.py
from Vista import vista_principal


def test_normalizar_fecha():
    """Verifica que normalizar_fecha convierte correctamente distintos formatos."""
    assert vista_principal.normalizar_fecha("2025-11-06") == "2025-11-06"
    assert vista_principal.normalizar_fecha("06/11/2025") == "2025-11-06"
    assert vista_principal.normalizar_fecha("06-11-2025") == "2025-11-06"
    assert vista_principal.normalizar_fecha("2025/11/06") == "2025-11-06"
    # Formato incorrecto debe devolverse igual
    assert vista_principal.normalizar_fecha("06_11_25") == "06_11_25"


def test_guardar_y_cargar_json(tmp_path):
    """Comprueba que guardar_json y cargar_json funcionan bien."""
    ruta = tmp_path / "datos.json"
    datos = [{"id": 1, "nombre": "Juan"}]

    vista_principal.guardar_json(ruta, datos)
    cargado = vista_principal.cargar_json(ruta)

    assert cargado == datos


def test_guardar_citas_csv_y_cargar(tmp_path):
    """Verifica que las citas se guardan y se pueden volver a leer."""
    ruta = tmp_path / "citas.csv"
    citas = [
        {"id": "1", "documento_paciente": "123", "documento_medico": "456", "fecha": "2025-11-06", "hora": "10:00", "motivo": "Consulta", "estado": "pendiente"}
    ]

    assert vista_principal.guardar_citas_csv(ruta, citas)

    cargado = vista_principal.cargar_csv_simple(ruta)
    assert isinstance(cargado, list)
    assert cargado[0]["id"] == "1"
    assert cargado[0]["estado"] == "pendiente"


def test_cargar_y_eliminar_cita(tmp_path):
    """Prueba que cargar_citas y eliminar_cita_por_id funcionan correctamente."""
    ruta_base = tmp_path / "citas"
    ruta_json = ruta_base.with_suffix(".json")
    ruta_csv = ruta_base.with_suffix(".csv")

    citas = [
        {"id": "1", "documento_paciente": "123", "documento_medico": "456", "fecha": "2025-11-06", "hora": "10:00", "motivo": "Dolor", "estado": "pendiente"}
    ]

    # Crear archivos JSON y CSV
    vista_principal.guardar_json(ruta_json, citas)
    vista_principal.guardar_citas_csv(ruta_csv, citas)

    # Cargar citas combinadas
    cargadas = vista_principal.cargar_citas(str(ruta_base))
    assert len(cargadas) == 2  # json + csv
    assert all("fecha" in c for c in cargadas)

    # Eliminar la cita
    resultado = vista_principal.eliminar_cita_por_id("1", str(ruta_base))
    assert resultado["json"] is True
    assert resultado["csv"] is True


def test_cargar_json_inexistente(tmp_path):
    """Debe devolver lista vacía si el archivo no existe."""
    ruta = tmp_path / "no_existe.json"
    assert vista_principal.cargar_json(ruta) == []
