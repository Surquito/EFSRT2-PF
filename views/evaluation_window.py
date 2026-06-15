import tkinter as tk
from tkinter import ttk, messagebox
import database.queries as queries
from datetime import datetime


class EvaluationView(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent)

        self.columnconfigure(0, weight=1)

        self.frame_busqueda = ttk.LabelFrame(
            self,
            text=" Evaluación de Desempeño ",
            padding=15
        )
        self.frame_busqueda.pack(fill="x", padx=10, pady=10)

        tk.Label(
            self.frame_busqueda,
            text="Buscar Empleado:",
            font=("Arial", 10, "bold"),
            fg="#1e293b"
        ).grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.entry_busqueda = ttk.Entry(self.frame_busqueda, width=30)
        self.entry_busqueda.grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(
            self.frame_busqueda,
            text="SEARCH",
            command=self.buscar_empleado
        ).grid(row=0, column=2, padx=5, pady=5)

        tk.Label(self.frame_busqueda, text="Código:", font=("Arial", 10, "bold")).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_codigo = ttk.Entry(self.frame_busqueda)
        self.entry_codigo.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.frame_busqueda, text="Área:", font=("Arial", 10, "bold")).grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_area = ttk.Entry(self.frame_busqueda)
        self.entry_area.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.frame_busqueda, text="Fecha:", font=("Arial", 10, "bold")).grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.entry_fecha = ttk.Entry(self.frame_busqueda)
        self.entry_fecha.grid(row=3, column=1, padx=5, pady=5)

        self.var_calidad = tk.StringVar(value="17")
        self.var_operativa = tk.StringVar(value="16")
        self.var_blandas = tk.StringVar(value="18")
        self.var_productividad = tk.StringVar(value="15")

        frame_notas = ttk.LabelFrame(
            self,
            text=" Resultados de Evaluación ",
            padding=15
        )
        frame_notas.pack(fill="x", padx=10, pady=5)

        ttk.Label(frame_notas, text="Calidad").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(frame_notas, textvariable=self.var_calidad, state="readonly").grid(row=0, column=1)

        ttk.Label(frame_notas, text="Operativa").grid(row=1, column=0, padx=5, pady=5)
        ttk.Entry(frame_notas, textvariable=self.var_operativa, state="readonly").grid(row=1, column=1)

        ttk.Label(frame_notas, text="Habilidades Blandas").grid(row=2, column=0, padx=5, pady=5)
        ttk.Entry(frame_notas, textvariable=self.var_blandas, state="readonly").grid(row=2, column=1)

        ttk.Label(frame_notas, text="Productividad").grid(row=3, column=0, padx=5, pady=5)
        ttk.Entry(frame_notas, textvariable=self.var_productividad, state="readonly").grid(row=3, column=1)

        frame_comentario = ttk.LabelFrame(
            self,
            text=" Comentario del Supervisor ",
            padding=15
        )
        frame_comentario.pack(fill="both", expand=True, padx=10, pady=5)

        self.txt_comentario = tk.Text(frame_comentario, height=6)
        self.txt_comentario.pack(fill="both", expand=True)

        frame_botones = ttk.Frame(self)
        frame_botones.pack(pady=10)

        ttk.Button(frame_botones, text="MODIFICAR", command=self.modificar).pack(side="left", padx=5)
        ttk.Button(frame_botones, text="AGREGAR", command=self.agregar).pack(side="left", padx=5)
        ttk.Button(frame_botones, text="CANCELAR", command=self.cancelar).pack(side="left", padx=5)

    def buscar_empleado(self):

        criterio = self.entry_busqueda.get().strip()

        resultados = queries.buscar_empleados(criterio)

        if not resultados:
            messagebox.showinfo("Búsqueda", "No se encontraron empleados.")
            return

        empleado = resultados[0]

        self.entry_codigo.delete(0, tk.END)
        self.entry_codigo.insert(0, empleado[0])

        self.entry_area.delete(0, tk.END)
        self.entry_area.insert(0, empleado[7])

        self.entry_fecha.delete(0, tk.END)
        self.entry_fecha.insert(0, datetime.now().strftime("%Y-%m-%d"))

    def modificar(self):
        self.entry_codigo.config(state="normal")
        self.entry_area.config(state="normal")
        self.entry_fecha.config(state="normal")

    def agregar(self):

        comentario = self.txt_comentario.get("1.0", tk.END).strip()

        messagebox.showinfo(
            "Evaluación",
            f"Comentario registrado correctamente.\n\n{comentario}"
        )

    def cancelar(self):

        self.txt_comentario.delete("1.0", tk.END)

        self.entry_codigo.config(state="readonly")
        self.entry_area.config(state="readonly")
        self.entry_fecha.config(state="readonly")
