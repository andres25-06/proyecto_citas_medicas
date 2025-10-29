# -- coding: utf-8 --
"""
Vista del Módulo de Médicos con selector interactivo (flechas ↑ ↓)
y diseño mejorado con emojis para el CRUD.
"""
import calendar
import datetime
import json
import csv
import os
import readchar
import time
from Modelo import medico, paciente, cita
from Modelo import cita
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt, Confirm
from rich.table import Table
from Vista.vista_principal import vista_principal 
from Validaciones import validar_campos
from Validaciones import entrada_datos


console = Console()

# --- Configuración de rutas ---
DIRECTORIO_DATOS = 'data'
NOMBRE_ARCHIVO_CSV = 'citas.csv'
NOMBRE_ARCHIVO_JSON = 'citas.json'


# =========================================================
# 🔹 Funciones auxiliares
# =========================================================
def limpiar():
    """
        Está función limpia la consola para mejorar la legibilidad.
        
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
        vista_principal()
        return None


def selector_interactivo(titulo, opciones):
    """ 
        Permite moverse con flechas ↑ ↓ y seleccionar con Enter.

        Args:
            titulo (str): Título del menú.
            opciones (List[str]): Lista de opciones del menú.
        Returns:
            int: Índice de la opción seleccionada.
            
    """
    seleccion = 0
    while True:
        limpiar()
        console.print(Panel(f"[bold cyan]{titulo}[/bold cyan]"))
        for i, opt in enumerate(opciones):
            prefix = "👉 " if i == seleccion else "   "
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

def mostrar_calendario(anio, mes, dia_actual):
    """
    Muestra el calendario del mes con el día seleccionado resaltado.
    """
    tabla = Table(show_header=False, box=None, padding=(0, 1))
    tabla.add_row("L", "M", "X", "J", "V", "S", "D")

    cal = calendar.Calendar(firstweekday=0)
    dias_mes = cal.monthdayscalendar(anio, mes)

    for semana in dias_mes:
        fila = []
        for dia in semana:
            if dia == 0:
                fila.append(" ")
            elif dia == dia_actual:
                fila.append(f"[bold reverse green]{dia:2}[/bold reverse green]")
            else:
                fila.append(f"[orange1]{dia:2}[/orange1]")
        tabla.add_row(*fila)

    nombre_mes = datetime.date(anio, mes, 1).strftime("%B %Y")
    console.print(Panel.fit(tabla, title=f"[bold cyan]{nombre_mes}[/bold cyan]", border_style="green"))

def seleccionar_fecha():
    """
    Selector interactivo de fecha con movimiento entre días.
    """
    hoy = datetime.date.today()
    anio, mes = hoy.year, hoy.month
    dia_actual = hoy.day

    while True:
        limpiar()
        mostrar_calendario(anio, mes, dia_actual)
        console.print("\n⬅️ [blue]Día anterior[/blue]   ➡️ [blue]Día siguiente[/blue]   ⏎ [green]Seleccionar[/green]   Q [red]Salir[/red]")
        tecla = readchar.readkey()

        if tecla == readchar.key.RIGHT:
            # Día siguiente
            dia_actual += 1
            ultimo_dia = calendar.monthrange(anio, mes)[1]
            if dia_actual > ultimo_dia:
                dia_actual = 1
                mes += 1
                if mes > 12:
                    mes = 1
                    anio += 1

        elif tecla == readchar.key.LEFT:
            # Día anterior
            dia_actual -= 1
            if dia_actual < 1:
                mes -= 1
                if mes < 1:
                    mes = 12
                    anio -= 1
                dia_actual = calendar.monthrange(anio, mes)[1]

        elif tecla == readchar.key.UP:
            # Subir una semana (7 días)
            dia_actual -= 7
            if dia_actual < 1:
                mes -= 1
                if mes < 1:
                    mes = 12
                    anio -= 1
                dia_actual += calendar.monthrange(anio, mes)[1]

        elif tecla == readchar.key.DOWN:
            # Bajar una semana (7 días)
            dia_actual += 7
            ultimo_dia = calendar.monthrange(anio, mes)[1]
            if dia_actual > ultimo_dia:
                dia_actual -= ultimo_dia
                mes += 1
                if mes > 12:
                    mes = 1
                    anio += 1

        elif tecla == readchar.key.ENTER:
            return datetime.date(anio, mes, dia_actual).strftime("%Y-%m-%d")

        elif tecla.lower() == "q":
            return None


def calendario():
    limpiar()
    console.print(Panel.fit("[bold cyan]📅 Selecciona la fecha de la cita[/bold cyan]"))
    fecha = seleccionar_fecha()
    if fecha:
        console.print(f"\nHas seleccionado la fecha: [bold green]{fecha}[/bold green]")
        hora = console.input("[bold yellow]⏰ Ingresa la hora (HH:MM): [/bold yellow]")
        console.print(f"\n✅ Cita agendada para el [bold cyan]{fecha}[/bold cyan] a las [bold cyan]{hora}[/bold cyan].")
        return f"{fecha} {hora}"  # ✅ Retorna fecha + hora
    else:
        console.print("[red]Operación cancelada.[/red]")
        return None
    
# =========================================================
# 🔹 Estado de la cita
# =========================================================
def estado_cita(permitir_vacio: bool = False) -> str | None:
    """
    Permite seleccionar el estado de la cita (Completatada, Pendiente o Cancelada) usando un selector interactivo.

    Args:
        permitir_vacio (bool): Si es True, permite dejar el estado sin cambiar.
    Returns:
        str | None: El estado seleccionado o None si se permite vacío y no se cambia.
    """
    tipos = {
        '1': 'Completada',
        '2': 'Pendiente',
        '3': 'Cancelada'
    }

    descripciones = {
        '1': '✅ Completada',
        '2': '⚠️ Pendiente',
        '3': '❌ Cancelada'
    }

    opciones = [desc for desc in descripciones.values()]

    if permitir_vacio:
        opciones.insert(0, "🔸 No cambiar")

    seleccion = selector_interactivo("📋 Seleccione el estado de la cita", opciones)

    # Si se permite dejar vacío y se elige "No cambiar"
    if permitir_vacio and seleccion == 0:
        console.print("[bold yellow]⚠ No se modificará el estado de la cita.[/bold yellow]")
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

# =========================================================
# 🔹 Funciones del módulo de Citas
# =========================================================
def menu_agendar_cita(filepath: str, lista_pacientes: list, lista_medicos: list):
    """
    Menú para agendar una nueva cita médica.

    Args:
        filepath (str): Ruta del archivo donde se almacenan las citas.
        lista_pacientes (list): Lista de pacientes registrados.
        lista_medicos (list): Lista de médicos registrados.
    """
    limpiar()
    console.print(Panel.fit("[bold cyan]🩺 Agendar Nueva Cita[/bold cyan]"))

    # --- Solicitar datos con validaciones ---
    documento_paciente = validar_campos.validar_cedula("Documento del Paciente", filepath)
    documento_medico = validar_campos.validar_cedula("Documento del Médico", filepath)
    fecha = calendario()
    motivo = validar_campos.validar_texto("Motivo de la consulta")
    estado = estado_cita()

    # --- Validar existencia de relaciones ---
    if not entrada_datos.validar_existencia_relacion(documento_paciente,    lista_pacientes, "paciente"):
        console.print(Panel("⚠ El paciente no existe en el sistema.", border_style="red", title="Error"))
        input("\nPresione Enter para continuar...")
        return

    if not entrada_datos.validar_existencia_relacion(documento_medico, lista_medicos, "médico"):
        console.print(Panel("⚠ El médico no existe en el sistema.", border_style="red", title="Error"))
        input("\nPresione Enter para continuar...")
        return

    # --- Crear diccionario de la cita ---
    nueva_cita = {
        "documento_paciente": documento_paciente.strip(),
        "documento_medico": documento_medico.strip(),
        "fecha": fecha.strip() if isinstance(fecha, str) else fecha,
        "motivo": motivo.strip(),
        "estado": estado.strip(),
    }

    # --- Validar campos obligatorios ---
    campos_obligatorios = ["documento_paciente", "documento_medico", "fecha", "motivo", "estado"]
    if not entrada_datos.validar_datos_relacion_obligatorios(nueva_cita, campos_obligatorios, "cita"):
        console.print(Panel("⚠ Faltan datos obligatorios.", border_style="red", title="Error"))
        input("\nPresione Enter para continuar...")
        return

    # --- Intentar crear la cita ---
    try:
        cita_creada = cita.crear_cita(
            filepath,
            documento_paciente,
            documento_medico,
            fecha,
            motivo,
            estado
        )
    except Exception as e:
        console.print(Panel(f"❌ Error al crear la cita: {e}", border_style="red", title="Error"))
        input("\nPresione Enter para continuar...")
        return

    # --- Confirmar resultado ---
    if cita_creada:
        console.print(Panel(
            f"✅ ¡Cita creada con éxito!\n\nID asignado: [bold yellow]{cita_creada['id']}[/bold yellow]",
            border_style="green",
            title="Éxito"
        ))
    else:
        console.print(Panel(
            "⚠️ Ya existe una cita con esos datos o ocurrió un error.",
            border_style="red",
            title="Error"
        ))
    input("\nPresione Enter para continuar...")




def menu_cancelar_cita(filepath: str):
    """
    Menú para cancelar todas las citas de un paciente según su documento.
    """

    console.print(Panel.fit("[bold cyan]🗑️ Cancelar Cita por Documento[/bold cyan]"))

    # Solicitar documento del paciente
    documento = Prompt.ask("Ingrese el documento del paciente")

    # Confirmar acción
    if Confirm.ask(f"¿Está seguro de cancelar todas las citas del paciente con documento {documento}?", default=False):
        # Llamar a la función que elimina las citas
        exito = cita.eliminar_cita_por_documento(filepath, documento)

        if exito:
            console.print("[bold green]✅ Cita(s) cancelada(s) exitosamente.[/bold green]")
        else:
            console.print("[bold yellow]⚠️ No se encontraron citas para ese documento.[/bold yellow]")
    else:
        console.print("[yellow]Operación cancelada.[/yellow]")

    input("\nPresione Enter para continuar...")


def leer_datos_archivo(filepath: str):
    """
        Lee datos desde un archivo JSON o CSV y devuelve una lista de diccionarios.
        Args:
            filepath (str): Ruta al archivo de datos.
        Returns:
            List[Dict[str, Any]]: Lista de diccionarios con los datos.
    
    """
    if filepath.endswith(".json"):
        with open(filepath, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    elif filepath.endswith(".csv"):
        with open(filepath, "r", encoding="utf-8") as f:
            lector = csv.DictReader(f)
            return list(lector)
    else:
        return []

def obtener_nombre_completo_por_documento(filepath: str, documento: str, tipo: str) -> str:
    """Devuelve el nombre completo de un paciente o médico según su documento (JSON o CSV)."""
    registros = leer_datos_archivo(filepath)

    for r in registros:
        if r.get("documento") == documento:
            return f"{r.get('nombres', '')} {r.get('apellidos', '')}".strip()

    return f"{documento} (no encontrado)"

# --- MENÚ DE CITAS ---

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
        input("\nPresione Enter para continuar...")
        return

    tabla = Table(title="Citas Médicas Registradas", border_style="blue", header_style="bold magenta")
    tabla.add_column("ID", style="dim", width=6)
    tabla.add_column("Paciente")
    tabla.add_column("Médico")
    tabla.add_column("Fecha", justify="center")
    tabla.add_column("Hora", justify="center")
    tabla.add_column("Motivo")
    tabla.add_column("Estado", justify="center")

    for c in citas_registradas:
        paciente_nombre = obtener_nombre_completo_por_documento("data/pacientes.json", c["documento_paciente"], "paciente")
        medico_nombre = obtener_nombre_completo_por_documento("data/medicos.json", c["documento_medico"], "medico")

        tabla.add_row(
            c["id"],
            paciente_nombre,
            medico_nombre,
            c["fecha"],
            c["hora"],
            c["motivo"],
            c["estado"]
        )

    console.print(tabla)
    input("\nPresione Enter para continuar...")


def obtener_nombre_completo_por_documento(filepath: str, documento: str, tipo: str) -> str:
    """
        Devuelve el nombre completo de un paciente o médico según su documento.

        Args:
            filepath (str): Ruta al archivo de datos (JSON o CSV).
            documento (str): Documento del paciente o médico.
            tipo (str): "paciente" o "medico".
        Returns:    
            str: Nombre completo o mensaje de no encontrado.
        
    """
    try:
        if tipo == "paciente":
            registros = paciente.leer_todos_los_pacientes("data/pacientes.json")
            registros = paciente.leer_todos_los_pacientes("data/pacientes.csv")
        else:
            registros = medico.leer_todos_los_medicos("data/medicos.json")
            registros = medico.leer_todos_los_medicos("data/medicos.csv")

        for r in registros:
            if r.get("documento") == documento:
                return f"{r.get('nombres', '')} {r.get('apellidos', '')}".strip()
        return f"{documento} (no encontrado)"
    except Exception as e:
        return f"Error: {e}"

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
    
    # Cargar citas desde archivo
    filepath = os.path.join(DIRECTORIO_DATOS, NOMBRE_ARCHIVO_JSON)
    citas_encontradas = cita.leer_todas_las_citas(filepath)

    if citas_encontradas:
        for item in citas_encontradas:
            paciente_nombre = obtener_nombre_completo_por_documento("data/pacientes.json", item["documento_paciente"], "paciente")
            medico_nombre = obtener_nombre_completo_por_documento("data/medicos.json", item["documento_medico"], "medico")

            console.print(Panel(
                f"[bold green]Cita encontrada:[/bold green]\n"
                f"🧍 Paciente: [yellow]{paciente_nombre}[/yellow]\n"
                f"🩺 Médico: [yellow]{medico_nombre}[/yellow]\n"
                f"📅 Fecha: [cyan]{item['fecha']}[/cyan]\n"
                f"⏰ Hora: [cyan]{item['hora']}[/cyan]\n"
                f"💬 Motivo: {item['motivo']}\n"
                f"📌 Estado: {item['estado']}",
                border_style="green",
                title=f"Cita #{item['id']}"
            ))
    else:
        console.print("[yellow]⚠️ No se encontró ninguna cita con ese documento.[/yellow]")
    
    input("\nPresione Enter para continuar...")


# =========================================================
# 🔹 Menú principal interactivo
# =========================================================
def main_vista_citas():
    """
        Función principal para manejar el menú de citas médicas.
    """
    limpiar()
    archivo = elegir_almacenamiento()
    console.print(f"\n[bold green]Usando archivo:[/bold green] {archivo}")

    # Definir título y opciones del menú
    titulo = "📅 MENÚ DE CITAS MÉDICAS"
    opciones = [
        "➕ Agendar cita",
        "❌ Cancelar cita",
        "📋 Ver todas las citas",
        "🔎 Buscar cita",
        "⬅ Volver al menú principal"
    ]

    while True:
        seleccion = selector_interactivo(titulo, opciones)

        if seleccion == 0:
            pacientes = paciente.leer_todos_los_pacientes("data/pacientes.json")
            medicos = medico.leer_todos_los_medicos("data/medicos.json")
            menu_agendar_cita(archivo, pacientes, medicos)
        elif seleccion == 1:
            menu_cancelar_cita(archivo)
        elif seleccion == 2:
            menu_ver_todas_citas(archivo)
        elif seleccion == 3:
            # Si aún no existe la función de buscar, dejamos un aviso
            console.print("[yellow]⚠️ La función 'Buscar cita' aún no está implementada.[/yellow]")
            input("\nPresione Enter para continuar...")
        elif seleccion == 4:
            console.print("\n[bold red]⬅ Volviendo al menú principal...[/bold red]")
            break


# =========================================================
# 🔹 Ejecución directa (para pruebas)
# =========================================================
if __name__ == "__main__":
    main_vista_citas()
