# Vista/navegacion.py

from Vista import vista_principal, vista_cita, vista_medico, vista_paciente


def ir_a_menu_principal():
    """Llama al menú principal."""
    vista_principal.vista_principal()


def ir_a_menu_citas():
    """Llama al menú de citas médicas."""
    vista_cita.main_vista_citas()


def ir_a_menu_medicos():
    """Llama al menú de gestión de médicos."""
    vista_medico.main_vista_medicos()


def ir_a_menu_pacientes():
    """Llama al menú de gestión de pacientes."""
    vista_paciente.main_vista_pacientes()
