import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from services.evaluation_service import EvaluationService


class ReportsView(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.service = EvaluationService()

        self.create_widgets()
        self.load_dashboard()

    # =============================
    # UI (SIN TÍTULO GRANDE)
    # =============================
    def create_widgets(self):

        container = ttk.Frame(self, padding=5)
        container.pack(fill=tk.BOTH, expand=True)

        self.dashboard_frame = ttk.Frame(container)
        self.dashboard_frame.pack(fill=tk.BOTH, expand=True)

    # =============================
    # DASHBOARD 2x2
    # =============================
    def load_dashboard(self):

        top = ttk.Frame(self.dashboard_frame)
        top.pack(fill=tk.BOTH, expand=True)

        bottom = ttk.Frame(self.dashboard_frame)
        bottom.pack(fill=tk.BOTH, expand=True)

        self.create_ranking_chart(top)
        self.create_area_chart(top)

        self.create_trend_chart(bottom)
        self.create_pie_chart(bottom)

    # =============================
    # 1. Ranking
    # =============================
    def create_ranking_chart(self, parent):

        frame = ttk.Frame(parent)
        frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.service.cursor.execute("""
            SELECT e.nombres, AVG(ev.total_puntos)
            FROM evaluaciones ev
            JOIN empleados e ON e.codigo = ev.codigo_empleado
            GROUP BY e.nombres
            ORDER BY AVG(ev.total_puntos) DESC
            LIMIT 5
        """)

        data = self.service.cursor.fetchall()

        nombres = [r[0] for r in data]
        valores = [float(r[1]) for r in data]

        colors = ["green" if v >= 45 else "orange" if v >= 35 else "red" for v in valores]

        fig, ax = plt.subplots(figsize=(4, 2))

        ax.bar(nombres, valores, color=colors)
        ax.set_title("Top", fontsize=9)

        plt.xticks(rotation=20, ha="right", fontsize=8)

        for i, v in enumerate(valores):
            ax.text(i, v + 0.3, f"{v:.1f}", ha='center', fontsize=8)

        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # =============================
    # 2. Área
    # =============================
    def create_area_chart(self, parent):

        frame = ttk.Frame(parent)
        frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.service.cursor.execute("""
            SELECT a.nombre, AVG(ev.total_puntos)
            FROM evaluaciones ev
            JOIN empleados e ON e.codigo = ev.codigo_empleado
            JOIN areas a ON a.id = e.area_id
            GROUP BY a.nombre
        """)

        data = self.service.cursor.fetchall()

        areas = [r[0] for r in data]
        valores = [float(r[1]) for r in data]

        fig, ax = plt.subplots(figsize=(4, 2))

        ax.bar(areas, valores, color="orange")
        ax.set_title("Área", fontsize=9)

        plt.xticks(rotation=20, ha="right", fontsize=8)

        for i, v in enumerate(valores):
            ax.text(i, v + 0.3, f"{v:.1f}", ha='center', fontsize=8)

        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # =============================
    # 3. Evolución
    # =============================
    def create_trend_chart(self, parent):

        frame = ttk.Frame(parent)
        frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.service.cursor.execute("""
            SELECT 
                EXTRACT(MONTH FROM created_at),
                AVG(total_puntos)
            FROM evaluaciones
            GROUP BY 1
            ORDER BY 1
        """)

        data = self.service.cursor.fetchall()

        meses = [f"M{int(r[0])}" for r in data]
        valores = [float(r[1]) for r in data]

        fig, ax = plt.subplots(figsize=(4, 2))

        ax.plot(meses, valores, marker="o", color="blue")
        ax.set_title("Evolución", fontsize=9)

        plt.xticks(rotation=20, fontsize=8)

        for i, v in enumerate(valores):
            ax.text(i, v, f"{v:.1f}", ha='center', fontsize=8)

        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # =============================
    # 4. Pie
    # =============================
    def create_pie_chart(self, parent):

        frame = ttk.Frame(parent)
        frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.service.cursor.execute("""
            SELECT promedio_total 
            FROM evaluacion_desempeno
        """)

        data = self.service.cursor.fetchall()

        excelente = sum(1 for (x,) in data if x > 45)
        muybueno = sum(1 for (x,) in data if 40 < x <= 45)
        bueno = sum(1 for (x,) in data if 35 < x <= 40)
        regular = sum(1 for (x,) in data if 30 < x <= 35)
        deficiente = sum(1 for (x,) in data if x <= 30)

        sizes = [excelente, muybueno, bueno, regular, deficiente]

        if sum(sizes) == 0:
            sizes = [1, 1, 1, 1, 1]

        labels = ["Excelente", "Muy bueno", "Bueno", "Regular", "Deficiente"]
        colors = ["green", "yellow", "orange", "lightgray", "red"]

        fig, ax = plt.subplots(figsize=(4, 2))

        ax.pie(
            sizes,
            labels=labels,
            autopct='%1.1f%%',
            colors=colors,
            textprops={'fontsize': 8}
        )

        ax.set_title("Calificación", fontsize=9)

        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)