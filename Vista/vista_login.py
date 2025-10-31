# vista_login.py
import json
import os
import random
import re
import string
import time

import readchar
from rich.align import Align
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.progress import BarColumn, Progress, TextColumn
from rich.table import Table
from rich.theme import Theme

# -------------------------------------------------------------
# CONFIGURACIÓN DE CONSOLA Y TEMA
# -------------------------------------------------------------
custom_theme = Theme({
    "title": "bold white on blue",
    "menu": "cyan",
    "selected_normal": "bold white on blue",
    "selected_danger": "bold white on red",
    "danger": "red",
    "ok": "green",
    "warn": "yellow",
    "error": "bold red"
})
console = Console(theme=custom_theme)

DATA_PATH = "data/usuarios.json"
CORREOS_SIMULADOS = "data/correos_simulados.txt"

# -------------------------------------------------------------
# UTILIDADES GENERALES
# -------------------------------------------------------------
def limpiar():
    """
    Está función limpia la consola según el sistema operativo.
    Además, mejora la legibilidad del código.
    Args:
        None
    Returns:
        None
    """
    os.system("cls" if os.name == "nt" else "clear")

def asegurar_data():
    """Asegura que el archivo de datos de usuarios exista.
    Args:
        None
    Returns:
        None
    """
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(DATA_PATH):
        admin = [{
            "usuario": "admin",
            "contrasena": "1234",
            "rol": "superadmin",
            "activo": True,
            "correo": "admin@hospital.com"
        }]
        with open(DATA_PATH, "w", encoding="utf-8") as f:
            json.dump(admin, f, indent=4, ensure_ascii=False)

def leer_usuarios():
    """
    Encargada de leer los usuarios desde el archivo JSON.
    Args:
        None
    Returns:
        List[Dict[str, Any]]: Lista de usuarios.
    """
    asegurar_data()
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_usuarios(u):
    """
    Encargada de guardar los usuarios en el archivo JSON.
    Args:
        u (List[Dict[str, Any]]): Lista de usuarios a guardar.
    Returns:
        None
    """
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(u, f, indent=4, ensure_ascii=False)

def generar_codigo():
    """
    Encargada de generar un código aleatorio de 6 caracteres
    para recuperación de contraseña.
    Args:
        None
    Returns:
        str: Código generado.
    """
    return "".join(random.choices(
        string.ascii_uppercase + string.digits, k=6))

def enviar_correo_simulado(dest, asunto, mensaje):
    """
    Está función simula el envío de un correo
    guardando el contenido en un archivo de texto.
    Args:
        dest (str): Destinatario del correo.
        asunto (str): Asunto del correo.
        mensaje (str): Cuerpo del correo.
    Returns:
        None
    """
    os.makedirs("data", exist_ok=True)
    with open(CORREOS_SIMULADOS, "a", encoding="utf-8") as f:
        f.write(f"Para: {dest}\nAsunto: {asunto}\n{mensaje}\n{'-'*40}\n")


