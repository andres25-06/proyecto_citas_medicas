import csv
import json
import os

from Modelo import medico, paciente


def obtener_nombre_completo_por_documento(
    filepath: str, documento: str, tipo: str
    ) -> str:
    """
    Devuelve el nombre completo de un paciente o médico según su documento.
    Args:
        filepath (str): Ruta al archivo de datos (JSON o CSV).
        documento (str): Documento del paciente o médico.
        tipo (str): "paciente" o "medico".
    Returns:
        str: Nombre completo o mensaje de no encontrado.
    """
    try:
        registros = []
        if tipo == "paciente":
            # Intentar JSON
            try:
                registros = paciente.leer_todos_los_pacientes(
                    "data/pacientes.json"
                    )
            except Exception:
                registros = []
            # Si no hay registros JSON, intentar CSV
            if not registros:
                try:
                    registros = paciente.leer_todos_los_pacientes(
                        "data/pacientes.csv"
                        )
                except Exception:
                    registros = []
        else:  # medico
            try:
                registros = medico.leer_todos_los_medicos(
                    "data/medicos.json"
                    )
            except Exception:
                registros = []
            if not registros:
                try:
                    registros = medico.leer_todos_los_medicos(
                        "data/medicos.csv"
                        )
                except Exception:
                    registros = []

        for r in registros:
            if r.get("documento") == documento:
                return f"{r.get('nombres', '')} {r.get(
                    'apellidos', ''
                    )}".strip()
        return f"{documento} (no encontrado)"
    except Exception as e:
        return f"Error: {e}"


def obtener_nombre_por_documento(
    filepath_base: str, documento: str
    ) -> str:
    """
    Busca el nombre completo de una persona
    (paciente o médico)
    por su documento en archivos JSON o CSV
    (busca en ambos si existen).
    Args:
        filepath_base (str): Ruta base sin
        extensión o con extensión (.json o .csv)
        documento (str): Documento a buscar
    Returns:
        str: Nombre completo o mensaje de error
    """
    documento = str(documento).strip()

    # Quitar extensión si viene incluida
    base, ext = os.path.splitext(filepath_base)
    if ext not in (".json", ".csv"):
        # Probar con ambas rutas
        rutas = [f"{base}.json", f"{base}.csv"]
    else:
        rutas = [filepath_base]

    for ruta in rutas:
        if not os.path.exists(ruta):
            continue

        try:
            # Leer JSON
            if ruta.endswith(".json"):
                with open(ruta, "r", encoding="utf-8") as f:
                    personas = json.load(f)
            # Leer CSV
            elif ruta.endswith(".csv"):
                with open(ruta, "r", encoding="utf-8") as f:
                    lector = csv.DictReader(f)
                    personas = list(lector)
            else:
                continue
        except Exception:
            continue

        # Buscar persona por documento
        for p in personas:
            doc = str(p.get("documento", "")).strip()
            if doc == documento:
                nombre = p.get("nombres", "") or p.get("nombre", "")
                apellido = p.get("apellidos", "") or p.get("apellido", "")
                if nombre and apellido:
                    return f"{nombre.strip()} {apellido.strip()}"
                elif nombre:
                    return nombre.strip()
                else:
                    return "Sin nombre"

    return "No encontrado"
