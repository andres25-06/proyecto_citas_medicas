# -*- coding: utf-8 -*-
"""
Módulo de Lógica de Negocio.

Contiene todas las funciones para gestionar los pacientes (CRUD).
Este módulo utiliza 'gestor_datos' para la persistencia.
"""

from typing import Any, Dict, List, Optional

from Controlador import gestor_datos


def generar_id(medico: List[Dict[str, Any]]) -> int:
    """
    Genera un nuevo ID autoincremental para un medico.

    Args:
        medicos (List[Dict[str, Any]]): La lista actual de medicos .

    Returns:
        int: El nuevo ID a asignar.
    """
    if not medico:
        return 1
    max_id = max(int(ap.get('id', 0)) for ap in medico)
    return max_id + 1

def crear_medico(
        filepath: str,
        tipo_documento: str,
        documento: int,
        nombres: str,
        apellidos: str,
        especialidad:str,
        telefono: int,
        estado: bool,
        consultorio: str,
        hospital: str
) -> Optional[Dict[str, Any]]:
    """
    (CREATE) Agrega un nuevo medico a la agenda.

    Valida que el número de documento no exista antes de agregarlo.

    Args:
        filepath (str): Ruta al archivo de datos.
        tipo_documento (str): Abreviatura del tipo de documento (ej. 'C.C').
        documento (int): Número de documento del medico.
        nombres (str): Nombres del medico.
        apellidos (str): Apellidos del medico.
        especialidad (str): especialidad del medico.
        telefono (int): Número de teléfono.
        estado (bool): Estado del medico.
        consultorio (str): Consultorio del que esta asignado el medico.
        hospital (str): Hospital para que esta asignado el medico.

    Returns:
        Optional[Dict[str, Any]]: El diccionario del medico creado o None si ya existía.
    """
    medicos = gestor_datos.cargar_datos(filepath)
    str_documento = str(documento)

    if any(ap.get('documento') == str_documento for ap in medicos):
        print(f"\n Error: El documento '{str_documento}' ya se encuentra registrado.")
        return None

    nuevo_id = generar_id(medicos)

    nuevo_medicos = {
        'id': str(nuevo_id),
        'tipo_documento': tipo_documento,
        'documento': str_documento,
        'nombres': nombres,
        'apellidos': apellidos,
        'especialidad': especialidad,
        'telefono': str(telefono),
        'estado': bool(estado),
        'consultorio': consultorio,
        'hospital': hospital 
    }

    medicos.append(nuevo_medicos)
    gestor_datos.guardar_datos(filepath, medicos)
    return nuevo_medicos

def leer_todos_los_pacientes(filepath: str) -> List[Dict[str, Any]]:
    """
    (READ) Obtiene la lista completa de los medicos .

    Args:
        filepath (str): Ruta al archivo de datos.

    Returns:
        List[Dict[str, Any]]: La lista de medicos.
    """
    return gestor_datos.cargar_datos(filepath)

def buscar_medico_por_documento(filepath: str, documento: str) -> Optional[Dict[str, Any]]:
    """
    Busca un medico específico por su número de documento.

    Args:
        filepath (str): Ruta al archivo de datos.
        documento (str): El documento a buscar.

    Returns:
        Optional[Dict[str, Any]]: El diccionario del medico si se encuentra, de lo contrario None.
    """
    medicos = gestor_datos.cargar_datos(filepath)
    for medico in medicos:
        if medico.get('documento') == documento:
            return medico
    return None

def actualizar_medicos(
        filepath: str,
        documento: str,
        datos_nuevos: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """
    (UPDATE) Modifica los datos de un medico existente.

    Args:
        filepath (str): Ruta al archivo de datos.
        documento (str): El documento del medico a actualizar.
        datos_nuevos (Dict[str, Any]): Un diccionario con los campos a actualizar.

    Returns:
        Optional[Dict[str, Any]]: El diccionario del paciente actualizado, o None si no se encontró.
    """
    medicos = gestor_datos.cargar_datos(filepath)
    medicos_encontrado = None
    indice = -1

    for i, aprendiz in enumerate(medicos):
        if medicos.get('documento') == documento:
            medicos_encontrado = medicos
            indice = i
            break

    if medicos_encontrado:
        # Convertimos todos los nuevos valores a string para consistencia
        for key, value in datos_nuevos.items():
            datos_nuevos[key] = str(value)

        medicos_encontrado.update(datos_nuevos)
        medicos[indice] = medicos_encontrado
        gestor_datos.guardar_datos(filepath, medicos)
        return medicos_encontrado

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
    medicos = gestor_datos.cargar_datos(filepath)
    medico_a_eliminar = None

    for medico in medicos:
        if medico.get('documento') == documento:
            medico_a_eliminar = medico
            break

    if medico_a_eliminar:
        medico.remove(medico_a_eliminar)
        gestor_datos.guardar_datos(filepath, medicos)
        return True

    return False

