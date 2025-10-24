# Vista/vista_principal.py
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from rich import box
from colorama import init
import os
import time
import json
import calendar
import readchar
from datetime import datetime, timedelta
from collections import Counter
import re


# Inicializa colorama para Windows
init(autoreset=True)

console = Console()

# -------------------- UTILIDADES --------------------
def limpiar():
    """
    Está función limpia la consola dependiendo del sistema operativo.
    
    Args:
        none    
    Returns:
        none
    """
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
    for i in range(18):
        console.print("." , end="", style="cyan")
        time.sleep(0.02)
    console.print("\n")

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
        console.file.flush()
        time.sleep(velocidad)
    console.print()

# -------------------- IO DATOS --------------------
def cargar_json(ruta):
    """
    Carga un archivo JSON y retorna su contenido.
    
    Args:
        ruta (str): Ruta al archivo JSON.
    Returns:
        any: Contenido del archivo JSON.
    """
    if not os.path.exists(ruta):
        return []
    with open(ruta, "r", encoding="utf-8") as f:
        try:
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
    Carga CSV simple asumiendo encabezado en la primera línea y comas como separador.
    
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
        # evitar mismatch de longitud
        while len(valores) < len(encabezado):
            valores.append("")
        filas.append(dict(zip(encabezado, valores)))
    return filas

# -------------------- TABLAS VISUALES --------------------
def mostrar_tabla_citas(citas, titulo="Citas"):
    """
    Estructura y muestra una tabla de citas médicas usando Rich.
    
    Args:
        citas (List[Dict[str, str]]): Lista de diccionarios con los datos de las citas.
        titulo (str): Título de la tabla.
    Returns:
        none
    """
    tabla = Table(title=titulo, show_lines=True, box=box.SIMPLE)
    tabla.add_column("ID Cita", style="bold yellow")
    tabla.add_column("Paciente", style="cyan")
    tabla.add_column("Médico", style="magenta")
    tabla.add_column("Fecha", justify="center")
    tabla.add_column("Hora", justify="center")
    tabla.add_column("Motivo")
    for c in citas:
        tabla.add_row(
            c.get("id_cita", ""),
            c.get("paciente_nombre", c.get("id_paciente", "")),
            c.get("medico_nombre", c.get("id_medico", "")),
            c.get("fecha", ""),
            c.get("hora", ""),
            c.get("motivo_consulta", "")
        )
    console.print(tabla)

def mostrar_tabla_generica(lista, columnas, titulo="Tabla"):
    """
    Estructura y muestra una tabla genérica usando Rich.
    
    Args:
        lista (List[Dict[str, str]]): Lista de diccionarios con los datos
        columnas (List[str]): Lista de nombres de columnas a mostrar.
        titulo (str): Título de la tabla.
    Returns:
        none
    """
    tabla = Table(title=titulo, show_lines=True, box=box.SIMPLE)
    for col in columnas:
        tabla.add_column(col, style="bold")
    for item in lista:
        tabla.add_row(*[str(item.get(c, "")) for c in columnas])
    console.print(tabla)

# -------------------- BUSCADOR --------------------
def buscador(lista, campo, termino):
    """
    Efectúa una búsqueda simple en una lista de diccionarios por un campo específico.
    
    Args:
        lista (List[Dict[str, str]]): Lista de diccionarios donde buscar.
        campo (str): Campo del diccionario donde buscar.
        termino (str): Término a buscar (case insensitive).
    Returns:
        List[Dict[str, str]]: Sublista con los elementos que coinciden con el término.
        
    """
    
    patron = re.compile(re.escape(termino), re.IGNORECASE)
    return [item for item in lista if patron.search(item.get(campo, ""))]

# -------------------- ENRIQUECER CITAS --------------------
def enriquecer_citas(citas, ruta_pacientes="data/pacientes.csv", ruta_medicos="data/medicos.csv"):
    """
    Enriquece las citas añadiendo nombres de pacientes y médicos desde archivos CSV.
    
    Args:
        citas (List[Dict[str, str]]): Lista de diccionarios con los datos de las citas.
        ruta_pacientes (str): Ruta al archivo CSV de pacientes.
        ruta_medicos (str): Ruta al archivo CSV de médicos.
    Returns:
        List[Dict[str, str]]: Lista de citas enriquecidas con nombres.
        
    """
    pacientes = cargar_csv_simple(ruta_pacientes)
    medicos = cargar_csv_simple(ruta_medicos)
    map_p = {p.get("id_paciente"): p.get("nombre") for p in pacientes}
    map_m = {m.get("id_medico"): m.get("nombre") for m in medicos}
    for c in citas:
        c["paciente_nombre"] = map_p.get(c.get("id_paciente"), c.get("id_paciente"))
        c["medico_nombre"] = map_m.get(c.get("id_medico"), c.get("id_medico"))
    return citas

