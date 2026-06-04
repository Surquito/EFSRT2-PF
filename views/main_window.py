import tkinter as tk
from tkinter import ttk
from views.employee_window import EmployeeView
#from views.evaluacion_view import EvaluacionView

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("FinSupport Contact Center")

        # ✅ Tamaño fijo
        width = 700
        height = 400

        # ✅ Centrar ventana
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))

        root.geometry(f"{width}x{height}+{x}+{y}")
        root.resizable(True, True)

        # ======================
        # NOTEBOOK (Pestañas)
        # ======================
        notebook = ttk.Notebook(root)
        notebook.pack(fill='both', expand=True)

        # ✅ HOME (pantalla inicial)
        tab_home = ttk.Frame(notebook)
        notebook.add(tab_home, text="🏠 Home")

        # Contenido HOME
        tk.Label(
            tab_home,
            text="Bienvenido a FinSupport",
            font=("Arial", 16, "bold")
        ).pack(pady=20)

        tk.Label(
            tab_home,
            text="Sistema de Evaluación de Desempeño\nCall Center Financiero",
            justify="center"
        ).pack(pady=10)

        tk.Label(
            tab_home,
            text="Seleccione una pestaña para continuar",
            fg="gray"
        ).pack(pady=10)

        # ✅ Otras pestañas
        notebook.add(EmployeeView(notebook), text="🧑 Employee")
        # notebook.add(EvaluacionView(notebook), text="📊 Evaluación")

        # ✅ Mostrar HOME al iniciar
        notebook.select(tab_home)
