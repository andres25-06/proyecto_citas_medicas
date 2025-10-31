import pytest
from Controlador import gestor_datos_medico as gestor


# TEST JSON
def test_crud_medicos_json(tmp_path):
    filepath = tmp_path / "medicos.json"

    # Inicializar archivo
    gestor.inicializar_archivo(str(filepath))

    medico = {
        "id": "1",
        "tipo_documento": "CC",
        "documento": "12345678",
        "nombres": "Laura",
        "apellidos": "Mora",
        "direccion": "Calle 1",
        "especialidad": "Cardiología",
        "telefono": "3125554444",
        "estado": "activo",
        "consultorio": "101",
        "hospital": "Hospital Central"
    }

    # CREAR
    datos = gestor.cargar_datos(str(filepath))
    datos.append(medico)
    gestor.guardar_datos(str(filepath), datos)

    # LEER
    lista = gestor.cargar_datos(str(filepath))
    assert len(lista) == 1
    assert lista[0]["nombres"] == "Laura"

    # ACTUALIZAR
    lista[0]["especialidad"] = "Dermatología"
    gestor.guardar_datos(str(filepath), lista)
    actualizado = gestor.cargar_datos(str(filepath))
    assert actualizado[0]["especialidad"] == "Dermatología"

    # ELIMINAR
    actualizado.pop(0)
    gestor.guardar_datos(str(filepath), actualizado)
    final = gestor.cargar_datos(str(filepath))
    assert final == []

# TEST CSV
def test_crud_medicos_csv(tmp_path):
    filepath = tmp_path / "medicos.csv"

    # Inicializar archivo
    gestor.inicializar_archivo(str(filepath))

    medico = {
        "id": "2",
        "tipo_documento": "CC",
        "documento": "87654321",
        "nombres": "Carlos",
        "apellidos": "Ruiz",
        "direccion": "Calle 2",
        "especialidad": "Pediatría",
        "telefono": "3101239876",
        "estado": "activo",
        "consultorio": "102",
        "hospital": "Hospital Norte"
    }

    # CREAR
    datos = gestor.cargar_datos(str(filepath))
    datos.append(medico)
    gestor.guardar_datos(str(filepath), datos)

    # LEER
    lista = gestor.cargar_datos(str(filepath))
    assert len(lista) == 1
    assert lista[0]["nombres"] == "Carlos"

    # ACTUALIZAR
    lista[0]["especialidad"] = "Neurología"
    gestor.guardar_datos(str(filepath), lista)
    actualizado = gestor.cargar_datos(str(filepath))
    assert actualizado[0]["especialidad"] == "Neurología"

    # ELIMINAR
    actualizado.pop(0)
    gestor.guardar_datos(str(filepath), actualizado)
    final = gestor.cargar_datos(str(filepath))
    assert final == []