# -------------------- CALENDARIO INTERACTIVO --------------------
def mostrar_calendario_interactivo(ruta_citas="data/citas.json"):
    """
    Estructura y muestra un calendario interactivo de citas médicas.
    
    Args:
        ruta_citas (str): Ruta al archivo JSON donde se almacenan las citas.
    Returns:
        none
        
    """
    hoy = datetime.now()
    año, mes = hoy.year, hoy.month

    while True:
        limpiar()
        citas = cargar_json(ruta_citas)
        # obtener días con citas en el mes/año actual
        dias_citas = set()
        for c in citas:
            try:
                f = datetime.strptime(c["fecha"], "%Y-%m-%d")
                if f.year == año and f.month == mes:
                    dias_citas.add(f.day)
            except Exception:
                continue

        cal = calendar.monthcalendar(año, mes)
        panel_titulo = f"[bold cyan]{calendar.month_name[mes]} {año}[/bold cyan]"
        console.print(Panel(panel_titulo, border_style="bright_blue"))

        # encabezado días (L M X J V S D)
        dias_semana = ["L", "M", "X", "J", "V", "S", "D"]
        encabezado = "  ".join([f"[bold yellow]{d}[/bold yellow]" for d in dias_semana])
        console.print(encabezado)

        for semana in cal:
            linea = ""
            for dia in semana:
                if dia == 0:
                    linea += "    "
                else:
                    # resaltar hoy
                    if dia == hoy.day and mes == hoy.month and año == hoy.year:
                        linea += f"[reverse green]{dia:2d}[/reverse green]  "
                    elif dia in dias_citas:
                        linea += f"[bold red]{dia:2d}[/bold red]  "
                    else:
                        linea += f"{dia:2d}  "
            console.print(linea)

        console.print("\n[cyan]← →[/cyan] cambiar mes  |  [cyan]Enter[/cyan] ver día  |  [cyan]s[/cyan] estadísticas  |  [cyan]q[/cyan] volver")
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
        elif tecla == 'q':
            return
        elif tecla == 's':
            estadisticas_citas_por_medico()
        elif tecla == readchar.key.ENTER:
            # pedir día para ver (más robusto que detectar posición en el calendario)
            dia_str = console.input("[cyan]Ingrese el número de día a ver (ej: 15): [/cyan]")
            if dia_str.isdigit():
                dia = int(dia_str)
                if 1 <= dia <= 31:
                    mostrar_citas_por_dia(año, mes, dia, ruta_citas)
                else:
                    console.print("[red]Día inválido.[/red]")
                    time.sleep(0.8)
            else:
                console.print("[red]Entrada no válida.[/red]")
                time.sleep(0.8)

# -------------------- MOSTRAR / CANCELAR CITAS POR DÍA --------------------
def mostrar_citas_por_dia(año, mes, dia, ruta_citas="data/citas.json"):
    """
    Estructura y muestra las citas de un día específico, permitiendo cancelar.
    
    Args:
        año (int): Año de la fecha a mostrar.
        mes (int): Mes de la fecha a mostrar.
        dia (int): Día de la fecha a mostrar.
        ruta_citas (str): Ruta al archivo JSON donde se almacenan las citas.
    Returns:
        none
        
    """
    fecha = f"{año:04d}-{mes:02d}-{dia:02d}"
    citas = cargar_json(ruta_citas)
    citas_dia = [c for c in citas if c.get("fecha") == fecha]
    citas_dia = enriquecer_citas(citas_dia)  # añadir nombres para mostrar
    limpiar()
    if not citas_dia:
        console.print(f"[yellow]No hay citas para el {fecha}[/yellow]")
        input("Enter para volver...")
        return

    mostrar_tabla_citas(citas_dia, titulo=f"Citas del {fecha}")
    console.print("\n[c]Acciones:[/c] [cyan]id_cita[/cyan] para cancelar, Enter para volver.")
    opcion = console.input("[cyan]Ingrese ID de cita a cancelar (o Enter): [/cyan]").strip()
    if opcion == "":
        return
    # eliminar cita si existe
    citas_all = cargar_json(ruta_citas)
    if not any(c.get("id_cita") == opcion for c in citas_all):
        console.print("[red]ID no encontrado.[/red]")
        time.sleep(0.8)
        return
    citas_all = [c for c in citas_all if c.get("id_cita") != opcion]
    guardar_json(ruta_citas, citas_all)
    console.print("[green]Cita cancelada con éxito.[/green]")
    time.sleep(0.8)

# -------------------- ESTADÍSTICAS --------------------
def estadisticas_citas_por_medico(ruta_medicos="data/medicos.csv", ruta_citas="data/citas.json"):
    """
    Estructura y muestra estadísticas de citas por médico.
    
    Args:
        ruta_medicos (str): Ruta al archivo CSV de médicos.
        ruta_citas (str): Ruta al archivo JSON donde se almacenan las citas.
    Returns:
        none
        
    """
    medicos = cargar_csv_simple(ruta_medicos)
    citas = cargar_json(ruta_citas)
    contador = Counter([c.get("id_medico") for c in citas])
    tabla = Table(title="Estadísticas por Médico", show_lines=True, box=box.SIMPLE)
    tabla.add_column("Médico")
    tabla.add_column("Especialidad")
    tabla.add_column("Citas", justify="right")
    for m in medicos:
        tabla.add_row(
            m.get("nombre", m.get("id_medico", "")),
            m.get("especialidad", ""),
            str(contador.get(m.get("id_medico"), 0))
        )
    console.print(tabla)
    input("Enter para volver...")

