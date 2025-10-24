# -- coding: utf-8 --
"""
Vista del Módulo de Médicos con selector interactivo (flechas ↑ ↓)
y diseño mejorado con emojis para el CRUD.
"""

import os
import readchar
from Controlador import gestor_datos_pacientes
from Modelo import medico
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, IntPrompt, Prompt
from rich.table import Table

console = Console()

DIRECTORIO_DATOS = 'data'
NOMBRE_ARCHIVO_CSV = 'medicos.csv'
NOMBRE_ARCHIVO_JSON = 'medicos.json'


# =========================================================
# 🔹 Funciones Auxiliares
# =========================================================
def limpiar():
    """
    Limpia la consola según el sistema operativo.
    
    Args:
        none
    Returns:
        none
    """
    os.system("cls" if os.name == "nt" else "clear")


def elegir_almacenamiento() -> str:
    """
    Seleccionar tipo de almacenamiento (CSV o JSON).
    
    Args:
        none
    Returns:
        str: Ruta al archivo seleccionado.
    """
    console.print(Panel.fit("[bold cyan]⚙️ Configuración de Almacenamiento[/bold cyan]"))
    console.print(
        "¿Dónde desea almacenar los datos?\n"
        "[bold yellow]1[/bold yellow]. CSV (Archivo de texto plano)\n"
        "[bold yellow]2[/bold yellow]. JSON (Formato estructurado)"
    )
    opcion = Prompt.ask("Opción", choices=["1", "2"], default="2", show_choices=False)
    if opcion == '1':
        return os.path.join(DIRECTORIO_DATOS, NOMBRE_ARCHIVO_CSV)
    return os.path.join(DIRECTORIO_DATOS, NOMBRE_ARCHIVO_JSON)


# =========================================================
# 🔹 Selector Interactivo
# =========================================================
def selector_interactivo(titulo, opciones):
    """
    Permite navegar con flechas ↑ ↓ y seleccionar con Enter.
    
    Args:
        titulo (str): Título del menú.
        opciones (List[str]): Lista de opciones para mostrar.
    Returns:
        int: Índice de la opción seleccionada.
    """
    
    seleccion = 0
    while True:
        limpiar()
        console.print(Panel(f"[bold cyan]{titulo}[/bold cyan]"))
        for i, opt in enumerate(opciones):
            prefix = "👉 " if i == seleccion else "   "
            # Verde para opciones normales, rojo si es “volver”
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
# 🔹 Funciones del Módulo de Médicos
# =========================================================
def menu_crear_medico(filepath: str):
    """
    Menú para registrar un nuevo médico.
    
    Args:
        filepath (str): La ruta al archivo donde se almacenan los médicos.
    Returns:
        none
    """
    console.print(Panel.fit("[bold cyan]➕🩺 Registrar Nuevo Médico[/bold cyan]"))

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
            f"✅ ¡Médico registrado con éxito!\nID Asignado: [bold yellow]{medico_creado['id']}[/bold yellow]",
            border_style="green", title="Éxito"
        ))
    else:
        console.print(Panel("⚠️ No se pudo registrar al médico.", border_style="red", title="Error"))
    input("\nPresione Enter para continuar...")


def menu_leer_medicos(filepath: str):
    """
    Menú para ver todos los médicos registrados.
    
    Args:
        filepath (str): La ruta al archivo donde se almacenan los médicos.
    Returns:
        none        
    """
    console.print(Panel.fit("[bold cyan]📄👨‍⚕️ Lista de Médicos[/bold cyan]"))
    medicos = medico.leer_todos_los_medicos(filepath)

    if not medicos:
        console.print("[yellow]No hay médicos registrados.[/yellow]")
        input("\nPresione Enter para continuar...")
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
    input("\nPresione Enter para continuar...")


