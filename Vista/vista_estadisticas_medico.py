# -- coding: utf-8 --


import csv
import json
import os

from rich.console import Console
from rich.table import Table

console = Console()


def cargar_datos(ruta):
    """Carga datos desde un archivo CSV o JSON."""
    if not os.path.exists(ruta):
        return []

    try:
        if ruta.endswith(".csv"):
            with open(ruta, "r", encoding="utf-8") as f:
                return list(csv.DictReader(f))
        elif ruta.endswith(".json"):
            with open(ruta, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            console.print(f"[yellow]⚠ Formato no soportado: {ruta}[/yellow]")
            return []
    except Exception as e:
        console.print(f"[red]⚠ Error al leer {ruta}:[/red] {e}")
        return []


def estadisticas_citas_por_medico(
    ruta_medicos_csv="data/medicos.csv",
    ruta_medicos_json="data/medicos.json",
    ruta_citas_csv="data/citas.csv",
    ruta_citas_json="data/citas.json",
    mostrar=True
):
    """
    Genera estadísticas de citas por médico, combinando datos
    de archivos CSV y/o JSON según disponibilidad.
    """

    # --- Cargar médicos (prioriza CSV, luego JSON) ---
    medicos_data = cargar_datos(ruta_medicos_csv) or cargar_datos(ruta_medicos_json)
    # --- Cargar citas (prioriza JSON, luego CSV) ---
    citas_data = cargar_datos(ruta_citas_json) or cargar_datos(ruta_citas_csv)

    estadisticas = []

    for med in medicos_data:
        doc_medico = str(med.get("documento", "")).strip()
        nombre = f"{med.get('nombres', '')} {med.get('apellidos', '')}".strip()
        especialidad = med.get("especialidad", "N/A")

        # Buscar citas asociadas (comparación flexible)
        citas_medico = [
            c for c in citas_data
            if str(c.get("documento_medico", "")).strip() == doc_medico
        ]

        total = len(citas_medico)
        pendientes = aprobadas = canceladas = 0

        for c in citas_medico:
            estado = str(c.get("estado", "")).strip().lower()
            if estado == "pendiente":
                pendientes += 1
            elif estado in ["completada", "aprobada", "finalizada"]:
                aprobadas += 1
            elif estado in ["cancelada", "anulada"]:
                canceladas += 1

        estadisticas.append({
            "nombre": nombre,
            "especialidad": especialidad,
            "total": total,
            "pendientes": pendientes,
            "aprobadas": aprobadas,
            "canceladas": canceladas
        })

    # --- Mostrar tabla ---
    if mostrar:
        tabla = Table(
            title="📊 Estadísticas de Citas por Médico",
            border_style="cyan",
            header_style="bold magenta"
        )

        tabla.add_column("👨‍⚕️ Médico")
        tabla.add_column("🩺 Especialidad")
        tabla.add_column("📅 Total", justify="center")
        tabla.add_column("⏳ Pendientes", justify="center")
        tabla.add_column("✅ Aprobadas", justify="center")
        tabla.add_column("❌ Canceladas", justify="center")

        for e in estadisticas:
            tabla.add_row(
                e["nombre"],
                e["especialidad"],
                str(e["total"]),
                str(e["pendientes"]),
                str(e["aprobadas"]),
                str(e["canceladas"]),
            )

        console.print(tabla)

    return estadisticas


# Permitir ejecución directa desde consola
if __name__ == "__main__":
    estadisticas_citas_por_medico()
