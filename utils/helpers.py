import re

def validar_correo(correo):
    patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(patron, correo))

def validar_telefono(telefono):
    patron = r'^\+?[\d\s-]{7,15}$'
    return bool(re.match(patron, telefono))
