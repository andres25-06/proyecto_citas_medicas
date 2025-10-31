# -- coding: utf-8 --
"""
Vista del Módulo de Citas con selector interactivo (flechas ↑ ↓)
y diseño mejorado con emojis para el CRUD.
"""
import calendar
import csv
import datetime
import json
import os
import time
from typing import Any, Dict, List, Optional

import readchar
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, IntPrompt, Prompt
from rich.table import Table

from Modelo import cita, medico, paciente
from Validaciones import entrada_datos, validar_campos
from Vista import navegacion

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


def elegir_almacenamiento() -> Optional[str]:
    """
    Seleccionar tipo de almacenamiento (CSV o JSON) usando el selector interactivo.
    
    Args:
        none
    Returns:    
        str: Ruta del archivo seleccionado para almacenamiento.
    """
    limpiar()
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


def selector_interactivo(titulo: str, opciones: List[str]) -> int:
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
            if "Volver" in opt or "⬅" in opt:
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


def mostrar_calendario(anio: int, mes: int, dia_actual: int):
    """
    Muestra el calendario del mes con el día seleccionado resaltado.
    Los días pasados se muestran en gris.
    
    Args:
        anio (int): Año del calendario.
        mes (int): Mes del calendario.
        dia_actual (int): Día actualmente seleccionado.
    Returns:
        none
    """
    hoy = datetime.date.today()
    tabla = Table(show_header=False, box=None, padding=(0, 1))
    tabla.add_row("L", "M", "X", "J", "V", "S", "D")

    cal = calendar.Calendar(firstweekday=0)
    dias_mes = cal.monthdayscalendar(anio, mes)

    for semana in dias_mes:
        fila = []
        for dia in semana:
            if dia == 0:
                fila.append(" ")
            else:
                fecha_dia = datetime.date(anio, mes, dia)

                # 🕒 Colores según condición
                if fecha_dia < hoy:
                    fila.append(f"[grey50]{dia:2}[/grey50]")  # Día pasado
                elif dia == dia_actual:
                    fila.append(f"[bold reverse green]{dia:2}[/bold reverse green]")  # Día actual seleccionado
                else:
                    fila.append(f"[orange1]{dia:2}[/orange1]")  # Día disponible
        tabla.add_row(*fila)

    nombre_mes = datetime.date(anio, mes, 1).strftime("%B %Y")
    console.print(Panel.fit(tabla, title=f"[bold cyan]{nombre_mes}[/bold cyan]", border_style="green"))


