from datetime import datetime, time

def convertir_a_time(valor):
    try:
        # Convierte de "HH:mm" a un objeto de tipo time
        return datetime.strptime(valor, "%H:%M").time()
    except ValueError:
        raise ValueError(f"El valor '{valor}' no tiene el formato correcto de hora (HH:mm).") 
