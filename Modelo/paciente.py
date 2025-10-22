# -*- coding: utf-8 -*-
"""
Módulo de Lógica de Negocio.

Contiene todas las funciones para gestionar los pacientes (CRUD).
Este módulo utiliza 'gestor_datos' para la persistencia.
"""

from typing import Any, Dict, List, Optional

from Controlador import gestor_datos_pacientes


def generar_id(pacientes: List[Dict[str, Any]]) -> int:
    """
    Genera un nuevo ID autoincremental para un aprendiz.

    Args:
        pacientes (List[Dict[str, Any]]): La lista actual de aprendices.

    Returns:
        int: El nuevo ID a asignar.
    """
    if not pacientes:
        return 1
    max_id = max(int(ap.get('id', 0)) for ap in pacientes)
    return max_id + 1

def crear_paciente(
        filepath: str,
        tipo_documento: str,
        documento: int,
        nombres: str,
        apellidos: str,
        direccion: str,
        telefono: int
) -> Optional[Dict[str, Any]]:
    """
    (CREATE) Agrega un nuevo paciente a la agenda.

    Valida que el número de documento no exista antes de agregarlo.

    Args:
        filepath (str): Ruta al archivo de datos.
        tipo_documento (str): Abreviatura del tipo de documento (ej. 'C.C').
        documento (int): Número de documento del aprendiz.
        nombres (str): Nombres del aprendiz.
        apellidos (str): Apellidos del aprendiz.
        direccion (str): Dirección de residencia.
        telefono (int): Número de teléfono.

    Returns:
        Optional[Dict[str, Any]]: El diccionario del paciente creado o None si ya existía.
    """
    pacientes = gestor_datos_pacientes.cargar_datos(filepath)
    str_documento = str(documento)

    if any(ap.get('documento') == str_documento for ap in pacientes):
        print(f"\n❌ Error: El documento '{str_documento}' ya se encuentra registrado.")
        return None

    nuevo_id = generar_id(pacientes)

    nuevo_paciente = {
        'id': str(nuevo_id),
        'tipo_documento': tipo_documento,
        'documento': str_documento,
        'nombres': nombres,
        'apellidos': apellidos,
        'direccion': direccion,
        'telefono': str(telefono)
    }

    pacientes.append(nuevo_paciente)
    gestor_datos_pacientes.guardar_datos(filepath, pacientes)
    return nuevo_paciente

def leer_todos_los_pacientes(filepath: str) -> List[Dict[str, Any]]:
    """
    (READ) Obtiene la lista completa de los pacientes.

    Args:
        filepath (str): Ruta al archivo de datos.

    Returns:
        List[Dict[str, Any]]: La lista de pacientes.
    """
    return gestor_datos_pacientes.cargar_datos(filepath)

def buscar_paciente_por_documento(filepath: str, documento: str) -> Optional[Dict[str, Any]]:
    """
    Busca un paciente específico por su número de documento.

    Args:
        filepath (str): Ruta al archivo de datos.
        documento (str): El documento a buscar.

    Returns:
        Optional[Dict[str, Any]]: El diccionario del paciente si se encuentra, de lo contrario None.
    """
    pacientes = gestor_datos_pacientes.cargar_datos(filepath)
    for paciente in pacientes:
        if paciente.get('documento') == documento:
            return paciente
    return None

def actualizar_paciente(
        filepath: str,
        documento: str,
        datos_nuevos: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """
    (UPDATE) Modifica los datos de un paciente existente.

    Args:
        filepath (str): Ruta al archivo de datos.
        documento (str): El documento del paciente a actualizar.
        datos_nuevos (Dict[str, Any]): Un diccionario con los campos a actualizar.

    Returns:
        Optional[Dict[str, Any]]: El diccionario del paciente actualizado, o None si no se encontró.
    """
    pacientes = gestor_datos_pacientes.cargar_datos(filepath)
    paciente_encontrado = None
    indice = -1

    for i, aprendiz in enumerate(pacientes):
        if pacientes.get('documento') == documento:
            paciente_encontrado = pacientes
            indice = i
            break

    if paciente_encontrado:
        # Convertimos todos los nuevos valores a string para consistencia
        for key, value in datos_nuevos.items():
            datos_nuevos[key] = str(value)

        paciente_encontrado.update(datos_nuevos)
        pacientes[indice] = paciente_encontrado
        gestor_datos_pacientes.guardar_datos(filepath, pacientes)
        return paciente_encontrado

    return None

def eliminar_paciente(filepath: str, documento: str) -> bool:
    """
    (DELETE) Elimina un paciente de la agenda.

    Args:
        filepath (str): Ruta al archivo de datos.
        documento (str): El documento del pac a eliminar.

    Returns:
        bool: True si el pac fue eliminado, False si no se encontró.
    """
    pacientes = gestor_datos_pacientes.cargar_datos(filepath)
    aprendiz_a_eliminar = None

    for paciente in pacientes:
        if paciente.get('documento') == documento:
            paciente_a_eliminar = paciente
            break

    if paciente_a_eliminar:
        paciente.remove(aprendiz_a_eliminar)
        gestor_datos_pacientes.guardar_datos(filepath, pacientes)
        return True

    return False

