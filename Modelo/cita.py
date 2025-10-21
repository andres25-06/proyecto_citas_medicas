# -*- coding: utf-8 -*-
"""
Módulo de Lógica de Negocio - Citas

Contiene todas las funciones para gestionar las citas (CRUD).
Este módulo utiliza 'gestor_datos' para la persistencia.
"""

from typing import Any, Dict, List, Optional
from Controlador import gestor_datos


def generar_id(citas: List[Dict[str, Any]]) -> int:
    """
    Genera un nuevo ID autoincremental para una cita.

    Args:
        citas (List[Dict[str, Any]]): La lista actual de las citas.

    Returns:
        int: El nuevo ID a asignar.
    """
    if not citas:
        return 1
    max_id = max(int(cita.get('id', 0)) for cita in citas)
    return max_id + 1


def crear_cita(
        filepath: str,
        documento_paciente: str,
        documento_medico: str,
        fecha: str,
        hora: str,
        motivo: str,
        estado: str
) -> Optional[Dict[str, Any]]:
    """
    (CREATE) Agrega una nueva cita.

    Valida que no exista una cita para el mismo paciente, médico, fecha y hora.

    Args:
        filepath (str): Ruta al archivo de datos.
        documento_paciente (str): Documento del paciente.
        documento_medico (str): Documento del médico.
        fecha (str): Fecha de la cita (YYYY-MM-DD).
        hora (str): Hora de la cita (HH:MM).
        motivo (str): Motivo de la cita.
        estado (str): Estado actual de la cita (ej. 'Pendiente', 'Completada', 'Cancelada').

    Returns:
        Optional[Dict[str, Any]]: El diccionario de la cita creada o None si ya existía.
    """
    citas = gestor_datos.cargar_datos(filepath)

    # Validar si ya existe una cita para el mismo paciente, médico, fecha y hora
    for cita in citas:
        if (cita.get('documento_paciente') == documento_paciente and
            cita.get('documento_medico') == documento_medico and
            cita.get('fecha') == fecha and
            cita.get('hora') == hora):
            print(f"\n Error: Ya existe una cita registrada para ese paciente, médico, fecha y hora.")
            return None

    nuevo_id = generar_id(citas)

    nueva_cita = {
        'id': str(nuevo_id),
        'documento_paciente': documento_paciente,
        'documento_medico': documento_medico,
        'fecha': fecha,
        'hora': hora,
        'motivo': motivo,
        'estado': estado
    }

    citas.append(nueva_cita)
    gestor_datos.guardar_datos(filepath, citas)
    return nueva_cita


def leer_todas_las_citas(filepath: str) -> List[Dict[str, Any]]:
    """
    (READ) Obtiene la lista completa de las citas.

    Args:
        filepath (str): Ruta al archivo de datos.

    Returns:
        List[Dict[str, Any]]: La lista de citas.
    """
    return gestor_datos.cargar_datos(filepath)


def buscar_cita_por_id(filepath: str, id_cita: str) -> Optional[Dict[str, Any]]:
    """
    Busca una cita específica por su ID.

    Args:
        filepath (str): Ruta al archivo de datos.
        id_cita (str): ID de la cita a buscar.

    Returns:
        Optional[Dict[str, Any]]: El diccionario de la cita si se encuentra, de lo contrario None.
    """
    citas = gestor_datos.cargar_datos(filepath)
    for cita in citas:
        if cita.get('id') == id_cita:
            return cita
    return None


def actualizar_cita(
        filepath: str,
        id_cita: str,
        datos_nuevos: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """
    (UPDATE) Modifica los datos de una cita existente.

    Args:
        filepath (str): Ruta al archivo de datos.
        id_cita (str): El ID de la cita a actualizar.
        datos_nuevos (Dict[str, Any]): Un diccionario con los campos a actualizar.

    Returns:
        Optional[Dict[str, Any]]: El diccionario de la cita actualizada, o None si no se encontró.
    """
    citas = gestor_datos.cargar_datos(filepath)
    cita_encontrada = None
    indice = -1

    for i, cita in enumerate(citas):
        if cita.get('id') == id_cita:
            cita_encontrada = cita
            indice = i
            break

    if cita_encontrada:
        # Convertimos todos los nuevos valores a string para consistencia
        for key, value in datos_nuevos.items():
            datos_nuevos[key] = str(value)

        cita_encontrada.update(datos_nuevos)
        citas[indice] = cita_encontrada
        gestor_datos.guardar_datos(filepath, citas)
        return cita_encontrada

    return None


def eliminar_cita(filepath: str, id_cita: str) -> bool:
    """
    (DELETE) Elimina una cita por su ID.

    Args:
        filepath (str): Ruta al archivo de datos.
        id_cita (str): El ID de la cita a eliminar.

    Returns:
        bool: True si la cita fue eliminada, False si no se encontró.
    """
    citas = gestor_datos.cargar_datos(filepath)
    cita_a_eliminar = None

    for cita in citas:
        if cita.get('id') == id_cita:
            cita_a_eliminar = cita
            break

    if cita_a_eliminar:
        citas.remove(cita_a_eliminar)
        gestor_datos.guardar_datos(filepath, citas)
        return True

    return False
