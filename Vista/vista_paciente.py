# -- coding: utf-8 --
"""
Vista del Módulo de Pacientes.

Maneja la interacción con el usuario (menús, entradas, salidas)
usando la librería Rich. Toda la lógica de presentación y flujo
del módulo de pacientes está aquí.
"""

import os
from Modelo import paciente  # Importamos la lógica del modelo

# --- Importaciones de la librería Rich ---
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, IntPrompt, Prompt
from rich.table import Table

# --- Inicialización de la Consola de Rich ---
console = Console()

# --- Constantes de Configuración de Rutas ---
DIRECTORIO_DATOS = 'data'
NOMBRE_ARCHIVO_CSV = 'pacientes.csv'
NOMBRE_ARCHIVO_JSON = 'pacientes.json'


# =========================================================
# 🔹 Funciones Auxiliares
# =========================================================
def solicitar_tipo_documento(permitir_vacio: bool = False) -> str | None:
    """Muestra un menú para que el usuario elija el tipo de documento."""
    console.print("\nSeleccione el tipo de documento:", style="cyan")
    tipos = {
        '1': 'C.C', '2': 'T.I', '3': 'R.C', '4': 'C.E', '5': 'Pasaporte', '6': 'PPT'
    }
    descripciones = {
        '1': 'Cédula de Ciudadanía', '2': 'Tarjeta de Identidad', '3': 'Registro Civil',
        '4': 'Cédula de Extranjería', '5': 'Pasaporte', '6': 'Permiso de Permanencia Temporal'
    }

    opciones = list(tipos.keys())
    prompt_texto = ""

    if permitir_vacio:
        prompt_texto += "[bold yellow]0[/bold yellow]. No cambiar\n"
        opciones.insert(0, '0')

    for key, value in descripciones.items():
        prompt_texto += f"[bold yellow]{key}[/bold yellow]. {value}\n"

    console.print(prompt_texto)
    opcion = Prompt.ask("Opción", choices=opciones, show_choices=False)

    if permitir_vacio and opcion == '0':
        return None
    return tipos[opcion]


def elegir_almacenamiento() -> str:
    """Pregunta al usuario qué formato de archivo desea usar y construye la ruta."""
    console.print(Panel.fit("[bold cyan]⚙ Configuración de Almacenamiento[/bold cyan]"))
    prompt_texto = (
        "¿Dónde desea almacenar los datos?\n"
        "[bold yellow]1[/bold yellow]. CSV (Archivo de texto plano)\n"
        "[bold yellow]2[/bold yellow]. JSON (Formato estructurado)"
    )
    console.print(prompt_texto)

    opcion = Prompt.ask("Opción", choices=["1", "2"], default="2", show_choices=False)
    if opcion == '1':
        return os.path.join(DIRECTORIO_DATOS, NOMBRE_ARCHIVO_CSV)
    else:
        return os.path.join(DIRECTORIO_DATOS, NOMBRE_ARCHIVO_JSON)


# =========================================================
# 🔹 Funciones del Menú de Pacientes
# =========================================================
def menu_crear_paciente(filepath: str):
    """Registrar un nuevo paciente."""
    console.print(Panel.fit("[bold cyan]📝 Registrar Nuevo Paciente[/bold cyan]"))

    tipo_documento = solicitar_tipo_documento()
    documento = IntPrompt.ask("Número de Documento")
    nombres = Prompt.ask("Nombres")
    apellidos = Prompt.ask("Apellidos")
    direccion = Prompt.ask("Dirección")
    telefono = IntPrompt.ask("Teléfono")

    paciente_creado = paciente.crear_paciente(
        filepath, tipo_documento, documento, nombres, apellidos, direccion, telefono
    )

    if paciente_creado:
        console.print(Panel(
            f"✅ ¡Paciente registrado con éxito!\n   ID Asignado: [bold yellow]{paciente_creado['id']}[/bold yellow]",
            border_style="green", title="Éxito"
        ))
    else:
        console.print(Panel(
            "⚠ No se pudo registrar al paciente. Verifique los datos.",
            border_style="red", title="Error"
        ))


def menu_leer_pacientes(filepath: str):
    """Mostrar todos los pacientes en una tabla."""
    console.print(Panel.fit("[bold cyan]👥 Lista de Pacientes[/bold cyan]"))
    pacientes = paciente.leer_todos_los_pacientes(filepath)

    if not pacientes:
        console.print("[yellow]No hay pacientes registrados.[/yellow]")
        return

    tabla = Table(title="Pacientes Registrados", border_style="blue", show_header=True, header_style="bold magenta")
    tabla.add_column("ID", style="dim", width=5)
    tabla.add_column("Tipo Doc.", justify="center")
    tabla.add_column("Documento", justify="center")
    tabla.add_column("Nombre Completo")
    tabla.add_column("Teléfono", justify="center")
    tabla.add_column("Direccion", justify="center")

    for p in pacientes:
        tabla.add_row(
            p['id'],
            p['tipo_documento'],
            p['documento'],
            f"{p['nombres']} {p['apellidos']}",
            p['telefono'],
            p['direccion']
        )

    console.print(tabla)


