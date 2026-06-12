import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk  
import os
from views.employee_window import EmployeeView

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("FinSupport Contact Center")

        width = 900
        height = 650

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))

        root.geometry(f"{width}x{height}+{x}+{y}")
        root.resizable(True, True)

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TNotebook", background="#f2f2f2")
        style.configure("TNotebook.Tab", background="#e2e8f0", foreground="#1e293b", padding=[12, 6], font=("Arial", 10, "bold"))
        style.map("TNotebook.Tab", background=[("selected", "#f2f2f2")], foreground=[("selected", "#0f172a")])
        style.configure("TFrame", background="#f2f2f2")

        notebook = ttk.Notebook(root)
        notebook.pack(fill='both', expand=True)

        tab_home = ttk.Frame(notebook)
        notebook.add(tab_home, text="Inicio")

        ruta_imagen = "img/Portada_FinSupport.jpg"

        try:
            if os.path.exists(ruta_imagen):
                imagen_original = Image.open(ruta_imagen)
                imagen_redimensionada = imagen_original.resize((880, 560), Image.Resampling.LANCZOS)
                self.foto_home = ImageTk.PhotoImage(imagen_redimensionada)
                label_portada = tk.Label(tab_home, image=self.foto_home, bg="#f2f2f2")
                label_portada.pack(expand=True, fill="both", pady=10)
            else:
                tk.Label(
                    tab_home, 
                    text=f"¡Bienvenido a FinSupport!\n\nNo se encontró la imagen: '{ruta_imagen}'", 
                    fg="#475569", 
                    bg="#f2f2f2",
                    font=("Arial", 14, "bold"),
                    justify="center"
                ).pack(expand=True)
        except Exception as e:
            tk.Label(
                tab_home, 
                text=f"Error al cargar la imagen:\n{e}", 
                fg="red", 
                bg="#f2f2f2",
                justify="center"
            ).pack(expand=True)

        notebook.add(EmployeeView(notebook), text="Empleados")
        notebook.select(tab_home)