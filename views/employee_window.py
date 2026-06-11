import tkinter as tk
from tkinter import ttk, messagebox
from models.employee import Employee
#from services.agente_service import EmployeeService

class EmployeeView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # self.service = EmployeeService()

        tk.Label(self, text="Nombre").grid(row=0, column=0)
        self.entry_nombre = tk.Entry(self)
        self.entry_nombre.grid(row=0, column=1)

        tk.Label(self, text="Área").grid(row=1, column=0)
        self.entry_area = tk.Entry(self)
        self.entry_area.grid(row=1, column=1)

        tk.Button(self, text="Guardar", command=self.guardar).grid(row=2, column=0, columnspan=2)

    def guardar(self):
        employee = Employee(
            nombre=self.entry_nombre.get(),
            area=self.entry_area.get()
        )
        self.service.guardar_employee(employee)
        messagebox.showinfo("OK", "Employee guardado")