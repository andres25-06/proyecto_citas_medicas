import pytest
import json
from unittest.mock import patch
from Validaciones.validar_campos import (
    validar_texto,
    validar_numero,
    validar_telefono,
    validar_cedula
)