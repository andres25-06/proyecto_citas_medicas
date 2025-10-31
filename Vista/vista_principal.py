# Vista/vista_principal.py

import calendar
import csv as _csv
import json
import os
import re
import time
from datetime import datetime

import readchar
from rich import box
from rich.align import Align
from rich.box import ROUNDED
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm
from rich.table import Table
from rich.text import Text

from Vista import navegacion
from Vista.vista_cita import obtener_nombre_por_documento
from Vista.vista_estadisticas_medico import estadisticas_citas_por_medico

# ---------------------------------
# Inicialización
# ---------------------------------
console = Console()

# ---------------------------------
# UTILIDADES
# ---------------------------------

def limpiar():
    """ Está función limpia la consola dependiendo del sistema operativo.
        Args:
            none
        Returns:
            none"""
    os.system("cls" if os.name == "nt" else "clear")


def animacion_carga(mensaje="Cargando..."):
    """
        Pequeña animación (usa Rich progress internamente simple).
        Args:
            mensaje (str): Mensaje a mostrar durante la animación.
        Returns:
            none
    """
    # una animación sencilla usando prints para compatibilidad
    limpiar()
    console.print(f"[cyan]{mensaje}[/cyan]")
    for _ in range(18):
        console.print('.', end='')
        time.sleep(0.02)
    console.print('\n')


def escribir_mensaje(texto, velocidad=0.01, color="magenta"):
    """
        Efecto typing sencillo.
        Args:
            texto (str): Texto a mostrar con efecto typing.
            velocidad (float): Tiempo de espera entre caracteres.
            color (str): Color del texto.
        Returns:
            none
    """
    for c in texto:
        console.print(c, end="", style=f"bold {color}")
        try:
            console.file.flush()
        except Exception:
            pass
        time.sleep(velocidad)
    console.print()

# ---------------------------------
# IO: JSON / CSV helpers
# ---------------------------------

def cargar_json(ruta):
    """
        Carga un archivo JSON y retorna su contenido
        Args:
            ruta (str): Ruta al archivo JSON.
        Returns:
            any: Contenido del archivo JSON.
    """
    if not os.path.exists(ruta):
        return []
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def guardar_json(ruta, datos):
    """
        Escribe datos en un archivo JSON.
        Args:
            ruta (str): Ruta al archivo JSON.
            datos (any): Datos a escribir en el archivo.
        Returns:
            none
    """
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)


def cargar_csv_simple(ruta):
    """
        Carga CSV simple asumiendo encabezado en la primera
        línea y comas como separador.
        Args:
            ruta (str): Ruta al archivo CSV.
        Returns:
            List[Dict[str, str]]: Lista de diccionarios con los datos del CSV
    """
    if not os.path.exists(ruta):
        return []
    with open(ruta, "r", encoding="utf-8") as f:
        lineas = [l.rstrip("\n") for l in f.readlines() if l.strip() != ""]
    if not lineas:
        return []
    encabezado = [c.strip() for c in lineas[0].split(",")]
    filas = []
    for ln in lineas[1:]:
        valores = [v.strip() for v in ln.split(",")]
        while len(valores) < len(encabezado):
            valores.append("")
        filas.append(dict(zip(encabezado, valores)))
    return filas


def guardar_citas_csv(ruta_csv, citas):
    """
    Guarda las citas en formato CSV.
    Args:
        ruta_csv (str): Ruta al archivo CSV
        citas (list): Lista de diccionarios con las citas
    Returns:
        bool: True si se guardó correctamente
    """
    if not citas:
        # Si no hay citas, crear archivo vacío con encabezados
        with open(ruta_csv, 'w', encoding='utf-8', newline='') as f:
            writer = _csv.DictWriter(f, fieldnames=[
                'id',
                'documento_paciente',
                'documento_medico',
                'fecha',
                'hora',
                'motivo',
                'estado'])
            writer.writeheader()
        return True

    try:
        # Obtener todos los campos posibles
        campos = []
        for cita in citas:
            for k in cita.keys():
                if k not in campos and not k.startswith("_"):
                    campos.append(k)

        # Asegurar orden de campos comunes
        campos_ordenados = [
            'id',
            'documento_paciente',
            'documento_medico',
            'fecha', 'hora',
            'motivo',
            'estado']
        for c in campos:
            if c not in campos_ordenados:
                campos_ordenados.append(c)

        with open(ruta_csv, 'w', encoding='utf-8', newline='') as f:
            writer = _csv.DictWriter(f, fieldnames=campos_ordenados)
            writer.writeheader()
            # quitar campos internos antes de escribir
            filas = []
            for c in citas:
                row = {k: v for k, v in c.items() if not k.startswith("_")}
                filas.append(row)
            writer.writerows(filas)
        return True
    except Exception as e:
        console.print(f"[red]Error al guardar CSV: {e}[/red]")
        return False

