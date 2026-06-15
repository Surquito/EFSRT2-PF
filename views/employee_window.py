import tkinter as tk
from tkinter import ttk, messagebox
from models.employee import Employee
import services.employee_service as employee_service
from utils.helpers import validar_correo, validar_telefono
from datetime import datetime

class EmployeeView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.dict_areas = {}
        
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        
        self.frame_formulario = ttk.LabelFrame(self, text=" Registro de Empleados ", padding=15)
        self.frame_formulario.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        for i in range(4):
            self.frame_formulario.columnconfigure(i, weight=1)
            
        lbl_nombres = tk.Label(self.frame_formulario, text="Nombres:", font=("Arial", 10, "bold"), fg="#1e293b", anchor="w")
        lbl_nombres.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_nombres = ttk.Entry(self.frame_formulario, font=("Arial", 10))
        self.entry_nombres.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        lbl_fecha = tk.Label(self.frame_formulario, text="Fecha Ingreso (AAAA-MM-DD):", font=("Arial", 10, "bold"), fg="#1e293b", anchor="w")
        lbl_fecha.grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.entry_fecha = ttk.Entry(self.frame_formulario, font=("Arial", 10))
        self.entry_fecha.grid(row=0, column=3, padx=5, pady=5, sticky="ew")
        self.entry_fecha.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        lbl_apellidos = tk.Label(self.frame_formulario, text="Apellidos:", font=("Arial", 10, "bold"), fg="#1e293b", anchor="w")
        lbl_apellidos.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_apellidos = ttk.Entry(self.frame_formulario, font=("Arial", 10))
        self.entry_apellidos.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        lbl_area = tk.Label(self.frame_formulario, text="Área:", font=("Arial", 10, "bold"), fg="#1e293b", anchor="w")
        lbl_area.grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.combo_area = ttk.Combobox(self.frame_formulario, state="readonly", font=("Arial", 10))
        self.combo_area.grid(row=1, column=3, padx=5, pady=5, sticky="ew")
        
        lbl_correo = tk.Label(self.frame_formulario, text="Correo:", font=("Arial", 10, "bold"), fg="#1e293b", anchor="w")
        lbl_correo.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_correo = ttk.Entry(self.frame_formulario, font=("Arial", 10))
        self.entry_correo.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        
        lbl_codigo = tk.Label(self.frame_formulario, text="Código:", font=("Arial", 10, "bold"), fg="#1e293b", anchor="w")
        lbl_codigo.grid(row=2, column=2, padx=5, pady=5, sticky="w")
        self.entry_codigo = ttk.Entry(self.frame_formulario, font=("Arial", 10))
        self.entry_codigo.grid(row=2, column=3, padx=5, pady=5, sticky="ew")
        
        lbl_telefono = tk.Label(self.frame_formulario, text="Teléfono:", font=("Arial", 10, "bold"), fg="#1e293b", anchor="w")
        lbl_telefono.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.entry_telefono = ttk.Entry(self.frame_formulario, font=("Arial", 10))
        self.entry_telefono.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        
        lbl_estado = tk.Label(self.frame_formulario, text="Estado:", font=("Arial", 10, "bold"), fg="#1e293b", anchor="w")
        lbl_estado.grid(row=3, column=2, padx=5, pady=5, sticky="w")
        
        self.var_estado = tk.StringVar(value="Activo")
        frame_radio = ttk.Frame(self.frame_formulario)
        frame_radio.grid(row=3, column=3, padx=5, pady=5, sticky="w")
        
        r_activo = ttk.Radiobutton(frame_radio, text="Activo", variable=self.var_estado, value="Activo")
        r_activo.pack(side="left", padx=5)
        r_inactivo = ttk.Radiobutton(frame_radio, text="Inactivo", variable=self.var_estado, value="Inactivo")
        r_inactivo.pack(side="left", padx=5)
        
        frame_botones = ttk.Frame(self.frame_formulario)
        frame_botones.grid(row=4, column=0, columnspan=4, pady=10)
        
        style = ttk.Style()
        style.configure("Accent.TButton", font=("Arial", 10, "bold"), foreground="white", background="#10b981")
        style.map("Accent.TButton", background=[("active", "#059669")])
        
        btn_crear = ttk.Button(frame_botones, text="CREAR", width=12, style="Accent.TButton", command=self.crear)
        btn_crear.pack(side="left", padx=8)
        
        btn_buscar = ttk.Button(frame_botones, text="BUSCAR", width=12, command=self.buscar)
        btn_buscar.pack(side="left", padx=8)
        
        btn_guardar = ttk.Button(frame_botones, text="GUARDAR", width=12, command=self.guardar)
        btn_guardar.pack(side="left", padx=8)
        
        btn_eliminar = ttk.Button(frame_botones, text="ELIMINAR", width=12, command=self.eliminar)
        btn_eliminar.pack(side="left", padx=8)
        
        btn_limpiar = ttk.Button(frame_botones, text="LIMPIAR", width=12, command=self.limpiar_formulario)
        btn_limpiar.pack(side="left", padx=8)
        
        self.frame_tabla = ttk.LabelFrame(self, text=" Empleados Registrados ", padding=5)
        self.frame_tabla.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        self.frame_tabla.columnconfigure(0, weight=1)
        self.frame_tabla.rowconfigure(0, weight=1)
        
        columnas = ("codigo", "nombres", "apellidos", "correo", "telefono", "estado", "fecha", "area")
        self.tree = ttk.Treeview(self.frame_tabla, columns=columnas, show="headings")
        
        self.tree.heading("codigo", text="Código")
        self.tree.heading("nombres", text="Nombres")
        self.tree.heading("apellidos", text="Apellidos")
        self.tree.heading("correo", text="Correo")
        self.tree.heading("telefono", text="Teléfono")
        self.tree.heading("estado", text="Estado")
        self.tree.heading("fecha", text="Fecha de Ingreso")
        self.tree.heading("area", text="Área")
        
        self.tree.column("codigo", width=80, anchor="center")
        self.tree.column("nombres", width=120)
        self.tree.column("apellidos", width=120)
        self.tree.column("correo", width=160)
        self.tree.column("telefono", width=100, anchor="center")
        self.tree.column("estado", width=80, anchor="center")
        self.tree.column("fecha", width=110, anchor="center")
        self.tree.column("area", width=120)
        
        scroll_y = ttk.Scrollbar(self.frame_tabla, orient="vertical", command=self.tree.yview)
        scroll_x = ttk.Scrollbar(self.frame_tabla, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")
        
        self.tree.bind("<<TreeviewSelect>>", self.al_seleccionar_fila)
        
        self.cargar_combobox_areas()
        self.cargar_tabla()

    def cargar_combobox_areas(self):
        areas = employee_service.obtener_areas()
        self.dict_areas = {a[1]: a[0] for a in areas}
        self.combo_area['values'] = list(self.dict_areas.keys())
        if self.combo_area['values']:
            self.combo_area.set("Seleccione")

    def cargar_tabla(self, lista_empleados=None):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        if lista_empleados is None:
            lista_empleados = employee_service.obtener_empleados()
            
        for emp in lista_empleados:
            self.tree.insert("", "end", values=(
                emp[0], emp[1], emp[2], emp[3], emp[4], emp[5], emp[6], emp[7]
            ))

    def al_seleccionar_fila(self, event):
        seleccion = self.tree.selection()
        if not seleccion:
            return
            
        valores = self.tree.item(seleccion[0], "values")
        if valores:
            self.limpiar_campos()
            
            self.entry_codigo.delete(0, tk.END)
            self.entry_codigo.insert(0, valores[0])
            self.entry_codigo.config(state="readonly")
            
            self.entry_nombres.insert(0, valores[1])
            self.entry_apellidos.insert(0, valores[2])
            self.entry_correo.insert(0, valores[3])
            self.entry_telefono.insert(0, valores[4])
            self.var_estado.set(valores[5])
            
            self.entry_fecha.delete(0, tk.END)
            self.entry_fecha.insert(0, valores[6])
            
            self.combo_area.set(valores[7] if valores[7] else "Seleccione")

    def limpiar_campos(self):
        self.entry_codigo.config(state="normal")
        self.entry_codigo.delete(0, tk.END)
        self.entry_nombres.delete(0, tk.END)
        self.entry_apellidos.delete(0, tk.END)
        self.entry_correo.delete(0, tk.END)
        self.entry_telefono.delete(0, tk.END)
        self.entry_fecha.delete(0, tk.END)
        self.entry_fecha.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.combo_area.set("Seleccione")
        self.var_estado.set("Activo")

    def limpiar_formulario(self):
        self.limpiar_campos()
        self.tree.selection_remove(self.tree.selection())
        self.cargar_tabla()

    def recolectar_datos(self):
        codigo = self.entry_codigo.get().strip()
        nombres = self.entry_nombres.get().strip()
        apellidos = self.entry_apellidos.get().strip()
        correo = self.entry_correo.get().strip()
        telefono = self.entry_telefono.get().strip()
        fecha_str = self.entry_fecha.get().strip()
        estado = self.var_estado.get()
        area_nombre = self.combo_area.get()
        
        if not codigo or not nombres or not apellidos or not correo or not telefono or not fecha_str:
            messagebox.showwarning("Atención", "Por favor, llene todos los campos.")
            return None
            
        if area_nombre == "Seleccione" or not area_nombre:
            messagebox.showwarning("Atención", "Seleccione un área de la lista.")
            return None
            
        if not validar_correo(correo):
            messagebox.showwarning("Atención", "El correo no tiene un formato válido.")
            return None
            
        if not validar_telefono(telefono):
            messagebox.showwarning("Atención", "El número de teléfono no es válido.")
            return None
            
        try:
            datetime.strptime(fecha_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showwarning("Atención", "Use el formato AAAA-MM-DD para la fecha.")
            return None
            
        area_id = self.dict_areas.get(area_nombre)
        
        return Employee(
            codigo=codigo,
            nombres=nombres,
            apellidos=apellidos,
            correo=correo,
            telefono=telefono,
            estado=estado,
            fecha_ingreso=fecha_str,
            area_id=area_id,
            area_nombre=area_nombre
        )

    def crear(self):
        emp = self.recolectar_datos()
        if not emp:
            return
            
        empleados_existentes = employee_service.obtener_empleados()
        codigos = [e[0] for e in empleados_existentes]
        if emp.codigo in codigos:
            messagebox.showerror("Error", "Este código ya existe.")
            return
            
        exito = employee_service.crear_empleado(emp)
        if exito:
            messagebox.showinfo("Éxito", "¡Empleado registrado con éxito!")
            self.limpiar_formulario()
            self.cargar_tabla()
        else:
            messagebox.showerror("Error", "Hubo un error al guardar.")

    def buscar(self):
        criterio = self.entry_codigo.get().strip()
        if not criterio:
            criterio = self.entry_nombres.get().strip()
        if not criterio:
            criterio = self.entry_apellidos.get().strip()
            
        if not criterio:
            messagebox.showwarning("Atención", "Escriba un término de búsqueda.")
            return
            
        resultados = employee_service.buscar_empleados(criterio)
        self.cargar_tabla(resultados)
        if not resultados:
            messagebox.showinfo("Búsqueda", "No se encontró ningún empleado.")

    def guardar(self):
        emp = self.recolectar_datos()
        if not emp:
            return
            
        exito = employee_service.actualizar_empleado(emp)
        if exito:
            messagebox.showinfo("Éxito", "¡Datos modificados con éxito!")
            self.limpiar_formulario()
            self.cargar_tabla()
        else:
            messagebox.showerror("Error", "Error al modificar los datos.")

    def eliminar(self):
        codigo = self.entry_codigo.get().strip()
        if not codigo:
            messagebox.showwarning("Atención", "Seleccione un empleado para poder eliminarlo.")
            return
            
        confirmar = messagebox.askyesno("Confirmar", f"¿Seguro que quieres eliminar al empleado con código '{codigo}'?")
        if confirmar:
            exito = employee_service.eliminar_empleado(codigo)
            if exito:
                messagebox.showinfo("Éxito", "¡Empleado eliminado!")
                self.limpiar_formulario()
                self.cargar_tabla()
            else:
                messagebox.showerror("Error", "No se pudo eliminar.")