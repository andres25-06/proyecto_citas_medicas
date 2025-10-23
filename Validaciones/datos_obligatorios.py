# Campos vacíos
# Tipos de datos (números, texto, fechas, etc.)
# Longitud mínima y máxima
# Formato (correo, teléfono, cédula, etc.)
# Rango de valores (por ejemplo, edad entre 18 y 100)

# -*- coding: utf-8 -*-
"""
Módulo de Validaciones de Datos (con Rich).

Incluye:
- Campos vacíos
- Tipos de datos
- Longitud mínima y máxima
- Formato (correo, teléfono, cédula, etc.)
- Rango de valores
"""

import re
from rich.console import Console

console = Console()


def validar_campo_vacio(valor: str, nombre_campo: str):
    if not valor.strip():
        console.print(f"[bold red]⚠️ El campo '{nombre_campo}' no puede estar vacío.[/bold red]")
        return False
    return True



def validar_tipo(valor, tipo_esperado, nombre_campo: str):
    if not isinstance(valor, tipo_esperado):
        console.print(f"[bold red]⚠️ El campo '{nombre_campo}' debe ser de tipo {tipo_esperado.__name__}.[/bold red]")
        return False
    return True



def validar_longitud(valor: str, minimo: int, maximo: int, nombre_campo: str):
    if len(valor) < minimo or len(valor) > maximo:
        console.print(f"[bold yellow]⚠️ El campo '{nombre_campo}' debe tener entre {minimo} y {maximo} caracteres.[/bold yellow]")
        return False
    return True



def validar_formato_correo(correo: str):
    patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if not re.match(patron, correo):
        console.print("[bold red]⚠️ El correo electrónico no tiene un formato válido.[/bold red]")
        return False
    return True



def validar_rango(valor: int | float, minimo: int | float, maximo: int | float, nombre_campo: str):
    if valor < minimo or valor > maximo:
        console.print(f"[bold yellow]⚠️ El campo '{nombre_campo}' debe estar entre {minimo} y {maximo}.[/bold yellow]")
        return False
    return True



def mostrar_resultado_validacion(resultados: list):
    """Recibe una lista de booleanos. Si todos son True → ✅"""
    if all(resultados):
        console.print("[bold green]✅ Todos los datos son válidos.[/bold green]")
        return True
    else:
        console.print("[bold red]\n❌ Corrige los errores antes de continuar.[/bold red]")
        return False