# ---------------------------------
# FECHAS: normalizar
# ---------------------------------
def normalizar_fecha(fecha_str):
    """
    Intenta normalizar una fecha a formato YYYY-MM-DD.
    Si no puede parsear, devuelve la cadena original.
    Soporta formatos comunes: YYYY-MM-DD, DD/MM/YYYY, DD-MM-YYYY, YYYY/MM/DD.
    """
    if not fecha_str:
        return ""
    fecha_str = fecha_str.strip()
    formatos = ["%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%Y/%m/%d", "%Y-%d-%m"]
    for fmt in formatos:
        try:
            dt = datetime.strptime(fecha_str, fmt)
            return dt.strftime("%Y-%m-%d")
        except Exception:
            continue
    # si no pudo, intentar heurística: si contiene '/' y patrón dd/mm/yyyy invert
    m = re.match(r"(\d{1,2})[\/\-](\d{1,2})[\/\-](\d{2,4})", fecha_str)
    if m:
        d, mo, y = m.groups()
        if len(y) == 2:
            y = "20" + y
        try:
            dt = datetime(int(y), int(mo), int(d))
            return dt.strftime("%Y-%m-%d")
        except Exception:
            pass
    # fallback: devolver original (no normalizada)
    return fecha_str

# ---------------------------------
# CARGAR / ELIMINAR CITAS (JSON + CSV juntos)
# ---------------------------------
def cargar_citas(ruta_base="data/citas"):
    """
    Carga citas desde JSON y CSV, las fusiona y retorna la lista combinada.
    Cada cita contiene el campo interno "_source" con valor "json" o "csv".
    Args:
        ruta_base (str): Ruta base sin extensión
    Returns:
        list: lista de citas combinadas
    """
    ruta_json = ruta_base + ".json"
    ruta_csv = ruta_base + ".csv"

    citas_comb = []

    # JSON
    if os.path.exists(ruta_json):
        try:
            j = cargar_json(ruta_json)
            if isinstance(j, list):
                for c in j:
                    c = dict(c)  # copia
                    # normalizar fecha si existe
                    raw_fecha = c.get("fecha", "")
                    c["_original_fecha"] = raw_fecha
                    c["fecha"] = normalizar_fecha(raw_fecha) if raw_fecha else ""
                    c["_source"] = "json"
                    citas_comb.append(c)
        except Exception:
            pass

    # CSV
    if os.path.exists(ruta_csv):
        try:
            cvs = cargar_csv_simple(ruta_csv)
            for c in cvs:
                c = dict(c)  # copia
                raw_fecha = c.get("fecha", "")
                c["_original_fecha"] = raw_fecha
                c["fecha"] = normalizar_fecha(raw_fecha) if raw_fecha else ""
                c["_source"] = "csv"
                citas_comb.append(c)
        except Exception:
            pass

    return citas_comb

