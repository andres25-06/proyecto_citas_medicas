# tests/test_gestor_datos_pacientes.py
# -*- coding: utf-8 -*-
from Controlador import gestor_datos_pacientes as gestor


# TEST JSON
def test_crud_pacientes_json(tmp_path):
    filepath = tmp_path / "pacientes.json"

    # Inicializar archivo
    gestor.inicializar_archivo(str(filepath))

    paciente = {
        "id": "1",
        "tipo_documento": "CC",
        "documento": "111",
        "nombres": "Juan",
        "apellidos": "Pérez",
        "direccion": "Calle 1",
        "telefono": "3001234567"
    }

    # CREAR
    datos = gestor.cargar_datos(str(filepath))
    datos.append(paciente)
    gestor.guardar_datos(str(filepath), datos)

    # LEER
    lista = gestor.cargar_datos(str(filepath))
    assert len(lista) == 1
    assert lista[0]["nombres"] == "Juan"

    # ACTUALIZAR
    lista[0]["direccion"] = "Calle 2"
    gestor.guardar_datos(str(filepath), lista)
    actualizado = gestor.cargar_datos(str(filepath))
    assert actualizado[0]["direccion"] == "Calle 2"

    # ELIMINAR
    actualizado.pop(0)
    gestor.guardar_datos(str(filepath), actualizado)
    final = gestor.cargar_datos(str(filepath))
    assert final == []

# TEST CSV
def test_crud_pacientes_csv(tmp_path):
    filepath = tmp_path / "pacientes.csv"

    # Inicializar archivo
    gestor.inicializar_archivo(str(filepath))

    paciente = {
        "id": "2",
        "tipo_documento": "TI",
        "documento": "222",
        "nombres": "Ana",
        "apellidos": "López",
        "direccion": "Calle 3",
        "telefono": "3019998877"
    }

    # CREAR
    datos = gestor.cargar_datos(str(filepath))
    datos.append(paciente)
    gestor.guardar_datos(str(filepath), datos)

    # LEER
    lista = gestor.cargar_datos(str(filepath))
    assert len(lista) == 1
    assert lista[0]["nombres"] == "Ana"

    # ACTUALIZAR
    lista[0]["direccion"] = "Calle 4"
    gestor.guardar_datos(str(filepath), lista)
    actualizado = gestor.cargar_datos(str(filepath))
    assert actualizado[0]["direccion"] == "Calle 4"

    # ELIMINAR
    actualizado.pop(0)
    gestor.guardar_datos(str(filepath), actualizado)
    final = gestor.cargar_datos(str(filepath))
    assert final == []
