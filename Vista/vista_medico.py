"""
Vista del Módulo de Médicos.

Maneja la interacción con el usuario (menús, entradas, salidas)
usando la librería Rich. Toda la lógica de presentación y flujo
del módulo de médicos está aquí.
"""

import os

from Controlador import gestor_datos_pacientes
from Modelo import medico  # Importamos la lógica del modelo

# --- Importaciones de la librería Rich ---
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, IntPrompt, Prompt
from rich.table import Table

# --- Inicialización de la Consola de Rich ---
console = Console()

# --- Constantes de Configuración de Rutas ---
DIRECTORIO_DATOS = 'data'
NOMBRE_ARCHIVO_CSV = 'medicos.csv'
NOMBRE_ARCHIVO_JSON = 'medicos.json'


# =========================================================
# 🔹 Funciones Auxiliares
# =========================================================
def elegir_almacenamiento() -> str:
    """Pregunta al usuario qué formato de archivo desea usar y construye la ruta."""
    console.print(Panel.fit("[bold cyan]⚙️ Configuración de Almacenamiento[/bold cyan]"))
    prompt_texto = (
        "¿Dónde desea almacenar los datos?\n"
        "[bold yellow]1[/bold yellow]. CSV (Archivo de texto plano)\n"
        "[bold yellow]2[/bold yellow]. JSON (Formato estructurado)"
    )
    console.print(prompt_texto)

    opcion = Prompt.ask("Opción", choices=["1", "2"], default="1", show_choices=False)
    if opcion == '1':
        return os.path.join(DIRECTORIO_DATOS, NOMBRE_ARCHIVO_CSV)
    else:
        return os.path.join(DIRECTORIO_DATOS, NOMBRE_ARCHIVO_JSON)


# =========================================================
# 🔹 Funciones del Menú de Médicos
# =========================================================
def menu_crear_medico(filepath: str):
    """Registrar un nuevo médico."""
    console.print(Panel.fit("[bold cyan]🩺 Registrar Nuevo Médico[/bold cyan]"))

    tipo_documento = Prompt.ask("Tipo de Documento (CC, TI, CE, etc.)")
    documento = IntPrompt.ask("Número de Documento")
    nombres = Prompt.ask("Nombres")
    apellidos = Prompt.ask("Apellidos")
    especialidad = Prompt.ask("Especialidad")
    telefono = IntPrompt.ask("Teléfono")
    estado = Prompt.ask("Estado (Activo/Inactivo)", choices=["Activo", "Inactivo"], default="Activo")
    consultorio = Prompt.ask("Número de Consultorio")
    hospital = Prompt.ask("Hospital")

    medico_creado = medico.crear_medico(
        filepath,
        tipo_documento,
        documento,
        nombres,
        apellidos,
        especialidad,
        telefono,
        estado,
        consultorio,
        hospital
    )

    if medico_creado:
        console.print(Panel(
            f"✅ ¡Médico registrado con éxito!\n   ID Asignado: [bold yellow]{medico_creado['id']}[/bold yellow]",
            border_style="green", title="Éxito"
        ))
    else:
        console.print(Panel(
            "⚠️ No se pudo registrar al médico. Verifique los datos.",
            border_style="red", title="Error"
        ))

def menu_leer_medicos(filepath: str):
    """Mostrar todos los médicos en una tabla."""
    console.print(Panel.fit("[bold cyan]👨‍⚕️ Lista de Médicos[/bold cyan]"))
    medicos = medico.leer_todos_los_medicos(filepath)

    if not medicos:
        console.print("[yellow]No hay médicos registrados.[/yellow]")
        return

    tabla = Table(
        title="Médicos Registrados",
        border_style="blue",
        show_header=True,
        header_style="bold magenta"
    )
    tabla.add_column("ID", style="dim", width=5)
    tabla.add_column("Nombre Completo")
    tabla.add_column("Especialidad")
    tabla.add_column("Teléfono", justify="right")
    tabla.add_column("Estado", justify="center")
    tabla.add_column("Consultorio", justify="center")
    tabla.add_column("Hospital", justify="center")

    for m in medicos:
        tabla.add_row(
            m.get('id', 'N/A'),
            f"{m.get('nombres', '')} {m.get('apellidos', '')}",
            m.get('especialidad', 'N/A'),
            m.get('telefono', 'N/A'),
            m.get('estado', 'N/A'),
            m.get('consultorio', 'N/A'),
            m.get('hospital', 'N/A')
        )

    console.print(tabla)