def eliminar_cita_por_id(id_cita, ruta_base="data/citas"):
    """
    Elimina la cita con id `id_cita` buscando tanto en JSON como en CSV.
    Si existe en ambos, elimina de ambos (retorna info de dónde fue eliminada).
    Args:
        id_cita (str)
        ruta_base (str)
    Returns:
        dict: {'json': bool, 'csv': bool} indicando si se eliminó en cada formato
    """
    id_cita = str(id_cita)
    ruta_json = ruta_base + ".json"
    ruta_csv = ruta_base + ".csv"
    resultado = {"json": False, "csv": False}

    # JSON
    if os.path.exists(ruta_json):
        try:
            citas = cargar_json(ruta_json) or []
            citas_n = [c for c in citas if str(c.get("id", "")) != id_cita]
            if len(citas_n) != len(citas):
                guardar_json(ruta_json, citas_n)
                resultado["json"] = True
        except Exception:
            pass

    # CSV
    if os.path.exists(ruta_csv):
        try:
            cvs = cargar_csv_simple(ruta_csv) or []
            cvs_n = [c for c in cvs if str(c.get("id", "")) != id_cita]
            if len(cvs_n) != len(cvs):
                guardar_citas_csv(ruta_csv, cvs_n)
                resultado["csv"] = True
        except Exception:
            pass

    return resultado

# ============================================================
# MOSTRAR TABLA DE CITAS (se mantiene la versión genérica)
# ============================================================

def mostrar_tabla_generica(lista, columnas, titulo="Tabla"):
    """
        Muestra una tabla genérica con Rich.
    """
    if not lista:
        console.print(Panel
                    ("[bold red]⚠ No hay datos para mostrar.[/bold red]",
                    border_style="red")
                    )
        return

    tabla = Table(
        title=titulo, show_lines=True, box=box.SIMPLE_HEAVY, border_style="cyan")
    for col in columnas:
        tabla.add_column(col, style="bold")

    for item in lista:
        fila = [str(item.get(col.lower(), "")) for col in columnas]
        tabla.add_row(*fila)
    console.print(tabla)

# ---------------------------------
# MOSTRAR TABLA DE CITAS (NO CALENDAR)
# ---------------------------------
def mostrar_tabla_citas(
    citas,
    titulo="📋 Lista de Citas"
):
    """
    Muestra las citas médicas con formato visual enriquecido.
    Ahora puede recibir citas ya fusionadas (tienen _source).
    """

    if not citas:
        console.print(Panel
                    ("[bold red]⚠ No hay citas registradas.[/bold red]",
                    border_style="red")
                    )
        return

    tabla = Table(
        title=f"[bold bright_white]{titulo}[/bold bright_white]",
        title_style="bold white on dark_green",
        header_style="bold white on #007ACC",
        show_lines=True,
        box=box.ROUNDED,
        border_style="bright_blue"
    )

    tabla.add_column("🆔 ID", justify="center", style="bold yellow")
    tabla.add_column("👤 Paciente", style="bright_cyan")
    tabla.add_column("🩺 Médico", style="bright_magenta")
    tabla.add_column("📅 Fecha", justify="center", style="bright_green")
    tabla.add_column("⏰ Hora", justify="center", style="bright_yellow")
    tabla.add_column("💬 Motivo", style="white")
    tabla.add_column("📁 Origen", justify="center", style="white")
    tabla.add_column("📌 Estado", justify="center", style="bold")

    for idx, c in enumerate(citas, start=1):
        # Usar los nombres de campos correctos del modelo
        doc_paciente = c.get("documento_paciente", "")
        doc_medico = c.get("documento_medico", "")

        nombre_paciente = obtener_nombre_por_documento("data/pacientes", doc_paciente)
        nombre_medico = obtener_nombre_por_documento("data/medicos", doc_medico)

        estado = str(c.get("estado", "Desconocido")).capitalize()
        if estado.lower() == "pendiente":
            color_estado = "[bold yellow]🕒 Pendiente[/bold yellow]"
        elif estado.lower() in ("completada", "realizada"):
            color_estado = "[bold green]✅ Completada[/bold green]"
        elif estado.lower() == "cancelada":
            color_estado = "[bold red]❌ Cancelada[/bold red]"
        else:
            color_estado = f"[dim]{estado}[/dim]"

        origen = c.get("_source", "desconocido").upper()

        tabla.add_row(
            str(c.get('id', '')),
            nombre_paciente,
            nombre_medico,
            c.get('fecha', ''),
            c.get('hora', ''),
            c.get('motivo', ''),
            origen,
            color_estado
        )

    console.print(
        Panel(
            tabla,
            title="💠 [bold cyan]Agenda Médica[/bold cyan]",
            subtitle="[green]💡 Usa ↑ ↓ para navegar y Enter para seleccionar[/green]",
            border_style="bright_cyan",
            padding=(1, 2)
        )
    )

