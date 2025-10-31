# tests/test_vista_principal.py
# -- coding: utf-8 --

import io
import json

import Vista.vista_principal as vp

# --------------------------------------------------------------------
# UTILIDADES Y ENTRADA / SALIDA
# --------------------------------------------------------------------

def test_limpiar(monkeypatch):
    """Debe ejecutar el comando adecuado según el sistema operativo."""
    called = {}
    def fake_system(cmd):
        called["cmd"] = cmd
    monkeypatch.setattr("os.system", fake_system)
    vp.limpiar()
    assert "cls" in called["cmd"] or "clear" in called["cmd"]


def test_animacion_carga(monkeypatch):
    """Verifica que imprime el mensaje y puntos."""
    fake_prints = []
    monkeypatch.setattr(vp.console, "print", lambda *a, **k: fake_prints.append(a[0]))
    monkeypatch.setattr("time.sleep", lambda x: None)
    vp.animacion_carga("Cargando test...")
    assert any("Cargando" in str(p) for p in fake_prints)


def test_escribir_mensaje(monkeypatch):
    """Debe imprimir los caracteres con color."""
    salida = io.StringIO()
    monkeypatch.setattr(vp.console, "print", lambda *a, **k: print(*a, file=salida))
    monkeypatch.setattr("time.sleep", lambda x: None)
    vp.escribir_mensaje("Hola", velocidad=0)
    contenido = salida.getvalue()
    assert "H" in contenido and "a" in contenido


# --------------------------------------------------------------------
# JSON / CSV
# --------------------------------------------------------------------

def test_cargar_y_guardar_json(tmp_path):
    """Debe guardar y leer datos JSON correctamente."""
    ruta = tmp_path / "test.json"
    datos = [{"id": 1, "nombre": "Juan"}]
    vp.guardar_json(str(ruta), datos)
    resultado = vp.cargar_json(str(ruta))
    assert resultado == datos


def test_cargar_csv_simple(tmp_path):
    """Debe cargar un CSV y devolver una lista de diccionarios."""
    ruta = tmp_path / "datos.csv"
    contenido = "id,nombre\n1,Juan\n2,Ana\n"
    ruta.write_text(contenido, encoding="utf-8")
    resultado = vp.cargar_csv_simple(str(ruta))
    assert len(resultado) == 2
    assert resultado[0]["id"] == "1"


# --------------------------------------------------------------------
# FUNCIONES VISUALES
# --------------------------------------------------------------------

def test_mostrar_tabla_generica(monkeypatch):
    """Debe mostrar tabla o advertir si no hay datos."""
    salida = []
    monkeypatch.setattr(vp.console, "print", lambda x, **k: salida.append(str(x)))
    datos = [{"nombre": "Juan", "edad": 30}]
    vp.mostrar_tabla_generica(datos, ["Nombre", "Edad"], titulo="Usuarios")
    assert any("Usuarios" in s for s in salida)


def test_buscador():
    """Debe encontrar elementos por coincidencia insensible a mayúsculas."""
    datos = [{"nombre": "Juan"}, {"nombre": "Ana"}]
    res = vp.buscador(datos, "nombre", "ju")
    assert len(res) == 1 and res[0]["nombre"] == "Juan"


def test_enriquecer_citas(tmp_path):
    """Debe añadir nombres de paciente y médico desde CSV."""
    ruta_pacientes = tmp_path / "pacientes.csv"
    ruta_medicos = tmp_path / "medicos.csv"
    ruta_pacientes.write_text("id_paciente,nombre\n1,Juan\n", encoding="utf-8")
    ruta_medicos.write_text("id_medico,nombre\nM1,Dr. Pérez\n", encoding="utf-8")
    citas = [{"id_paciente": "1", "id_medico": "M1"}]
    resultado = vp.enriquecer_citas(citas, str(ruta_pacientes), str(ruta_medicos))
    assert resultado[0]["paciente_nombre"] == "Juan"
    assert resultado[0]["medico_nombre"].startswith("Dr.")


