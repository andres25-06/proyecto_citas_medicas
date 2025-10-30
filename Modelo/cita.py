# -*- coding: utf-8 -*-
"""
Módulo de Lógica de Negocio - Citas

Contiene todas las funciones para gestionar las citas (CRUD).
Este módulo utiliza 'gestor_datos' para la persistencia.
"""
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from typing import Any, Dict, List, Optional

from Controlador import gestor_datos_citas


def generar_id(citas: List[Dict[str, Any]]) -> int:
    """
    Genera un nuevo ID autoincremental para una cita.

        Args:
            citas (List[Dict[str, Any]]): La lista actual de las citas.
            
        Returns:
            int: El nuevo ID a asignar.
    """
    if not citas:
        return 1
    max_id = max(int(cita.get('id', 0)) for cita in citas)
    return max_id + 1


def crear_cita(
        filepath: str,
        documento_paciente: str,
        documento_medico: str,
        fecha: str,
        hora: str,
        motivo: str,
        estado: str
) -> Optional[Dict[str, Any]]:
    """
    (CREATE) Agrega una nueva cita.

        Valida que no exista una cita para el mismo paciente, médico, fecha y hora.

        Args:
            filepath (str): Ruta al archivo de datos.
            documento_paciente (str): Documento del paciente.
            documento_medico (str): Documento del médico.
            fecha (str): Fecha de la cita (YYYY-MM-DD).
            motivo (str): Motivo de la cita.
            estado (str): Estado actual de la cita (ej. 'Pendiente', 'Completada', 'Cancelada').

        Returns:
            Optional[Dict[str, Any]]: El diccionario de la cita creada o None si ya existía.
    """
    citas = gestor_datos_citas.cargar_datos(filepath)

    # Validar si ya existe una cita para el mismo paciente, médico, fecha y hora
    for cita in citas:
        if (cita.get('documento_paciente') == documento_paciente and
            cita.get('documento_medico') == documento_medico and
            cita.get('fecha') == fecha ):
            cita.get('hora') == hora
            print("\n Error: Ya existe una cita registrada para ese paciente, médico, fecha y hora.")
            return None

    nuevo_id = generar_id(citas)

    nueva_cita = {
        'id': str(nuevo_id),
        'documento_paciente': documento_paciente,
        'documento_medico': documento_medico,
        'fecha': fecha,
        'hora': hora,
        'motivo': motivo,
        'estado': estado
    }

    citas.append(nueva_cita)
    gestor_datos_citas.guardar_datos(filepath, citas)
    return nueva_cita


def leer_todas_las_citas(filepath: str) -> List[Dict[str, Any]]:
    """
        (READ) Obtiene la lista completa de las citas.

        Args:
            filepath (str): Ruta al archivo de datos.

        Returns:
            List[Dict[str, Any]]: La lista de citas.
    """
    return gestor_datos_citas.cargar_datos(filepath)



def buscar_cita_por_documento(filepath: str, documento_paciente: str) -> list[Dict[str, Any]]:
    """
        Busca una cita específica por su documento.

        Args:
            filepath (str): Ruta al archivo de datos.
            documento (str): documento de la cita a buscar.

        Returns:
            Optional[Dict[str, Any]]: El diccionario de la cita si se encuentra, de lo contrario None.
    """
    citas = gestor_datos_citas.cargar_datos(filepath)
    return [c for c in citas if c.get('documento_paciente') == documento_paciente]


def actualizar_cita(filepath: str, id_cita: str, datos_nuevos: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    (UPDATE) Actualiza los datos de una cita existente.

    Args:
        filepath (str): Ruta del archivo JSON con las citas.
        id_cita (str): ID de la cita a actualizar.
        datos_nuevos (Dict[str, Any]): Campos que se actualizarán.

    Returns:
        Optional[Dict[str, Any]]: Cita actualizada o None si no se encontró.
    """
    # ✅ CORRECCIÓN 1: Eliminar la importación incorrecta de aquí
    # Ya está importado al inicio del archivo
    
    citas = gestor_datos_citas.cargar_datos(filepath)
    cita_encontrada = None
    indice = -1

    for i, c in enumerate(citas):
        # ✅ CORRECCIÓN 2: Cambiar 'id_cita' por 'id'
        if c.get('id') == id_cita:
            cita_encontrada = c
            indice = i
            break

    if cita_encontrada is None:
        return None
    
    cita_encontrada.update(datos_nuevos)
    citas[indice] = cita_encontrada

    gestor_datos_citas.guardar_datos(filepath, citas)
    return cita_encontrada

console = Console()
def eliminar_cita_por_documento(filepath: str, documento: str) -> bool:
    """
    Permite eliminar una cita específica de un paciente mostrando sus citas en una tabla.
    
    Args:
        filepath (str): Ruta del archivo de citas
        documento (str): Documento del paciente
        
    Returns:
        bool: True si se eliminó una cita, False si no se eliminó nada
    """

    citas = gestor_datos_citas.cargar_datos(filepath)

    citas_paciente = [c for c in citas if c.get("documento_paciente") == documento]

    if not citas_paciente:
        console.print(Panel("[bold yellow]⚠️ No se encontraron citas asociadas a este documento.[/bold yellow]", border_style="yellow"))
        return False

    table = Table(title="📅 Citas del paciente", show_lines=True, border_style="cyan")
    table.add_column("N°", justify="center", style="bold cyan")
    table.add_column("Fecha", justify="center")
    table.add_column("Hora", justify="center")
    table.add_column("Motivo", justify="left")
    table.add_column("Estado", justify="center")

    for i, cita in enumerate(citas_paciente, start=1):
        table.add_row(
            str(i),
            cita.get("fecha", "N/A"),
            cita.get("hora", "N/A"),
            cita.get("motivo", "N/A"),
            cita.get("estado", "Pendiente"),
        )

    console.print(table)

    try:
        opcion = int(Prompt.ask("\nIngrese el número de la cita que desea eliminar"))
        if opcion < 1 or opcion > len(citas_paciente):
            console.print("[bold red]❌ Opción no válida.[/bold red]")
            return False
    except ValueError:
        console.print("[bold red]❌ Debe ingresar un número válido.[/bold red]")
        return False

    cita_a_eliminar = citas_paciente[opcion - 1]

    console.print(Panel.fit(
        f"¿Eliminar la cita del [bold cyan]{cita_a_eliminar.get('fecha', 'N/A')}[/bold cyan] a las [bold cyan]{cita_a_eliminar.get('hora', 'N/A')}[/bold cyan]?",
        border_style="red"
    ))

    confirmacion = Prompt.ask("Escriba [bold red]S[/bold red] para confirmar o [bold yellow]N[/bold yellow] para cancelar").strip().lower()
    if confirmacion != "s":
        console.print("[yellow]Operación cancelada por el usuario.[/yellow]")
        return False

    citas.remove(cita_a_eliminar)
    gestor_datos_citas.guardar_datos(filepath, citas)

    console.print(Panel("[bold green]✅ Cita eliminada correctamente.[/bold green]", border_style="green"))
    return True