# ---------------------------------
# CALENDARIO INTERACTIVO
# ---------------------------------


def mostrar_calendario_interactivo(ruta_citas="data/citas"):
    """
    Estructura y muestra un calendario interactivo de citas médicas.
    Soporta tanto JSON como CSV (fusionando ambos).
    """
    hoy = datetime.now()
    año, mes = hoy.year, hoy.month

    while True:
        limpiar()

        citas = cargar_citas(ruta_citas)

        dias_citas = set()
        for c in citas:
            fecha_str = c.get("fecha", "")
            if not fecha_str:
                continue
            try:
                f = datetime.strptime(fecha_str, "%Y-%m-%d")
                if f.year == año and f.month == mes:
                    dias_citas.add(f.day)
            except Exception:
                continue

        nombre_mes = calendar.month_name[mes]
        citas_este_mes = 0
        for c in citas:
            fecha_str = c.get("fecha", "")
            try:
                f = datetime.strptime(fecha_str, "%Y-%m-%d")
                if f.year == año and f.month == mes:
                    citas_este_mes += 1
            except Exception:
                continue

        formatos_presentes = sorted(list(
            {c.get("_source", "") for c in citas if c.get("_source")}))
        formato_display = "+".join(
            [f.upper() for f in formatos_presentes]
            ) if formatos_presentes else "Ninguno"
        icono_formato = "🧾" if "json" in formatos_presentes and "csv" not in formatos_presentes else ("📄"
            if "csv" in formatos_presentes and "json" not in formatos_presentes
            else "🧾📄" if formatos_presentes else "❓")

        panel_titulo = Panel.fit(
            f"📅 [bold bright_cyan]{nombre_mes} {año}[/bold bright_cyan]\n"
            f"[dim]Citas este mes: {citas_este_mes} | Formato: {
                icono_formato} {formato_display}[/dim]",
            border_style="bright_green",
            box=ROUNDED,
            padding=(0, 4)
        )
        console.print(Align.center(panel_titulo))

        dias_semana = ["L", "M", "X", "J", "V", "S", "D"]
        encabezado = "  ".join(f"[bold yellow]{d}[/bold yellow]" for d in dias_semana)
        console.print(Align.center(encabezado))

        cal = calendar.monthcalendar(año, mes)

        for semana in cal:
            linea = ""
            for dia in semana:
                if dia == 0:
                    linea += "    "
                elif dia == hoy.day and mes == hoy.month and año == hoy.year:
                    linea += f"[white on bright_green]{dia:2d}[/white on bright_green]"
                elif dia in dias_citas:
                    linea += f"[bold bright_red]{dia:2d}[/bold bright_red]  "
                else:
                    linea += f"[white]{dia:2d}[/white]  "
            console.print(Align.center(linea))

        controles = (
            "⬅️  [cyan]Anterior[/cyan]    "
            "➡️  [cyan]Siguiente[/cyan]    "
            "🔍  [cyan]Enter = Ver día[/cyan]    "
            "📊  [cyan]S = Estadísticas[/cyan]    "
            "❌  [red]Q = Salir[/red]"
        )

        console.print(
            Align.center(
                Panel(
                    Text.from_markup(controles),
                    border_style="dim",
                    box=ROUNDED,
                    padding=(0, 2)
                )
            )
        )

        tecla = readchar.readkey()

        if tecla == readchar.key.RIGHT:
            mes += 1
            if mes > 12:
                mes = 1
                año += 1

        elif tecla == readchar.key.LEFT:
            mes -= 1
            if mes < 1:
                mes = 12
                año -= 1

        elif tecla.lower() == 'q':
            return

        elif tecla.lower() == 's':
            limpiar()
            console.print(Panel(
            "[bold magenta]📊 Mostrando estadísticas"
            " de citas por médico...[/bold magenta]",
            border_style="magenta"))
            try:
                estadisticas_citas_por_medico()
            except Exception as e:
                console.print(f"[red]Error generando estadísticas: {e}[/red]")
            console.input("\n[cyan]Presiona Enter para volver[/cyan]")

        elif tecla == readchar.key.ENTER:
            dia_str = console.input(
                "\n[cyan]Ingrese el número de día a ver (ej: 15): [/cyan]")
            if dia_str.isdigit():
                dia = int(dia_str)
                if 1 <= dia <= 31:
                    mostrar_citas_por_dia(año, mes, dia, ruta_citas)
                else:
                    console.print("[red]❌ Día inválido.[/red]")
                    time.sleep(0.8)
            else:
                console.print("[red]❌ Entrada no válida.[/red]")
                time.sleep(0.8)


