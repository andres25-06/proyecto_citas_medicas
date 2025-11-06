from Modelo import cita
from rich.prompt import Prompt


# TEST: CREAR CITA NUEVA
def test_crear_cita_json(tmp_path):
    filepath = tmp_path / "citas.json"

    nueva_cita = {
        "documento_paciente": "11111",
        "documento_medico": "22222",
        "fecha": "2025-10-31",
        "hora": "10:00",
        "motivo": "Consulta general",
        "estado": "Pendiente"
    }

    creada = cita.crear_cita(
        str(filepath),
        nueva_cita["documento_paciente"],
        nueva_cita["documento_medico"],
        nueva_cita["fecha"],
        nueva_cita["hora"],
        nueva_cita["motivo"],
        nueva_cita["estado"]
    )

    assert creada is not None
    assert creada["motivo"] == "Consulta general"
    assert creada["documento_paciente"] == "11111"

# TEST: EVITAR DUPLICADOS
def test_no_permite_citas_duplicadas(tmp_path):
    filepath = tmp_path / "citas.json"

    # Crear una primera cita
    cita.crear_cita(str(filepath), "333", "444", "2025-10-31", "09:00", "Chequeo", "Pendiente")

    # Intentar crear otra igual
    duplicada = cita.crear_cita(str(filepath), "333", "444", "2025-10-31", "09:00", "Chequeo", "Pendiente")

    assert duplicada is None  # No debe permitir duplicados

# TEST: LEER TODAS LAS CITAS
def test_leer_todas_las_citas(tmp_path):
    filepath = tmp_path / "citas.json"
    cita.crear_cita(str(filepath), "555", "666", "2025-11-01", "08:00", "Examen", "Pendiente")
    cita.crear_cita(str(filepath), "777", "888", "2025-11-02", "11:00", "Control", "Completada")

    todas = cita.leer_todas_las_citas(str(filepath))
    assert len(todas) == 2
    assert todas[0]["estado"] in ["Pendiente", "Completada"]

# TEST: BUSCAR CITA POR DOCUMENTO
def test_buscar_cita_por_documento(tmp_path):
    filepath = tmp_path / "citas.json"
    cita.crear_cita(str(filepath), "999", "111", "2025-12-01", "07:00", "Odontología", "Pendiente")

    resultado = cita.buscar_cita_por_documento(str(filepath), "999")

    assert len(resultado) == 1
    assert resultado[0]["motivo"] == "Odontología"

# TEST: ACTUALIZAR CITA (usa documento_paciente)
def test_cargar_citas_json(tmp_path):
    filepath = tmp_path / "citas.json"

    # Crear una cita
    cita.crear_cita(
        str(filepath),
        "12345",
        "67890",
        "2025-10-30",
        "12:00",
        "Control general",
        "Pendiente"
    )

    # Cargar (leer) las citas del archivo
    citas_cargadas = cita.leer_todas_las_citas(str(filepath))

    # Verificar que se haya cargado correctamente
    assert len(citas_cargadas) == 1
    assert citas_cargadas[0]["documento_paciente"] == "12345"
    assert citas_cargadas[0]["motivo"] == "Control general"
    assert citas_cargadas[0]["estado"] == "Pendiente"


# TEST: ELIMINAR CITA POR DOCUMENTO
def test_eliminar_cita_por_documento(tmp_path, monkeypatch):
    filepath = tmp_path / "citas.json"
    cita.crear_cita(str(filepath), "20202", "30303", "2025-11-03", "14:00", "Vacunación", "Pendiente")

    # Simular respuestas del usuario:
    # 1 → selecciona la primera cita
    # s → confirma la eliminación
    respuestas = iter(["1", "s"])
    monkeypatch.setattr(cita.Prompt, "ask", lambda *args, **kwargs: next(respuestas))

    eliminada = cita.eliminar_cita_por_documento(str(filepath), "20202")
    assert eliminada is True

    restantes = cita.leer_todas_las_citas(str(filepath))
    assert len(restantes) == 0