def seleccionar_fecha() -> Optional[str]:
    """
    Selector interactivo de fecha con movimiento entre días.
    No permite seleccionar fechas anteriores al día actual.
    
    Args:
        none
    Returns:
        Optional[str]: Fecha seleccionada en formato YYYY-MM-DD o None si se cancela.
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
            dia_actual += 1
            ultimo_dia = calendar.monthrange(anio, mes)[1]
            if dia_actual > ultimo_dia:
                dia_actual = 1
                mes += 1
                if mes > 12:
                    mes = 1
                    anio += 1

        elif tecla == readchar.key.LEFT:
            dia_actual -= 1
            if dia_actual < 1:
                mes -= 1
                if mes < 1:
                    mes = 12
                    anio -= 1
                dia_actual = calendar.monthrange(anio, mes)[1]

        elif tecla == readchar.key.UP:
            dia_actual -= 7
            if dia_actual < 1:
                mes -= 1
                if mes < 1:
                    mes = 12
                    anio -= 1
                dia_actual += calendar.monthrange(anio, mes)[1]

        elif tecla == readchar.key.DOWN:
            dia_actual += 7
            ultimo_dia = calendar.monthrange(anio, mes)[1]
            if dia_actual > ultimo_dia:
                dia_actual -= ultimo_dia
                mes += 1
                if mes > 12:
                    mes = 1
                    anio += 1

        elif tecla == readchar.key.ENTER:
            fecha_seleccionada = datetime.date(anio, mes, dia_actual)
            if fecha_seleccionada < hoy:
                console.print("[red]❌ No puedes seleccionar una fecha anterior a hoy.[/red]")
                console.input("[yellow]Presiona Enter para continuar...[/yellow]")
            else:
                return fecha_seleccionada.strftime("%Y-%m-%d")

        elif tecla.lower() == "q":
            return None


def calendario() -> Optional[str]:
    """
    Menú para seleccionar fecha y hora de la cita.
    
    Args:
        none
    Returns:
        Optional[str]: Fecha seleccionada o None si se cancela.
    """
    limpiar()
    console.print(Panel.fit("[bold cyan]📅 Selecciona la fecha de la cita[/bold cyan]"))
    fecha = seleccionar_fecha()
    if fecha:
        console.print(f"\n✅ Cita agendada para el [bold cyan]{fecha}[/bold cyan]")
        return f"{fecha}"
    else:
        console.print("[red]Operación cancelada.[/red]")
        return None


# =========================================================
# 🔹 Estado de la cita
# =========================================================
def estado_cita(permitir_vacio: bool = False) -> Optional[str]:
    """
    Permite seleccionar el estado de la cita (Completada, Pendiente o Cancelada) usando un selector interactivo.

    Args:
        permitir_vacio (bool): Si es True, permite dejar el estado sin cambiar.
    Returns:
        Optional[str]: El estado seleccionado o None si se permite vacío y no se cambia.
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
# 🔹 Funciones para cargar datos desde archivos
# =========================================================
def cargar_datos(ruta: str) -> List[Dict[str, Any]]:
    """
    Carga datos desde un archivo CSV o JSON.
    
    Args:
        ruta (str): Ruta al archivo.
    Returns:
        List[Dict[str, Any]]: Lista de diccionarios con los datos.
    """
    if not os.path.exists(ruta):
        return []

    try:
        if ruta.endswith('.json'):
            with open(ruta, 'r', encoding='utf-8') as f:
                return json.load(f)
        elif ruta.endswith('.csv'):
            with open(ruta, 'r', encoding='utf-8') as f:
                return list(csv.DictReader(f))
    except Exception:
        return []
    return []


def leer_datos_archivo(filepath: str) -> List[Dict[str, Any]]:
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


# =========================================================
# 🔹 Funciones para cargar médicos y pacientes
# =========================================================
def cargar_medicos_y_pacientes():
    """
    Carga médicos y pacientes desde JSON o CSV.
    Intenta primero JSON, luego CSV.
    
    Returns:
        tuple: (lista_pacientes, lista_medicos)
    """
    # Cargar pacientes
    pacientes = []
    try:
        if os.path.exists("data/pacientes.json"):
            pacientes = paciente.leer_todos_los_pacientes("data/pacientes.json")
    except Exception:
        pass

    if not pacientes:
        try:
            if os.path.exists("data/pacientes.csv"):
                pacientes = paciente.leer_todos_los_pacientes("data/pacientes.csv")
        except Exception:
            pass

    # Cargar médicos
    medicos = []
    try:
        if os.path.exists("data/medicos.json"):
            medicos = medico.leer_todos_los_medicos("data/medicos.json")
    except Exception:
        pass

    if not medicos:
        try:
            if os.path.exists("data/medicos.csv"):
                medicos = medico.leer_todos_los_medicos("data/medicos.csv")
        except Exception:
            pass

    return pacientes, medicos


# =========================================================
# 🔹 Funciones para obtener nombres
# =========================================================
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
        registros = []
        if tipo == "paciente":
            # Intentar JSON
            try:
                registros = paciente.leer_todos_los_pacientes("data/pacientes.json")
            except Exception:
                registros = []
            # Si no hay registros JSON, intentar CSV
            if not registros:
                try:
                    registros = paciente.leer_todos_los_pacientes("data/pacientes.csv")
                except Exception:
                    registros = []
        else:  # medico
            try:
                registros = medico.leer_todos_los_medicos("data/medicos.json")
            except Exception:
                registros = []
            if not registros:
                try:
                    registros = medico.leer_todos_los_medicos("data/medicos.csv")
                except Exception:
                    registros = []

        for r in registros:
            if r.get("documento") == documento:
                return f"{r.get('nombres', '')} {r.get('apellidos', '')}".strip()
        return f"{documento} (no encontrado)"
    except Exception as e:
        return f"Error: {e}"