def mostrar_citas_por_dia(año, mes, dia, ruta_citas="data/citas"):
    """
    Muestra las citas de un día específico y permite cancelar.
    Soporta JSON + CSV fusionados.
    """
    fecha = f"{año:04d}-{mes:02d}-{dia:02d}"

    citas = cargar_citas(ruta_citas)
    citas_dia = []
    for c in citas:
        if c.get("fecha") == fecha:
            citas_dia.append(c)

    limpiar()
    if not citas_dia:
        console.print(f"[yellow]No hay citas para el {fecha}[/yellow]")
        console.input("[cyan]Enter para volver...[/cyan]")
        return



    tabla = Table(
        title=f"📅 Citas del {fecha}",
        show_lines=True,
        box=box.ROUNDED,
        border_style="bright_blue"
    )

    tabla.add_column("Índice", justify="center", style="dim")
    tabla.add_column("🆔 ID", justify="center", style="bold yellow")
    tabla.add_column("👤 Paciente", style="bright_cyan")
    tabla.add_column("🩺 Médico", style="bright_magenta")
    tabla.add_column("⏰ Hora", justify="center", style="bright_yellow")
    tabla.add_column("💬 Motivo", style="white")
    tabla.add_column("📁 Origen", justify="center", style="white")
    tabla.add_column("📌 Estado", justify="center", style="bold")

    for idx, c in enumerate(citas_dia, start=1):
        nombre_paciente = obtener_nombre_por_documento(
            "data/pacientes",
            c.get("documento_paciente",
                ""))
        nombre_medico = obtener_nombre_por_documento(
            "data/medicos",
            c.get("documento_medico",
                ""))
        estado = str(c.get("estado", "Desconocido")).capitalize()
        if estado.lower() == "pendiente":
            color_estado = "[bold yellow]🕒 Pendiente[/bold yellow]"
        elif estado.lower() in ("completada", "realizada"):
            color_estado = "[bold green]✅ Completada[/bold green]"
        elif estado.lower() == "cancelada":
            color_estado = "[bold red]❌ Cancelada[/bold red]"
        else:
            color_estado = f"[dim]{estado}[/dim]"

        origen = c.get("_source", "desconocido").upper()

        tabla.add_row(
            str(idx),
            str(c.get("id", "")),
            nombre_paciente,
            nombre_medico,
            c.get("hora", ""),
            c.get("motivo", ""),
            origen,
            color_estado
        )

    console.print(tabla)

    console.print(
        "\n[cyan]Acciones:[/cyan] Ingrese [yellow]ID de cita[/yellow] para cancelar "
        "(se mostrará el origen), o [cyan]Enter[/cyan] para volver."
    )
    opcion = console.input(
        "[cyan]Ingrese ID de cita a cancelar (o Enter): [/cyan]").strip()

    if opcion == "":
        return

    # Buscar coincidencias por id en las citas del día
    matches = [c for c in citas_dia if str(c.get("id")) == opcion]
    if not matches:
        console.print("[red]❌ ID no encontrado en las citas de este día.[/red]")
        time.sleep(0.8)
        return

    # Si hay múltiples coincidencias (mismo id en ambos archivos), pedir elegir cuál
    cita_seleccionada = None
    if len(matches) == 1:
        cita_seleccionada = matches[0]
    else:
        console.print(
            "[yellow]Se encontraron múltiples citas con ese ID"
            " en diferentes orígenes:[/yellow]")
        for i, c in enumerate(matches, start=1):
            console.print(
                f"[{i}] ID: {c.get(
                    'id')} | Origen: {c.get(
                        '_source')} | Hora: {c.get(
                            'hora')} | Motivo: {c.get(
                                'motivo')}")
        sel = console.input(
            "[cyan]Ingrese el número de la cita a cancelar: [/cyan]").strip()
        if sel.isdigit():
            sel_i = int(sel)
            if 1 <= sel_i <= len(matches):
                cita_seleccionada = matches[sel_i - 1]
            else:
                console.print("[red]Selección inválida.[/red]")
                time.sleep(0.8)
                return
        else:
            console.print("[red]Entrada inválida.[/red]")
            time.sleep(0.8)
            return

    # Detalles de la cita seleccionada
    console.print(Panel.fit(
        f"[bold yellow]Cita a cancelar:[/bold yellow]\n"
        f"🆔 ID: {cita_seleccionada.get('id')}\n"
        f"📅 Fecha: {cita_seleccionada.get('fecha')}\n"
        f"⏰ Hora: {cita_seleccionada.get('hora')}\n"
        f"💬 Motivo: {cita_seleccionada.get('motivo')}\n"
        f"📁 Origen: {cita_seleccionada.get('_source')}",
        border_style="yellow"
    ))

    # Confirmar cancelación
    if Confirm.ask("¿Está seguro de cancelar esta cita?", default=False):
        res = eliminar_cita_por_id(cita_seleccionada.get("id"), ruta_citas)
        eliminado_en = [k for k, v in res.items() if v]
        if eliminado_en:
            console.print(Panel(
                f"[bold green]✅ Cita eliminada en: {', '.join(
                    eliminado_en).upper()}[/bold green]",
                border_style="green"
            ))
            try:
                estadisticas_citas_por_medico()
            except Exception:
                pass
        else:
            console.print(Panel(
                "[bold red]❌ No se pudo eliminar la cita"
                " (archivo no encontrado o error).[/bold red]",
                border_style="red"
            ))
    else:
        console.print("[yellow]Operación cancelada por el usuario.[/yellow]")

    time.sleep(1.2)

