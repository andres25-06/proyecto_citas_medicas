# -*- coding: utf-8 -*-
"""
Vista del Módulo de Citas Médicas con navegación por flechas ↑ ↓
y estilo visual coherente con los demás módulos.
"""

import os
import readchar
from Modelo import medico, paciente, cita
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt, Confirm
from rich.table import Table

console = Console()

# --- Configuración de rutas ---
DIRECTORIO_DATOS = 'data'
NOMBRE_ARCHIVO_JSON = 'citas.json'


# =========================================================
# 🔹 Funciones auxiliares
# =========================================================
def limpiar():
    os.system("cls" if os.name == "nt" else "clear")


def selector_interactivo(titulo, opciones):
    """Permite moverse con flechas ↑ ↓ y seleccionar con Enter."""
    seleccion = 0
    while True:
        limpiar()
        console.print(Panel(f"[bold cyan]{titulo}[/bold cyan]"))
        for i, opt in enumerate(opciones):
            prefix = "👉 " if i == seleccion else "   "
            if "Volver" in opt:
                estilo = "reverse bold red" if i == seleccion else "bold red"
            else:
                estilo = "reverse bold green" if i == seleccion else ""
            console.print(prefix + opt, style=estilo)

        tecla = readchar.readkey()
        if tecla == readchar.key.UP:
            seleccion = (seleccion - 1) % len(opciones)
        elif tecla == readchar.key.DOWN:
            seleccion = (seleccion + 1) % len(opciones)
        elif tecla == readchar.key.ENTER:
            return seleccion


# =========================================================
# 🔹 Funciones del módulo de Citas
# =========================================================
def menu_agendar_cita(filepath: str):
    console.print(Panel.fit("[bold cyan]📅 Agendar Nueva Cita[/bold cyan]"))

    documento_paciente = Prompt.ask("Documento del Paciente")
    documento_medico = Prompt.ask("Documento del Médico")
    fecha = Prompt.ask("Fecha (YYYY-MM-DD)")
    hora = Prompt.ask("Hora (HH:MM)")
    motivo = Prompt.ask("Motivo de la consulta")
    estado = Prompt.ask("Estado de la cita (Pendiente/Completada/Cancelada)", default="Pendiente")

    cita_creada = cita.crear_cita(filepath, documento_paciente, documento_medico, fecha, hora, motivo, estado)

    if cita_creada:
        console.print(Panel(
            f"✅ ¡Cita creada con éxito!\nID: [bold yellow]{cita_creada['id']}[/bold yellow]",
            border_style="green", title="Éxito"
        ))
    else:
        console.print(Panel(
            "⚠️ Ya existe una cita con esos datos o ocurrió un error.",
            border_style="red", title="Error"
        ))
    input("\nPresione Enter para continuar...")


def menu_cancelar_cita(filepath: str):
    """Cancelar (eliminar) una cita médica por documento del paciente."""
    console.print(Panel.fit("[bold cyan]❌ Cancelar Cita por Documento del Paciente[/bold cyan]"))

    documento = Prompt.ask("Ingrese el documento del paciente para cancelar su cita")
    citas_encontradas = cita.buscar_cita_por_documento(filepath, documento)

    if not citas_encontradas:
        console.print("[bold red]❌ No se encontró ninguna cita con ese documento.[/bold red]")
        input("\nPresione Enter para continuar...")
        return

    console.print(f"\n[bold green]Se encontraron {len(citas_encontradas)} cita(s):[/bold green]")
    for c in citas_encontradas:
        console.print(
            f"  • ID: {c.get('id')} | Fecha: {c.get('fecha')} | Médico: {c.get('documento_medico')} | Estado: {c.get('estado')}"
        )

    if Confirm.ask(f"¿Está seguro de cancelar todas las citas del paciente con documento {documento}?", default=False):
        if cita.eliminar_cita_por_documento(filepath, documento):
            console.print("[bold green]✅ Cita(s) cancelada(s) exitosamente.[/bold green]")
        else:
            console.print("[bold red]❌ Error al cancelar la(s) cita(s).[/bold red]")
    else:
        console.print("[yellow]Operación cancelada.[/yellow]")
    input("\nPresione Enter para continuar...")


def obtener_nombre_completo_por_documento(filepath: str, documento: str, tipo: str) -> str:
    """Devuelve el nombre completo de un paciente o médico según su documento."""
    try:
        if tipo == "paciente":
            registros = paciente.leer_todos_los_pacientes(filepath)
        else:
            registros = medico.leer_todos_los_medicos(filepath)

        for r in registros:
            if r.get("documento") == documento:
                return f"{r.get('nombres', '')} {r.get('apellidos', '')}".strip()
        return f"{documento} (no encontrado)"
    except Exception as e:
        return f"Error: {e}"

