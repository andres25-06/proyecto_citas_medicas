# tests/test_modelo_cita.py
# -*- coding: utf-8 -*-
import pytest
import csv
from Modelo import cita


# def test_crud_cita_json(tmp_path):
#     filepath = tmp_path / "citas.json"

#     nueva_cita = {
#         "documento_paciente": "12345",
#         "documento_medico": "67890",
#         "fecha": "2025-10-30",
#         "hora": "09:30",
#         "motivo": "Control general",
#         "estado": "Pendiente"
#     }

#     # Crear cita
#     cita.crear_cita(
#         str(filepath),
#         nueva_cita["documento_paciente"],
#         nueva_cita["documento_medico"],
#         nueva_cita["fecha"],
#         nueva_cita["hora"],
#         nueva_cita["motivo"],
#         nueva_cita["estado"]
#     )

#     # Leer citas
#     lista = cita.leer_todas_las_citas(str(filepath))
#     assert len(lista) == 1

#     # Buscar cita (por documento del paciente)
#     encontradas = cita.buscar_cita_por_documento(str(filepath), "12345")
#     assert len(encontradas) == 1
#     encontrada = encontradas[0]
#     assert encontrada["motivo"] == "Control general"

#     # Actualizar cita
#     cita.actualizar_cita(
#         str(filepath),
#         documento="12345",
#         datos_nuevos={"motivo": "Revisión anual"}
#     )

#     actualizadas = cita.buscar_cita_por_documento(str(filepath), "12345")
#     assert actualizadas[0]["motivo"] == "Revisión anual"

#     # Eliminar cita
#     cita.eliminar_cita_por_documento(str(filepath), "12345")
#     assert cita.leer_todas_las_citas(str(filepath)) == []


# def test_crud_cita_csv(tmp_path):
#     filepath = tmp_path / "citas.csv"
#     campos = ["id", "documento_paciente", "documento_medico", "fecha", "hora", "motivo", "estado"]

#     with open(filepath, "w", newline="", encoding="utf-8") as f:
#         writer = csv.DictWriter(f, fieldnames=campos)
#         writer.writeheader()

#     nueva_cita = {
#         "documento_paciente": "54321",
#         "documento_medico": "09876",
#         "fecha": "2025-11-01",
#         "hora": "10:00",
#         "motivo": "Chequeo dental",
#         "estado": "Pendiente"
#     }

#     # Crear cita
#     cita.crear_cita(
#         str(filepath),
#         nueva_cita["documento_paciente"],
#         nueva_cita["documento_medico"],
#         nueva_cita["fecha"],
#         nueva_cita["hora"],
#         nueva_cita["motivo"],
#         nueva_cita["estado"]
#     )

#     lista = cita.leer_todas_las_citas(str(filepath))
#     assert len(lista) == 1
#     assert lista[0]["motivo"] == "Chequeo dental"
