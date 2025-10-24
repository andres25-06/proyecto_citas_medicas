# Vista/vista_principal.py 

from collections import Counter
from datetime import datetime
import calendar
import csv
import json
import os
import re
import time

import readchar
from rich import box
from rich.align import Align
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.box import ROUNDED

# ---------------------------------
# Inicialización
# ---------------------------------
console = Console()

# ---------------------------------
# UTILIDADES
# ---------------------------------

def limpiar():
    """Limpia la terminal (Windows / Unix)."""
    os.system("cls" if os.name == "nt" else "clear")


def animacion_carga(mensaje="Cargando..."):
    """Animación simple de carga (compatible con terminales)."""
    limpiar()
    console.print(f"[cyan]{mensaje}[/cyan]")
    for _ in range(18):
        console.print('.', end='')
        time.sleep(0.02)
    console.print('\n')


def escribir_mensaje(texto, velocidad=0.01, color="magenta"):
    """Efecto 'typing' usando Rich. Usa console.print con end='' para no crear saltos extra."""
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
    if not os.path.exists(ruta):
        return []
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def guardar_json(ruta, datos):
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)


def cargar_csv_simple(ruta):
    """Carga CSV simple asumiendo encabezado en la primera línea y comas como separador.
    Devuelve una lista de diccionarios.
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


def cargar_datos(filepath):
    """Carga datos desde JSON o CSV. Mantiene compatibilidad con otras vistas que lo usen."""
    if not os.path.exists(filepath):
        return []
    try:
        if filepath.endswith('.json'):
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        elif filepath.endswith('.csv'):
            with open(filepath, 'r', encoding='utf-8') as f:
                return list(csv.DictReader(f))
    except Exception as e:
        console.print(f"[red]Error al cargar {filepath}: {e}[/red]")
    return []

# ---------------------------------
# BÚSQUEDAS / UTILIDADES DE NOMBRE
# ---------------------------------

def obtener_nombre_por_documento(lista, documento):
    """Busca nombre y apellidos en una lista de dicts por campo 'documento'."""
    for item in lista:
        if str(item.get("documento") or item.get("id") or "").strip() == str(documento).strip():
            nombre = item.get("nombres", "")
            apellidos = item.get("apellidos", "")
            return f"{nombre} {apellidos}".strip() or "Sin nombre"
    return "Desconocido"


def buscador(lista, campo, termino):
    patron = re.compile(re.escape(termino), re.IGNORECASE)
    return [item for item in lista if patron.search(str(item.get(campo, "")))]

# ---------------------------------
# MOSTRAR TABLA DE CITAS
# ---------------------------------

def mostrar_tabla_citas(
    citas,
    ruta_pacientes="data/pacientes.csv",
    ruta_medicos="data/medicos.csv",
    titulo="📋 Lista de Citas"
):
    pacientes = cargar_datos(ruta_pacientes)
    medicos = cargar_datos(ruta_medicos)

    if not citas:
        console.print(Panel("[bold red]⚠ No hay citas registradas.[/bold red]", border_style="red"))
        return

    tabla = Table(
        title=f"[bold bright_white]{titulo}[/bold bright_white]",
        title_style="bold white on dark_green",
        header_style="bold white on #007ACC",
        show_lines=True,
        box=box.ROUNDED,
        border_style="bright_blue"
    )

    tabla.add_column("🆔 ID", style="bold yellow", justify="center")
    tabla.add_column("👤 Paciente", style="bright_cyan")
    tabla.add_column("🩺 Médico", style="bright_magenta")
    tabla.add_column("📅 Fecha", justify="center", style="bright_green")
    tabla.add_column("⏰ Hora", justify="center", style="bright_yellow")
    tabla.add_column("💬 Motivo", style="white")
    tabla.add_column("📌 Estado", justify="center", style="bold")

    for idx, c in enumerate(citas, start=1):
        doc_paciente = c.get("documento_paciente") or c.get("id_paciente") or c.get("paciente")
        doc_medico = c.get("documento_medico") or c.get("id_medico") or c.get("medico")

        nombre_paciente = obtener_nombre_por_documento(pacientes, doc_paciente)
        nombre_medico = obtener_nombre_por_documento(medicos, doc_medico)

        estado = str(c.get("estado", "Desconocido")).capitalize()
        if estado.lower() == "pendiente":
            color_estado = "[bold yellow]🕒 Pendiente[/bold yellow]"
        elif estado.lower() in ("completada", "completado", "realizada"):
            color_estado = "[bold green]✅ Completada[/bold green]"
        elif estado.lower() == "cancelada":
            color_estado = "[bold red]❌ Cancelada[/bold red]"
        else:
            color_estado = f"[dim]{estado}[/dim]"

        fila_color = "white" if idx % 2 == 0 else "bright_white"

        tabla.add_row(
            f"[{fila_color}]{c.get('id', '')}[/{fila_color}]",
            f"[{fila_color}]{nombre_paciente}[/{fila_color}]",
            f"[{fila_color}]{nombre_medico}[/{fila_color}]",
            f"[{fila_color}]{c.get('fecha', '')}[/{fila_color}]",
            f"[{fila_color}]{c.get('hora', '')}[/{fila_color}]",
            f"[{fila_color}]{c.get('motivo', '')}[/{fila_color}]",
            color_estado
        )

    panel = Panel(
        tabla,
        title="💠 [bold cyan]Agenda Médica[/bold cyan]",
        subtitle="[green]💡 Usa ↑ ↓ para navegar y Enter para seleccionar[/green]",
        border_style="bright_cyan",
        padding=(1, 2)
    )
    console.print(panel)

# ---------------------------------
# ENRIQUECER CITAS (añadir nombres si hay ids)
# ---------------------------------

def enriquecer_citas(citas, ruta_pacientes="data/pacientes.csv", ruta_medicos="data/medicos.csv"):
    pacientes = cargar_csv_simple(ruta_pacientes)
    medicos = cargar_csv_simple(ruta_medicos)
    map_p = {p.get("id_paciente") or p.get("id") or p.get("documento"): p.get("nombre") or p.get("nombres") for p in pacientes}
    map_m = {m.get("id_medico") or m.get("id") or m.get("documento"): m.get("nombre") or m.get("nombres") for m in medicos}
    for c in citas:
        c["paciente_nombre"] = map_p.get(c.get("id_paciente") or c.get("documento_paciente"), c.get("id_paciente") or c.get("documento_paciente"))
        c["medico_nombre"] = map_m.get(c.get("id_medico") or c.get("documento_medico"), c.get("id_medico") or c.get("documento_medico"))
    return citas

# ---------------------------------
# CALENDARIO INTERACTIVO
# ---------------------------------

def mostrar_calendario_interactivo(ruta_citas="data/citas.json"):
    hoy = datetime.now()
    año, mes = hoy.year, hoy.month

    while True:
        limpiar()
        citas = cargar_json(ruta_citas)

        dias_citas = set()
        for c in citas:
            try:
                f = datetime.strptime(c.get("fecha", ""), "%Y-%m-%d")
                if f.year == año and f.month == mes:
                    dias_citas.add(f.day)
            except Exception:
                continue

        nombre_mes = calendar.month_name[mes]
        panel_titulo = Panel.fit(
            f"📅 [bold bright_cyan]{nombre_mes} {año}[/bold bright_cyan]",
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
                else:
                    if dia == hoy.day and mes == hoy.month and año == hoy.year:
                        linea += f"[white on bright_green]{dia:2d}[/white on bright_green]  "
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
            console.print(Panel("[bold magenta]📊 Mostrando estadísticas de citas por médico...[/bold magenta]", border_style="magenta"))
            estadisticas_citas_por_medico()
            console.input("\n[cyan]Presiona Enter para volver[/cyan]")

        elif tecla == readchar.key.ENTER:
            dia_str = console.input("\n[cyan]Ingrese el número de día a ver (ej: 15): [/cyan]")
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

# ---------------------------------
# MOSTRAR / CANCELAR CITAS POR DÍA
# ---------------------------------

def mostrar_citas_por_dia(año, mes, dia, ruta_citas="data/citas.json"):
    fecha = f"{año:04d}-{mes:02d}-{dia:02d}"
    citas = cargar_json(ruta_citas)
    citas_dia = [c for c in citas if c.get("fecha") == fecha]
    citas_dia = enriquecer_citas(citas_dia)
    limpiar()
    if not citas_dia:
        console.print(f"[yellow]No hay citas para el {fecha}[/yellow]")
        console.input("[cyan]Enter para volver...[/cyan]")
        return

    mostrar_tabla_citas(citas_dia, titulo=f"Citas del {fecha}")
    console.print("\n[c]Acciones:[/c] [cyan]id_cita[/cyan] para cancelar, Enter para volver.")
    opcion = console.input("[cyan]Ingrese ID de cita a cancelar (o Enter): [/cyan]").strip()
    if opcion == "":
        return

    citas_all = cargar_json(ruta_citas)
    if not any(str(c.get("id")) == opcion for c in citas_all):
        console.print("[red]ID no encontrado.[/red]")
        time.sleep(0.8)
        return

    citas_all = [c for c in citas_all if str(c.get("id")) != opcion]
    guardar_json(ruta_citas, citas_all)
    console.print("[green]Cita cancelada con éxito.[/green]")
    time.sleep(0.8)

# ---------------------------------
# ESTADÍSTICAS
# ---------------------------------

def estadisticas_citas_por_medico(ruta_medicos="data/medicos.csv", ruta_citas="data/citas.json"):
    limpiar()
    medicos = cargar_csv_simple(ruta_medicos)
    citas = cargar_json(ruta_citas)

    contador = Counter([c.get("documento_medico") or c.get("id_medico") for c in citas])

    titulo = Text("📊 Estadísticas de Citas por Médico", style="bold cyan")
    console.print(Panel(titulo, border_style="cyan", box=ROUNDED, padding=(0, 2)))

    tabla = Table(
        show_lines=True,
        box=ROUNDED,
        header_style="bold white on blue",
        title_style="bold cyan",
        pad_edge=False
    )
    tabla.add_column("🩺 Médico", justify="left", style="bold white")
    tabla.add_column("💼 Especialidad", justify="left", style="white")
    tabla.add_column("📅 Total Citas", justify="center", style="bold yellow")

    for m in medicos:
        id_medico = str(m.get("documento") or m.get("id") or "")
        nombre = f"{m.get('nombres', '')} {m.get('apellidos', '')}".strip() or "Desconocido"
        especialidad = m.get("especialidad", "—")
        total = contador.get(id_medico, 0)

        color_citas = "green" if total > 0 else "dim"
        tabla.add_row(nombre, especialidad, f"[{color_citas}]{total}[/{color_citas}]")

    panel = Panel(
        tabla,
        title="[bold cyan]Resumen General[/bold cyan]",
        border_style="blue",
        box=ROUNDED,
        padding=(1, 2)
    )
    console.print(panel, justify="left")
    console.print("\n[dim cyan]Presiona Enter para volver...[/dim cyan]")
    console.input()

# ---------------------------------
# SELECTOR INTERACTIVO
# ---------------------------------

def selector_interactivo(titulo, opciones):
    """Permite navegar con flechas ↑ ↓ y seleccionar con Enter.
    Devuelve el índice seleccionado.
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
    opciones_tabla.add_row("[bold green][1][/bold green] 👤 Gestionar Pacientes")
    opciones_tabla.add_row("[bold green][2][/bold green] 🩺 Gestionar Médicos")
    opciones_tabla.add_row("[bold green][3][/bold green] 📅 Agendar / Ver Citas")
    opciones_tabla.add_row("[bold green][4][/bold green] 📊 Ver Calendario de Citas (Inter.)")
    opciones_tabla.add_row("[bold green][5][/bold green] 📈 Estadísticas por médico")
    opciones_tabla.add_row("[/] [bold red][0][/bold red] 🚪 Salir")

    console.print(opciones_tabla)
    console.print("[yellow]───────────────────────────────────────────────[/yellow]")

    opcion = console.input("[bold cyan]Seleccione una opción (o use flechas con Enter): [/bold cyan]")
    return opcion


