# Datos obligatorios en registros relacionados
# Coherencia entre módulos (por ejemplo, pedido vinculado a cliente existente)
# -*- coding: utf-8 -*-
"""
Validaciones de Relaciones y Coherencia entre Módulos (con Rich).

Verifica:
- Que existan los datos obligatorios en registros relacionados.
- Que las relaciones sean coherentes (ej: pedido vinculado a cliente existente).
"""

from rich.console import Console

console = Console()


def validar_existencia_relacion(id_relacion, lista_registros, nombre_relacion: str):
    """
    Verifica que un ID relacionado (por ejemplo, id_cliente) exista en otra lista o módulo.

    Parámetros:
    - id_relacion: valor del ID que se está comprobando (ej: 3)
    - lista_registros: lista de diccionarios con los registros existentes (ej: lista de clientes)
    - nombre_relacion: texto descriptivo de la relación (ej: 'cliente', 'paciente', 'médico')

    Retorna:
    - True si existe
    - False si no existe (y muestra advertencia)
    """
    existe = any(str(r.get("id")) == str(id_relacion) for r in lista_registros)

    if not existe:
        console.print(f"[bold red]❌ No se encontró un {nombre_relacion} con ID {id_relacion}. "
                    f"Verifica que el {nombre_relacion} exista antes de continuar.[/bold red]")
        return False

    console.print(f"[bold green]✅ {nombre_relacion.capitalize()} con ID {id_relacion} verificado correctamente.[/bold green]")
    return True



def validar_datos_relacion_obligatorios(datos: dict, campos_obligatorios: list, nombre_relacion: str):
    """
    Comprueba que los campos requeridos de una relación (como cliente o médico)
    no estén vacíos o faltantes.

    Parámetros:
    - datos: diccionario del registro (ej: {"id":1,"nombre":"Juan"})
    - campos_obligatorios: lista de campos que deben existir y tener valor
    - nombre_relacion: texto descriptivo del módulo o relación
    """
    faltantes = [campo for campo in campos_obligatorios if not datos.get(campo)]

    if faltantes:
        console.print(f"[bold yellow]⚠️ Faltan datos obligatorios del {nombre_relacion}: "
                    f"{', '.join(faltantes)}[/bold yellow]")
        return False

    console.print(f"[bold green]✅ Todos los datos obligatorios del {nombre_relacion} están completos.[/bold green]")
    return True