# -------------------- SELECTOR INTERACTIVO PARA MENÚ PRINCIPAL --------------------
def selector_interactivo(titulo, opciones):
    """
    Estructura un selector interactivo usando readchar.
    
    Args:
        titulo (str): Título del menú.
        opciones (List[str]): Lista de opciones a mostrar.
    Returns:
        int: Índice de la opción seleccionada.
        
    """
    seleccion = 0
    while True:
        limpiar()
        console.print(Panel(f"[bold cyan]{titulo}[/bold cyan]"))
        for i, opt in enumerate(opciones):
            prefix = "👉 " if i == seleccion else "   "
            style = "reverse bold green" if i == seleccion else ""
            console.print(prefix + opt, style=style)
        tecla = readchar.readkey()
        if tecla == readchar.key.UP:
            seleccion = (seleccion - 1) % len(opciones)
        elif tecla == readchar.key.DOWN:
            seleccion = (seleccion + 1) % len(opciones)
        elif tecla == readchar.key.ENTER:
            return seleccion

# -------------------- VISTA PRINCIPAL (INTERFAZ) --------------------
def mostrar_menu_simple():
    """
    Estructura y muestra un menú simple por consola.
    
    Args:   
        none
    Returns:
        str: Opción seleccionada por el usuario.
        
    """
    limpiar()

    opciones_tabla = Table(show_header=False, box=box.SIMPLE_HEAVY)
    opciones_tabla.add_row("[bold green][1][/bold green] 👤 Gestionar Pacientes")
    opciones_tabla.add_row("[bold green][2][/bold green] 🩺 Gestionar Médicos")
    opciones_tabla.add_row("[bold green][3][/bold green] 📅 Agendar / Ver Citas")
    opciones_tabla.add_row("[bold green][4][/bold green] 📊 Ver Calendario de Citas (Inter.)")
    opciones_tabla.add_row("[bold green][5][/bold green] 📈 Estadísticas por médico")
    opciones_tabla.add_row("[bold red][0][/bold red] 🚪 Salir")

    console.print(opciones_tabla)
    console.print("[yellow]───────────────────────────────────────────────[/yellow]")

    opcion = console.input("[bold cyan]Seleccione una opción (o use flechas con Enter): [/bold cyan]")
    return opcion

def vista_principal():
    """
    Estructura y maneja el menú principal interactivo del sistema de citas médicas.
    
    Args:
        none
    Returns:
        none
        
    """
    # menú que soporta selector interactivo y entrada por número (compatible)
    opciones = [
        "👤 Gestionar Pacientes",
        "🩺 Gestionar Médicos",
        "📅 Agendar / Ver Citas",
        "📊 Ver Calendario de Citas (Interactivo)",
        "📈 Estadísticas por médico",
        "🚪 Salir"
    ]
    while True:
        # permitimos usar selector interactivo
        try:
            indice = selector_interactivo("BIENVENIDO AL SISTEMA DE CITAS MÉDICAS\n🏥 Menú Principal (usa ↑ ↓ + Enter \npara navegar dentro de las opciones)", opciones)
        except Exception:
            # si readchar da problema, fallback a menú simple por input
            opcion = mostrar_menu_simple()
            if opcion == "0":
                indice = 5
            elif opcion in ["1","2","3","4","5"]:
                indice = int(opcion)-1
            else:
                console.print("[bold red]Opción no válida.[/bold red]")
                time.sleep(0.8)
                continue

        # manejar selección
        if indice == 0:
            # intentar llamar a la vista de pacientes (si existe)
            animacion_carga("Abriendo módulo de pacientes...")
            try:
                from Vista.vista_paciente import main_vista_pacientes
                main_vista_pacientes()
            except Exception as e:
                console.print(f"[red]Error al cargar módulo de pacientes:[/red] {e}")
                input("Enter para volver...")
        elif indice == 1:
            animacion_carga("Abriendo módulo de médicos...")
            try:
                from Vista.vista_medico import main_vista_medicos
                main_vista_medicos()
            except Exception:
                console.print("[yellow]Módulo de médicos no encontrado. (Placeholder)[/yellow]")
                input("Enter para volver...")
        elif indice == 2:
            animacion_carga("Abriendo módulo de citas...")
            try:
                from Vista.vista_cita import main_vista_citas
                main_vista_citas()
            except Exception:
                console.print("[yellow]Módulo de citas no encontrado. (Placeholder)[/yellow]")
                input("Enter para volver...")
        elif indice == 3:
            # calendario interactivo completo
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

# -------------------- EJECUCIÓN DIRECTA (para pruebas) --------------------
if __name__ == "__main__":
    vista_principal()
