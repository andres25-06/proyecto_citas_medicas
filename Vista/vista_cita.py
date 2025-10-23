# -*- coding: utf-8 -*-
"""
Vista del Módulo de Cita sss.

Maneja la interacción con el usuario (menús, entradas, salidas)
usando la librería Rich. Toda la lógica de presentación y flujo
del módulo de citas está aquí.
"""

import os
from Modelo import  medico, paciente  # Importamos la lógica de los modelos
from Modelo import cita  

# --- Librería Rich ---
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt, Confirm
from rich.table import Table
import os


console = Console()

# --- Configuración de rutas ---
DIRECTORIO_DATOS = 'data'
NOMBRE_ARCHIVO_JSON = 'citas.json'


def menu_agendar_cita(filepath: str):
    console.print(Panel.fit("[bold cyan]🩺 Agendar Nueva Cita[/bold cyan]"))

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


def menu_cancelar_cita(filepath: str):
    """Cancelar (eliminar) una cita médica por documento del paciente."""
    console.print(Panel.fit("[bold cyan]🗓️  Cancelar Cita por Documento del Paciente[/bold cyan]"))
    
    documento = Prompt.ask("Ingrese el documento del paciente para cancelar su cita")
    
    # ✅ Primero buscar si existen citas con ese documento
    import Modelo.cita as cita
    citas_encontradas = cita.buscar_cita_por_documento(filepath, documento)
    
    if not citas_encontradas:
        console.print("[bold red]❌ No se encontró ninguna cita con ese documento.[/bold red]")
        return
    
    # Mostrar las citas encontradas
    console.print(f"\n[bold green]Se encontraron {len(citas_encontradas)} cita(s):[/bold green]")
    for c in citas_encontradas:
        console.print(f"  • ID: {c.get('id')} - Fecha: {c.get('fecha')} - Médico: {c.get('documento_medico')} - Estado: {c.get('estado')}")
    
    # Pedir confirmación
    if Confirm.ask(f"¿Está seguro de cancelar todas las citas del paciente con documento {documento}?", default=False):
        # Aquí va tu lógica de eliminación
        if cita.eliminar_cita_por_documento(filepath, documento):
           console.print("[bold green]✅ Cita(s) cancelada(s) exitosamente.[/bold green]")
        else:
            console.print("[bold red]❌ Error al cancelar la(s) cita(s).[/bold red]")

def menu_ver_todas_citas(filepath: str):
    """Mostrar todas las citas médicas registradas."""
    console.print(Panel.fit("[bold cyan]📋 Lista de Todas las Citas[/bold cyan]"))
    citas_registradas = cita.leer_todas_las_citas(filepath)

    if not citas_registradas:
        console.print("[yellow]No hay citas registradas.[/yellow]")
        return

    tabla = Table(title="Citas Médicas Registradas", border_style="blue", header_style="bold magenta")
    tabla.add_column("ID", style="dim", width=6)
    tabla.add_column("Documento Paciente")
    tabla.add_column("Documento Médico")
    tabla.add_column("Fecha", justify="center")
    tabla.add_column("Hora", justify="center")
    tabla.add_column("Motivo")
    tabla.add_column("Estado", justify="center")

    for c in citas_registradas:
        paciente_nombre = paciente.obtener_nombre_por_documento(c["documento_paciente"]) if hasattr(paciente, "obtener_nombre_por_documento") else c["documento_paciente"]
        medico_nombre = medico.obtener_nombre_por_documento(c["documento_medico"]) if hasattr(medico, "obtener_nombre_por_documento") else c["documento_medico"]

        tabla.add_row(
            c["id"], paciente_nombre, medico_nombre,
            c["fecha"], c["hora"], c["motivo"], c["estado"]
        )

    console.print(tabla)


def menu_buscar_cita(filepath: str):
    """Buscar una cita por documento"""
    console.print(Panel.fit("[bold cyan]🔍 Buscar Cita por documento[/bold cyan]"))
    documento = Prompt.ask("Ingrese el documento de la cita")
    cita_encontrada = cita.buscar_cita_por_documento(filepath, documento)

    if cita_encontrada:
        for item in cita_encontrada:  # ← Aquí cambia
            console.print(Panel(
                f"[bold green]Cita encontrada:[/bold green]\n"
                f"Paciente: {item['documento_paciente']}\n"
                f"Médico: {item['documento_medico']}\n"
                f"Fecha: {item['fecha']}\n"
                f"Hora: {item['hora']}\n"
                f"Motivo: {item['motivo']}\n"
                f"Estado: {item['estado']}",
                border_style="green",
                title=f"Cita #{item['id']}"
            ))
    else:
        console.print("[yellow]No se encontró ninguna cita con ese documento.[/yellow]")



# =========================================================
# 🔹 Menú principal del módulo
# =========================================================
def mostrar_menu_citas():
    """Imprime el menú principal del módulo de citas."""
    opciones = (
        "[bold yellow]1[/bold yellow]. Agendar una nueva cita\n"
        "[bold yellow]2[/bold yellow]. Cancelar una cita\n"
        "[bold yellow]3[/bold yellow]. Ver todas las citas\n"
        "[bold yellow]4[/bold yellow]. Buscar cita por \n"
        "[bold red]5[/bold red]. Volver al menú principal"
    )
    console.print(Panel(opciones, title="[bold cyan]MÓDULO DE CITAS MÉDICAS[/bold cyan]", border_style="green"))

def main_vista_citas():
    """Bucle principal del módulo de citas."""
    archivo_citas = os.path.join(DIRECTORIO_DATOS, NOMBRE_ARCHIVO_JSON)
    console.print(f"\n📁 Usando archivo de datos: [bold green]{archivo_citas}[/bold green]")

    while True:
        mostrar_menu_citas()
        opcion = Prompt.ask("Seleccione una opción", choices=["1", "2", "3", "4", "5"], show_choices=False)

        if opcion == "1":
            menu_agendar_cita(archivo_citas)
        elif opcion == "2":
            menu_cancelar_cita(archivo_citas)
        elif opcion == "3":
            menu_ver_todas_citas(archivo_citas)
        elif opcion == "4":
            menu_buscar_cita(archivo_citas)
        elif opcion == "5":
            console.print("\n[cyan]⬅️ Volviendo al menú principal...[/cyan]")
            break
