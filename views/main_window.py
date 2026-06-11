import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk  
import os
from views.employee_window import EmployeeView
#from views.evaluacion_view import EvaluacionView

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("FinSupport Contact Center")

        # ✅ Tamaño fijo
        width = 800
        height = 500

        # ✅ Centrar ventana
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))

        root.geometry(f"{width}x{height}+{x}+{y}")
        root.resizable(True, True)

        # ==========================================
        # 🎨 ESTILOS PARA COMPATIBILIDAD CON #f2f2f2
        # ==========================================
        style = ttk.Style()
        style.theme_use('clam')  # 'clam' permite modificar mejor los fondos en ttk
        style.configure("TNotebook", background="#f2f2f2")
        style.configure("TNotebook.Tab", background="#e2e8f0", foreground="#1e293b", padding=[10, 4])
        style.map("TNotebook.Tab", background=[("selected", "#f2f2f2")], foreground=[("selected", "#0f172a")])
        style.configure("TFrame", background="#f2f2f2")

        # ======================
        # NOTEBOOK (Pestañas)
        # ======================
        notebook = ttk.Notebook(root)
        notebook.pack(fill='both', expand=True)

        # ✅ HOME (pantalla inicial)
        tab_home = ttk.Frame(notebook)
        notebook.add(tab_home, text="🏠 Home")

        # ==========================================
        # REEMPLAZO DE CONTENIDO HOME CON IMAGEN
        # ==========================================
        ruta_imagen = "img/Portada_FinSupport.jpg"  # Ruta relativa a tu proyecto

        try:
            if os.path.exists(ruta_imagen):
                imagen_original = Image.open(ruta_imagen)  # Ruta relativa a tu proyecto
                
                # Redimensionamos a 680x320 para que encaje de forma óptima en tu ventana de 700x400
                imagen_redimensionada = imagen_original.resize((780, 420), Image.Resampling.LANCZOS)
                self.foto_home = ImageTk.PhotoImage(imagen_redimensionada)
                
                # Colocamos la imagen dentro de un Label con fondo acoplado
                label_portada = tk.Label(tab_home, image=self.foto_home, bg="#f2f2f2")
                label_portada.pack(expand=True, fill="both", pady=10)
            else:
                # Label de contingencia amigable si olvidas colocar la imagen en la carpeta
                tk.Label(
                    tab_home, 
                    text=f"¡Bienvenido a FinSupport!\n\nNo se encontró el archivo: '{ruta_imagen}'\nGuarda la imagen diseñada en la carpeta del proyecto.", 
                    fg="#475569", 
                    bg="#f2f2f2",
                    font=("Arial", 12, "bold"),
                    justify="center"
                ).pack(expand=True)

        except Exception as e:
            # Captura de errores técnicos por si falla la lectura/Pillow
            tk.Label(
                tab_home, 
                text=f"Error de interfaz gráfica:\n{e}", 
                fg="red", 
                bg="#f2f2f2",
                justify="center"
            ).pack(expand=True)

        # ==========================================
        # ✅ Otras pestañas
        # ==========================================
        notebook.add(EmployeeView(notebook), text="🧑 Employee")
        # notebook.add(EvaluacionView(notebook), text="📊 Evaluación")

        # ✅ Mostrar HOME al iniciar
        notebook.select(tab_home)