def obtener_nombre_por_documento(filepath_base: str, documento: str) -> str:
    """
    Busca el nombre completo de una persona (paciente o médico)
    por su documento en archivos JSON o CSV (busca en ambos si existen).

    Args:
        filepath_base (str): Ruta base sin extensión o con extensión (.json o .csv)
        documento (str): Documento a buscar
    Returns:
        str: Nombre completo o mensaje de error
    """
    documento = str(documento).strip()

    # Quitar extensión si viene incluida
    base, ext = os.path.splitext(filepath_base)
    if ext not in (".json", ".csv"):
        # Probar con ambas rutas
        rutas = [f"{base}.json", f"{base}.csv"]
    else:
        rutas = [filepath_base]

    for ruta in rutas:
        if not os.path.exists(ruta):
            continue

        try:
            # Leer JSON
            if ruta.endswith(".json"):
                with open(ruta, "r", encoding="utf-8") as f:
                    personas = json.load(f)
            # Leer CSV
            elif ruta.endswith(".csv"):
                with open(ruta, "r", encoding="utf-8") as f:
                    lector = csv.DictReader(f)
                    personas = list(lector)
            else:
                continue
        except Exception:
            continue

        # Buscar persona por documento
        for p in personas:
            doc = str(p.get("documento", "")).strip()
            if doc == documento:
                nombre = p.get("nombres", "") or p.get("nombre", "")
                apellido = p.get("apellidos", "") or p.get("apellido", "")
                if nombre and apellido:
                    return f"{nombre.strip()} {apellido.strip()}"
                elif nombre:
                    return nombre.strip()
                else:
                    return "Sin nombre"

    return "No encontrado"


