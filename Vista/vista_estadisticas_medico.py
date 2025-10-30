# Vista/vista_estadisticas_medico.py
from rich.console import Console
from rich.table import Table
from Modelo import cita, medico
import json, csv, os

console = Console()

def estadisticas_citas_por_medico(ruta_medicos="data/medicos.csv", ruta_citas="data/citas.json", mostrar=True):
    """
    Genera estadísticas de citas por médico.
    Si mostrar=False, actualiza internamente sin imprimir la tabla.
    """
    # --- Leer médicos ---
    if ruta_medicos.endswith(".csv"):
        with open(ruta_medicos, "r", encoding="utf-8") as f:
            medicos_data = list(csv.DictReader(f))
    else:
        with open(ruta_medicos, "r", encoding="utf-8") as f:
            medicos_data = json.load(f)

    # --- Leer citas ---
    if ruta_citas.endswith(".csv"):
        with open(ruta_citas, "r", encoding="utf-8") as f:
            citas_data = list(csv.DictReader(f))
    else:
        with open(ruta_citas, "r", encoding="utf-8") as f:
            try:
                citas_data = json.load(f)
            except json.JSONDecodeError:
                citas_data = []

    # --- Calcular estadísticas ---
    estadisticas = []
    for med in medicos_data:
        doc_medico = med.get("documento", "")
        nombre = f"{med.get('nombres', '')} {med.get('apellidos', '')}".strip()
        especialidad = med.get("especialidad", "N/A")

        citas_medico = [c for c in citas_data if c.get("documento_medico") == doc_medico]
        total = len(citas_medico)
        pendientes = sum(1 for c in citas_medico if c.get("estado") == "Pendiente")
        aprobadas = sum(1 for c in citas_medico if c.get("estado") == "Completada")
        canceladas = sum(1 for c in citas_medico if c.get("estado") == "Cancelada")

        estadisticas.append({
            "nombre": nombre,
            "especialidad": especialidad,
            "total": total,
            "pendientes": pendientes,
            "aprobadas": aprobadas,
            "canceladas": canceladas
        })

    if mostrar:
        tabla = Table(title="📊 Estadísticas de Citas por Médico", border_style="cyan", header_style="bold magenta")
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