# -------------------------------------------------------------
# VALIDACIÓN DE CONTRASEÑA (solo para registro)
# -------------------------------------------------------------
def evaluar_contrasena(passw: str) -> dict:
    """
    Evalúa la seguridad de la contraseña.
    Args:
        passw (str): Contraseña a evaluar.
    Returns:
        dict: Resultado de la evaluación con reglas y puntaje.
    """
    reglas = {
        "min_length": len(passw) >= 8,
        "has_lower": bool(re.search(r"[a-z]", passw)),
        "has_upper": bool(re.search(r"[A-Z]", passw)),
        "has_digit": bool(re.search(r"\d", passw)),
        "has_special": bool(
            re.search(
                r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?`~]", passw)),
    }
    score = sum(reglas.values())
    return {"reglas": reglas, "score": score, "max": len(reglas)}

def nivel_seguridad(score: int, max_score: int) -> tuple[str, int]:
    """
    Evalúa el nivel de seguridad basado en el puntaje.
    Args:
        score (int): Puntaje obtenido.
        max_score (int): Puntaje máximo posible.
    Returns:
        tuple[str, int]: Nivel de seguridad y porcentaje.
    """
    porcentaje = int((score / max_score) * 100)
    if score <= 2:
        return ("Débil", porcentaje)
    elif score (3, 4):
        return ("Media", porcentaje)
    else:
        return ("Fuerte", porcentaje)

def construir_panel(masked: str, evaluacion: dict) -> Panel:
    """
    Crea panel visual de la contraseña.
    Args:
        masked (str): Contraseña en
        evaluacion (dict): Resultado de la evaluación.
    Returns:
        Panel: Panel de Rich con la evaluación visual.
    """
    reglas = evaluacion["reglas"]
    score = evaluacion["score"]
    max_score = evaluacion["max"]
    estado, pct = nivel_seguridad(score, max_score)

    check = lambda x: "[green]✔[/green]" if x else "[red]✖[/red]"
    tabla = Table.grid(padding=(0, 1))
    tabla.add_column(justify="left")
    tabla.add_column(justify="left")
    tabla.add_row("Contraseña:", f"[bold]{masked}[/bold]")
    tabla.add_row("Nivel:", f"[bold]{estado}[/bold] ({pct}%)")
    tabla.add_row("", "")
    tabla.add_row(check(reglas["min_length"]),
                "Mínimo 8 caracteres")
    tabla.add_row(check(reglas["has_lower"]),
                "Al menos una letra minúscula")
    tabla.add_row(check(reglas["has_upper"]),
                "Al menos una letra mayúscula")
    tabla.add_row(check(reglas["has_digit"]),
                "Al menos un número")
    tabla.add_row(check(reglas["has_special"]),
                "Al menos un caracter especial")

    progress = Progress(
        TextColumn("{task.description}"),
        BarColumn(bar_width=None),
        TextColumn(
            "[progress.percentage]{task.percentage:>3.0f}%"),
        expand=True,
        transient=True,
    )
    progress.add_task(
        "[bold]Seguridad:[/bold]", total=max_score, completed=score)

    contenedor = Table.grid()
    contenedor.add_row(tabla)
    contenedor.add_row(progress)

    return Panel(
        contenedor, title="[bold cyan]Validación de contraseña[/bold cyan]",
        border_style="cyan")

def input_oculto_registro(prompt="Contraseña: ", require_strong=False):
    """
    Entrada oculta con validación visual (solo para registro).
    Args:
        prompt (str): Texto del prompt.
    Returns:
        str: Contraseña ingresada.
    """
    contrasena = ""
    console.print(prompt, end="", style="menu")

    with Live(refresh_per_second=12, console=console) as live:
        while True:
            masked = "*" * len(contrasena)
            evaluacion = evaluar_contrasena(contrasena)
            panel = construir_panel(masked, evaluacion)
            live.update(panel)

            ch = readchar.readchar()
            if ch in ("\r", "\n"):
                if require_strong and evaluacion["score"] < evaluacion["max"]:
                    console.print(
                        "\n[red]La contraseña aún no cumple los requisitos.[/red]")
                    time.sleep(1)
                    console.print(prompt, end="", style="menu")
                    continue
                print()
                return contrasena
            elif ch in ("\x08", "\x7f"):
                contrasena = contrasena[:-1]
            elif ch == "\x03":
                raise KeyboardInterrupt
            elif len(contrasena) < 128:
                contrasena += ch


# -------------------------------------------------------------
# INPUT OCULTO SIMPLE (para iniciar sesión)
# -------------------------------------------------------------
def input_oculto_simple(prompt="Contraseña: "):
    """
    Entrada oculta simple con asteriscos visibles.
    Args:
        prompt (str): Texto del prompt.
    Returns:
        str: Contraseña ingresada.
    """
    contrasena = ""
    console.print(prompt, end="", style="menu")
    while True:
        ch = readchar.readchar()
        # ENTER
        if ch in ("\r", "\n"):
            print()
            return contrasena
        # BACKSPACE
        elif ch in ("\x08", "\x7f"):
            if contrasena:
                contrasena = contrasena[:-1]
                # borra el último asterisco visualmente
                print("\b \b", end="", flush=True)
        # CTRL+C
        elif ch == "\x03":
            raise KeyboardInterrupt
        # CARACTER NORMAL
        elif len(contrasena) < 128:
            contrasena += ch
            # muestra asterisco visual
            print("*", end="", flush=True)



# -------------------------------------------------------------
# RENDER DEL CUADRO DE LOGIN
# -------------------------------------------------------------
def cuadro_login_render(opciones, seleccion):
    """
    Estructura y muestra el cuadro de login con opciones.
    Args:
        opciones (List[str]): Lista de opciones del menú.
        seleccion (int): Índice de la opción seleccionada.
    Returns:
        None
    """
    lines = []
    for i, op in enumerate(opciones):
        is_selected = (i == seleccion)
        if any(k in op.lower() for k in ("salir", "eliminar", "borrar")):
            if is_selected:
                lines.append(f"[selected_danger]  ▶ {op}[/selected_danger]")
            else:
                lines.append(f"[danger]  {op}[/danger]")
        elif is_selected:
            lines.append(f"[selected_normal]  ▶ {op}[/selected_normal]")
        else:
            lines.append(f"[menu]  {op}[/menu]")
    contenido = "\n".join(lines)
    panel = Panel(Align.center(contenido),
                title="[bold cyan]💊 INGRESO AL SISTEMA -"
                " CUADRO DE LOGIN 💊[/bold cyan]",
                border_style="bright_blue", width=60, padding=(1, 3))
    console.print(Align.center(panel))

def selector_con_flechas(opciones):
    """
    Estructura el selector de opciones con flechas.
    Args:
        opciones (List[str]): Lista de opciones del menú.
    Returns:
        int: Índice de la opción seleccionada.
    """
    seleccion = 0
    while True:
        limpiar()
        cuadro_login_render(opciones, seleccion)
        key = readchar.readkey()
        if key == readchar.key.UP:
            seleccion = (seleccion - 1) % len(opciones)
        elif key == readchar.key.DOWN:
            seleccion = (seleccion + 1) % len(opciones)
        elif key == readchar.key.ENTER:
            return seleccion


# -------------------------------------------------------------
# FUNCIONALIDADES DE LOGIN
# -------------------------------------------------------------
def registrar_usuario():
    """
    Está función gestiona el registro de un nuevo usuario.
    Args:
        None
    Returns:
        None
    """
    limpiar()
    console.print(Panel(
        "[bold yellow]🧾 Registro de nuevo usuario[/bold yellow]",
        border_style="bright_yellow", width=60))
    usuario = console.input(
        "Nombre de usuario: ").strip()
    correo = console.input(
        "Correo (opcional, para recuperación): ").strip()
    contrasena = input_oculto_registro(
        "Contraseña: ", require_strong=True)
    confirmar = input_oculto_registro("Confirmar contraseña: ")

    if contrasena != confirmar:
        console.print(
            "[error]❌ Las contraseñas no coinciden.[/error]")
        time.sleep(1.5)
        return

    if not usuario or not contrasena:
        console.print(
            "[warn]❗ Usuario y contraseña son obligatorios.[/warn]")
        time.sleep(1.5)
        return

    usuarios = leer_usuarios()
    if any(u["usuario"] == usuario for u in usuarios):
        console.print("[error]❌ Ya existe ese nombre de usuario.[/error]")
        time.sleep(1.5)
        return

    usuarios.append({
        "usuario": usuario,
        "contrasena": contrasena,
        "correo": correo,
        "rol": "usuario",
        "activo": False
    })
    guardar_usuarios(usuarios)
    console.print("[ok]✅ Registro completado. Espera aprobación del superadmin.[/ok]")
    time.sleep(1.8)

def validar_credenciales(usuario, contrasena):
    """
    Encargada de validar las credenciales de inicio de sesión.
    Args:
        usuario (str): Nombre de usuario.
        contrasena (str): Contraseña.
    Returns:
        dict|str|None: Diccionario del usuario si es válido,
        "pendiente" si está inactivo, None si no es válido.
    """
    usuarios = leer_usuarios()
    for u in usuarios:
        if u["usuario"] == usuario and u["contrasena"] == contrasena:
            if not u.get("activo", False):
                return "pendiente"
            return u
    return None

def recuperar_contrasena():
    """
    Está función gestiona la recuperación de contraseña.
    Args:
        None
    Returns:
        None
    """
    limpiar()
    console.print(Panel(
        "[bold yellow]🔑 Recuperación de contraseña[/bold yellow]",
        border_style="bright_yellow", width=60))
    usuario = console.input("Nombre de usuario: ").strip()
    usuarios = leer_usuarios()
    for u in usuarios:
        if u["usuario"] == usuario:
            codigo = generar_codigo()
            u["contrasena"] = codigo
            guardar_usuarios(usuarios)
            if u.get("correo"):
                enviar_correo_simulado(
                    u["correo"], "Recuperación de contraseña",
                    f"Tu nueva contraseña temporal es: {codigo}")
            console.print(
                "[ok]✅ Contraseña temporal generada"
                " para '{usuario}': [bold]{codigo}[/bold][/ok]")
            console.print(
                "[warn](Se ha simulado envío si tenías correo registrado)[/warn]")
            time.sleep(2.5)
            return
    console.print("[error]❌ Usuario no encontrado.[/error]")
    time.sleep(1.5)


# -------------------------------------------------------------
# INICIAR SESIÓN
# -------------------------------------------------------------
def iniciar_sesion():
    """
    Está función gestiona el inicio de sesión.
    Args:
        None
    Returns:
        dict|None: Diccionario del usuario si inicio exitoso,
        None si falló.
    """
    limpiar()
    console.print(Panel(
        "[bold cyan]🔐 Iniciar sesión[/bold cyan]",
        border_style="bright_blue", width=60))
    usuario = console.input("Nombre de usuario: ").strip()
    contrasena = input_oculto_simple("Contraseña: ")  # ← aquí entrada sin validación

    resultado = validar_credenciales(usuario, contrasena)
    if resultado == "pendiente":
        console.print(
            "[warn]⚠ Tu cuenta está pendiente de aprobación por el superadmin.[/warn]")
        time.sleep(1.8)
        return None
    if resultado:
        console.print(f"[ok]✅ Bienvenido {usuario}![/ok]")
        time.sleep(1)
        return resultado
    console.print("[error]❌ Usuario o contraseña incorrectos.[/error]")
    time.sleep(1.5)
    return None


# -------------------------------------------------------------
# FUNCIÓN PRINCIPAL DEL LOGIN
# -------------------------------------------------------------



def login():
    """
    Está función gestiona el flujo principal del login.
    Args:
        None
    Returns:
        dict|None: Diccionario del usuario si inicio exitoso,
        None si el usuario decide salir.
    """
    from Vista.vista_superadmin import panel_superadmin
    asegurar_data()
    opciones = ["Iniciar sesión", "Registrarse", "Recuperar contraseña", "Salir"]
    while True:
        idx = selector_con_flechas(opciones)
        opcion = opciones[idx]
        if opcion == "Iniciar sesión":
            usuario = iniciar_sesion()
            if usuario:
                if usuario.get("rol") == "superadmin":
                    panel_superadmin(usuario)
                return usuario
        elif opcion == "Registrarse":
            registrar_usuario()
        elif opcion == "Recuperar contraseña":
            recuperar_contrasena()
        elif opcion == "Salir":
            limpiar()
            console.print(Panel(
                "[bold red]👋 Saliendo del sistema...[/bold red]",
                border_style="red", width=60))
            time.sleep(1)
            exit()