def menu_actualizar_paciente(filepath: str):
    """Actualizar los datos de un paciente."""
    console.print(Panel.fit("[bold cyan]✏ Actualizar Datos de Paciente[/bold cyan]"))
    documento = IntPrompt.ask("Ingrese el Documento del paciente a actualizar")

    paciente_actual = paciente.buscar_paciente_por_documento(filepath, str(documento))
    if not paciente_actual:
        console.print("\n[bold red]❌ No se encontró ningún paciente con ese documento.[/bold red]")
        return

    console.print("\nDatos actuales. Presione Enter para no modificar un campo.")
    datos_nuevos = {}

    nuevo_tipo_doc = solicitar_tipo_documento(permitir_vacio=True)
    if nuevo_tipo_doc:
        datos_nuevos['tipo_documento'] = nuevo_tipo_doc

    nombres = Prompt.ask(f"Nombres ({paciente_actual['nombres']})", default=paciente_actual['nombres'])
    if nombres != paciente_actual['nombres']:
        datos_nuevos['nombres'] = nombres

    apellidos = Prompt.ask(f"Apellidos ({paciente_actual['apellidos']})", default=paciente_actual['apellidos'])
    if apellidos != paciente_actual['apellidos']:
        datos_nuevos['apellidos'] = apellidos

    direccion = Prompt.ask(f"Dirección ({paciente_actual['direccion']})", default=paciente_actual['direccion'])
    if direccion != paciente_actual['direccion']:
        datos_nuevos['direccion'] = direccion

    telefono = IntPrompt.ask(f"Teléfono ({paciente_actual['telefono']})", default=int(paciente_actual['telefono']))
    if telefono != int(paciente_actual['telefono']):
        datos_nuevos['telefono'] = telefono

    if not datos_nuevos:
        console.print("\n[yellow]No se modificó ningún dato.[/yellow]")
        return

    paciente_actualizado = paciente.actualizar_paciente(filepath, str(documento), datos_nuevos)
    if paciente_actualizado:
        console.print(Panel("✅ ¡Datos del paciente actualizados con éxito!", border_style="green", title="Éxito"))
    else:
        console.print(Panel("❌ Ocurrió un error al actualizar.", border_style="red", title="Error"))


def menu_eliminar_paciente(filepath: str):
    """Eliminar un paciente existente."""
    console.print(Panel.fit("[bold cyan]🗑 Eliminar Paciente[/bold cyan]"))
    documento = IntPrompt.ask("Ingrese el Documento del paciente a eliminar")

    paciente_encontrado = paciente.buscar_paciente_por_documento(filepath, str(documento))
    if not paciente_encontrado:
        console.print("\n[bold red]❌ No se encontró ningún paciente con ese documento.[/bold red]")
        return

    confirmacion = Confirm.ask(
        f"¿Está seguro de eliminar a [bold]{paciente_encontrado['nombres']} {paciente_encontrado['apellidos']}[/bold]?",
        default=False
    )

    if confirmacion:
        if paciente.eliminar_paciente(filepath, str(documento)):
            console.print(Panel("✅ ¡Paciente eliminado con éxito!", border_style="green", title="Éxito"))
        else:
            console.print(Panel("❌ Ocurrió un error al eliminar.", border_style="red", title="Error"))
    else:
        console.print("\n[yellow]Operación cancelada.[/yellow]")


def mostrar_menu_pacientes():
    """Imprime el menú principal del módulo de pacientes."""
    menu_texto = (
        "[bold yellow]1[/bold yellow]. Registrar un nuevo paciente\n"
        "[bold yellow]2[/bold yellow]. Ver todos los pacientes\n"
        "[bold yellow]3[/bold yellow]. Actualizar datos de un paciente\n"
        "[bold yellow]4[/bold yellow]. Eliminar un paciente\n"
        "[bold red]5[/bold red]. Volver al menú principal"
    )
    console.print(Panel(menu_texto, title="[bold]MÓDULO DE PACIENTES[/bold]", border_style="green"))


# =========================================================
# 🔹 Función principal del módulo (llamada desde main.py)
# =========================================================
def main_vista_pacientes():
    """Bucle principal del módulo de pacientes."""
    archivo_seleccionado = elegir_almacenamiento()
    console.print(f"\n👍 Usando el archivo: [bold green]{archivo_seleccionado}[/bold green]")

    while True:
        mostrar_menu_pacientes()
        opcion = Prompt.ask("Opción", choices=["1", "2", "3", "4", "5"], show_choices=False)

        if opcion == '1':
            menu_crear_paciente(archivo_seleccionado)
        elif opcion == '2':
            menu_leer_pacientes(archivo_seleccionado)
        elif opcion == '3':
            menu_actualizar_paciente(archivo_seleccionado)
        elif opcion == '4':
            menu_eliminar_paciente(archivo_seleccionado)
        elif opcion == '5':
            console.print("\n[bold cyan]⬅ Volviendo al menú principal...[/bold cyan]")
            break