# Campos vacíos
# Tipos de datos (números, texto, fechas, etc.)
# Longitud mínima y máxima
# Formato (correo, teléfono, cédula, etc.)
# Rango de valores (por ejemplo, edad entre 18 y 100)

import re

def validar_campo_vacio(valor: str, nombre_campo: str):
    if not valor.strip():
        return f"El campo '{nombre_campo}' no puede estar vacío."
    return None


def validar_tipo(valor, tipo_esperado, nombre_campo):
    if not isinstance(valor, tipo_esperado):
        return f"El campo '{nombre_campo}' debe ser de tipo {tipo_esperado.__name__}."
    return None


def validar_longitud(valor: str, minimo: int, maximo: int, nombre_campo: str):
    if len(valor) < minimo or len(valor) > maximo:
        return f"El campo '{nombre_campo}' debe tener entre {minimo} y {maximo} caracteres."
    return None


def validar_formato_correo(correo: str):
    if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', correo):
        return "El correo electrónico no tiene un formato válido."
    return None


def validar_rango(valor: int | float, minimo: int | float, maximo: int | float, nombre_campo: str):
    if valor < minimo or valor > maximo:
        return f"El campo '{nombre_campo}' debe estar entre {minimo} y {maximo}."
    return None
