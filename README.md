# 💉✨ Sistema de Gestión de Citas Médicas — Grupo 5  

> 🩺 Proyecto en **consola** desarrollado en **Python** para gestionar pacientes, médicos y la programación de citas en un consultorio.  
> 🎨 Interfaz de usuario enriquecida con `rich`, persistencia con CSV y JSON, validaciones estrictas (incluida prevención de doble reserva) y calidad garantizada con `ruff` y `pytest`.

---

## 📚 Índice

0️⃣ **Integrantes**  
1️⃣ Descripción general  
2️⃣ Objetivos y alcance  
3️⃣ Entidades y formatos de datos  
4️⃣ Funcionalidades principales  
5️⃣ Estructura del proyecto  
6️⃣ Requisitos e instalación  
7️⃣ Uso — comandos y ejemplos  
8️⃣ Validaciones y reglas de negocio  
9️⃣ Calidad, pruebas y linters  
🔟 Buenas prácticas de Git  
1️⃣1️⃣ Ejemplos de archivos  

---

## 🧑‍💻 0. Integrantes
 
**Desarrolladores:**  
- 👨‍💻 Developer 1 - Backend y Frontend : **EIDER ANDRES ARDILA PITA**  
- 👨‍💻 Developer 2 - Backend y Frontend : **JIMY SEBASTIAN ANGARITA TRIANA**  
- 👨‍💻 Developer 3 - Backend : **MARIA KAMILA FUENTES VARGAS**  
- 👨‍💻 Developer 4 - QA y Test : **SERGIO ALEJANDRO GARCIA SOSA**

**Ficha:** 2993648  
**Programa de Formación:** Análisis y Desarrollo de Software  
**Centro de Formación:** Centro Minero  

**Instructores:**  
- 🧑‍🏫 Instructor 1: Andres Felipe Sandoval  
- 👩‍🏫 Instructor 2: Diego Ojeda  

---

## 🩺 1. Descripción general

Este proyecto es un **Sistema de Gestión de Citas Médicas** para consola, que permite:

✅ Administrar **pacientes** y **médicos** (CRUD completo).  
✅ **Agendar y cancelar citas** con validaciones.  
✅ **Evitar solapamientos** de horarios.  
✅ Mostrar toda la información con tablas y paneles elegantes gracias a `rich`.

> 💡 Diseñado para consultorios pequeños, con enfoque académico y código limpio y modular.

---

## 🎯 2. Objetivos y alcance

### 🎯 Objetivo general
Desarrollar un sistema modular, validado y testeable que cumpla los requisitos funcionales de gestión de citas médicas.

### 🎯 Objetivos específicos
- Registrar y persistir **pacientes y médicos** (CSV).  
- Gestionar **citas** en formato JSON.  
- Prevenir conflictos de horarios para médicos.  
- Mantener estándares de calidad (tipado, docstrings, linters y pruebas).  
- Cumplir con los lineamientos del curso (uso de `pytest`, `ruff`, modularidad y validaciones robustas).  

---

## 🧾 3. Entidades y formatos de datos

### 👨‍⚕️ Médicos — `medicos.csv`

| Campo | Tipo | Descripción |
|-------|------|--------------|
| `id_medico` | str/int | Identificador único |
| `nombre` | str | Nombre completo |
| `especialidad` | str | Área médica |

#### Ejemplo:
```csv
id_medico,nombre,especialidad
1,Dr. Carlos Ruiz,Cardiología
2,Dr. Ana Torres,Pediatría
```

---

### 🧍 Pacientes — `pacientes.csv`

| Campo | Tipo | Descripción |
|-------|------|--------------|
| `id_paciente` | str/int | Identificador único |
| `nombre` | str | Nombre del paciente |
| `telefono` | str | Teléfono de contacto |

#### Ejemplo:
```csv
id_paciente,nombre,telefono
1,María Pérez,3001234567
2,Juan Gómez,3109876543
```

---

### 📅 Citas — `citas.json`

| Clave | Tipo | Ejemplo |
|-------|------|----------|
| `id_cita` | str/int | "1" |
| `id_paciente` | str/int | "10" |
| `id_medico` | str/int | "3" |
| `fecha` | str (YYYY-MM-DD) | "2025-12-01" |
| `hora` | str (HH:MM) | "09:30" |
| `motivo_consulta` | str | "Control general" |

#### Ejemplo:
```json
[
  {
    "id_cita": "1",
    "id_paciente": "10",
    "id_medico": "3",
    "fecha": "2025-12-01",
    "hora": "09:30",
    "motivo_consulta": "Control general"
  }
]
```

