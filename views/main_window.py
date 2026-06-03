import tkinter as tk
from tkinter import ttk
from views.agente_view import AgenteView
from views.evaluacion_view import EvaluacionView

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("FinSupport")

        notebook = ttk.Notebook(root)
        notebook.pack(fill='both', expand=True)

        notebook.add(AgenteView(notebook), text="Agente")
        notebook.add(EvaluacionView(notebook), text="Evaluación")