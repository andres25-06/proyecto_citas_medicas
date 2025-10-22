# -*- coding: utf-8 -*-
"""
Archivo principal del sistema de citas médicas.
Ejecuta el menú principal y redirige a las vistas.
"""

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

# Importamos la vista actual (pacientes)
from Vista import vista_paciente
from Vista import vista_medico
from Vista import vista_cita
# En el futuro puedes agregar más vistas:
# from Vista import vista_medicos, vista_citas

console = Console()


def mostrar_menu_principal():
    """Muestra el menú principal del sistema."""
    menu_texto = (
        "[bold yellow]1[/bold yellow]. Módulo de pacientes\n"
        "[bold yellow]2[/bold yellow]. Módulo de médicos\n"
        "[bold yellow]3[/bold yellow]. Módulo de citas\n"
        "[bold red]4[/bold red]. Salir"
    )
    console.print(Panel(menu_texto, title="[bold]SISTEMA DE CITAS MÉDICAS[/bold]", border_style="cyan"))


def main():
    """Controla el flujo principal del programa."""
    while True:
        mostrar_menu_principal()
        opcion = Prompt.ask("Seleccione una opción", choices=["1", "2", "3", "4"], show_choices=False)

        if opcion == "1":
            # Llamamos la vista de pacientes
            vista_paciente.main_vista_pacientes()

        elif opcion == "2":
            vista_medico.main_vista_medicos()

        elif opcion == "3":
            console.print("[blue]📅 El módulo de citas estará disponible pronto...[/blue]")

        elif opcion == "4":
            console.print("\n[bold magenta]👋 ¡Hasta luego![/bold magenta]")
            break


if __name__ == "__main__":
    main()
