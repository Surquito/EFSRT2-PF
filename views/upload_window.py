# views/upload_window.py

import tkinter as tk

from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

import os

from services.etl_service import process_excel
from database.connection import get_connection


class EvaluationUploadView(ttk.Frame):

    def __init__(self, parent):

        super().__init__(parent)

        # ==================================
        # VARIABLES
        # ==================================
        self.selected_file_path = tk.StringVar()

        self.create_widgets()

        # ==================================
        # CARGAR HISTORIAL
        # ==================================
        self.load_history()

    # ==================================
    # UI
    # ==================================
    def create_widgets(self):

        main_container = ttk.Frame(
            self,
            padding="30 30 30 30"
        )

        main_container.pack(
            fill=tk.BOTH,
            expand=True
        )

        # ==================================
        # DESCRIPCIÓN
        # ==================================
        instruction_text = (
            "Módulo de ingesta de datos para el "
            "procesamiento y normalización de "
            "archivos de evaluación (.xlsx)."
        )

        instruction_label = ttk.Label(
            main_container,
            text=instruction_text,
            wraplength=800,
            justify=tk.LEFT,
            font=("Arial", 10),
            foreground="#475569"
        )

        instruction_label.pack(
            anchor=tk.W,
            pady=(0, 30)
        )

        # ==================================
        # FILE FRAME
        # ==================================
        file_frame = ttk.LabelFrame(
            main_container,
            text=" Selección de archivo ",
            padding="20 20 20 20"
        )

        file_frame.pack(
            fill=tk.X,
            pady=(0, 25)
        )

        # ==================================
        # INPUT PATH
        # ==================================
        self.entry_path = ttk.Entry(
            file_frame,
            textvariable=self.selected_file_path,
            width=70,
            state="disabled"
        )

        self.entry_path.pack(
            side=tk.LEFT,
            padx=(0, 15),
            ipady=4
        )

        # ==================================
        # BOTÓN BUSCAR
        # ==================================
        self.btn_browse = ttk.Button(
            file_frame,
            text="Buscar Archivo...",
            command=self.browse_file
        )

        self.btn_browse.pack(
            side=tk.LEFT,
            ipady=2
        )

        # ==================================
        # TIPO EVALUACIÓN
        # ==================================
        ttk.Label(
            main_container,
            text="Tipo de Evaluación:"
        ).pack(anchor=tk.W)

        self.evaluation_type_combo = ttk.Combobox(
            main_container,
            state="readonly",
            values=[
                "Calidad",
                "Operativa",
                "Productividad",
                "Habilidades Blandas",
            ]
        )

        self.evaluation_type_combo.pack(
            fill=tk.X,
            pady=(5, 20)
        )

        # ==================================
        # PROCESS FRAME
        # ==================================
        process_frame = ttk.Frame(
            main_container
        )

        process_frame.pack(
            fill=tk.X,
            pady=(0, 20)
        )

        # ==================================
        # PROGRESS BAR
        # ==================================
        self.progress_bar = ttk.Progressbar(
            process_frame,
            mode="determinate"
        )

        self.progress_bar.pack(
            fill=tk.X,
            pady=(0, 20)
        )

        # ==================================
        # BOTÓN CARGAR
        # ==================================
        self.btn_upload = ttk.Button(
            process_frame,
            text="Procesar y Cargar a Supabase",
            state="disabled",
            command=self.process_and_upload
        )

        self.btn_upload.pack(
            anchor=tk.E,
            ipady=4,
            ipadx=10
        )

        # ==================================
        # TABLA HISTORIAL
        # ==================================
        table_frame = ttk.LabelFrame(
            main_container,
            text=" Historial de Archivos Procesados ",
            padding="10"
        )

        table_frame.pack(
            fill=tk.BOTH,
            expand=True,
            pady=(5, 0)
        )

        columns = (
            "file_name",
            "evaluation_type",
            "upload_date",
            "status"
        )

        self.history_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=8
        )

        self.history_tree.pack(
            side=tk.LEFT,
            fill=tk.BOTH,
            expand=True
        )

        # ==================================
        # HEADERS
        # ==================================
        self.history_tree.heading(
            "file_name",
            text="Archivo"
        )

        self.history_tree.heading(
            "evaluation_type",
            text="Tipo Evaluación"
        )

        self.history_tree.heading(
            "upload_date",
            text="Fecha Carga"
        )

        self.history_tree.heading(
            "status",
            text="Estado"
        )

        # ==================================
        # COLUMNAS
        # ==================================
        self.history_tree.column(
            "file_name",
            width=260,
            anchor=tk.W
        )

        self.history_tree.column(
            "evaluation_type",
            width=180,
            anchor=tk.CENTER
        )

        self.history_tree.column(
            "upload_date",
            width=180,
            anchor=tk.CENTER
        )

        self.history_tree.column(
            "status",
            width=120,
            anchor=tk.CENTER
        )

        # ==================================
        # SCROLLBAR
        # ==================================
        scrollbar = ttk.Scrollbar(
            table_frame,
            orient=tk.VERTICAL,
            command=self.history_tree.yview
        )

        self.history_tree.configure(
            yscrollcommand=scrollbar.set
        )

        scrollbar.pack(
            side=tk.RIGHT,
            fill=tk.Y
        )

    # ==================================
    # BUSCAR ARCHIVO
    # ==================================
    def browse_file(self):

        file_types = [
            ("Excel Files", "*.xlsx")
        ]

        file_selected = filedialog.askopenfilename(
            title="Seleccionar Dataset",
            filetypes=file_types
        )

        if file_selected:

            self.selected_file_path.set(
                file_selected
            )

            self.btn_upload.config(
                state="normal"
            )

    # ==================================
    # PROCESAR EXCEL
    # ==================================
    def process_and_upload(self):

        full_path = self.selected_file_path.get()

        evaluation_type = (
            self.evaluation_type_combo.get()
        )

        if not full_path:

            messagebox.showwarning(
                "Advertencia",
                "Seleccione un archivo"
            )

            return

        if not evaluation_type:

            messagebox.showwarning(
                "Advertencia",
                "Seleccione un tipo de evaluación"
            )

            return

        try:

            # BLOQUEAR BOTONES
            self.btn_upload.config(
                state="disabled"
            )

            self.btn_browse.config(
                state="disabled"
            )

            # BARRA PROGRESO
            self.progress_bar['value'] = 20

            self.update_idletasks()

            # ==================================
            # PROCESAR ETL
            # ==================================
            process_excel(
                full_path,
                evaluation_type
            )

            self.progress_bar['value'] = 100

            # ==================================
            # RECARGAR HISTORIAL
            # ==================================
            self.reload_history()

            # ==================================
            # MENSAJE
            # ==================================
            messagebox.showinfo(
                "Éxito",
                "Archivo procesado correctamente"
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

        finally:

            # RESET UI
            self.progress_bar['value'] = 0

            self.selected_file_path.set("")

            self.evaluation_type_combo.set("")

            self.btn_upload.config(
                state="disabled"
            )

            self.btn_browse.config(
                state="normal"
            )

    # ==================================
    # CARGAR HISTORIAL
    # ==================================
    def load_history(self):

        conn = get_connection()

        cursor = conn.cursor()

        try:

            cursor.execute("""
                SELECT
                    nombre_archivo,
                    tipo_evaluacion,
                    fecha_carga,
                    estado
                FROM historial_cargas
                ORDER BY fecha_carga DESC
            """)

            rows = cursor.fetchall()

            for row in rows:

                self.history_tree.insert(
                    "",
                    tk.END,
                    values=row
                )

        except Exception as e:

            print(
                "Error cargando historial:",
                e
            )

        finally:

            cursor.close()

            conn.close()

    # ==================================
    # RECARGAR TREEVIEW
    # ==================================
    def reload_history(self):

        # LIMPIAR TABLA
        for item in self.history_tree.get_children():

            self.history_tree.delete(item)

        # VOLVER A CARGAR
        self.load_history()

