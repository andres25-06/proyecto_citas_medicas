# tests/test_gestor_datos_citas.py
# -*- coding: utf-8 -*-
import csv

from Controlador import gestor_datos_citas as gestor


def test_crud_citas_json(tmp_path):
    filepath = tmp_path / "citas.json"

    cita = {
        "id": 1,
        "paciente": "Juan Pérez",
        "medico": "Laura Mora",
        "fecha": "2025-10-28",
        "hora": "08:00",
        "motivo": "Chequeo"
    }

    gestor.crear_cita(cita, str(filepath))
    lista = gestor.leer_todas_las_citas(str(filepath))
    assert len(lista) == 1

    buscada = gestor.buscar_cita_por_id(1, str(filepath))
    assert buscada["motivo"] == "Chequeo"

    buscada["motivo"] = "Control anual"
    gestor.actualizar_cita(buscada, str(filepath))
    actualizada = gestor.buscar_cita_por_id(1, str(filepath))
    assert actualizada["motivo"] == "Control anual"

    gestor.eliminar_cita(1, str(filepath))
    assert gestor.leer_todas_las_citas(str(filepath)) == []


def test_crud_citas_csv(tmp_path):
    filepath = tmp_path / "citas.csv"
    campos = ["id", "paciente", "medico", "fecha", "hora", "motivo"]

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()

    cita = {
        "id": 2,
        "paciente": "Ana Gómez",
        "medico": "Carlos Ruiz",
        "fecha": "2025-10-29",
        "hora": "09:00",
        "motivo": "Revisión"
    }

    gestor.crear_cita(cita, str(filepath))
    lista = gestor.leer_todas_las_citas(str(filepath))
    assert lista[0]["motivo"] == "Revisión"