---

## ⚙️ 4. Funcionalidades principales

### 🧩 Pacientes
- Crear, listar, editar y eliminar pacientes.

### 🧑‍⚕️ Médicos
- CRUD completo + búsqueda por especialidad.

### 📆 Citas
- Agendar y cancelar citas.  
- Listar citas por médico y fecha.  
- Validar disponibilidad de horario (sin solapamientos).

### 🎨 Interfaz visual en consola
- Tablas, paneles y colores usando `rich`.

---

## 🧱 5. Estructura del proyecto

```plaintext
PROYECTO_CITAS_MEDICAS/
├─ Controlador/
│  ├─ gestor_datos_citas.py
│  ├─ gestor_datos_medico.py
│  └─ gestor_datos_pacientes.py
├─ Modelo/
│  ├─ medico.py
│  ├─ paciente.py
│  └─ cita.py
├─ Validaciones/
│  ├─ entrada_datos.py
│  └─ validar_campos.py
├─ Vista/
│  ├─ vista_login.py
│  ├─ vista_medico.py
│  ├─ vista_paciente.py
│  ├─ vista_principal.py
│  └─ vista_superadmin.py
├─ data/
│  ├─ pacientes.csv
│  ├─ medicos.csv
│  └─ citas.json
├─ tests/
├─ pyproject.toml
├─ main.py
└─ README.md
```

---

## 💻 6. Requisitos e instalación

### 🔧 Requisitos
- Python 3.10 o superior  
- Librerías: `rich`, `pytest`, `ruff`

### 🚀 Instalación rápida
```bash
# Clonar el repositorio
git clone https://github.com/andres25-06/proyecto_citas_medicas.git

# Crear entorno virtual
uv venv .venv

# Activar entorno
# Windows
.\.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# Instalar dependencias
uv sync

# Ejecutar la aplicación
python main.py
```

---

## 🧠 7. Uso — comandos y ejemplos

### 🩺 Agendar una cita
1️⃣ Selecciona “Agendar cita”.  
2️⃣ Ingresa el ID del paciente.  
3️⃣ Ingresa el ID del médico.  
4️⃣ Indica la fecha (YYYY-MM-DD).  
5️⃣ Escribe la hora (HH:MM, formato 24h).  
6️⃣ Añade el motivo de la consulta.  

🟢 Si la hora está libre → la cita se guarda exitosamente.  
🔴 Si hay conflicto → se notifica al usuario y no se guarda.  

---

## 🧩 8. Validaciones y reglas de negocio
✔️ Validación de formato de fecha y hora.  
✔️ Confirmación de existencia de IDs válidos.  
✔️ Prevención de doble reserva (mismo médico, misma hora y fecha).  
✔️ Manejo robusto de errores (`try/except`).  
✔️ Responsabilidad única por función.  

---

## 🧪 9. Calidad, pruebas y linters

### 🧩 Pruebas unitarias
- CRUD de pacientes y médicos.  
- Agendamiento exitoso.  
- Rechazo por conflicto de horario.  
- Eliminación de cita.

### 🧹 Linting con Ruff
```bash
ruff check .
```

### 📏 Buenas prácticas
- Tipado estático (`type hints`).  
- Docstrings descriptivos.  
- Nombres coherentes y estilo uniforme.  

---

## 🌿 10. Buenas prácticas de Git

- Mensajes de commit claros y descriptivos.  
- Flujo con ramas por funcionalidad.  
- PRs con descripciones detalladas.  

```bash
git checkout -b feature/agendar-cita
git add .
git commit -m "✨ Agregar validación de duplicidad al agendar citas"
git push origin feature/agendar-cita
```

---

## 📂 11. Ejemplos de archivos

### 🧍 pacientes.csv
```csv
id_paciente,nombre,telefono
1,María Pérez,3001234567
2,Juan Gómez,3109876543
```

### 👨‍⚕️ medicos.csv
```csv
id_medico,nombre,especialidad
1,Dr. Carlos Ruiz,Cardiología
2,Dr. Ana Torres,Pediatría
```

### 📅 citas.json
```json
[
  {
    "id_cita": "1",
    "id_paciente": "1",
    "id_medico": "2",
    "fecha": "2025-11-20",
    "hora": "10:00",
    "motivo_consulta": "Consulta inicial"
  }
]
```

---

💚 **¡Gracias por leer!**  
Proyecto académico — **Grupo 5**  
Desarrollado con ❤️ y Python 🐍
