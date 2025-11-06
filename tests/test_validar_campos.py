import builtins

from Validaciones import validar_campos


# ===========================================================
# VALIDAR TEXTO
# ===========================================================
def test_validar_texto_valido(monkeypatch):
    # Simula que el usuario escribe "Hola"
    monkeypatch.setattr(validar_campos.Prompt, "ask", lambda *a, **k: "Hola")
    assert validar_campos.validar_texto("Nombre") == "Hola"


def test_validar_texto_vacio(monkeypatch):
    # Simula respuestas: "" (vacío) y luego "Correcto"
    respuestas = iter(["", "Correcto"])
    monkeypatch.setattr(validar_campos.Prompt, "ask", lambda *a, **k: next(respuestas))
    assert validar_campos.validar_texto("Campo") == "Correcto"


# ===========================================================
# VALIDAR NÚMERO
# ===========================================================
def test_validar_numero_valido(monkeypatch):
    monkeypatch.setattr(validar_campos.Prompt, "ask", lambda *a, **k: "25")
    assert validar_campos.validar_numero("Edad") == 25


def test_validar_numero_no_valido(monkeypatch):
    # Primero "abc" (inválido), luego "10" (válido)
    respuestas = iter(["abc", "10"])
    monkeypatch.setattr(validar_campos.Prompt, "ask", lambda *a, **k: next(respuestas))
    assert validar_campos.validar_numero("Edad") == 10


# ===========================================================
# VALIDAR TELÉFONO
# ===========================================================
def test_validar_telefono(monkeypatch):
    monkeypatch.setattr(validar_campos.Prompt, "ask", lambda *a, **k: "3124567890")
    assert validar_campos.validar_telefono("Teléfono") == "3124567890"


# ===========================================================
# VALIDAR CÉDULA (sin duplicado)
# ===========================================================
def test_validar_cedula_json(tmp_path, monkeypatch):
    filepath = tmp_path / "personas.json"
    filepath.write_text("[]", encoding="utf-8")

    monkeypatch.setattr(validar_campos.Prompt, "ask", lambda *a, **k: "123456")
    assert validar_campos.validar_cedula("Cédula", str(filepath)) == "123456"


# ===========================================================
# VALIDAR HORA (usa input())
# ===========================================================
def test_validar_hora_valida(monkeypatch):
    # Simula input del usuario: "09:30"
    monkeypatch.setattr(builtins, "input", lambda *a, **k: "09:30")
    assert validar_campos.validar_hora("hora") == "09:30"


def test_validar_hora_invalida(monkeypatch):
    # Responde primero "20:00" (fuera de rango), luego "07:15"
    respuestas = iter(["20:00", "07:15"])
    monkeypatch.setattr(builtins, "input", lambda *a, **k: next(respuestas))
    assert validar_campos.validar_hora("hora") == "07:15"