def vista_principal():
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
                "BIENVENIDO AL SISTEMA DE CITAS MÉDICAS\n🏥 Menú Principal (usa ↑ ↓ + Enter \npara navegar dentro de las opciones)",
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
                from Vista.vista_paciente import main_vista_pacientes
                main_vista_pacientes()
            except Exception as e:
                console.print(f"[red]Error al cargar módulo de pacientes:[/red] {e}")
                console.input("Enter para volver...")

        elif indice == 1:
            animacion_carga("Abriendo módulo de médicos...")
            try:
                from Vista.vista_medico import main_vista_medicos
                main_vista_medicos()
            except Exception:
                console.print("[yellow]Módulo de médicos no encontrado. (Placeholder)[/yellow]")
                console.input("Enter para volver...")

        elif indice == 2:
            animacion_carga("Abriendo módulo de citas...")
            try:
                from Vista.vista_cita import main_vista_citas
                main_vista_citas()
            except Exception:
                console.print("[yellow]Módulo de citas no encontrado. (Placeholder)[/yellow]")
                console.input("Enter para volver...")

        elif indice == 3:
            mostrar_calendario_interactivo()

        elif indice == 4:
            estadisticas_citas_por_medico()

        elif indice == 5:
            console.print("\n[bold red]Saliendo del sistema...[/bold red]")
            time.sleep(0.8)
            break

        else:
            console.print("[bold red]Opción no válida.[/bold red]")
            time.sleep(0.6)

# ---------------------------------
# EJECUCIÓN DIRECTA (debug / pruebas)
# ---------------------------------
if __name__ == "__main__":
    vista_principal()
