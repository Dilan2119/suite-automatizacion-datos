## 📜 Resumen del Proyecto

**Suite de Automatización para Gestión Clínica** es una aplicación de escritorio desarrollada en Python y Tkinter, diseñada específicamente para optimizar los flujos de trabajo del **área administrativa de una clínica**. Esta herramienta centraliza y automatiza tareas de facturación, procesamiento de datos y gestión de archivos que son cruciales en el sector salud.

El objetivo es reducir drásticamente el tiempo invertido en procesos manuales y minimizar los errores humanos, permitiendo que el personal administrativo se enfoque en tareas de mayor valor.

## ✨ Características Principales

Esta suite incluye cuatro módulos de automatización enfocados en necesidades del sector salud:

| Módulo | Función Principal en el Contexto Clínico |
| :--- | :--- |
| **📄 Modificador de JSON** | Estandariza archivos de reporte (RIPS) en formato JSON, corrigiendo automáticamente el `codTecnologiaSalud` para asegurar la compatibilidad con sistemas de facturación y auditoría. |
| **✏️ Renombrador de Archivos TXT** | Organiza lotes de archivos de facturación o reportes (ej. `_F123_ID456.txt`) renombrándolos a un formato corto y consistente (ej. `_F123.txt`) para facilitar su archivo y búsqueda. |
| **📊 Consolidador de Glosas en Excel** | Procesa reportes de glosas en Excel, unificando múltiples objeciones de una misma factura. Suma el `VALOR REAL GLOSA` para obtener un total consolidado por factura, simplificando el proceso de conciliación. |
| **⚙️ Procesador PGP en Excel** | Automatiza el análisis de archivos de Pago Global Prospectivo (PGP). Asigna consecutivos por paciente, cuenta los servicios (CUPS) prestados y recalcula los valores totales para auditorías y reportes financieros. |

## 🛠️ Tecnologías Utilizadas

* **Lenguaje:** Python 3
* **Interfaz Gráfica (GUI):** Tkinter, ttk
* **Manipulación de Datos:** Pandas
* **Interacción con el Sistema:** os, glob, json
* **Programación Concurrente:** Threading (para mantener la interfaz responsiva)
* **Empaquetado (Opcional):** PyInstaller, auto-py-to-exe

## 🚀 Instalación y Uso

Para ejecutar esta aplicación desde el código fuente, sigue estos pasos:

1.  **Clona el repositorio:**
    ```bash
    git clone [https://github.com/tu-usuario/suite-automatizacion-datos.git](https://github.com/tu-usuario/suite-automatizacion-datos.git)
    cd suite-automatizacion-datos
    ```

2.  **(Opcional) Crea un entorno virtual:**
    ```bash
    python -m venv venv
    source venv/Scripts/activate  # En Windows
    ```

3.  **Instala las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Ejecuta la aplicación:**
    ```bash
    python suite_herramientas.py
    ```