# =========================================================
# 🔹 Funciones del módulo de Citas (CRUD)
# =========================================================
def menu_agendar_cita(filepath: str, lista_pacientes: list, lista_medicos: list):
    """
    Menú para agendar una nueva cita médica.

    Args:
        filepath (str): Ruta del archivo donde se almacenan las citas.
        lista_pacientes (list): Lista de pacientes registrados.
        lista_medicos (list): Lista de médicos registrados.
    Returns:
        none
    """
    limpiar()
    console.print(Panel.fit("[bold cyan]🩺 Agendar Nueva Cita[/bold cyan]"))

    # --- Solicitar datos con validaciones ---
    documento_paciente = validar_campos.validar_cedula("Documento del Paciente", filepath)
    documento_medico = validar_campos.validar_cedula("Documento del Médico", filepath)

    fecha = calendario()
    if fecha is None:
        input("\nPresione Enter para continuar...")
        return
    hora = validar_campos.validar_hora("[bold yellow]⏰ Ingresa la hora (HH:MM): [/bold yellow]")
    motivo = validar_campos.validar_texto("Motivo de la consulta")
    estado = estado_cita()

    # --- Validar existencia de relaciones ---
    if not entrada_datos.validar_existencia_relacion(documento_paciente, lista_pacientes, "pacientes"):
        console.print(Panel("⚠ El paciente no existe en el sistema.", border_style="red", title="Error"))
        input("\nPresione Enter para continuar...")
        return

    if not entrada_datos.validar_existencia_relacion(documento_medico, lista_medicos, "medicos"):
        console.print(Panel("⚠ El médico no existe en el sistema.", border_style="red", title="Error"))
        input("\nPresione Enter para continuar...")
        return

    # ✅ VALIDACIÓN: Verificar que el médico esté activo
    medico_encontrado = None
    for m in lista_medicos:
        doc = str(m.get("documento", "")).strip()
        if doc == str(documento_medico).strip():
            medico_encontrado = m
            break

    if medico_encontrado:
        estado_medico = str(medico_encontrado.get("estado", "")).strip()

        if estado_medico.lower() == "inactivo":
            console.print(Panel(
                f"⚠️ El médico está INACTIVO y no puede atender citas.\n\n"
                f"Médico: {medico_encontrado.get('nombres', '')} {medico_encontrado.get('apellidos', '')}\n"
                f"Especialidad: {medico_encontrado.get('especialidad', 'N/A')}\n"
                f"Estado: [bold red]{estado_medico}[/bold red]",
                border_style="red",
                title="❌ Error - Médico Inactivo"
            ))
            input("\nPresione Enter para continuar...")
            return

    # --- Crear diccionario de la cita ---
    nueva_cita = {
        "documento_paciente": documento_paciente.strip(),
        "documento_medico": documento_medico.strip(),
        "fecha": fecha.strip(),
        "hora": hora.strip(),
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
            hora,
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

        # 🔹 Mostrar actualización de estadísticas sin romper el flujo
        try:
            from Vista.vista_estadisticas_medico import estadisticas_citas_por_medico
            console.print("\n[cyan]📊 Actualizando estadísticas médicas...[/cyan]")
            estadisticas_citas_por_medico(
                ruta_medicos="data/medicos.csv",
                ruta_citas="data/citas.json",
                mostrar=False
            )
        except Exception as e:
            console.print(f"[red]No se pudo actualizar estadísticas: {e}[/red]")
    else:
        console.print(Panel(
            "⚠️ Ya existe una cita con esos datos o ocurrió un error.",
            border_style="red",
            title="Error"
        ))
    input("\nPresione Enter para continuar...")


def menu_actualizar_cita(filepath: str):
    """
    Menú para actualizar datos de una cita existente.
    
    Args:
        filepath (str): Ruta del archivo donde se almacenan las citas.
    Returns:
        none
    """
    console.print(Panel.fit("[bold cyan]✏️📅 Actualizar Datos de Cita[/bold cyan]", border_style="cyan"))

    documento = Prompt.ask("Ingrese el documento del paciente")
    # Mostrar todas las citas del paciente y permitir elegir cuál actualizar (mejor UX)
    citas_paciente = [c for c in cita.gestor_datos_citas.cargar_datos(filepath) if c.get("documento_paciente") == documento]

    if not citas_paciente:
        console.print("[bold red]❌ No se encontró ninguna cita para ese documento.[/bold red]")
        input("\nPresione Enter para continuar...")
        return

    # Mostrar tabla de citas del paciente
    tabla = Table(title="Citas del paciente", show_lines=True, header_style="bold magenta")
    tabla.add_column("N°", justify="center")
    tabla.add_column("ID", justify="center")
    tabla.add_column("Fecha", justify="center")
    tabla.add_column("Hora", justify="center")
    tabla.add_column("Motivo", justify="left")
    tabla.add_column("Estado", justify="center")

    for i, c in enumerate(citas_paciente, start=1):
        tabla.add_row(str(i), str(c.get("id", "")), c.get("fecha", ""), c.get("hora", ""), c.get("motivo", ""), c.get("estado", ""))

    console.print(tabla)

    try:
        seleccion = IntPrompt.ask("Ingrese el número (N°) de la cita que desea actualizar", default=1)
        if seleccion < 1 or seleccion > len(citas_paciente):
            console.print("[bold red]❌ Selección inválida.[/bold red]")
            input("\nPresione Enter para continuar...")
            return
    except Exception:
        console.print("[bold red]❌ Entrada inválida.[/bold red]")
        input("\nPresione Enter para continuar...")
        return

    cita_actual = citas_paciente[seleccion - 1]

    console.print(Panel.fit("Presione Enter para dejar un campo sin cambios.", border_style="yellow"))
    datos_nuevos: Dict[str, Any] = {}

    nueva_fecha = Prompt.ask(f"Fecha ({cita_actual.get('fecha', 'N/A')})", default=str(cita_actual.get('fecha', '')))
    if nueva_fecha and nueva_fecha != cita_actual.get('fecha'):
        datos_nuevos['fecha'] = nueva_fecha

    nueva_hora = Prompt.ask(f"Hora ({cita_actual.get('hora', 'N/A')})", default=str(cita_actual.get('hora', '')))
    if nueva_hora and nueva_hora != cita_actual.get('hora'):
        datos_nuevos['hora'] = nueva_hora

    nuevo_motivo = Prompt.ask(f"Motivo ({cita_actual.get('motivo', 'N/A')})", default=str(cita_actual.get('motivo', '')))
    if nuevo_motivo and nuevo_motivo != cita_actual.get('motivo'):
        datos_nuevos['motivo'] = nuevo_motivo

    # Permitir no cambiar el estado
    estado = estado_cita(permitir_vacio=True)
    if estado is not None and estado != cita_actual.get('estado'):
        datos_nuevos['estado'] = estado

    if not datos_nuevos:
        console.print("[yellow]⚠️ No se modificó ningún dato.[/yellow]")
        input("\nPresione Enter para continuar...")
        return

    if Confirm.ask("¿Desea guardar los cambios?", default=True):
        cita_actualizada = cita.actualizar_cita(
            filepath,
            cita_actual.get("id"),
            datos_nuevos
        )

        if cita_actualizada:
            console.print(Panel("[bold green]✅ ¡Cita actualizada con éxito![/bold green]", border_style="green"))
        else:
            console.print(Panel("[bold red]❌ Error al actualizar la cita.[/bold red]", border_style="red"))
    else:
        console.print("[yellow]Operación cancelada por el usuario.[/yellow]")

    input("\nPresione Enter para continuar...")


def menu_cancelar_cita(filepath: str):
    """
    Menú para cancelar todas las citas de un paciente según su documento.
    
    Args:
        filepath (str): Ruta del archivo donde se almacenan las citas.
    Returns:
        none
    """
    console.print(Panel.fit("[bold cyan]🗑️ Cancelar Cita por Documento[/bold cyan]"))

    # Solicitar documento del paciente
    documento = Prompt.ask("Ingrese el documento del paciente")

    # Confirmar acción
    if Confirm.ask(
        f"¿Está seguro de cancelar todas las citas del paciente con documento {documento}?",
        default=False
    ):
        # Llamar a la función que elimina las citas
        exito = cita.eliminar_cita_por_documento(filepath, documento)

        if exito:
            console.print("[bold green]✅ Cita(s) cancelada(s) exitosamente.[/bold green]")

            # 🔹 Actualizar estadísticas automáticamente
            try:
                from Vista.vista_estadisticas_medico import (
                    estadisticas_citas_por_medico,
                )
                console.print("\n[cyan]📊 Actualizando estadísticas de médicos...[/cyan]")
                estadisticas_citas_por_medico(
                    ruta_medicos="data/medicos.csv",
                    ruta_citas="data/citas.json",
                    mostrar=False
                )
            except Exception as e:
                console.print(f"[red]⚠ No se pudieron actualizar las estadísticas: {e}[/red]")

        else:
            console.print("[bold yellow]⚠️ No se encontraron citas para ese documento.[/bold yellow]")
    else:
        console.print("[yellow]Operación cancelada.[/yellow]")

    input("\nPresione Enter para continuar...")


def menu_ver_todas_citas(filepath: str):
    """
    Muestra todas las citas médicas registradas.
    
    Args:
        filepath (str): La ruta al archivo donde se almacenan las citas.
    Returns:
        none
    """
    console.print(Panel.fit("[bold cyan]📋 Lista de Citas[/bold cyan]"))

    # --- Leer citas ---
    citas_registradas = cita.leer_todas_las_citas(filepath)

    if not citas_registradas:
        console.print("[yellow]⚠️ No hay citas registradas.[/yellow]")
        input("\nPresione Enter para continuar...")
        return

    # --- Crear tabla ---
    tabla = Table(title="Citas Médicas Registradas", border_style="blue", header_style="bold magenta")
    tabla.add_column("ID", style="dim", width=6)
    tabla.add_column("Paciente", justify="center")
    tabla.add_column("Médico", justify="center")
    tabla.add_column("Fecha ", justify="center")
    tabla.add_column("Hora", justify="center")
    tabla.add_column("Motivo", justify="center")
    tabla.add_column("Estado", justify="center")

    # --- Llenar tabla ---
    for c in citas_registradas:
        paciente_nombre = obtener_nombre_completo_por_documento(
            "data/pacientes.json", c.get("documento_paciente", ""), "paciente"
        )
        medico_nombre = obtener_nombre_completo_por_documento(
            "data/medicos.json", c.get("documento_medico", ""), "medico"
        )

        tabla.add_row(
            str(c.get("id")),
            paciente_nombre,
            medico_nombre,
            c.get("fecha", ""),
            c.get("hora", ""),
            c.get("motivo", ""),
            c.get("estado", "")
        )

    console.print(tabla)
    input("\nPresione Enter para continuar...")


def buscar_cita_por_documento(citas: List[Dict[str, Any]], documento: str) -> List[Dict[str, Any]]:
    """
    Busca todas las citas asociadas a un documento de paciente.
    
    Args:
        citas (List[Dict[str, Any]]): Lista de todas las citas.
        documento (str): Documento del paciente a buscar.
    Returns:
        List[Dict[str, Any]]: Lista de citas encontradas.
    """
    posibles_claves = ["documento_paciente", "documento", "doc_paciente"]
    resultados = []
    documento = str(documento).strip()

    for c in citas:
        for clave in posibles_claves:
            if clave in c and str(c[clave]).strip() == documento:
                resultados.append(c)
                break
    return resultados


def menu_buscar_cita_por_documento(filepath: str):
    """
    Permite buscar y mostrar las citas de un paciente por su documento.
    
    Args:
        filepath (str): Ruta del archivo donde se almacenan las citas.
    Returns:
        none
    """
    citas = leer_datos_archivo(filepath)

    if not citas:
        console.print("[red]❌ No hay citas registradas o el archivo no existe.[/red]")
        console.input("\n[cyan]Presione Enter para volver al menú...[/cyan]")
        return

    documento = console.input("[cyan]Ingrese el documento del paciente: [/cyan]").strip()
    resultados = buscar_cita_por_documento(citas, documento)

    if resultados:
        tabla = Table(title=f"Citas del paciente con documento {documento}")
        tabla.add_column("ID", style="dim", width=6)
        tabla.add_column("Paciente", justify="center")
        tabla.add_column("Médico", justify="center")
        tabla.add_column("Fecha", justify="center")
        tabla.add_column("Hora", justify="center")
        tabla.add_column("Motivo", justify="center")
        tabla.add_column("Estado", justify="center")

        for c in resultados:
            nombre_paciente = obtener_nombre_por_documento("data/pacientes", c.get("documento_paciente"))
            nombre_medico = obtener_nombre_por_documento("data/medicos", c.get("documento_medico"))

            tabla.add_row(
                str(c.get("id_cita", c.get("id", ""))),
                nombre_paciente,
                nombre_medico,
                c.get("fecha", "N/A"),
                c.get("hora", "N/A"),
                c.get("motivo", "N/A"),
                c.get("estado", "N/A")
            )

        console.print(tabla)
    else:
        console.print(f"[red]❌ No se encontraron citas para el documento {documento}.[/red]")

    console.input("\n[cyan]Presione Enter para volver al menú...[/cyan]")


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
    
    Args:
        none
    Returns:
        none
    """
    limpiar()
    archivo = elegir_almacenamiento()
    if not archivo:
        return
    console.print(f"\n[bold green]Usando archivo:[/bold green] {archivo}")

    # Definir título y opciones del menú
    titulo = "📅 MENÚ DE CITAS MÉDICAS"
    opciones = [
        "➕ Agendar cita",
        "✏️  Actualizar cita",
        "❌ Cancelar cita",
        "📋 Ver todas las citas",
        "🔎 Buscar cita",
        "⬅ Volver al menú principal"
    ]

    while True:
        seleccion = selector_interactivo(titulo, opciones)

        if seleccion == 0:
            # 🔹 CARGAR DATOS CORRECTAMENTE
            pacientes, medicos = cargar_medicos_y_pacientes()
            menu_agendar_cita(archivo, pacientes, medicos)
        elif seleccion == 1:
            menu_actualizar_cita(archivo)
        elif seleccion == 2:
            menu_cancelar_cita(archivo)
        elif seleccion == 3:
            menu_ver_todas_citas(archivo)
        elif seleccion == 4:
            menu_buscar_cita_por_documento(archivo)
        elif seleccion == 5:
            console.print("\n[bold red]⬅ Volviendo al menú principal...[/bold red]")
            break


# =========================================================
# 🔹 Ejecución directa (para pruebas)
# =========================================================
if __name__ == "__main__":
    main_vista_citas()
