# 🏨 Sistema de Gestión Hotelera

Un sistema de escritorio desarrollado en **Python** para la administración de un hotel, permitiendo **gestionar reservas, clientes y habitaciones** de forma sencilla y organizada.

---

## 🚀 Características principales

- 🧾 **Gestión de reservas:** creación, modificación y cancelación.  
- 👤 **Registro de clientes:** alta, baja y modificación de datos.  
- 🏠 **Administración de habitaciones:** carga, disponibilidad y detalles.  
- 💾 **Base de datos SQLite integrada** (fácil de portar y sin necesidad de servidor).  
- 🔐 **Sistema de login** para el acceso al sistema.  
- 🖥️ **Interfaz gráfica** desarrollada con Python y una estructura modular clara.

---

## 📂 Estructura del proyecto

```
proyecto/
│
├── config.py              # Configuración general del proyecto
├── run_app.py             # Archivo principal de ejecución
├── schema.sql             # Script de creación de base de datos
│
├── apli/                  # Lógica de negocio y servicios
│   ├── service.py
│   └── __init__.py
│
├── main/                  # Interfaz gráfica principal
│   ├── app.py
│   ├── login.py
│   ├── main_window.py
│   └── __init__.py
│
└── model/                 # Modelos de datos y conexión con la base
    ├── cliente.py
    ├── database.py
    ├── habitacion.py
    ├── reserva.py
    └── __init__.py
```

---

## ⚙️ Requisitos

- Python **3.11+**
- Librerías utilizadas:
  ```bash
  pip install tkinter sqlite3
  ```

---

## ▶️ Ejecución del proyecto

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/tuusuario/proyecto-hotel.git
   ```
2. Entrar a la carpeta del proyecto:
   ```bash
   cd proyecto-hotel
   ```
3. Ejecutar el sistema:
   ```bash
   python run_app.py
   ```

---

## 🧠 Organización interna

- **model/** → Módulos encargados de interactuar con la base de datos.  
- **main/** → Archivos de la interfaz principal y lógica de ventanas.  
- **apli/** → Servicios generales del sistema.  
- **schema.sql** → Contiene las tablas de `cliente`, `reserva` y `habitacion`.

---

## 💡 Integrantes

**Gabriel Carlos Prestes**  
**Mauricio Ruperez**  
**Ian Fleck**  
💼 Proyecto desarrollado para prácticas de programación y gestión de software en Programacion Orientada a Obajetos.