# ---------------------------------
# SELECTOR INTERACTIVO
# ---------------------------------

def selector_interactivo(titulo, opciones):
    """
        Estructura un selector interactivo usando readchar.
    """
    seleccion = 0
    while True:
        limpiar()
        console.print(Panel(f"[bold cyan]{titulo}[/bold cyan]"))
        for i, opt in enumerate(opciones):
            prefix = "👉 " if i == seleccion else "   "
            if "Salir" in opt or "🚪" in opt:
                estilo = "reverse bold red" if i == seleccion else "bold red"
            else:
                estilo = "reverse bold green" if i == seleccion else None
            console.print(prefix + opt, style=estilo)

        tecla = readchar.readkey()
        if tecla == readchar.key.UP:
            seleccion = (seleccion - 1) % len(opciones)
        elif tecla == readchar.key.DOWN:
            seleccion = (seleccion + 1) % len(opciones)
        elif tecla == readchar.key.ENTER:
            return seleccion

# ---------------------------------
# VISTA PRINCIPAL
# ---------------------------------

def mostrar_menu_simple():
    limpiar()

    opciones_tabla = Table(show_header=False, box=box.SIMPLE_HEAVY)
    opciones_tabla.add_row(
        "[bold green][1][/bold green] 👤 Gestionar Pacientes"
        )
    opciones_tabla.add_row(
        "[bold green][2][/bold green] 🩺 Gestionar Médicos"
        )
    opciones_tabla.add_row(
        "[bold green][3][/bold green] 📅 Agendar / Ver Citas"
        )
    opciones_tabla.add_row(
        "[bold green][4][/bold green] 📊 Ver Calendario de Citas (Inter.)"
        )
    opciones_tabla.add_row(
        "[bold green][5][/bold green] 📈 Estadísticas por médico"
        )
    opciones_tabla.add_row(
        "[/] [bold red][0][/bold red] 🚪 Salir"
        )

    console.print(opciones_tabla)
    console.print("[yellow]───────────────────────────────────────────────[/yellow]")

    opcion = console.input(
        "[bold cyan]Seleccione una opción (o use flechas con Enter): [/bold cyan]"
        )
    return opcion


