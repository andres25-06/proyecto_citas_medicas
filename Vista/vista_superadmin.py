# vista_superadmin.py
import os
import time
import readchar
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.theme import Theme

# Importar funciones del login
from Vista.vista_login import leer_usuarios, guardar_usuarios

# ---------- CONFIGURACIÓN ----------
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

# ---------- UTILIDADES ----------
def limpiar_consola():
    """Limpia la consola de forma compatible con Windows y Linux."""
    os.system("cls" if os.name == "nt" else "clear")

# ---------- SELECTOR CON FLECHAS ----------
def selector_lista_con_flechas(titulo, items, allow_back=True):
    """
    items: lista de strings.
    Retorna índice seleccionado o None si 'Volver' fue elegido.
    """
    seleccion = 0
    while True:
        limpiar_consola()
        opciones = items[:] + (["Volver"] if allow_back else [])
        contenido = []
        for i, it in enumerate(opciones):
            if i == seleccion:
                if any(k in it.lower() for k in ("salir", "eliminar", "borrar")):
                    contenido.append(f"[bold white on red]  ▶ {it}[/bold white on red]")
                else:
                    contenido.append(f"[bold white on blue]  ▶ {it}[/bold white on blue]")
            else:
                if any(k in it.lower() for k in ("salir", "eliminar", "borrar")):
                    contenido.append(f"[red]  {it}[/red]")
                else:
                    contenido.append(f"[cyan]  {it}[/cyan]")

        panel = Panel(
            Align.center("\n".join(contenido)),
            title=f"[bold cyan]⚙ {titulo.upper()} ⚙[/bold cyan]",
            border_style="bright_blue",
            width=70,
            padding=(1, 3)
        )
        console.print(Align.center(panel))

        key = readchar.readkey()
        if key == readchar.key.UP:
            seleccion = (seleccion - 1) % len(opciones)
        elif key == readchar.key.DOWN:
            seleccion = (seleccion + 1) % len(opciones)
        elif key == readchar.key.ENTER:
            if allow_back and seleccion == len(opciones) - 1:
                return None
            return seleccion

# ---------- CONFIRMACIONES ----------
def confirmar_accion(mensaje, color="red"):
    """
    Pregunta si el usuario está seguro de continuar.
    Retorna True si confirma, False si no.
    """
    panel = Panel(
        Align.center(f"⚠️ {mensaje}\n\n[bold white]¿Deseas continuar? (s/n)[/bold white]"),
        title=f"[{color}]CONFIRMACIÓN[/]",
        border_style=color,
        width=70,
        padding=(1, 3)
    )
    console.print(panel)
    while True:
        tecla = readchar.readkey().lower()
        if tecla in ("s", "y"):
            return True
        elif tecla == "n":
            return False

