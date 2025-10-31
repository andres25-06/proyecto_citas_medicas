# tests/test_modelo_cita.py
# -*- coding: utf-8 -*-
import csv

from Modelo import cita


def test_crud_cita_json(tmp_path):
    filepath = tmp_path / "citas.json"

    nueva_cita = {
        "id": 1,
        "paciente": "María Gómez",
        "medico": "Pedro Jiménez",
        "fecha": "2025-10-30",
        "hora": "09:30",
        "motivo": "Control general"
    }

    cita.crear_cita(nueva_cita, str(filepath))

    lista = cita.leer_todas_las_citas(str(filepath))
    assert len(lista) == 1

    encontrada = cita.buscar_cita_por_id(1, str(filepath))
    assert encontrada["motivo"] == "Control general"

    encontrada["motivo"] = "Revisión anual"
    cita.actualizar_cita(encontrada, str(filepath))
    actualizada = cita.buscar_cita_por_id(1, str(filepath))
    assert actualizada["motivo"] == "Revisión anual"

    cita.eliminar_cita(1, str(filepath))
    assert cita.leer_todas_las_citas(str(filepath)) == []


def test_crud_cita_csv(tmp_path):
    filepath = tmp_path / "citas.csv"
    campos = ["id", "paciente", "medico", "fecha", "hora", "motivo"]

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()

    nueva_cita = {
        "id": 2,
        "paciente": "Luis Torres",
        "medico": "Claudia Morales",
        "fecha": "2025-11-01",
        "hora": "10:00",
        "motivo": "Chequeo dental"
    }

    cita.crear_cita(nueva_cita, str(filepath))
    lista = cita.leer_todas_las_citas(str(filepath))
    assert lista[0]["motivo"] == "Chequeo dental"