def vista_principal():
    """
        Menu principal interactivo.
    """
    opciones = [
        "👤 Gestionar Pacientes",
        "🩺 Gestionar Médicos",
        "📅 Agendar / Ver Citas",
        "📊 Ver Calendario de Citas (Interactivo)",
        "📈 Estadísticas por médico",
        "🚪 Salir"
    ]
    while True:
        try:
            indice = selector_interactivo(
                "BIENVENIDO AL SISTEMA DE CITAS MÉDICAS"
                "\n🏥 Menú Principal"
                "\n(usa ↑ ↓ + Enter \npara navegar dentro de las opciones)",
                opciones
            )
        except Exception:
            opcion = mostrar_menu_simple()
            if opcion == "0":
                indice = 5
            elif opcion in ["1", "2", "3", "4", "5"]:
                indice = int(opcion) - 1
            else:
                console.print("[bold red]Opción no válida.[/bold red]")
                time.sleep(0.8)
                continue

        if indice == 0:
            animacion_carga("Abriendo módulo de pacientes...")
            try:
                navegacion.ir_a_menu_pacientes()
            except Exception as e:
                console.log(e)
                console.print(
                    f"[red]Error al cargar módulo de pacientes:[/red] {e}"
                    )
                console.input("Enter para volver...")
        elif indice == 1:
            animacion_carga("Abriendo módulo de médicos...")
            try:
                navegacion.ir_a_menu_medicos()
            except Exception as e:
                console.log(e)
                console.print(
                            "[yellow]Módulo de médicos no encontrado. "
                            "(Placeholder)[/yellow]"
                            )
                console.input("Enter para volver...")
        elif indice == 2:
            animacion_carga("Abriendo módulo de citas...")
            try:
                navegacion.ir_a_menu_citas()
            except Exception as e:
                console.log(e)
                console.print(
                    "[yellow]Módulo de citas no encontrado. "
                    "(Placeholder)[/yellow]"
                    )
                console.input("Enter para volver...")
        elif indice == 3:
            mostrar_calendario_interactivo()

        elif indice==4:
            animacion_carga("Abriendo módulo de estadísticas...")
            try:
                stats = estadisticas_citas_por_medico()
                if not stats:
                    console.print(Panel(
                        "[bold yellow]⚠️ No hay estadísticas del médico.[/bold yellow]",
                        border_style="yellow"
                    ))
                    console.input("\n[cyan]Presiona Enter para volver al menú[/cyan]")
                else:
                    console.input("\n[cyan]Presiona Enter para volver al menú[/cyan]")
            except Exception as e:
                console.log(e)
                console.input("Enter para volver...")
        elif indice==5:
            console.print(
                "\n[bold red]Saliendo del sistema...[/bold red]"
                )
            time.sleep(0.8)
            break
        else:
            console.print(
                "[bold red]Opción no válida.[/bold red]"
                )
            time.sleep(0.6)

# ---------------------------------
# FUNCIÓN DE DEBUG (OPCIONAL)
# ---------------------------------
def verificar_citas_debug():
    """
    Función de debugging para verificar que las citas se estén cargando correctamente.
    Ejecutar solo para pruebas.
    """
    ruta = "data/citas.json"
    if os.path.exists(ruta):
        with open(ruta, 'r', encoding='utf-8') as f:
            citas = json.load(f)

        console.print(Panel(f"[bold green]✅ Archivo encontrado: {ruta}[/bold green]"))
        console.print(f"[cyan]Total de citas:[/cyan] {len(citas)}")

        if citas:
            console.print("\n[yellow]Primera cita como ejemplo:[/yellow]")
            console.print(json.dumps(citas[0], indent=2, ensure_ascii=False))

            console.print("\n[yellow]Campos disponibles:[/yellow]")
            console.print(list(citas[0].keys()))

            console.print("\n[yellow]Fechas encontradas:[/yellow]")
            for c in citas[:5]:  # Mostrar máximo 5
                console.print(f"  - ID {c.get('id')}: {c.get('fecha')}")
    else:
        console.print(Panel(f"[bold red]❌ Archivo no encontrado: {ruta}[/bold red]"))

    console.input("\n[cyan]Presiona Enter para continuar...[/cyan]")

if __name__ == "__main__":
    verificar_citas_debug()
    vista_principal()
