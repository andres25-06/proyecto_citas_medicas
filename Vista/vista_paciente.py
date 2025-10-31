# -- coding: utf-8 --
"""
Vista del Módulo de Pacientes con selector interactivo (flechas ↑ ↓).
"""

import os
import time

import readchar
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, IntPrompt, Prompt
from rich.table import Table

from Modelo import paciente
from Validaciones import entrada_datos, validar_campos
from Vista import navegacion

console = Console()

DIRECTORIO_DATOS = 'data'
NOMBRE_ARCHIVO_CSV = 'pacientes.csv'
NOMBRE_ARCHIVO_JSON = 'pacientes.json'


def solicitar_tipo_documento(permitir_vacio: bool = False) -> str | None:
    limpiar()
    """
        Solicitar al usuario que seleccione un tipo de documento usando el selector interactivo.
        
        Args:
            permitir_vacio (bool): Si es True, permite no cambiar el tipo de documento.
        Returns:
            str | None: El tipo de documento seleccionado o None si no se cambia.
            
    """
    tipos = {
        '1': 'C.C',
        '2': 'T.I',
        '3': 'R.C',
        '4': 'C.E',
        '5': 'Pasaporte',
        '6': 'PPT'
    }

    descripciones = {
        '1': '🆔 Cédula de Ciudadanía',
        '2': '🎫 Tarjeta de Identidad',
        '3': '📜 Registro Civil',
        '4': '🌎 Cédula de Extranjería',
        '5': '🧳 Pasaporte',
        '6': '📄 Permiso de Permanencia Temporal'
    }

    opciones = [desc for desc in descripciones.values()]

    if permitir_vacio:
        opciones.insert(0, "🔸 No cambiar")

    opciones.append("🔙 Volver al menú anterior")

    seleccion = selector_interactivo("📑 Seleccione el tipo de documento", opciones)

    if permitir_vacio and seleccion == 0:
        console.print("[bold yellow]⚠ No se modificará el tipo de documento.[/bold yellow]")
        time.sleep(1)
        return None

    # Si selecciona "Volver"
    if seleccion == len(opciones) - 1:
        console.print("[bold red]↩ Regresando al menú anterior...[/bold red]")
        time.sleep(1)
        return elegir_almacenamiento()

    indice_real = seleccion if not permitir_vacio else seleccion - 1
    codigo = str(indice_real + 1)
    tipo = tipos[codigo]

    console.print(f"[bold green]✅ Tipo seleccionado:[/bold green] {descripciones[codigo]}")
    time.sleep(1)
    return tipo



def elegir_almacenamiento() -> str:
    """
        Esta función permite al usuario seleccionar el tipo de almacenamiento
        para los datos de pacientes (CSV o JSON) mediante un selector interactivo.
        
        Args:
            None
        Returns:
            str: Ruta del archivo seleccionado para almacenamiento.
        
    """
    limpiar()
    """Seleccionar tipo de almacenamiento (CSV o JSON) usando el selector interactivo."""
    opciones = [
        "📄 CSV (Archivo de texto plano)",
        "🧾 JSON (Formato estructurado)",
        "🔙 Volver al menú principal"
    ]

    seleccion = selector_interactivo("⚙️ Configuración de Almacenamiento", opciones)

    if seleccion == 0:
        console.print("[bold green]✅ Modo de almacenamiento seleccionado: CSV[/bold green]")
        time.sleep(1)
        return os.path.join(DIRECTORIO_DATOS, NOMBRE_ARCHIVO_CSV)

    elif seleccion == 1:
        console.print("[bold green]✅ Modo de almacenamiento seleccionado: JSON[/bold green]")
        time.sleep(1)
        return os.path.join(DIRECTORIO_DATOS, NOMBRE_ARCHIVO_JSON)

    elif seleccion == 2:
        console.print("[bold red]↩ Regresando al menú principal...[/bold red]")
        time.sleep(1)
        navegacion.ir_a_menu_principal()
        return None


def limpiar():
    """
        Limpia la consola dependiendo del sistema operativo.
        
        Args:
            None
        Returns:
            None
            
    """
    os.system("cls" if os.name == "nt" else "clear")


# =========================================================
# 🔹 Selector Interactivo
# =========================================================
def selector_interactivo(titulo, opciones):
    """
        Muestra un menú interactivo en la consola donde el usuario puede
        navegar usando las flechas ↑ ↓ y seleccionar una opción con Enter.
        
        Args:
            titulo (str): Título del menú.
            opciones (list): Lista de opciones para mostrar.
        Returns:
            int: Índice de la opción seleccionada.
    """
    limpiar()
    """Permite navegar con flechas ↑ ↓ y seleccionar con Enter."""
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
        Entradas para registrar un nuevo paciente y guardar en el archivo.
        
        Args:
            filepath (str): Ruta del archivo donde se guardarán los datos.
        Returns:
            None
    """
    limpiar()
    console.print(Panel.fit("[bold cyan]📝 Registrar Nuevo Paciente[/bold cyan]"))

    # --- Captura de datos con validaciones individuales ---
    tipo_documento = solicitar_tipo_documento()
    documento = validar_campos.validar_cedula("Número de Documento", filepath)
    nombres = validar_campos.validar_texto("Nombres").capitalize()
    apellidos = validar_campos.validar_texto("Apellidos").capitalize()
    direccion = validar_campos.validar_texto("Dirección")
    telefono = validar_campos.validar_telefono("Teléfono")

    # --- Crear diccionario temporal para validaciones posteriores ---
    nuevo_paciente = {
        "tipo_documento": tipo_documento,
        "documento": documento,
        "nombres": nombres,
        "apellidos": apellidos,
        "direccion": direccion,
        "telefono": telefono
    }

    # --- Validar campos obligatorios ---
    campos_obligatorios = ["tipo_documento", "documento", "nombres", "apellidos", "telefono"]
    if not entrada_datos.validar_datos_relacion_obligatorios(nuevo_paciente, campos_obligatorios, "paciente"):
        console.print(Panel("⚠ Faltan datos obligatorios.", border_style="red", title="Error"))
        input("\nPresione Enter para continuar...")
        return

    # --- Crear el paciente ---
    paciente_creado = paciente.crear_paciente(
        filepath, tipo_documento, documento, nombres, apellidos, direccion, telefono
    )

    # --- Confirmación ---
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
        Muestra una tabla con todos los pacientes registrados.
        Args:
            filepath (str): Ruta del archivo desde donde se leerán los datos.
        Returns:
            None
    
    """
    limpiar()
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
        Permite actualizar los datos de un paciente existente.
        
        Args:
            filepath (str): Ruta del archivo donde se encuentran los datos.
        Returns:
            None
            
    """
    limpiar()
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
        Permite eliminar un paciente existente.
        
        Args:
            filepath (str): Ruta del archivo donde se encuentran los datos.
        Returns:
            None
            
    """
    limpiar()
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
        Este es el menú principal del módulo de pacientes,
        el cual utiliza un selector interactivo para navegar
        entre las diferentes opciones disponibles.
        
        Args:
            None
        Returns:
            None    
            
    """
    limpiar()
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
