import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from services.evaluation_service import EvaluationService

class EvaluationPerformanceView(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent)

        self.service = EvaluationService()

        self.create_widgets()
        self.load_years()
        self.load_months()

    # ==================================
    # UI
    # ==================================
    def create_widgets(self):
        container = ttk.Frame(self, padding=30)
        container.pack(fill=tk.BOTH, expand=True)


        # AÑO
        ttk.Label(container, text="Año:").pack(anchor=tk.W)
        self.year_combo = ttk.Combobox(container, state="readonly")
        self.year_combo.pack(fill=tk.X, pady=(5, 15))
        self.year_combo.bind("<<ComboboxSelected>>", self.on_period_change)

        # MES
        ttk.Label(container, text="Mes:").pack(anchor=tk.W)
        self.month_combo = ttk.Combobox(container, state="readonly")
        self.month_combo.pack(fill=tk.X, pady=(5, 15))
        self.month_combo.bind("<<ComboboxSelected>>", self.on_period_change)

        # EMPLEADO
        ttk.Label(container, text="Empleado:").pack(anchor=tk.W)
        self.employee_combo = ttk.Combobox(container, state="readonly")
        self.employee_combo.pack(fill=tk.X, pady=(5, 15))

        # Evento al seleccionar empleado
        self.employee_combo.bind("<<ComboboxSelected>>", self.on_employee_selected)

        # ==================================
        # CONTENEDOR HORIZONTAL
        # ==================================
        top_frame = ttk.Frame(container)
        top_frame.pack(fill=tk.X, pady=(10, 20))

        # ==================================
        # NOTAS (IZQUIERDA)
        # ==================================
        notes_container = ttk.Frame(top_frame)
        notes_container.pack(side=tk.LEFT, fill=tk.X, expand=True)

        ttk.Label(notes_container, text="Notas del Periodo:").pack(anchor=tk.W)

        self.notes_frame = ttk.Frame(notes_container, height=120)
        self.notes_frame.pack(fill=tk.X, pady=(5, 0))
        self.notes_frame.pack_propagate(False)

        # ==================================
        # PROMEDIO (DERECHA)
        # ==================================
        average_container = ttk.Frame(top_frame)
        average_container.pack(side=tk.RIGHT, padx=(20, 0))

        ttk.Label(average_container, text="Promedio Total").pack()

        self.average_var = tk.StringVar()

        self.entry_average = ttk.Entry(
            average_container,
            textvariable=self.average_var,
            width=10,
            justify="center",
            state="readonly",
            font=("Arial", 12, "bold")
        )
        self.entry_average.pack(pady=(5, 10))

        # BOTÓN CALCULAR (debajo del promedio)
        btn_calculate = ttk.Button(
            average_container,
            text="Calcular",
            command=self.calculate_average
        )
        btn_calculate.pack()

        # COMENTARIO
        ttk.Label(container, text="Comentario:").pack(anchor=tk.W)

        self.txt_comment = tk.Text(container, height=5)
        self.txt_comment.pack(fill=tk.BOTH, pady=(5, 20))

        # BOTÓN GUARDAR
        ttk.Button(
            container,
            text="Guardar Evaluación",
            command=self.save_evaluation
        ).pack()

    # ==================================
    def load_years(self):
        self.year_combo["values"] = self.service.get_years()

    def load_months(self):
        self.month_data = {
            "Enero": 1, "Febrero": 2, "Marzo": 3,
            "Abril": 4, "Mayo": 5, "Junio": 6,
            "Julio": 7, "Agosto": 8, "Septiembre": 9,
            "Octubre": 10, "Noviembre": 11, "Diciembre": 12
        }
        self.month_combo["values"] = list(self.month_data.keys())

    # ==================================
    def on_period_change(self, event):
        year = self.year_combo.get()
        month_name = self.month_combo.get()

        # limpiar datos
        self.employee_combo.set("")
        self.average_var.set("")

        for w in self.notes_frame.winfo_children():
            w.destroy()

        if not year or not month_name:
            return

        year = int(year)  # ✅ FIX
        month = self.month_data[month_name]

        employees = self.service.get_employees_by_period(year, month)

        self.employee_data = {}
        values = []

        for codigo, nombre, apellido in employees:
            text = f"{codigo} - {nombre} {apellido}"
            values.append(text)
            self.employee_data[text] = codigo

        self.employee_combo["values"] = values

    # ==================================
    # NUEVO: carga automática de notas
    def on_employee_selected(self, event):
        selected = self.employee_combo.get()
        year = self.year_combo.get()
        month_name = self.month_combo.get()

        if not selected or not year or not month_name:
            return

        year = int(year)  # ✅ FIX
        month = self.month_data[month_name]
        codigo = self.employee_data[selected]

        evaluations = self.service.get_employee_evaluations(codigo, year, month)
        self.load_employee_evaluations(evaluations)

    # ==================================
    def load_employee_evaluations(self, evaluations):

        for w in self.notes_frame.winfo_children():
            w.destroy()

        if not evaluations:
            ttk.Label(self.notes_frame, text="No existen evaluaciones").pack()
            return

        for i, item in enumerate(evaluations):

            fecha, tipo, nota = item

            card = ttk.LabelFrame(self.notes_frame, text=str(tipo), padding=10)
            card.grid(row=0, column=i, padx=8)

            ttk.Label(card, text=f"Nota: {nota}").pack()
            ttk.Label(card, text=str(fecha).split(" ")[0]).pack()

    # ==================================
    def calculate_average(self):

        selected = self.employee_combo.get()

        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un empleado")
            return

        year = int(self.year_combo.get())   # ✅ FIX
        month = self.month_data[self.month_combo.get()]
        codigo = self.employee_data[selected]

        promedio = self.service.calculate_average(codigo, year, month)
        self.average_var.set(str(round(promedio, 2)))

    # ==================================
    def save_evaluation(self):

        selected = self.employee_combo.get()

        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione empleado")
            return

        year = int(self.year_combo.get())
        month = self.month_data[self.month_combo.get()]
        codigo = self.employee_data[selected]

        promedio = self.average_var.get()
        comentario = self.txt_comment.get("1.0", tk.END).strip()

        self.service.save_performance_evaluation(
            codigo,
            promedio,
            comentario,
            year,
            month
        )

        messagebox.showinfo("Éxito", "Guardado correctamente")

        # ==================================
        # ✅ LIMPIAR FORMULARIO
        # ==================================

        # Limpiar selección de empleado
        self.employee_combo.set("")

        # Limpiar promedio
        self.average_var.set("")

        # Limpiar comentario
        self.txt_comment.delete("1.0", tk.END)

        # Limpiar notas (cards)
        for widget in self.notes_frame.winfo_children():
            widget.destroy()