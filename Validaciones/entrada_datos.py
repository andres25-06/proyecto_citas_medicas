# Datos obligatorios en registros relacionados
# Validador de documento no repetido 
# -*- coding: utf-8 -*-


from rich.console import Console
from rich.panel import Panel
import csv
import json
import os

console = Console()


def validar_documento_unico(documento: str, lista_registros: list, nombre_archivo: str) -> bool:
    """
    Verifica si un documento ya está registrado en una lista de diccionarios.

    Args:
        documento (str): Documento a verificar.
        lista_registros (list): Lista de registros cargados desde archivo (cada uno es un dict).
        nombre_archivo (str): Nombre del módulo o tipo de registro (ej: 'Paciente', 'Médico').

    Returns:
        bool: True si el documento es único, False si ya existe.
    """
    for registro in lista_registros:
        if str(registro.get("documento", "")).strip() == str(documento).strip():
            console.print(Panel.fit(
                f"[bold red]⚠️ El documento {documento} ya está registrado en {nombre_archivo}.[/bold red]",
                border_style="red"
            ))
            return False
    return True


def validar_datos_relacion_obligatorios(datos: dict, campos_obligatorios: list, nombre_relacion: str):
    """
        Comprueba que los campos requeridos de una relación (como cliente o médico)
        no estén vacíos o faltantes.
        Args:
            datos (dict): Diccionario con los datos de la relación.
            campos_obligatorios (list): Lista de nombres de campos que son obligatorios.
            nombre_relacion (str): Nombre del tipo de relación (ej: 'Paciente', 'Médico').
        Returns:
            bool: True si todos los campos obligatorios están presentes, False si faltan.
    """
    faltantes = [campo for campo in campos_obligatorios if not datos.get(campo)]

    if faltantes:
        console.print(f"[bold yellow]⚠️ Faltan datos obligatorios del {nombre_relacion}: "
                    f"{', '.join(faltantes)}[/bold yellow]")
        return False

    console.print(f"[bold green]✅ Todos los datos obligatorios del {nombre_relacion} están completos.[/bold green]")
    return True

def validar_existencia_relacion(documento, lista, tipo):
    """
    Verifica si un paciente o médico existe en la lista, CSV o JSON.
    """
    print(f"\n[DEBUG] Buscando {tipo} con documento: {documento}")
    print("test",documento, lista, tipo)

    # --- Buscar en la lista en memoria ---
    for item in lista:
        print(f"[DEBUG] Revisando en lista: {item.get('documento')}")
        if str(item.get("documento")) == str(documento):
            print("[DEBUG] Encontrado en lista ✅")
            return True

    # --- Definir nombres de archivos según tipo ---
    nombre_base = tipo.lower()
    archivo_csv = f"Data/{nombre_base}.csv"
    archivo_json = f"Data/{nombre_base}.json"

    # --- Buscar en el CSV ---
    if os.path.exists(archivo_csv):
        print(f"[DEBUG] Buscando en {archivo_csv}...")
        with open(archivo_csv, "r", encoding="utf-8") as f:
            lector = csv.DictReader(f)
            for fila in lector:
                print(f"[DEBUG] Revisando CSV: {fila.get('documento')}")
                if str(fila.get("documento")) == str(documento):
                    print("[DEBUG] Encontrado en CSV ✅")
                    return True
    else:
        print(f"[DEBUG] No existe el archivo {archivo_csv}")

    # --- Buscar en el JSON ---
    if os.path.exists(archivo_json):
        print(f"[DEBUG] Buscando en {archivo_json}...")
        with open(archivo_json, "r", encoding="utf-8") as f:
            try:
                datos = json.load(f)
                for item in datos:
                    print(f"[DEBUG] Revisando JSON: {item.get('documento')}")
                    if str(item.get("documento")) == str(documento):
                        print("[DEBUG] Encontrado en JSON ✅")
                        return True
            except json.JSONDecodeError:
                print("[DEBUG] Error al leer el JSON (vacío o mal formado)")
    else:
        print(f"[DEBUG] No existe el archivo {archivo_json}")

    print("[DEBUG] No se encontró en ningún lugar ❌")
    
    return False