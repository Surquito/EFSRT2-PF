class Employee:
    def __init__(self, codigo, nombres, apellidos, correo, telefono, estado, fecha_ingreso, area_id=None, area_nombre=None):
        self.codigo = codigo
        self.nombres = nombres
        self.apellidos = apellidos
        self.correo = correo
        self.telefono = telefono
        self.estado = estado  # 'Activo' o 'Inactivo'
        self.fecha_ingreso = fecha_ingreso  # 'YYYY-MM-DD'
        self.area_id = area_id
        self.area_nombre = area_nombre