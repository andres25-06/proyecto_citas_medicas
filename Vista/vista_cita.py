"""
Vista del Módulo de Cita.

Maneja la interacción con el usuario (menús, entradas, salidas)
usando la librería Rich. Toda la lógica de presentación y flujo
del módulo de citas está aquí.
"""

import os
from Modelo import cita, medico, paciente  # Importamos la lógica de los modelos

# --- Importaciones de la librería Rich ---
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, IntPrompt, Prompt
from rich.table import Table

# --- Inicialización de la Consola de Rich ---
console = Console()

# --- Constantes de Configuración de Rutas ---
DIRECTORIO_DATOS = 'data'
NOMBRE_ARCHIVO_CSV = 'citas.csv'
NOMBRE_ARCHIVO_JSON = 'citas.json'


# =========================================================
# 🔹 Funciones del Menú de Citas
# =========================================================
def menu_agendar_cita(filepath: str):
    """Agendar una nueva cita médica."""
    console.print(Panel.fit("[bold cyan]🩺 Agendar Nueva Cita[/bold cyan]"))

    id_paciente = IntPrompt.ask("ID del Paciente")
    id_medico = IntPrompt.ask("ID del Médico")
    fecha = Prompt.ask("Fecha (formato: YYYY-MM-DD)")
    hora = Prompt.ask("Hora (formato 24h: HH:MM)")
    motivo = Prompt.ask("Motivo de la consulta")

    # Validar si el médico está disponible en esa fecha y hora
    if not cita.medico_disponible(filepath, id_medico, fecha, hora):
        console.print(Panel(
            "⚠️ El médico ya tiene una cita en esa fecha y hora. Intente con otro horario.",
            border_style="red", title="Conflicto de Horario"
        ))
        return

    cita_creada = cita.crear_cita(filepath, id_paciente, id_medico, fecha, hora, motivo)
    if cita_creada:
        console.print(Panel(
            f"✅ ¡Cita creada con éxito!\n   ID Cita: [bold yellow]{cita_creada['id_cita']}[/bold yellow]",
            border_style="green", title="Éxito"
        ))
    else:
        console.print(Panel(
            "❌ Ocurrió un error al crear la cita.",
            border_style="red", title="Error"
        ))


def menu_cancelar_cita(filepath: str):
    """Cancelar (eliminar) una cita médica."""
    console.print(Panel.fit("[bold cyan]🗑️ Cancelar Cita[/bold cyan]"))
    id_cita = IntPrompt.ask("Ingrese el ID de la cita a cancelar")

    confirmacion = Confirm.ask(f"¿Está seguro de cancelar la cita #{id_cita}?", default=False)

    if confirmacion:
        if cita.eliminar_cita(filepath, str(id_cita)):
            console.print(Panel("✅ ¡Cita cancelada con éxito!", border_style="green", title="Éxito"))
        else:
            console.print(Panel("❌ No se encontró la cita o no se pudo eliminar.", border_style="red", title="Error"))
    else:
        console.print("\n[yellow]Operación cancelada.[/yellow]")


def menu_ver_citas_por_medico(filepath: str):
    """Ver todas las citas programadas para un médico en una fecha específica."""
    console.print(Panel.fit("[bold cyan]📆 Ver Citas por Médico y Fecha[/bold cyan]"))
    id_medico = IntPrompt.ask("ID del Médico")
    fecha = Prompt.ask("Fecha (formato: YYYY-MM-DD)")

    citas_medico = cita.obtener_citas_por_medico_y_fecha(filepath, id_medico, fecha)

    if not citas_medico:
        console.print(f"[yellow]No hay citas para el médico #{id_medico} en la fecha {fecha}.[/yellow]")
        return

    tabla = Table(title=f"Citas del Médico #{id_medico} - {fecha}", border_style="blue", header_style="bold magenta")
    tabla.add_column("ID Cita", style="dim")
    tabla.add_column("Paciente")
    tabla.add_column("Hora", justify="center")
    tabla.add_column("Motivo")

    for c in citas_medico:
        paciente_info = paciente.obtener_nombre_por_id(c["id_paciente"])
        tabla.add_row(c["id_cita"], paciente_info, c["hora"], c["motivo_consulta"])

    console.print(tabla)


def menu_ver_todas_citas(filepath: str):
    """Mostrar todas las citas médicas programadas."""
    console.print(Panel.fit("[bold cyan]📋 Lista de Todas las Citas[/bold cyan]"))
    citas_registradas = cita.leer_todas_las_citas(filepath)

    if not citas_registradas:
        console.print("[yellow]No hay citas registradas.[/yellow]")
        return

    tabla = Table(title="Citas Médicas Registradas", border_style="blue", show_header=True, header_style="bold magenta")
    tabla.add_column("ID Cita", style="dim", width=8)
    tabla.add_column("Paciente")
    tabla.add_column("Médico")
    tabla.add_column("Fecha")
    tabla.add_column("Hora")
    tabla.add_column("Motivo")

    for c in citas_registradas:
        paciente_info = paciente.obtener_nombre_por_id(c["id_paciente"])
        medico_info = medico.obtener_nombre_por_id(c["id_medico"])
        tabla.add_row(c["id_cita"], paciente_info, medico_info, c["fecha"], c["hora"], c["motivo_consulta"])

    console.print(tabla)


def mostrar_menu_citas():
    """Imprime el menú principal del módulo de citas."""
    menu_texto = (
        "[bold yellow]1[/bold yellow]. Agendar una nueva cita\n"
        "[bold yellow]2[/bold yellow]. Cancelar una cita\n"
        "[bold yellow]3[/bold yellow]. Ver todas las citas\n"
        "[bold yellow]4[/bold yellow]. Ver citas por médico y fecha\n"
        "[bold red]5[/bold red]. Volver al menú principal"
    )
    console.print(Panel(menu_texto, title="[bold]MÓDULO DE CITAS MÉDICAS[/bold]", border_style="green"))


# =========================================================
# 🔹 Función principal del módulo (llamada desde main.py)
# =========================================================
def main_vista_citas():
    """Bucle principal del módulo de citas."""
    archivo_citas = os.path.join(DIRECTORIO_DATOS, NOMBRE_ARCHIVO_JSON)
    console.print(f"\n👍 Usando el archivo: [bold green]{archivo_citas}[/bold green]")

    while True:
        mostrar_menu_citas()
        opcion = Prompt.ask("Opción", choices=["1", "2", "3", "4", "5"], show_choices=False)

        if opcion == '1':
            menu_agendar_cita(archivo_citas)
        elif opcion == '2':
            menu_cancelar_cita(archivo_citas)
        elif opcion == '3':
            menu_ver_todas_citas(archivo_citas)
        elif opcion == '4':
            menu_ver_citas_por_medico(archivo_citas)
        elif opcion == '5':
            console.print("\n[bold cyan]⬅️ Volviendo al menú principal...[/bold cyan]")
            break