def buscar_medico_por_documento(filepath, documento):
    medicos = gestor_datos_pacientes.cargar_datos(filepath)
    for m in medicos:
        if m.get('documento') == str(documento):
            return m
    return None

def menu_actualizar_medico(filepath: str):
    """Actualizar los datos de un médico."""
    console.print(Panel.fit("[bold cyan]✏️ Actualizar Datos de Médico[/bold cyan]"))
    id_medico = IntPrompt.ask("Ingrese el documento del médico a actualizar")

    medico_actual = medico.buscar_medico_por_documento(filepath, str(id_medico))
    if not medico_actual:
        console.print("\n[bold red]❌ No se encontró ningún médico con ese ID.[/bold red]")
        return

    console.print("\nDatos actuales. Presione Enter para no modificar un campo.")
    datos_nuevos = {}

    nombres = Prompt.ask(f"Nombre ({medico_actual['nombres']})", default=medico_actual['nombres'])
    if nombres != medico_actual['nombres']:
        datos_nuevos['nombres'] = nombres

    especialidad = Prompt.ask(f"Especialidad ({medico_actual['especialidad']})", default=medico_actual['especialidad'])
    if especialidad != medico_actual['especialidad']:
        datos_nuevos['especialidad'] = especialidad

    telefono = IntPrompt.ask(f"Teléfono ({medico_actual['telefono']})", default=int(medico_actual['telefono']))
    if telefono != int(medico_actual['telefono']):
        datos_nuevos['telefono'] = telefono

    if not datos_nuevos:
        console.print("\n[yellow]No se modificó ningún dato.[/yellow]")
        return

    medico_actualizado = medico.actualizar_medico(filepath, str(id_medico), datos_nuevos)
    if medico_actualizado:
        console.print(Panel("✅ ¡Datos del médico actualizados con éxito!", border_style="green", title="Éxito"))
    else:
        console.print(Panel("❌ Ocurrió un error al actualizar.", border_style="red", title="Error"))


def menu_eliminar_medico(filepath: str):
    """Eliminar un médico existente."""
    console.print(Panel.fit("[bold cyan]🗑️ Eliminar Médico[/bold cyan]"))
    documento = IntPrompt.ask("Ingrese el documento del médico a eliminar")

    medico_encontrado = medico.buscar_medico_por_documento(filepath, str(documento))
    if not medico_encontrado:
        console.print("\n[bold red]❌ No se encontró ningún médico con ese ID.[/bold red]")
        return

    confirmacion = Confirm.ask(
        f"¿Está seguro de eliminar al Dr. [bold]{medico_encontrado['nombres']}[/bold]?",
        default=False
    )

    if confirmacion:
        if medico.eliminar_medico(filepath, str(documento)):
            console.print(Panel("✅ ¡Médico eliminado con éxito!", border_style="green", title="Éxito"))
        else:
            console.print(Panel("❌ Ocurrió un error al eliminar.", border_style="red", title="Error"))
    else:
        console.print("\n[yellow]Operación cancelada.[/yellow]")


def mostrar_menu_medicos():
    """Imprime el menú principal del módulo de médicos."""
    menu_texto = (
        "[bold yellow]1[/bold yellow]. Registrar un nuevo médico\n"
        "[bold yellow]2[/bold yellow]. Ver todos los médicos\n"
        "[bold yellow]3[/bold yellow]. Actualizar datos de un médico\n"
        "[bold yellow]4[/bold yellow]. Eliminar un médico\n"
        "[bold red]5[/bold red]. Volver al menú principal"
    )
    console.print(Panel(menu_texto, title="[bold]MÓDULO DE MÉDICOS[/bold]", border_style="green"))


# =========================================================
# 🔹 Función principal del módulo (llamada desde main.py)
# =========================================================
def main_vista_medicos():
    """Bucle principal del módulo de médicos."""
    archivo_seleccionado = elegir_almacenamiento()
    console.print(f"\n👍 Usando el archivo: [bold green]{archivo_seleccionado}[/bold green]")

    while True:
        mostrar_menu_medicos()
        opcion = Prompt.ask("Opción", choices=["1", "2", "3", "4", "5"], show_choices=False)

        if opcion == '1':
            menu_crear_medico(archivo_seleccionado)
        elif opcion == '2':
            menu_leer_medicos(archivo_seleccionado)
        elif opcion == '3':
            menu_actualizar_medico(archivo_seleccionado)
        elif opcion == '4':
            menu_eliminar_medico(archivo_seleccionado)
        elif opcion == '5':
            console.print("\n[bold cyan]⬅️ Volviendo al menú principal...[/bold cyan]")
            break
