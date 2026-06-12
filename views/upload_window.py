# views/upload_window.py
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import os
import time
from datetime import datetime

class EvaluationUploadView(ttk.Frame):
    def __init__(self, parent):
        # Initialize as a standard ttk.Frame integrated into the Notebook
        super().__init__(parent)
        
        # Variable to store the selected file path
        self.selected_file_path = tk.StringVar()
        
        self.create_widgets()
        
    def create_widgets(self):
        # Main layout container with margin padding
        main_container = ttk.Frame(self, padding="30 30 30 30")
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Header Section
        header_label = ttk.Label(
            main_container, 
            text="Carga Masiva de Evaluaciones (Proceso ETL)", 
            font=("Arial", 16, "bold"),
            foreground="#0f172a"
        )
        header_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Technical description according to project rules
        instruction_text = (
            "Módulo de ingesta de datos para el procesamiento y normalización de archivos de "
            "evaluación (.xlsx). El sistema procesará las 20 preguntas distribuidas en los bloques de "
            "Calidad, Operatividad, Habilidades Blandas y Productividad para calcular el rendimiento final."
        )
        instruction_label = ttk.Label(
            main_container, 
            text=instruction_text, 
            wraplength=800, 
            justify=tk.LEFT,
            font=("Arial", 10),
            foreground="#475569"
        )
        instruction_label.pack(anchor=tk.W, pady=(0, 30))
        
        # File Browser Area (Card-like layout)
        file_frame = ttk.LabelFrame(main_container, text=" Selección del Dataset ", padding="20 20 20 20")
        file_frame.pack(fill=tk.X, pady=(0, 25))
        
        # Path Display Entry
        self.entry_path = ttk.Entry(
            file_frame, 
            textvariable=self.selected_file_path, 
            width=70, 
            state="disabled"
        )
        self.entry_path.pack(side=tk.LEFT, padx=(0, 15), ipady=4)
        
        # Browse Button
        self.btn_browse = ttk.Button(
            file_frame, 
            text="Buscar Archivo...", 
            command=self.browse_file
        )
        self.btn_browse.pack(side=tk.LEFT, ipady=2)
        
        # Execution & Progress Area
        process_frame = ttk.Frame(main_container)
        process_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.progress_bar = ttk.Progressbar(process_frame, mode="determinate")
        self.progress_bar.pack(fill=tk.X, pady=(0, 20))
        
        # Action Buttons
        self.btn_upload = ttk.Button(
            process_frame, 
            text="Procesar y Cargar a Supabase", 
            state="disabled", 
            command=self.process_and_upload_mock
        )
        self.btn_upload.pack(anchor=tk.E, ipady=4, ipadx=10)

        # --- HISTORICAL TABLE SECTION ---
        table_frame = ttk.LabelFrame(main_container, text=" Historial de Archivos Procesados ", padding="10")
        table_frame.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        
        # Definition of columns for the Treeview standard (English naming convention)
        columns = ("file_name", "upload_date", "status")
        
        self.history_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=5)
        self.history_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Configure headers with clear naming
        self.history_tree.heading("file_name", text="Nombre del Archivo")
        self.history_tree.heading("upload_date", text="Fecha y Hora de Subida")
        self.history_tree.heading("status", text="Estado del Proceso")
        
        # Configure columns widths and alignments
        self.history_tree.column("file_name", width=400, anchor=tk.W)
        self.history_tree.column("upload_date", width=200, anchor=tk.CENTER)
        self.history_tree.column("status", width=150, anchor=tk.CENTER)
        
        # Vertical Scrollbar integration for Treeview 
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=scrollbar.set)

    def browse_file(self):
        """Opens a file dialog to select the evaluation dataset."""
        file_types = [("Excel Files", "*.xlsx")]
        file_selected = filedialog.askopenfilename(
            title="Seleccionar Dataset de Evaluaciones", 
            filetypes=file_types
        )
        
        if file_selected:
            self.selected_file_path.set(file_selected)
            self.btn_upload.config(state="normal") # Enable action button
            
    def process_and_upload_mock(self):
        """Simulates the backend data conversion and cloud storage transmission."""
        full_path = self.selected_file_path.get()
        # Extract only the file name from the full system path
        file_name = os.path.basename(full_path)
        
        # Lock buttons to prevent multiple concurrent execution flows
        self.btn_browse.config(state="disabled")
        self.btn_upload.config(state="disabled")
        
        # Reset and animate the progress bar UI
        self.progress_bar['value'] = 0
        self.update_idletasks()
        
        # Loop steps to simulate calculations across 20 attributes
        for i in range(1, 6):
            time.sleep(0.3)  # Simulates processing chunk execution
            self.progress_bar['value'] = i * 20
            self.update_idletasks()
        
        # Get exact real-time system date and time for tracking purposes
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Insert the metadata dynamically into the first position of the Treeview
        self.history_tree.insert("", 0, values=(file_name, current_time, "Éxito (Supabase)"))

        # UI success notification showing structured results
        messagebox.showinfo(
            "Proceso ETL Exitoso",
            "¡Ingesta de datos finalizada con éxito!\n\n"
            "- Archivo analizado: 'evaluacion_desempeño_finsupport.xlsx'\n"
            "- Parámetros evaluados: 20 preguntas (Calidad, Operatividad, Blandas, Productividad)\n"
            "- Registros procesados: 10 colaboradores (Empleados 2 - 11)\n"
            "- Persistencia: Métricas calculadas y sincronizadas con PostgreSQL en la nube."
        )
        
        # Reset view components to initial state
        self.progress_bar['value'] = 0
        self.selected_file_path.set("")
        self.btn_browse.config(state="normal")