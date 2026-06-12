import tkinter as tk
from views.main_window import MainWindow
from database.connection import setup_database

if __name__ == "__main__":
    # Inicializar base de datos (esquema, tablas y semillas)
    setup_database()
    
    # Iniciar la interfaz gráfica
    root = tk.Tk()
    app = MainWindow(root)
    
    root.mainloop()