import io
import json

from rich.console import Console

import Vista.vista_principal as vp


def test_limpiar(monkeypatch):
    called = {}
    def fake_system(cmd):
        called["cmd"] = cmd
    monkeypatch.setattr("os.system", fake_system)
    vp.limpiar()
    assert "cls" in called["cmd"] or "clear" in called["cmd"]


def test_animacion_carga(monkeypatch):
    fake_prints = []
    monkeypatch.setattr(vp.console, "print", lambda *a, **k: fake_prints.append(a[0]))
    monkeypatch.setattr("time.sleep", lambda x: None)
    vp.animacion_carga("Cargando test...")
    assert any("Cargando" in str(p) for p in fake_prints)


def test_escribir_mensaje(monkeypatch):
    salida = io.StringIO()
    monkeypatch.setattr(vp.console, "print", lambda *a, **k: print(*a, file=salida))
    monkeypatch.setattr("time.sleep", lambda x: None)
    vp.escribir_mensaje("Hola", velocidad=0)
    contenido = salida.getvalue()
    assert "H" in contenido and "a" in contenido


def test_cargar_y_guardar_json(tmp_path):
    ruta = tmp_path / "test.json"
    datos = [{"id": 1, "nombre": "Juan"}]
    vp.guardar_json(str(ruta), datos)
    resultado = vp.cargar_json(str(ruta))
    assert resultado == datos


def test_cargar_csv_simple(tmp_path):
    ruta = tmp_path / "datos.csv"
    contenido = "id,nombre\n1,Juan\n2,Ana\n"
    ruta.write_text(contenido, encoding="utf-8")
    resultado = vp.cargar_csv_simple(str(ruta))
    assert len(resultado) == 2
    assert resultado[0]["id"] == "1"



def test_mostrar_tabla_generica():
    # Crear buffer para capturar salida
    buf = io.StringIO()
    # Crear consola Rich que escribe en buffer
    test_console = Console(file=buf, width=60)
    # Guardar consola original para restaurar luego
    original_console = vp.console
    # Reemplazar la consola del módulo por la consola de prueba
    vp.console = test_console

    datos = [{"nombre": "Juan", "edad": 30}]
    columnas = ["Nombre", "Edad"]
    titulo = "Usuarios"

    # Llamar a la función con consola parcheada
    vp.mostrar_tabla_generica(datos, columnas, titulo)

    # Restaurar consola original
    vp.console = original_console

    # Obtener salida capturada
    output = buf.getvalue()

    # Comprobar que la salida sea la esperada
    assert titulo in output



def test_buscador():
    datos = [{"nombre": "Juan"}, {"nombre": "Ana"}]
    res = vp.buscador(datos, "nombre", "ju")
    assert len(res) == 1 and res[0]["nombre"] == "Juan"


def test_enriquecer_citas(tmp_path):
    ruta_pacientes = tmp_path / "pacientes.csv"
    ruta_medicos = tmp_path / "medicos.csv"
    ruta_pacientes.write_text("id_paciente,nombre\n1,Juan\n", encoding="utf-8")
    ruta_medicos.write_text("id_medico,nombre\nM1,Dr. Pérez\n", encoding="utf-8")
    citas = [{"id_paciente": "1", "id_medico": "M1"}]
    resultado = vp.enriquecer_citas(citas, str(ruta_pacientes), str(ruta_medicos))
    assert resultado[0]["paciente_nombre"] == "Juan"
    assert resultado[0]["medico_nombre"].startswith("Dr.")


def test_mostrar_menu_simple(monkeypatch):
    monkeypatch.setattr(vp, "limpiar", lambda: None)
    monkeypatch.setattr(vp.console, "print", lambda *a, **k: None)
    monkeypatch.setattr(vp.console, "input", lambda _: "3")
    opcion = vp.mostrar_menu_simple()
    assert opcion == "3"


def test_selector_interactivo(monkeypatch):
    teclas = [vp.readchar.key.DOWN, vp.readchar.key.ENTER]
    monkeypatch.setattr("readchar.readkey", lambda: teclas.pop(0))
    monkeypatch.setattr(vp, "limpiar", lambda: None)
    monkeypatch.setattr(vp.console, "print", lambda *a, **k: None)
    opciones = ["A", "B", "Salir"]
    indice = vp.selector_interactivo("Título", opciones)
    assert indice == 1


def test_mostrar_citas_por_dia(tmp_path, monkeypatch):
    archivo = tmp_path / "citas.json"
    citas = [{"id": "1", "fecha": "2025-10-27"}]
    archivo.write_text(json.dumps(citas), encoding="utf-8")

    monkeypatch.setattr(vp, "limpiar", lambda: None)
    # Parchear enriquecer_citas para evitar carga archivos CSV reales
    monkeypatch.setattr(vp, "enriquecer_citas", lambda x, **kw: x)
    # Parchear mostrar_tabla_citas para no imprimir realmente
    monkeypatch.setattr(vp, "mostrar_tabla_citas", lambda *args, **kwargs: None)
    # Simula que el usuario ingresa el ID de la cita para cancelar "1"
    monkeypatch.setattr(vp.console, "input", lambda *a, **k: "1")
    monkeypatch.setattr("time.sleep", lambda x: None)

    vp.mostrar_citas_por_dia(2025, 10, 27, str(archivo))

    # El archivo debe quedar vacío tras cancelar la cita
    contenido_final = json.loads(archivo.read_text(encoding="utf-8"))
    assert contenido_final == []



def test_estadisticas_citas_por_medico(tmp_path, monkeypatch):
    ruta_medicos = tmp_path / "medicos.csv"
    ruta_citas = tmp_path / "citas.json"
    ruta_medicos.write_text("id,nombres,apellidos,especialidad\na1,Carlos,Ramírez,Cardiólogo\n", encoding="utf-8")
    ruta_citas.write_text(json.dumps([{"id_medico": "a1"}]), encoding="utf-8")

    monkeypatch.setattr(vp.console, "print", lambda *a, **k: None)
    monkeypatch.setattr(vp.console, "input", lambda *a, **k: "")
    vp.estadisticas_citas_por_medico(str(ruta_medicos), str(ruta_citas))

    assert True