def menu_ver_todas_citas(filepath: str):
    """Mostrar todas las citas médicas registradas."""
    console.print(Panel.fit("[bold cyan]📋 Lista de Todas las Citas[/bold cyan]"))
    citas_registradas = cita.leer_todas_las_citas(filepath)

    if not citas_registradas:
        console.print("[yellow]No hay citas registradas.[/yellow]")
        input("\nPresione Enter para continuar...")
        return

    tabla = Table(title="Citas Médicas Registradas", border_style="blue", header_style="bold magenta")
    tabla.add_column("ID", style="dim", width=6)
    tabla.add_column("Paciente")
    tabla.add_column("Médico")
    tabla.add_column("Fecha", justify="center")
    tabla.add_column("Hora", justify="center")
    tabla.add_column("Motivo")
    tabla.add_column("Estado", justify="center")

    for c in citas_registradas:
        paciente_nombre = obtener_nombre_completo_por_documento("data/pacientes.json", c["documento_paciente"], "paciente")
        medico_nombre = obtener_nombre_completo_por_documento("data/medicos.json", c["documento_medico"], "medico")

        tabla.add_row(
            c["id"],
            paciente_nombre,
            medico_nombre,
            c["fecha"],
            c["hora"],
            c["motivo"],
            c["estado"]
        )

    console.print(tabla)
    input("\nPresione Enter para continuar...")


def obtener_nombre_completo_por_documento(filepath: str, documento: str, tipo: str) -> str:
    """Devuelve el nombre completo de un paciente o médico según su documento."""
    try:
        if tipo == "paciente":
            registros = paciente.leer_todos_los_pacientes("data/pacientes.json")
            registros = paciente.leer_todos_los_pacientes("data/pacientes.csv")
        else:
            registros = medico.leer_todos_los_medicos("data/medicos.json")
            registros = medico.leer_todos_los_medicos("data/medicos.csv")

        for r in registros:
            if r.get("documento") == documento:
                return f"{r.get('nombres', '')} {r.get('apellidos', '')}".strip()
        return f"{documento} (no encontrado)"
    except Exception as e:
        return f"Error: {e}"

def menu_buscar_cita(filepath: str):
    """Buscar una cita por documento (paciente o médico)."""
    console.print(Panel.fit("[bold cyan]🔍 Buscar Cita por Documento[/bold cyan]"))
    documento = Prompt.ask("Ingrese el documento del paciente o médico")
    citas_encontradas = cita.buscar_cita_por_documento(filepath, documento)

    if citas_encontradas:
        for item in citas_encontradas:
            paciente_nombre = obtener_nombre_completo_por_documento("data/pacientes.json", item["documento_paciente"], "paciente")
            medico_nombre = obtener_nombre_completo_por_documento("data/medicos.json", item["documento_medico"], "medico")

            console.print(Panel(
                f"[bold green]Cita encontrada:[/bold green]\n"
                f"🧍 Paciente: [yellow]{paciente_nombre}[/yellow]\n"
                f"🩺 Médico: [yellow]{medico_nombre}[/yellow]\n"
                f"📅 Fecha: [cyan]{item['fecha']}[/cyan]\n"
                f"⏰ Hora: [cyan]{item['hora']}[/cyan]\n"
                f"💬 Motivo: {item['motivo']}\n"
                f"📌 Estado: {item['estado']}",
                border_style="green",
                title=f"Cita #{item['id']}"
            ))
    else:
        console.print("[yellow]⚠️ No se encontró ninguna cita con ese documento.[/yellow]")
    
    input("\nPresione Enter para continuar...")


# =========================================================
# 🔹 Menú principal interactivo
# =========================================================
def main_vista_citas():
    """Bucle principal del módulo de citas con selector interactivo."""
    archivo_citas = os.path.join(DIRECTORIO_DATOS, NOMBRE_ARCHIVO_JSON)
    console.print(f"\n📁 Usando archivo de datos: [bold green]{archivo_citas}[/bold green]")

    opciones = [
        "🩺 Agendar una nueva cita",
        "❌ Cancelar una cita",
        "📋 Ver todas las citas",
        "🔍 Buscar cita por documento",
        "⬅️ Volver al menú principal"
    ]

    titulo = "📅 MÓDULO DE CITAS MÉDICAS\nUsa ↑ ↓ y Enter para seleccionar una opción"

    while True:
        seleccion = selector_interactivo(titulo, opciones)

        if seleccion == 0:
            menu_agendar_cita(archivo_citas)
        elif seleccion == 1:
            menu_cancelar_cita(archivo_citas)
        elif seleccion == 2:
            menu_ver_todas_citas(archivo_citas)
        elif seleccion == 3:
            menu_buscar_cita(archivo_citas)
        elif seleccion == 4:
            console.print("\n[bold red]⬅ Volviendo al menú principal...[/bold red]")
            break


# =========================================================
# 🔹 Ejecución directa (para pruebas)
# =========================================================
if __name__ == "__main__":
    main_vista_citas()