# ---------- PANEL PRINCIPAL ----------
def panel_superadmin(usuario):
    limpiar_consola()
    while True:
        opciones = [
            "👥 Ver usuarios",
            "✅ Aprobar usuario",
            "🗑 Eliminar usuario",
            "🔑 Resetear contraseña",
            "🔒 Cambiar mi contraseña",
            "🚪 Salir"
        ]
        idx = selector_lista_con_flechas("Panel Superadmin", opciones, allow_back=False)
        accion = opciones[idx]
        usuarios = leer_usuarios()

        # --- VER USUARIOS ---
        if "Ver usuarios" in accion:
            lista = "\n".join([
                f"- [bold]{u['usuario']}[/bold] ({u.get('rol','usuario')}) "
                f"{'✅ Activo' if u.get('activo') else '⛔ Inactivo'}"
                for u in usuarios
            ])
            panel = Panel(
                lista if lista else "No hay usuarios registrados.",
                title="[bold yellow]👥 Usuarios registrados[/bold yellow]",
                border_style="bright_blue",
                width=75
            )
            console.clear()
            console.print(panel)
            console.print("\n[cyan]Presione cualquier tecla para continuar...[/cyan]")
            readchar.readkey()

        # --- APROBAR USUARIO ---
        elif "Aprobar usuario" in accion:
            pendientes = [u for u in usuarios if not u.get("activo", False) and u.get("rol") != "superadmin"]
            if not pendientes:
                console.print(Panel("[green]✅ No hay usuarios pendientes de aprobación.[/green]", border_style="green", width=70))
                time.sleep(1.4)
                continue
            opciones_ = [p["usuario"] for p in pendientes]
            sel = selector_lista_con_flechas("Usuarios pendientes", opciones_)
            if sel is None:
                continue

            elegido = opciones_[sel]
            if confirmar_accion(f"¿Estás seguro de aprobar al usuario [bold cyan]{elegido}[/bold cyan]?", color="green"):
                for u in usuarios:
                    if u["usuario"] == elegido:
                        u["activo"] = True
                        guardar_usuarios(usuarios)
                        console.print(Panel(f"[ok]✅ Usuario '{elegido}' aprobado correctamente.[/ok]", border_style="green", width=70))
                        time.sleep(1.5)
                        break
            else:
                console.print(Panel("[warn]❗ Acción cancelada por el usuario.[/warn]", border_style="yellow", width=70))
                time.sleep(1.2)

        # --- ELIMINAR USUARIO ---
        elif "Eliminar usuario" in accion:
            candidatos = [u for u in usuarios if u.get("rol") != "superadmin"]
            if not candidatos:
                console.print(Panel("[warn]⚠ No hay usuarios eliminables.[/warn]", border_style="yellow", width=70))
                time.sleep(1.2)
                continue
            opciones_ = [c["usuario"] for c in candidatos]
            sel = selector_lista_con_flechas("Eliminar usuario", opciones_)
            if sel is None:
                continue

            eliminar = opciones_[sel]
            if confirmar_accion(f"¿Seguro que deseas eliminar al usuario [bold red]{eliminar}[/bold red]? Esta acción no se puede deshacer."):
                usuarios = [u for u in usuarios if u["usuario"] != eliminar]
                guardar_usuarios(usuarios)
                console.print(Panel(f"[error]🗑 Usuario '{eliminar}' eliminado correctamente.[/error]", border_style="red", width=70))
                time.sleep(1.5)
            else:
                console.print(Panel("[warn]❗ Eliminación cancelada.[/warn]", border_style="yellow", width=70))
                time.sleep(1.2)

        # --- RESETEAR CONTRASEÑA ---
        elif "Resetear contraseña" in accion:
            candidatos = [u for u in usuarios if u.get("rol") != "superadmin"]
            if not candidatos:
                console.print(Panel("[warn]No hay usuarios disponibles para resetear.[/warn]", border_style="yellow", width=70))
                time.sleep(1.2)
                continue
            opciones_ = [c["usuario"] for c in candidatos]
            sel = selector_lista_con_flechas("Resetear contraseña", opciones_)
            if sel is None:
                continue
            target = opciones_[sel]
            for u in usuarios:
                if u["usuario"] == target:
                    u["contrasena"] = "temporal123"
                    guardar_usuarios(usuarios)
                    console.print(Panel(f"[ok]🔑 Contraseña de '{target}' reseteada a [bold]temporal123[/bold]", border_style="green", width=75))
                    time.sleep(1.6)
                    break

        # --- CAMBIAR MI CONTRASEÑA ---
        elif "Cambiar mi contraseña" in accion:
            for u in usuarios:
                if u["usuario"] == usuario.get("usuario"):
                    nueva = console.input("[cyan]Ingrese la nueva contraseña: [/cyan]").strip()
                    if nueva:
                        u["contrasena"] = nueva
                        guardar_usuarios(usuarios)
                        console.print(Panel("[ok]🔒 Contraseña actualizada correctamente.[/ok]", border_style="green", width=70))
                        time.sleep(1.4)
                    break

        # --- SALIR ---
        elif "Salir" in accion:
            console.print(Panel("[bold red]👋 Cerrando sesión de superadmin...[/bold red]", border_style="red", width=70))
            time.sleep(1)
            return
 

