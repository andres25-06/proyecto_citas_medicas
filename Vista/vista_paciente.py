# -- coding: utf-8 --
"""
Vista del Módulo de Pacientes con selector interactivo (flechas ↑ ↓).
"""

import os
import readchar
from Modelo import paciente
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, IntPrompt, Confirm
from Vista.vista_principal import vista_principal 

console = Console()

DIRECTORIO_DATOS = 'data'
NOMBRE_ARCHIVO_CSV = 'pacientes.csv'
NOMBRE_ARCHIVO_JSON = 'pacientes.json'


def solicitar_tipo_documento(permitir_vacio: bool = False) -> str | None:
    """
    Solicita al usuario seleccionar un tipo de documento.
    Args:
        permitir_vacio (bool): Si es True, permite no seleccionar ningún tipo (retorna None).
    Returns:
        str | None: El tipo de documento seleccionado o None si se permite vacío y se elige esa opción.
    """
    console.print("\nSeleccione el tipo de documento:", style="cyan")
    tipos = {
        '1': 'C.C', '2': 'T.I', '3': 'R.C', '4': 'C.E', '5': 'Pasaporte', '6': 'PPT'
    }
    descripciones = {
        '1': 'Cédula de Ciudadanía', '2': 'Tarjeta de Identidad', '3': 'Registro Civil',
        '4': 'Cédula de Extranjería', '5': 'Pasaporte', '6': 'Permiso de Permanencia Temporal'
    }

    opciones = list(tipos.keys())
    texto = ""

    if permitir_vacio:
        texto += "[bold yellow]0[/bold yellow]. No cambiar\n"
        opciones.insert(0, '0')

    for k, v in descripciones.items():
        texto += f"[bold yellow]{k}[/bold yellow]. {v}\n"

    console.print(texto)
    opcion = Prompt.ask("Opción", choices=opciones, show_choices=False)
    if permitir_vacio and opcion == '0':
        return None
    return tipos[opcion]


def elegir_almacenamiento() -> str:
    """
    Elegir el tipo de almacenamiento (CSV o JSON) para los datos de pacientes.
    Args:
        none    
    Returns:
        str: Ruta al archivo seleccionado.
    """
    console.print(Panel.fit("[bold cyan]⚙ Configuración de Almacenamiento[/bold cyan]"))
    console.print(
        "¿Dónde desea almacenar los datos?\n"
        "[bold yellow]1[/bold yellow]. 📄 CSV (Archivo de texto plano)\n"
        "[bold yellow]2[/bold yellow]. 🧾 JSON (Formato estructurado)\n"
        "[bold yellow]3[/bold yellow]. 🔙 Volver al menú principal"
    )

    opcion = Prompt.ask(
        "Seleccione una opción",
        choices=["1", "2", "3"],
        show_choices=False
    )
    

    if opcion == "1":
        return os.path.join(DIRECTORIO_DATOS, NOMBRE_ARCHIVO_CSV)
    elif opcion == "2":
        return os.path.join(DIRECTORIO_DATOS, NOMBRE_ARCHIVO_JSON)
    elif opcion == "3":
        console.print("[bold red]↩ Regresando al menú principal...[/bold red]")
        vista_principal() 
        return None


def limpiar():
    os.system("cls" if os.name == "nt" else "clear")