def menu_actualizar_medico(filepath: str):
    """
    Está función permite actualizar los datos de un médico existente.   
    
    Args:
        filepath (str): La ruta al archivo donde se almacenan los médicos.
    Returns:        
        none
    
    """
    console.print(Panel.fit("[bold cyan]✏️🩺 Actualizar Datos de Médico[/bold cyan]"))
    id_medico = IntPrompt.ask("Ingrese el documento del médico a actualizar")

    medico_actual = medico.buscar_medico_por_documento(filepath, str(id_medico))
    if not medico_actual:
        console.print("\n[bold red]❌ No se encontró ningún médico con ese documento.[/bold red]")
        input("\nPresione Enter para continuar...")
        return

    console.print("\nPresione Enter para no modificar un campo.")
    datos_nuevos = {}

    nombres = Prompt.ask(f"Nombres ({medico_actual['nombres']})", default=medico_actual['nombres'])
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
        input("\nPresione Enter para continuar...")
        return

    medico_actualizado = medico.actualizar_medico(filepath, str(id_medico), datos_nuevos)
    if medico_actualizado:
        console.print(Panel("✅ ¡Datos del médico actualizados con éxito!", border_style="green", title="Éxito"))
    else:
        console.print(Panel("❌ Error al actualizar los datos.", border_style="red", title="Error"))
    input("\nPresione Enter para continuar...")


def menu_eliminar_medico(filepath: str):
    """
    Está función permite eliminar un médico existente.
    
    Args:
        filepath (str): La ruta al archivo donde se almacenan los médicos.
    Returns:        
        none
    """
    console.print(Panel.fit("[bold cyan]🗑️❌ Eliminar Médico[/bold cyan]"))
    documento = IntPrompt.ask("Ingrese el documento del médico a eliminar")

    medico_encontrado = medico.buscar_medico_por_documento(filepath, str(documento))
    if not medico_encontrado:
        console.print("\n[bold red]❌ No se encontró el médico.[/bold red]")
        input("\nPresione Enter para continuar...")
        return

    confirmacion = Confirm.ask(
        f"¿Está seguro de eliminar al Dr. [bold]{medico_encontrado['nombres']} {medico_encontrado['apellidos']}[/bold]?",
        default=False
    )

    if confirmacion:
        if medico.eliminar_medico(filepath, str(documento)):
            console.print(Panel("✅ ¡Médico eliminado con éxito!", border_style="green", title="Éxito"))
        else:
            console.print(Panel("❌ Error al eliminar.", border_style="red", title="Error"))
    else:
        console.print("\n[yellow]Operación cancelada.[/yellow]")
    input("\nPresione Enter para continuar...")


# =========================================================
# 🔹 Menú Principal Interactivo
# =========================================================
def main_vista_medicos():
    
    """
    Función principal para manejar el menú de médicos.
    
    Args:
        none
    Returns:
        none
    """
    archivo = elegir_almacenamiento()
    console.print(f"\n[bold green]Usando archivo:[/bold green] {archivo}")

    opciones = [
        "➕🩺 Registrar un nuevo médico",
        "📄👨‍⚕️ Ver todos los médicos",
        "✏️🩹 Actualizar datos de un médico",
        "❌🗑️ Eliminar un médico",
        "⬅️🔙 Volver al menú principal"
    ]

    while True:
        seleccion = selector_interactivo("MÓDULO DE MÉDICOS\nUsa ↑ ↓ y Enter para seleccionar", opciones)

        if seleccion == 0:
            menu_crear_medico(archivo)
        elif seleccion == 1:
            menu_leer_medicos(archivo)
        elif seleccion == 2:
            menu_actualizar_medico(archivo)
        elif seleccion == 3:
            menu_eliminar_medico(archivo)
        elif seleccion == 4:
            console.print("\n[bold red]⬅ Volviendo al menú principal...[/bold red]")
            break


# =========================================================
# 🔹 Ejecución directa (para pruebas)
# =========================================================
if __name__ == "__main__":
    main_vista_medicos()
