# tests/test_modelo_cita.py
# -*- coding: utf-8 -*-
import pytest
from Modelo import cita
import csv

def test_crud_cita_json(tmp_path):
    filepath = tmp_path / "citas.json"
    nueva_cita = {
        "documento_paciente": "12345",
        "documento_medico": "67890",
        "fecha": "2025-10-30",
        "hora": "12:00",
        "motivo": "Control general",
        "estado": "Pendiente"
    }
    cita_creada = cita.crear_cita(
        str(filepath),
        nueva_cita["documento_paciente"],
        nueva_cita["documento_medico"],
        nueva_cita["fecha"],    
        nueva_cita["hora"],   
        nueva_cita["motivo"],
        nueva_cita["estado"]
    )

    assert cita is not None
    lista=cita.leer_todas_las_citas(str(filepath))
    assert len(lista) == 1
   # Buscar por documento
    encontradas = cita.buscar_cita_por_documento(str(filepath), "12345")
    assert len(encontradas) == 1
    assert encontradas[0]["motivo"] == "Control general"

    # Actualizar cita
    datos_actualizados = {"motivo": "Revisión anual"}
    actualizada = cita.actualizar_cita(str(filepath), "12345", datos_actualizados)
    assert actualizada is not None
    assert actualizada["motivo"] == "Revisión anual"

    # Eliminar cita
    eliminada = cita.eliminar_cita_por_documento(str(filepath), "12345")
    assert eliminada is True
    assert cita.leer_todas_las_citas(str(filepath)) == []

def test_crud_cita_csv(tmp_path):
    filepath = tmp_path / "citas.csv"
    campos = ["id", "documento_paciente", "documento_medico", "fecha", "hora", "motivo", "estado"]

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()

    nueva_cita = {
        "documento_paciente": "54321",
        "documento_medico": "09876",
        "fecha": "2025-11-01",
        "motivo": "Chequeo dental",
        "estado": "Pendiente"
    }

    creada = cita.crear_cita(
        str(filepath),
        nueva_cita["documento_paciente"],
        nueva_cita["documento_medico"],
        nueva_cita["fecha"], 
        "10:00",                 
        nueva_cita["motivo"],
        nueva_cita["estado"]
    )

    assert creada is not None
    lista = cita.leer_todas_las_citas(str(filepath))
    assert len(lista) == 1
    assert lista[0]["motivo"] == "Chequeo dental"

    datos_actualizados = {"motivo": "Control dental"}
    actualizada = cita.actualizar_cita(str(filepath), "54321", datos_actualizados)
    assert actualizada is not None
    assert actualizada["motivo"] == "Control dental"

    eliminada = cita.eliminar_cita_por_documento(str(filepath), "54321")
    assert eliminada is True
    assert cita.leer_todas_las_citas(str(filepath)) == []