# --------------------------------------------------------------------
# MENÚ SIMPLE E INTERACTIVO
# --------------------------------------------------------------------

def test_mostrar_menu_simple(monkeypatch):
    """Simula selección de opción por input."""
    monkeypatch.setattr(vp, "limpiar", lambda: None)
    monkeypatch.setattr(vp.console, "print", lambda *a, **k: None)
    monkeypatch.setattr(vp.console, "input", lambda _: "3")
    opcion = vp.mostrar_menu_simple()
    assert opcion == "3"


def test_selector_interactivo(monkeypatch):
    """Simula navegación y selección con readchar."""
    teclas = [vp.readchar.key.DOWN, vp.readchar.key.ENTER]
    monkeypatch.setattr("readchar.readkey", lambda: teclas.pop(0))
    monkeypatch.setattr(vp, "limpiar", lambda: None)
    monkeypatch.setattr(vp.console, "print", lambda *a, **k: None)
    opciones = ["A", "B", "Salir"]
    indice = vp.selector_interactivo("Título", opciones)
    assert indice == 1


# --------------------------------------------------------------------
# FUNCIONES QUE ACCEDEN A ARCHIVOS
# --------------------------------------------------------------------

def test_mostrar_citas_por_dia(tmp_path, monkeypatch):
    """Debe eliminar cita si se selecciona ID válido."""
    ruta = tmp_path / "citas.json"
    datos = [{"id": "1", "fecha": "2025-10-27"}]
    ruta.write_text(json.dumps(datos))
    monkeypatch.setattr(vp, "limpiar", lambda: None)
    monkeypatch.setattr(vp, "enriquecer_citas", lambda x, **k: x)
    monkeypatch.setattr(vp.console, "print", lambda *a, **k: None)
    monkeypatch.setattr(vp.console, "input", lambda *a, **k: "1")
    monkeypatch.setattr("time.sleep", lambda x: None)
    vp.mostrar_citas_por_dia(2025, 10, 27, str(ruta))
    nuevo = json.loads(ruta.read_text())
    assert nuevo == []


# --------------------------------------------------------------------
# PRUEBA DE ESTADÍSTICAS
# --------------------------------------------------------------------

def test_estadisticas_citas_por_medico(tmp_path, monkeypatch):
    """Debe mostrar tabla de estadísticas sin errores."""
    ruta_med = tmp_path / "medicos.csv"
    ruta_citas = tmp_path / "citas.json"
    ruta_med.write_text("id,nombres,apellidos,especialidad\na1,Carlos,Ramírez,Cardiólogo\n", encoding="utf-8")
    ruta_citas.write_text(json.dumps([{"id_medico": "a1"}]), encoding="utf-8")
    monkeypatch.setattr(vp.console, "print", lambda *a, **k: None)
    monkeypatch.setattr(vp.console, "input", lambda *a, **k: "")
    vp.estadisticas_citas_por_medico(str(ruta_med), str(ruta_citas))
    # Si no lanza excepción, el test pasa
    assert True

def test_estadisticas_citas_por_especialidad(tmp_path, monkeypatch):
    """Debe mostrar tabla de estadísticas por especialidad sin errores."""
    ruta_med = tmp_path / "medicos.csv"
    ruta_citas = tmp_path / "citas.json"
    ruta_med.write_text("id,nombres,apellidos,especialidad\na1,Carlos,Ramírez,Cardiólogo\n", encoding="utf-8")
    ruta_citas.write_text(json.dumps([{"id_medico": "a1"}]), encoding="utf-8")
    monkeypatch.setattr(vp.console, "print", lambda *a, **k: None)
    monkeypatch.setattr(vp.console, "input", lambda *a, **k: "")
    vp.estadisticas_citas_por_especialidad(str(ruta_med), str(ruta_citas))
    # Si no lanza excepción, el test pasa
    assert True
