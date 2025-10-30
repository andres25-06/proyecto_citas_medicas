# -*- coding: utf-8 -*-
"""
Módulo de Lógica de Negocio - Médicos

Contiene todas las funciones para gestionar los médicos (CRUD).
Este módulo utiliza 'gestor_datos' para la persistencia.
"""

from typing import Any, Dict, List, Optional

from Controlador import gestor_datos_medico


def generar_id(medicos: List[Dict[str, Any]]) -> int:
    """
        Genera un nuevo ID autoincremental para un médico.

        Args:
            medicos (List[Dict[str, Any]]): Lista actual de los médicos.

        Returns:
            int: Nuevo ID a asignar.
    """
    if not medicos:
        return 1
    max_id = max(int(m.get('id', 0)) for m in medicos)
    return max_id + 1


def crear_medico(
        filepath: str,
        tipo_documento: str,
        documento: int,
        nombres: str,
        apellidos: str,
        especialidad: str,
        telefono: int,
        estado: str,
        consultorio: str,
) -> Optional[Dict[str, Any]]:
    """
    (CREATE) Agrega un nuevo médico.

    Args:
        filepath (str): Ruta del archivo de datos.
        tipo_documento (str): Tipo de documento (ej. 'C.C').
        documento (int): Número de documento.
        nombres (str): Nombres del médico.
        apellidos (str): Apellidos del médico.
        especialidad (str): Especialidad del médico.
        telefono (int): Teléfono del médico.
        estado (str): Estado ('Activo' o 'Inactivo').
        consultorio (str): Consultorio asignado.

    Returns:
        Optional[Dict[str, Any]]: El médico creado o None si ya existía.
    """
    medicos = gestor_datos_medico.cargar_datos(filepath)
    str_documento = str(documento)

    # --- Validar duplicado ---
    if any(m.get('documento') == str_documento for m in medicos):
        print(f"\n[bold red]⚠ Error:[/bold red] El documento '{str_documento}' ya se encuentra registrado.")
        return None

    # --- Generar nuevo ID ---
    nuevo_id = generar_id(medicos)

    nuevo_medico = {
        'id': str(nuevo_id),
        'tipo_documento': tipo_documento,
        'documento': str_documento,
        'nombres': nombres,
        'apellidos': apellidos,
        'especialidad': especialidad,
        'telefono': str(telefono),
        'estado': estado,
        'consultorio': consultorio,
    }

    # --- Guardar datos ---
    medicos.append(nuevo_medico)
    gestor_datos_medico.guardar_datos(filepath, medicos)

    return nuevo_medico

def leer_todos_los_medicos(filepath: str) -> List[Dict[str, Any]]:
    """
        (READ) Obtiene la lista completa de los médicos.

        Args:
            filepath (str): Ruta al archivo de datos.

        Returns:
            List[Dict[str, Any]]: Lista de médicos.
    """
    return gestor_datos_medico.cargar_datos(filepath)


def buscar_medico_por_documento(filepath: str, documento: str) -> Optional[Dict[str, Any]]:
    """
        (READ) Busca un médico por su número de documento.

        Args:
            filepath (str): Ruta al archivo de datos.
            documento (str): Documento a buscar.

        Returns:
            Optional[Dict[str, Any]]: El médico encontrado o None si no existe.
    """
    medicos = gestor_datos_medico.cargar_datos(filepath)
    for medico in medicos:
        if medico.get('documento') == documento:
            return medico
    return None


def actualizar_medico(filepath: str, documento: str, datos_nuevos: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
        (UPDATE) Actualiza los datos de un médico existente.

        Args:
            filepath (str): Ruta del archivo de datos.
            documento (str): Documento del médico a actualizar.
            datos_nuevos (Dict[str, Any]): Campos a actualizar.

        Returns:
            Optional[Dict[str, Any]]: Médico actualizado o None si no se encontró.
    """
    medicos = gestor_datos_medico.cargar_datos(filepath)
    medico_encontrado = None
    indice = -1

    for i, m in enumerate(medicos):
        if m.get('documento') == documento:
            medico_encontrado = m
            indice = i
            break

    if medico_encontrado:
        for key, value in datos_nuevos.items():
            medico_encontrado[key] = str(value)

        medicos[indice] = medico_encontrado
        gestor_datos_medico.guardar_datos(filepath, medicos)
        return medico_encontrado

    return None


def eliminar_medico(filepath: str, documento: str) -> bool:
    """
        (DELETE) Elimina un medico de la agenda.

        Args:
            filepath (str): Ruta al archivo de datos.
            documento (str): El documento del medico a eliminar.

        Returns:
            bool: True si el medico fue eliminado, False si no se encontró.
    """
    medicos = gestor_datos_medico.cargar_datos(filepath)
    medico_a_eliminar = None

    # Buscar el paciente
    for medico in medicos:
        if medico.get('documento') == documento:
            medico_a_eliminar = medico
            break

    # Eliminarlo si existe
    if medico_a_eliminar:
        medicos.remove(medico_a_eliminar)
        gestor_datos_medico.guardar_datos(filepath, medicos)
        return True

    return False
