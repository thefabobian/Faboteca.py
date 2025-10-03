# 📚 Faboteca

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/Tkinter-GUI-lightgrey)
![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-green?logo=mongodb&logoColor=white)

Faboteca es una aplicación de escritorio desarrollada en **Python** con **Tkinter** que permite la **gestión de usuarios, libros y préstamos** en una biblioteca.  
La persistencia de datos está implementada con **MongoDB Atlas** para garantizar seguridad, escalabilidad y acceso desde la nube.

---

## 🚀 Características principales
- Gestión de **Usuarios**:
  - Crear, listar, actualizar y eliminar usuarios.
  - Validación de cédula (solo números, sin duplicados).
  - Validación de correo electrónico.

- Gestión de **Libros**:
  - CRUD completo de libros.
  - Validación de campos obligatorios (título, autor, género).
  - Evita duplicados mediante título + autor.
  - Control de estado: Disponible / Prestado.

- Gestión de **Préstamos**:
  - Registrar préstamos (solo si el libro está disponible).
  - Eliminar préstamos (restaurando automáticamente el estado del libro a Disponible).
  - Manejo atómico de préstamos en la base de datos para evitar inconsistencias.

- **Arquitectura MVC**:
  - `model/`: interacción con la base de datos (MongoDB).
  - `controller/`: lógica de negocio y puente entre vistas y modelos.
  - `view/`: interfaz gráfica con Tkinter.

- **Conexión segura a MongoDB Atlas** mediante variables de entorno.

---

## 📂 Estructura del proyecto
```bash
Faboteca.py/
│── main.py                 # Punto de entrada principal
│── .env                    # Variables de entorno
│── mongodb.py              # Clase de conexión a MongoDB Atlas
│
├── model/                  # Modelos (acceso a datos)
│   ├── usuario_model.py
│   ├── libro_model.py
│   └── prestamo_model.py
│
├── controller/             # Controladores (lógica de negocio)
│   ├── usuario_controller.py
│   ├── libro_controller.py
│   └── prestamo_controller.py
│
└── view/                   # Vistas gráficas (Tkinter)
    ├── menu_view.py
    ├── usuario_view.py
    ├── libro_view.py
    └── prestamo_view.py
