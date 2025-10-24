import os
from Modelo import cita, medico, paciente
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt, Confirm
from rich.table import Table

console = Console()
DIRECTORIO_DATOS = 'data'
NOMBRE_ARCHIVO_JSON = 'citas.json'


def menu_agendar_cita(filepath: str):
    """
    Menú para agendar una nueva cita médica.
    
    Args:
        filepath (str): La ruta al archivo donde se almacenan las citas.
    
    Returns:
        none
    """
    console.print(Panel.fit("[bold cyan]🩺 Agendar Nueva Cita[/bold cyan]"))

    doc_paciente = Prompt.ask("Documento del Paciente")
    doc_medico = Prompt.ask("Documento del Médico")
    fecha = Prompt.ask("Fecha (YYYY-MM-DD)")
    hora = Prompt.ask("Hora (HH:MM)")
    motivo = Prompt.ask("Motivo de la consulta")
    estado = "Pendiente"

    cita_creada = cita.crear_cita(filepath, doc_paciente, doc_medico, fecha, hora, motivo, estado)

    if cita_creada:
        console.print(Panel(
            f"✅ ¡Cita creada con éxito!\nID: [yellow]{cita_creada['id']}[/yellow]",
            border_style="green", title="Éxito"
        ))
    else:
        console.print(Panel("⚠️ Ya existe una cita en ese horario.", border_style="red", title="Error"))


def menu_cancelar_cita(filepath: str):
    """
    Menú para cancelar una cita médica existente.
    
    Args:
        filepath (str): La ruta al archivo donde se almacenan las citas.        
        
    Returns:
        none    
    """
    console.print(Panel.fit("[bold cyan]🗑️ Cancelar Cita[/bold cyan]"))
    id_cita = Prompt.ask("ID de la cita a cancelar")

    if Confirm.ask(f"¿Está seguro de cancelar la cita #{id_cita}?"):
        if cita.eliminar_cita(filepath, id_cita):
            console.print(Panel("✅ ¡Cita cancelada!", border_style="green", title="Éxito"))
        else:
            console.print(Panel("❌ No se encontró la cita.", border_style="red", title="Error"))
    else:
        console.print("[yellow]Operación cancelada.[/yellow]")


def menu_ver_todas_citas(filepath: str):
    
    """
    Muestra todas las citas médicas registradas.
    
    Args:
        filepath (str): La ruta al archivo donde se almacenan las citas.
        
    Returns:
        none
    """
    console.print(Panel.fit("[bold cyan]📋 Lista de Citas[/bold cyan]"))
    citas_registradas = cita.leer_todas_las_citas(filepath)

    if not citas_registradas:
        console.print("[yellow]No hay citas registradas.[/yellow]")
        return

    tabla = Table(title="Citas Médicas", border_style="blue")
    tabla.add_column("ID", style="dim")
    tabla.add_column("Paciente")
    tabla.add_column("Médico")
    tabla.add_column("Fecha")
    tabla.add_column("Hora")
    tabla.add_column("Motivo")

    for c in citas_registradas:
        paciente_info = paciente.obtener_nombre_por_id(c["documento_paciente"])
        medico_info = medico.obtener_nombre_por_id(c["documento_medico"])
        tabla.add_row(c["id"], paciente_info, medico_info, c["fecha"], c["hora"], c["motivo"])

    console.print(tabla)


def mostrar_menu_citas():
    
    """
    Muestra el menú principal del módulo de citas.
    
    Args:
        none
    Returns:
        none
    """
    texto = (
        "[1] Agendar cita\n"
        "[2] Cancelar cita\n"
        "[3] Ver todas las citas\n"
        "[4] Volver al menú principal"
    )
    console.print(Panel(texto, title="[bold green]MÓDULO DE CITAS[/bold green]", border_style="cyan"))


def main_vista_citas():
    """
    Función principal para manejar el menú de citas médicas.
    
    Args:
        none
    Returns:
        none
    """
    filepath = os.path.join(DIRECTORIO_DATOS, NOMBRE_ARCHIVO_JSON)

    while True:
        mostrar_menu_citas()
        opcion = Prompt.ask("Opción", choices=["1", "2", "3", "4"], show_choices=False)

        if opcion == "1":
            menu_agendar_cita(filepath)
        elif opcion == "2":
            menu_cancelar_cita(filepath)
        elif opcion == "3":
            menu_ver_todas_citas(filepath)
        elif opcion == "4":
            console.print("[cyan]⬅️ Volviendo al menú principal...[/cyan]")
            break