# =========================================================
# 🔹 Selector Interactivo
# =========================================================
def selector_interactivo(titulo, opciones):
    """"
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
# 🔹 Funciones del Módulo de Pacientes
# =========================================================
def menu_crear_paciente(filepath: str):
    """
    Esta función permite registrar un nuevo paciente.
    
    Args:
        filepath (str): La ruta al archivo donde se almacenan los pacientes.
    Returns:
        none
    
    """
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
            f"✅ ¡Paciente registrado con éxito!\nID Asignado: [bold yellow]{paciente_creado['id']}[/bold yellow]",
            border_style="green", title="Éxito"
        ))
    else:
        console.print(Panel("⚠ No se pudo registrar el paciente.", border_style="red", title="Error"))
    input("\nPresione Enter para continuar...")


def menu_leer_pacientes(filepath: str):
    
    """
    Menú para ver todos los pacientes registrados.
    
    Args:
        filepath (str): La ruta al archivo donde se almacenan los pacientes.
    Returns:
        none
    """
    console.print(Panel.fit("[bold cyan]👥 Lista de Pacientes[/bold cyan]"))
    pacientes = paciente.leer_todos_los_pacientes(filepath)

    if not pacientes:
        console.print("[yellow]No hay pacientes registrados.[/yellow]")
        input("\nPresione Enter para continuar...")
        return

    tabla = Table(title="Pacientes Registrados", border_style="blue", show_header=True, header_style="bold magenta")
    tabla.add_column("ID", style="dim", width=5)
    tabla.add_column("Tipo Doc.", justify="center")
    tabla.add_column("Documento", justify="center")
    tabla.add_column("Nombre Completo")
    tabla.add_column("Teléfono", justify="center")
    tabla.add_column("Dirección", justify="center")

    for p in pacientes:
        tabla.add_row(
            p['id'], p['tipo_documento'], p['documento'],
            f"{p['nombres']} {p['apellidos']}",
            p['telefono'], p['direccion']
        )

    console.print(tabla)
    input("\nPresione Enter para continuar...")


def menu_actualizar_paciente(filepath: str):
    """
    Está función permite actualizar los datos de un paciente existente.
    
    Args:
        filepath (str): La ruta al archivo donde se almacenan los pacientes.
    Returns:        
        none
    """
    console.print(Panel.fit("[bold cyan]✏ Actualizar Datos de Paciente[/bold cyan]"))
    documento = IntPrompt.ask("Ingrese el Documento del paciente a actualizar")

    paciente_actual = paciente.buscar_paciente_por_documento(filepath, str(documento))
    if not paciente_actual:
        console.print("\n[bold red]❌ No se encontró el paciente.[/bold red]")
        input("\nPresione Enter para continuar...")
        return

    console.print("\nPresione Enter para no modificar un campo.")
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
        input("\nPresione Enter para continuar...")
        return

    paciente_actualizado = paciente.actualizar_paciente(filepath, str(documento), datos_nuevos)
    if paciente_actualizado:
        console.print(Panel("✅ ¡Datos actualizados con éxito!", border_style="green", title="Éxito"))
    else:
        console.print(Panel("❌ Error al actualizar.", border_style="red", title="Error"))
    input("\nPresione Enter para continuar...")


def menu_eliminar_paciente(filepath: str):
    """
    Está función permite eliminar un médico existente.
    
    Args:
        filepath (str): La ruta al archivo donde se almacenan los médicos.
    Returns:        
        none
    """
    console.print(Panel.fit("[bold cyan]🗑 Eliminar Paciente[/bold cyan]"))
    documento = IntPrompt.ask("Ingrese el Documento del paciente a eliminar")

    paciente_encontrado = paciente.buscar_paciente_por_documento(filepath, str(documento))
    if not paciente_encontrado:
        console.print("\n[bold red]❌ No se encontró el paciente.[/bold red]")
        input("\nPresione Enter para continuar...")
        return

    confirmacion = Confirm.ask(
        f"¿Desea eliminar a [bold]{paciente_encontrado['nombres']} {paciente_encontrado['apellidos']}[/bold]?",
        default=False
    )

    if confirmacion:
        if paciente.eliminar_paciente(filepath, str(documento)):
            console.print(Panel("✅ ¡Paciente eliminado con éxito!", border_style="green", title="Éxito"))
        else:
            console.print(Panel("❌ Error al eliminar.", border_style="red", title="Error"))
    else:
        console.print("\n[yellow]Operación cancelada.[/yellow]")
    input("\nPresione Enter para continuar...")


# =========================================================
# 🔹 Menú Principal Interactivo
# =========================================================
def main_vista_pacientes():
    """
    Función principal para manejar el menú de pacientes.
    
    Args:
        none
    Returns:
        none
    """
    archivo = elegir_almacenamiento()
    console.print(f"\n[bold green]Usando archivo:[/bold green] {archivo}")

    opciones = [
        "➕ Registrar un nuevo paciente",
        "📄 Ver todos los pacientes",
        "✏️ Actualizar datos de un paciente",
        "❌ Eliminar un paciente",
        "⬅️ Volver al menú principal"
    ]

    while True:
        seleccion = selector_interactivo("MÓDULO DE PACIENTES\nUsa ↑ ↓ y Enter para seleccionar", opciones)

        if seleccion == 0:
            menu_crear_paciente(archivo)
        elif seleccion == 1:
            menu_leer_pacientes(archivo)
        elif seleccion == 2:
            menu_actualizar_paciente(archivo)
        elif seleccion == 3:
            menu_eliminar_paciente(archivo)
        elif seleccion == 4:
            console.print("\n[bold red]⬅ Volviendo al menú principal...[/bold red]")
            break


# =========================================================
# 🔹 Ejecución directa (para pruebas)
# =========================================================
if __name__ == "__main__":
    main_vista_pacientes()
    main_vista_pacientes()
