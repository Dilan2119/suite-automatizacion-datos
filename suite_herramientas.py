# ==============================================================================
# SUITE DE HERRAMIENTAS DE AUTOMATIZACIÓN v2.3 - VERSIÓN CORREGIDA
# ==============================================================================
import tkinter as tk
from tkinter import ttk  # <<< LÍNEA AÑADIDA PARA SOLUCIONAR EL ERROR
from tkinter import filedialog, messagebox, scrolledtext
import os
import json
import glob
import pandas as pd
import threading

# --- ESTILO DE LA INTERFAZ ---
STYLE = {
    "BG_COLOR": "#282c34",
    "FG_COLOR": "#abb2bf",
    "TEXT_AREA_BG": "#21252b",
    "BUTTON_BG": "#3e4451",
    "BUTTON_HOVER_BG": "#528bff",
    "ACCENT_COLOR": "#61afef",
    "SUCCESS_COLOR": "#98c379",
    "ERROR_COLOR": "#e06c75",
    "FONT_FAMILY": "Segoe UI",
    "FONT_NORMAL": ("Segoe UI", 10),
    "FONT_BOLD": ("Segoe UI", 11, "bold"),
    "FONT_TITLE": ("Segoe UI", 18, "bold")
}

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # --- Configuración de la Ventana Principal ---
        self.title("Suite de Herramientas de Automatización")
        
        window_width = 800  # Ancho inicial
        window_height = 650 # Alto inicial
        
        # >>> INICIO: CÓDIGO PARA CENTRAR LA VENTANA <<<
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        
        self.geometry(f'{window_width}x{window_height}+{x}+{y}')
        # >>> FIN: CÓDIGO PARA CENTRAR LA VENTANA <<<

        # >>> INICIO: CÓDIGO PARA HACERLA RESPONSIVA Y MAXIMIZABLE <<<
        self.resizable(True, True)
        self.minsize(window_width, window_height)
        # >>> FIN: CÓDIGO PARA HACERLA RESPONSIVA Y MAXIMIZABLE <<<

        self.configure(bg=STYLE["BG_COLOR"])

        # --- Contenedor Principal (se expandirá para llenar la ventana) ---
        main_frame = tk.Frame(self, bg=STYLE["BG_COLOR"], padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)
        # Configurar la grid del main_frame para que sea responsiva
        main_frame.grid_columnconfigure(0, weight=1) # La columna 0 se expande horizontalmente
        main_frame.grid_rowconfigure(3, weight=1)    # La fila 3 (el log) se expande verticalmente

        title_label = tk.Label(main_frame, text="Suite de Herramientas", font=STYLE["FONT_TITLE"], bg=STYLE["BG_COLOR"], fg=STYLE["ACCENT_COLOR"])
        title_label.grid(row=0, column=0, pady=(0, 20))

        buttons_frame = tk.Frame(main_frame, bg=STYLE["BG_COLOR"])
        buttons_frame.grid(row=1, column=0, sticky="ew") # ew = expandir de Este a Oeste
        buttons_frame.grid_columnconfigure(0, weight=1)

        self.tools = [
            {"icon": "📄", "text": "Modificar Códigos en JSON", "command": self.run_script_1, "desc": "Busca archivos JSON en subcarpetas 'F...' y limpia el campo 'codTecnologiaSalud', eliminando el guion y lo que le sigue."},
            {"icon": "✏️", "text": "Renombrar Archivos de Texto", "command": self.run_script_2, "desc": "Busca archivos .txt con nombres largos en subcarpetas y los renombra a una versión corta, conservando el código principal."},
            {"icon": "📊", "text": "Consolidar Glosas en Excel", "command": self.run_script_3, "desc": "Unifica filas con el mismo número de factura en un Excel, sumando sus valores de glosa. El archivo original es modificado."},
            {"icon": "⚙️", "text": "Procesar Archivo PGP en Excel", "command": self.run_script_4, "desc": "Procesa un archivo PGP: agrupa datos, cuenta servicios por paciente y recalcula totales. Guarda el resultado en un archivo nuevo."}
        ]
        
        self.buttons = []
        for i, tool in enumerate(self.tools):
            button = self.create_button(buttons_frame, tool)
            button.grid(row=i, column=0, sticky="ew", pady=5)
            self.buttons.append(button)

        self.desc_label = tk.Label(main_frame, text="Pasa el ratón sobre una opción para ver su descripción.", font=STYLE["FONT_NORMAL"], bg=STYLE["BG_COLOR"], fg=STYLE["FG_COLOR"], wraplength=700, justify="center")
        self.desc_label.grid(row=2, column=0, pady=15, ipady=5, sticky="ew")

        log_frame = tk.Frame(main_frame, bg=STYLE["TEXT_AREA_BG"], relief="sunken", borderwidth=1)
        log_frame.grid(row=3, column=0, sticky="nsew", pady=(10, 0)) # nsew = expandir en todas direcciones
        log_frame.grid_columnconfigure(0, weight=1)
        log_frame.grid_rowconfigure(0, weight=1)

        self.log_widget = tk.Text(log_frame, bg=STYLE["TEXT_AREA_BG"], fg=STYLE["FG_COLOR"], relief="flat", borderwidth=0, font=("Courier New", 9), wrap="word")
        self.log_widget.grid(row=0, column=0, sticky="nsew") # nsew
        
        # Scrollbar (se muestra solo si es necesario)
        scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_widget.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.log_widget['yscrollcommand'] = scrollbar.set

        self.log_widget.config(state="disabled")
        self.log_widget.tag_config("ACCENT", foreground=STYLE["ACCENT_COLOR"])
        self.log_widget.tag_config("SUCCESS", foreground=STYLE["SUCCESS_COLOR"])
        self.log_widget.tag_config("ERROR", foreground=STYLE["ERROR_COLOR"])

    def create_button(self, parent, tool_info):
        btn_text = f"  {tool_info['icon']}  {tool_info['text']}"
        button = tk.Button(parent, text=btn_text, command=lambda: self.run_in_thread(tool_info["command"]),
                           font=STYLE["FONT_BOLD"], bg=STYLE["BUTTON_BG"], fg=STYLE["FG_COLOR"],
                           relief="flat", activebackground=STYLE["BUTTON_HOVER_BG"], activeforeground=STYLE["FG_COLOR"],
                           pady=8, anchor="w", justify="left")
        
        button.bind("<Enter>", lambda e, desc=tool_info["desc"]: (self.show_description(desc), e.widget.config(bg=STYLE["BUTTON_HOVER_BG"])))
        button.bind("<Leave>", lambda e: (self.reset_description(), e.widget.config(bg=STYLE["BUTTON_BG"])))
        return button

    def show_description(self, desc):
        self.desc_label.config(text=desc)

    def reset_description(self):
        self.desc_label.config(text="Pasa el ratón sobre una opción para ver su descripción.")

    def log(self, message, tag=None):
        self.log_widget.config(state="normal")
        self.log_widget.insert(tk.END, message + "\n", tag)
        self.log_widget.config(state="disabled")
        self.log_widget.see(tk.END)
        self.update_idletasks()

    def toggle_buttons_state(self, state):
        for btn in self.buttons:
            btn.config(state=state)

    def run_in_thread(self, target_func):
        def task_wrapper():
            self.toggle_buttons_state("disabled")
            try:
                target_func()
            finally:
                self.toggle_buttons_state("normal")
        
        thread = threading.Thread(target=task_wrapper, daemon=True)
        thread.start()

    # ==========================================================================
    # --- SCRIPT 1: Modificador de JSON ---
    # ==========================================================================
    def run_script_1(self):
        ruta_principal = filedialog.askdirectory(title="Selecciona la carpeta principal con las subcarpetas 'F...'")
        if not ruta_principal:
            self.log("Operación cancelada.", "ERROR")
            return

        self.log(f"\n--- Iniciando Script 1: Modificar JSON ---", "ACCENT")
        carpetas_procesadas = 0
        archivos_modificados = 0

        for nombre_carpeta in os.listdir(ruta_principal):
            ruta_subcarpeta = os.path.join(ruta_principal, nombre_carpeta)
            if os.path.isdir(ruta_subcarpeta) and nombre_carpeta.upper().startswith('F'):
                self.log(f"Procesando: {nombre_carpeta}")
                carpetas_procesadas += 1
                json_encontrado = False

                for nombre_archivo in os.listdir(ruta_subcarpeta):
                    if nombre_archivo.lower().endswith('.json'):
                        json_encontrado = True
                        ruta_archivo_json = os.path.join(ruta_subcarpeta, nombre_archivo)
                        self.log(f"  > Encontrado JSON: {nombre_archivo}")

                        try:
                            se_hizo_modificacion = False
                            with open(ruta_archivo_json, 'r', encoding='utf-8') as f:
                                data = json.load(f)

                            if 'usuarios' in data and isinstance(data['usuarios'], list):
                                for usuario in data.get('usuarios', []):
                                    for servicio in usuario.get('servicios', {}).get('otrosServicios', []):
                                        if 'codTecnologiaSalud' in servicio:
                                            codigo_original = servicio['codTecnologiaSalud']
                                            if isinstance(codigo_original, str) and '-' in codigo_original:
                                                codigo_modificado = codigo_original.split('-')[0]
                                                if codigo_original != codigo_modificado:
                                                    servicio['codTecnologiaSalud'] = codigo_modificado
                                                    se_hizo_modificacion = True
                                                    self.log(f"    -> Modificado '{codigo_original}' a '{codigo_modificado}'")
                            
                            if se_hizo_modificacion:
                                with open(ruta_archivo_json, 'w', encoding='utf-8') as f:
                                    json.dump(data, f, indent=4, ensure_ascii=False)
                                self.log(f"  > Archivo guardado.", "SUCCESS")
                                archivos_modificados += 1
                        except Exception as e:
                            self.log(f"  > ERROR procesando archivo: {e}", "ERROR")
                        break
        
        self.log(f"Proceso completado. Carpetas procesadas: {carpetas_procesadas}. Archivos modificados: {archivos_modificados}.", "SUCCESS")
        messagebox.showinfo("Éxito", "Modificación de archivos JSON completada.")

    # ==========================================================================
    # --- SCRIPT 2: Renombrador de Archivos TXT ---
    # ==========================================================================
    def run_script_2(self):
        ruta_principal = filedialog.askdirectory(title="Selecciona la carpeta principal a procesar")
        if not ruta_principal:
            self.log("Operación cancelada.", "ERROR")
            return
        
        self.log(f"\n--- Iniciando Script 2: Renombrar TXT ---", "ACCENT")
        archivos_renombrados = 0
        for nombre_subcarpeta in os.listdir(ruta_principal):
            ruta_subcarpeta = os.path.join(ruta_principal, nombre_subcarpeta)
            if os.path.isdir(ruta_subcarpeta):
                try:
                    archivos_encontrados = glob.glob(os.path.join(ruta_subcarpeta, '_F*.txt'))
                    if len(archivos_encontrados) == 1:
                        ruta_archivo_original = archivos_encontrados[0]
                        nombre_archivo_original = os.path.basename(ruta_archivo_original)
                        partes_nombre = nombre_archivo_original.split('_')
                        extension = os.path.splitext(nombre_archivo_original)[1]
                        nuevo_nombre = f"_{partes_nombre[1]}{extension}"
                        ruta_archivo_nuevo = os.path.join(ruta_subcarpeta, nuevo_nombre)
                        os.rename(ruta_archivo_original, ruta_archivo_nuevo)
                        self.log(f"En '{nombre_subcarpeta}': '{nombre_archivo_original}' -> '{nuevo_nombre}'")
                        archivos_renombrados += 1
                except Exception as e:
                    self.log(f"ERROR en carpeta '{nombre_subcarpeta}': {e}", "ERROR")

        self.log(f"Proceso completado. Total de archivos renombrados: {archivos_renombrados}.", "SUCCESS")
        messagebox.showinfo("Éxito", "Renombrado de archivos completado.")

    # ==========================================================================
    # --- SCRIPT 3: Consolidador de Glosas Excel ---
    # ==========================================================================
    def run_script_3(self):
        nombre_archivo_excel = filedialog.askopenfilename(title="Selecciona el archivo de Excel de Glosas", filetypes=[("Archivos de Excel", "*.xlsx *.xls")])
        if not nombre_archivo_excel:
            self.log("Operación cancelada.", "ERROR")
            return

        self.log(f"\n--- Iniciando Script 3: Consolidar Glosas ---", "ACCENT")
        try:
            nombre_hoja = 'DATA_GLOSAS'
            excel_file = pd.ExcelFile(nombre_archivo_excel)
            df = excel_file.parse(sheet_name=nombre_hoja)
            self.log(f"Hoja '{nombre_hoja}' cargada. Filas iniciales: {len(df)}")
            
            df['VALOR REAL GLOSA'] = pd.to_numeric(df['VALOR REAL GLOSA'], errors='coerce').fillna(0)
            df_consolidado = df.groupby('NUMERO DE FACTURA', as_index=False).agg(
                {'VALOR REAL GLOSA': 'sum', **{col: 'first' for col in df.columns if col not in ['NUMERO DE FACTURA', 'VALOR REAL GLOSA']}}
            )
            self.log(f"Consolidación completada. Filas finales: {len(df_consolidado)}")

            with pd.ExcelWriter(nombre_archivo_excel, engine='openpyxl', mode='w') as writer:
                df_consolidado.to_excel(writer, sheet_name=nombre_hoja, index=False)
                for sheet_name in excel_file.sheet_names:
                    if sheet_name != nombre_hoja:
                        other_df = excel_file.parse(sheet_name=sheet_name)
                        other_df.to_excel(writer, sheet_name=sheet_name, index=False)
            
            self.log(f"Archivo original '{os.path.basename(nombre_archivo_excel)}' modificado con éxito.", "SUCCESS")
            messagebox.showinfo("Éxito", "El archivo de glosas ha sido consolidado y guardado.")
        except Exception as e:
            self.log(f"ERROR: {e}", "ERROR")
            messagebox.showerror("Error", f"Ocurrió un error en el Script 3: {e}")

    # ==========================================================================
    # --- SCRIPT 4: Procesador PGP Excel ---
    # ==========================================================================
    def run_script_4(self):
        input_file = filedialog.askopenfilename(title="Selecciona el archivo PGP a procesar", filetypes=[("Archivos de Excel", "*.xlsx *.xls")])
        if not input_file:
            self.log("Operación cancelada.", "ERROR")
            return

        output_file = filedialog.asksaveasfilename(title="Guardar archivo PGP procesado como...", defaultextension=".xlsx", filetypes=[("Archivos de Excel", "*.xlsx")])
        if not output_file:
            self.log("Operación cancelada.", "ERROR")
            return
            
        self.log(f"\n--- Iniciando Script 4: Procesar PGP ---", "ACCENT")
        try:
            df = pd.read_excel(input_file)
            self.log(f"Archivo '{os.path.basename(input_file)}' cargado.")
            
            column_mapping = {'NRO. IDENTIFICACION DEL USUARIO': 'DOCUMENTO', 'CODIGO DEL SERVICIO': 'COD CUPS', 'FECHA DE PRESTACION DEL SERVICIO': 'FECHA PRESTACION', 'VALOR UNITARIO DE LA ACTIVIDAD, PROCEDIMIENTO O SERVICIO PRESTADO': 'VALOR UNITARIO', 'VALOR TOTAL DE LA ACTIVIDAD, PROCEDIMIENTO O SERVICIO PRESTADO': 'VALOR TOTAL'}
            df.rename(columns=column_mapping, inplace=True)
            self.log("Columnas estandarizadas.")

            df.insert(0, 'CONSECUTIVO', pd.factorize(df['DOCUMENTO'])[0] + 1)
            df['FECHA PRESTACION'] = pd.to_datetime(df['FECHA PRESTACION'], dayfirst=True, errors='coerce')
            
            self.log("Agrupando y consolidando datos...")
            df.sort_values(by=['CONSECUTIVO', 'COD CUPS', 'FECHA PRESTACION'], inplace=True)
            df['CANTIDAD_NUEVA'] = df.groupby(['CONSECUTIVO', 'COD CUPS'])['COD CUPS'].transform('size')
            df_final = df.drop_duplicates(subset=['CONSECUTIVO', 'COD CUPS'], keep='first').copy()
            df_final['CANTIDAD'] = df_final['CANTIDAD_NUEVA']
            df_final.drop(columns=['CANTIDAD_NUEVA'], inplace=True)
            
            self.log("Calculando valor total...")
            df_final['CANTIDAD'] = pd.to_numeric(df_final['CANTIDAD'], errors='coerce').fillna(0)
            df_final['VALOR UNITARIO'] = pd.to_numeric(df_final['VALOR UNITARIO'], errors='coerce').fillna(0)
            df_final['VALOR TOTAL'] = df_final['CANTIDAD'] * df_final['VALOR UNITARIO']
            
            df_final.to_excel(output_file, index=False)
            self.log(f"Proceso completado. Archivo guardado en '{os.path.basename(output_file)}'", "SUCCESS")
            messagebox.showinfo("Éxito", f"El archivo PGP ha sido procesado y guardado.")
        except Exception as e:
            self.log(f"ERROR: {e}", "ERROR")
            messagebox.showerror("Error", f"Ocurrió un error en el Script 4: {e}")

if __name__ == "__main__":
    app = App()
    app.mainloop()