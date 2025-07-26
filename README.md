# Suite de Automatización de Datos

## 📜 Resumen del Proyecto

**Suite de Automatización de Datos** es una aplicación de escritorio desarrollada en Python con una interfaz gráfica construida con Tkinter. Esta herramienta fue creada para optimizar flujos de trabajo de oficina, automatizando tareas repetitivas de manipulación de archivos que normalmente consumen mucho tiempo y son propensas a errores humanos.

La aplicación ofrece una interfaz centralizada, intuitiva y segura para que usuarios sin conocimientos técnicos puedan ejecutar procesos complejos con un solo clic.

## ✨ Características Principales

Esta suite incluye cuatro módulos de automatización clave:

| Módulo | Función Principal |
| :--- | :--- |
| **📄 Modificador de JSON** | Recorre recursivamente un directorio en busca de subcarpetas que sigan un patrón ('F...'). Dentro de ellas, localiza el primer archivo `.json` y estandariza el valor del campo `codTecnologiaSalud`, eliminando sufijos no deseados. |
| **✏️ Renombrador de Archivos TXT** | Analiza subdirectorios para encontrar archivos `.txt` con nomenclaturas largas o generadas por sistemas (ej. `_F123_ID456.txt`) y los renombra a una versión limpia y corta (ej. `_F123.txt`), manteniendo la consistencia de los datos. |
| **📊 Consolidador de Glosas en Excel** | Procesa archivos de Excel para unificar registros duplicados basados en el número de factura. Suma los valores de las glosas (`VALOR REAL GLOSA`) en una única fila por factura y reescribe el archivo original de forma segura, conservando las demás hojas. |
| **⚙️ Procesador PGP en Excel** | Automatiza el procesamiento de archivos PGP. Asigna un número consecutivo por paciente, estandariza columnas, agrupa y cuenta los servicios prestados, y recalcula los valores totales, generando un nuevo archivo de Excel con los datos limpios y consolidados. |

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