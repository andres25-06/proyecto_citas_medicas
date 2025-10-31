# -*- coding: utf-8 -*-


import csv
import json
import os
from datetime import datetime

from rich.console import Console
from rich.prompt import Prompt

console = Console()


# ======================================================
#  VALIDACIÓN DE CAMPOS VACÍOS Y LONGITUD
# ======================================================
def validar_texto(etiqueta: str, min_len: int = 1, max_len: int = 100) -> str:
    """
    Solicita al usuario un texto y valida que:
    - No esté vacío.
    - Cumpla una longitud mínima y máxima.

    Args:
        etiqueta (str): Texto que se muestra al usuario.
        min_len (int): Longitud mínima permitida (por defecto 1).
        max_len (int): Longitud máxima permitida (por defecto 100).

    Returns:
        str: Texto ingresado por el usuario que cumple las condiciones.
    """
    while True:
        valor = Prompt.ask(etiqueta).strip()
        if not valor:
            console.print("[bold red] Este campo no puede estar vacío.[/bold red]")
            continue
        if len(valor) < min_len or len(valor) > max_len:
            console.print(f"[bold red] El texto debe tener entre {min_len} y {max_len} caracteres.[/bold red]")
            continue
        return valor


# ======================================================
#  VALIDACIÓN DE NÚMEROS (ENTEROS) CON RANGO OPCIONAL
# ======================================================
def validar_numero(etiqueta: str, minimo: int = None, maximo: int = None) -> int:
    """
    Solicita un número entero y valida que:
    - No esté vacío.
    - Solo contenga dígitos.
    - (Opcional) Esté dentro de un rango permitido.

    Args:
        etiqueta (str): Texto que se muestra al usuario.
        minimo (int, opcional): Valor mínimo permitido.
        maximo (int, opcional): Valor máximo permitido.

    Returns:
        int: Número entero válido.
    """
    while True:
        valor = Prompt.ask(etiqueta).strip()
        if not valor:
            console.print("[bold red] Este campo no puede estar vacío.[/bold red]")
            continue
        if not valor.isdigit():
            console.print("[bold red] Debes ingresar solo números.[/bold red]")
            continue
        valor = int(valor)
        if minimo is not None and valor < minimo:
            console.print(f"[bold red] El valor no puede ser menor que {minimo}.[/bold red]")
            continue
        if maximo is not None and valor > maximo:
            console.print(f"[bold red] El valor no puede ser mayor que {maximo}.[/bold red]")
            continue
        return valor




# ======================================================
# VALIDACIÓN DE FORMATO ( TELÉFONO, CÉDULA)
# ======================================


def validar_telefono(etiqueta: str, min_digitos: int = 7, max_digitos: int = 10) -> str:
    """
    Solicita un número de teléfono y valida que:
    - No esté vacío.
    - Contenga solo dígitos.
    - Tenga una longitud válida (por defecto 7 a 10 dígitos).

    Args:
        etiqueta (str): Texto que se muestra al usuario.
        min_digitos (int): Longitud mínima permitida.
        max_digitos (int): Longitud máxima permitida.

    Returns:
        str: Número de teléfono válido.
    """
    while True:
        valor = Prompt.ask(etiqueta).strip()
        if not valor:
            console.print("[bold red] Este campo no puede estar vacío.[/bold red]")
            continue
        if not valor.isdigit() or not (min_digitos <= len(valor) <= max_digitos):
            console.print(f"[bold red] El teléfono debe tener entre {min_digitos} y {max_digitos} dígitos numéricos.[/bold red]")
            continue
        return valor


def validar_cedula(etiqueta: str, filepath: str, min_digitos: int = 6, max_digitos: int = 10) -> str:
    """
    Solicita un número de cédula y valida que:
    - No esté vacío.
    - Contenga solo dígitos.
    - Tenga una longitud válida.
    - No esté duplicada en el archivo (JSON o CSV).

    Args:
        etiqueta (str): Texto que se muestra al usuario.
        filepath (str): Ruta del archivo donde se guardan los registros.
        min_digitos (int): Longitud mínima permitida (por defecto 6).
        max_digitos (int): Longitud máxima permitida (por defecto 10).

    Returns:
        str: Número de cédula válido y no duplicado.
    """

    # --- Cargar registros existentes ---
    registros = []
    if os.path.exists(filepath):
        try:
            if filepath.endswith(".json"):
                with open(filepath, "r", encoding="utf-8") as f:
                    registros = json.load(f)
            elif filepath.endswith(".csv"):
                with open(filepath, "r", encoding="utf-8", newline="") as f:
                    lector = csv.DictReader(f)
                    registros = list(lector)
        except Exception as e:
            console.print(f"[bold yellow]⚠️ No se pudieron cargar los registros: {e}[/bold yellow]")

    # --- Ciclo de validación ---
    while True:
        valor = Prompt.ask(etiqueta).strip()

        # Validar campo vacío
        if not valor:
            console.print("[bold red]⚠️ Este campo no puede estar vacío.[/bold red]")
            continue

        # Validar formato y longitud
        if not valor.isdigit() or not (min_digitos <= len(valor) <= max_digitos):
            console.print(f"[bold red]⚠️ La cédula debe tener entre {min_digitos} y {max_digitos} dígitos numéricos.[/bold red]")
            continue

        # Validar duplicado
        duplicado = any(str(registro.get("documento", "")).strip() == valor for registro in registros)
        if duplicado:
            console.print(f"[bold red]🚫 La cédula {valor} ya está registrada.[/bold red]")
            continue

        # Si todo está correcto
        return valor


def validar_hora(etiqueta: str) -> str:
    """
    Solicita y valida una hora en formato HH:MM (24 horas).
    Solo permite horas entre 07:00 y 18:00 (7 a.m. - 6 p.m.).
    
    Args:
        etiqueta (str): Texto que se muestra al solicitar la hora.
    
    Returns:
        str: Hora validada en formato HH:MM.
    """
    while True:
        hora = input(f"Ingrese {etiqueta} (HH:MM): ").strip()
        try:
            hora_obj = datetime.strptime(hora, "%H:%M")
            # Validar rango permitido
            if 7 <= hora_obj.hour <= 18:
                # Si es exactamente las 18:00, solo se acepta si los minutos son 00
                if hora_obj.hour == 18 and hora_obj.minute > 0:
                    print("⚠️  La última cita permitida es a las 18:00 en punto.")
                else:
                    return hora
            else:
                print("⚠️  Solo se permiten horas entre las 07:00 y las 18:00.")
        except ValueError:
            print("⚠️  Formato de hora inválido. Use el formato HH:MM (ejemplo: 09:30).")
