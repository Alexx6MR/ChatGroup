import random
from colorama import Fore

# Lista de colores disponibles
colorsList = [Fore.RED, Fore.GREEN, Fore.BLUE, Fore.YELLOW, Fore.MAGENTA, Fore.CYAN, Fore.WHITE]
assignedColors = {}  # Diccionario para almacenar colores asignados a usuarios

def assign_color(nickname: str):
    if len(colorsList) > 0:
        color = random.choice(colorsList)
        colorsList.remove(color)  # Eliminar el color de la lista de colores disponibles
        assignedColors[nickname] = color  # Guardar el color asignado al nickname
        return color
    return None
