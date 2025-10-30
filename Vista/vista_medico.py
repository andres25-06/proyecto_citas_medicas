# -- coding: utf-8 --
"""
Vista del Módulo de Médicos con selector interactivo (flechas ↑ ↓)
y diseño mejorado con emojis para el CRUD.
"""

import os
import time
import json
import csv

import readchar
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, IntPrompt, Prompt
from rich.table import Table

from Modelo import medico
from Validaciones import entrada_datos, validar_campos
from Vista import navegacion

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
    limpiar()
    """
        Seleccionar tipo de almacenamiento (CSV o JSON) usando el selector interactivo.
        
        Args:
            none
        Returns:    
            str: Ruta del archivo seleccionado para almacenamiento.
            
    """
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

def solicitar_tipo_documento(permitir_vacio: bool = False) -> str | None:
    limpiar()
    """
        Permite seleccionar el tipo de documento usando el selector interactivo, con opción de volver.
        
        Args:
            permitir_vacio (bool): Si es True, permite no cambiar el tipo de documento.
        Returns:    
            str | None: Tipo de documento seleccionado o None si no se cambia.
            
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


# =========================================================
# 🔹 Especialidades del Medico
# =========================================================

def solicitar_especialidad_medica(permitir_vacio: bool = False) -> str | None:
    """
        Permite seleccionar la especialidad médica de un médico usando un menú interactivo.

        Args:
            permitir_vacio (bool): Si es True, permite no cambiar la especialidad.
        Returns:
            str | None: Especialidad seleccionada o None si no se cambia.
    """
    limpiar()
    especialidades = {
        '1': 'Medicina General',
        '2': 'Pediatría',
        '3': 'Ginecología y Obstetricia',
        '4': 'Medicina Interna',
        '5': 'Cardiología',
        '6': 'Dermatología',
        '7': 'Oftalmología',
        '8': 'Otorrinolaringología',
        '9': 'Traumatología y Ortopedia',
        '10': 'Neurología',
        '11': 'Psiquiatría',
        '12': 'Urología',
        '13': 'Gastroenterología',
        '14': 'Endocrinología',
        '15' : 'Odontologia'
    }

    descripciones = {
        '1': '🩺 Medicina General',
        '2': '👶 Pediatría',
        '3': '👩‍🍼 Ginecología y Obstetricia',
        '4': '🏥 Medicina Interna',
        '5': '❤️ Cardiología',
        '6': '🌿 Dermatología',
        '7': '👁️ Oftalmología',
        '8': '👂 Otorrinolaringología',
        '9': '🦴 Traumatología y Ortopedia',
        '10': '🧠 Neurología',
        '11': '💬 Psiquiatría',
        '12': '🚹 Urología',
        '13': '🍽️ Gastroenterología',
        '14': '🔬 Endocrinología',
        '15': '🦷Odontologia'
    }

    opciones = [desc for desc in descripciones.values()]

    if permitir_vacio:
        opciones.insert(0, "🔸 No cambiar especialidad")


    seleccion = selector_interactivo("🏥 Seleccione la especialidad médica", opciones)

    # Si permite dejar vacío
    if permitir_vacio and seleccion == 0:
        console.print("[bold yellow]⚠ No se modificará la especialidad médica.[/bold yellow]")
        time.sleep(1)
        return None

    indice_real = seleccion if not permitir_vacio else seleccion - 1
    codigo = str(indice_real + 1)
    especialidad = especialidades[codigo]

    console.print(f"[bold green]✅ Especialidad seleccionada:[/bold green] {descripciones[codigo]}")
    time.sleep(1)
    return especialidad

# =========================================================
# 🔹 Especialidades del Medico
# =========================================================

def estado_medico(permitir_vacio: bool = False) -> str | None:
    """
        Permite seleccionar el estado del médico (Activo o Inactivo) usando un selector interactivo.

        Args:
            permitir_vacio (bool): Si es True, permite no cambiar el estado actual.
        Returns:    
            str | None: Estado seleccionado o None si no se cambia.
    """
    tipos = {
        '1': 'Activo',
        '2': 'Inactivo'
    }

    descripciones = {
        '1': '✅ Activo',
        '2': '❌ Inactivo'
    }

    opciones = [desc for desc in descripciones.values()]

    if permitir_vacio:
        opciones.insert(0, "🔸 No cambiar")

    seleccion = selector_interactivo("📋 Seleccione el estado del médico", opciones)

    # Si se permite dejar vacío y se elige "No cambiar"
    if permitir_vacio and seleccion == 0:
        console.print("[bold yellow]⚠ No se modificará el estado del médico.[/bold yellow]")
        time.sleep(1)
        return None

    # Calcular índice real según si se permitió vacío
    indice_real = seleccion if not permitir_vacio else seleccion - 1
    codigo = str(indice_real + 1)

    # Obtener el estado correspondiente
    estado = tipos[codigo]

    console.print(f"[bold green]✅ Estado seleccionado:[/bold green] {descripciones[codigo]}")
    time.sleep(1)
    return estado


def leer_datos_archivo(filepath):
    """
    Lee datos desde un archivo JSON o CSV.
    Retorna una lista de diccionarios o lista vacía si hay error.
    """
    if not os.path.exists(filepath):
        return []

    try:
        if filepath.endswith(".json"):
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        elif filepath.endswith(".csv"):
            with open(filepath, "r", encoding="utf-8") as f:
                return list(csv.DictReader(f))
    except Exception:
        return []
    return []


def buscar_medicos(filepath_base, documento=None, especialidad=None):
    """
    Busca médicos por documento o especialidad en JSON o CSV.
    Si ambos están vacíos, retorna lista vacía.
    """
    documento = str(documento or "").strip()
    especialidad = str(especialidad or "").strip().lower()

    # Archivos posibles
    base, ext = os.path.splitext(filepath_base)
    if ext not in (".json", ".csv"):
        rutas = [f"{base}.json", f"{base}.csv"]
    else:
        rutas = [filepath_base]

    resultados = []
    for ruta in rutas:
        if not os.path.exists(ruta):
            continue

        medicos = leer_datos_archivo(ruta)
        for m in medicos:
            doc = str(m.get("documento", "")).strip()
            esp = str(m.get("especialidad", "")).strip().lower()

            # Buscar por documento
            if documento and doc == documento:
                resultados.append(m)
            # Buscar por especialidad
            elif especialidad and esp == especialidad:
                resultados.append(m)

    return resultados


def menu_crear_medico(filepath: str):
    """
        Permite registrar un nuevo médico en el sistema.

        Args:
            filepath (str): Ruta del archivo donde se almacenan los médicos.
        Returns:
            None
    """
    limpiar()
    console.print(Panel.fit("[bold cyan]➕🩺 Registrar Nuevo Médico[/bold cyan]"))

    # --- Entradas con validaciones ---
    tipo_documento = solicitar_tipo_documento()
    documento = validar_campos.validar_cedula("Número de Documento", filepath)
    nombres = validar_campos.validar_texto("Nombres").capitalize()
    apellidos = validar_campos.validar_texto("Apellidos").capitalize()
    especialidad = solicitar_especialidad_medica()
    telefono = validar_campos.validar_telefono("Teléfono")
    estado = estado_medico()
    consultorio = validar_campos.validar_numero("Número de Consultorio")

    # --- Crear diccionario con los datos del médico ---
    nuevo_medico = {
        "tipo_documento": tipo_documento,
        "documento": documento,
        "nombres": nombres,
        "apellidos": apellidos,
        "especialidad": especialidad,
        "telefono": telefono,
        "estado": estado,
        "consultorio": consultorio,
    }

    # --- Validar campos obligatorios ---
    campos_obligatorios = ["tipo_documento", "documento", "nombres", "apellidos", "telefono"]
    if not entrada_datos.validar_datos_relacion_obligatorios(nuevo_medico, campos_obligatorios, "médico"):
        console.print(Panel("⚠ Faltan datos obligatorios.", border_style="red", title="Error"))
        input("\nPresione Enter para continuar...")
        return

    # --- Crear el médico ---
    medico_creado = medico.crear_medico(
        filepath,
        tipo_documento,
        documento,
        nombres,
        apellidos,
        especialidad,
        telefono,
        estado,
        consultorio
    )

    # --- Confirmación ---
    if medico_creado:
        console.print(Panel(
            f"✅ ¡Médico registrado con éxito!\nID Asignado: [bold yellow]{medico_creado['id']}[/bold yellow]",
            border_style="green",
            title="Éxito"
        ))
    else:
        console.print(Panel("⚠ No se pudo registrar el médico.", border_style="red", title="Error"))

    input("\nPresione Enter para continuar...")


def menu_leer_medicos(filepath: str):
    """
        Esta función permite leer y mostrar todos los médicos registrados.
        
        Args:
            filepath (str): La ruta al archivo donde se almacenan los médicos.
        Returns:        
            none    
            
    """
    limpiar()
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

    for m in medicos:
        tabla.add_row(
            m.get('id', 'N/A'),
            f"{m.get('nombres', '')} {m.get('apellidos', '')}",
            m.get('especialidad', 'N/A'),
            m.get('telefono', 'N/A'),
            m.get('estado', 'N/A'),
            m.get('consultorio', 'N/A'),
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
    
def menu_buscar_medico(filepath_base: str):
    """
    Menú interactivo para buscar médicos por documento o especialidad.
    Funciona con archivos JSON o CSV.
    """
    console = Console()

    # Verificar si hay archivo disponible
    base, ext = os.path.splitext(filepath_base)
    posibles_rutas = [f"{base}.json", f"{base}.csv"] if ext == "" else [filepath_base]
    medicos = []

    for ruta in posibles_rutas:
        if os.path.exists(ruta):
            medicos = leer_datos_archivo(ruta)
            break

    if not medicos:
        console.print("[red]❌ No hay médicos registrados o no se encontró el archivo (.json / .csv).[/red]")
        console.input("\n[cyan]Presione Enter para volver al menú...[/cyan]")
        return

    # Entrada de usuario
    console.print("[bold cyan]🔎 Buscar médico[/bold cyan]")
    documento = console.input(
        "[cyan]Ingrese el documento o dar enter para buscar por especialidad buscar por especialidad: [/cyan]"
        ).strip()
    especialidad = ""
    if not documento:
        especialidad = console.input("[cyan]Ingrese la especialidad: [/cyan]").strip()

    if not documento and not especialidad:
        console.print("[red]⚠️ Debe ingresar al menos un dato (documento o especialidad).[/red]")
        console.input("\n[cyan]Presione Enter para volver al menú...[/cyan]")
        return

    resultados = buscar_medicos(filepath_base, documento, especialidad)

    if resultados:
        tabla = Table(title="Resultados de búsqueda")
        tabla.add_column("Documento", justify="center")
        tabla.add_column("Nombre", justify="center")
        tabla.add_column("Especialidad", justify="center")
        tabla.add_column("Teléfono", justify="center")
        tabla.add_column("Estado", justify="center")
        tabla.add_column("Consultorio", justify="center")

        for m in resultados:
            nombre = f"{m.get(
                'nombres', m.get('nombre', ''))} {m.get(
                'apellidos', m.get('apellido', ''))
                }".strip()
            tabla.add_row(
                m.get("documento", "N/A"),
                nombre or "Sin nombre",
                m.get("especialidad", "N/A"),
                m.get("telefono", "N/A"),
                m.get("estado", "N/A"),
                m.get("consultorio", "N/A")
            )

        console.print(tabla)
    else:
        console.print("[red]❌ No se encontraron médicos con esos datos.[/red]")

    console.input("\n[cyan]Presione Enter para volver al menú...[/cyan]")


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
        Es la función principal que maneja el menú interactivo del módulo de médicos.   
        Args:
            none
        Returns:        
            none
            
    """

    limpiar()
    archivo = elegir_almacenamiento()
    console.print(f"\n[bold green]Usando archivo:[/bold green] {archivo}")

    opciones = [
        "➕🩺 Registrar un nuevo médico",
        "📄👨‍⚕️ Ver todos los médicos",
        "✏️🩹 Actualizar datos de un médico",
        "🔎 Buscar medico",
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
            menu_buscar_medico(archivo)
        elif seleccion == 4:
            menu_eliminar_medico(archivo)
        elif seleccion == 5:
            console.print("\n[bold red]⬅ Volviendo al menú principal...[/bold red]")
            break


# =========================================================
# 🔹 Ejecución directa (para pruebas)
# =========================================================
if __name__ == "__main__":
    main_vista_medicos()
