import random
from colorama import Fore

colorsList = [Fore.GREEN, Fore.BLUE, Fore.YELLOW, Fore.MAGENTA, Fore.CYAN]  # List of Colors
usedColors = []

def assignColor() -> str:
    if len(colorsList) > 0:
        color = random.choice(colorsList)
        colorsList.remove(color)  # Remove color from list of available colors
        usedColors.append(color)
        return color
    return None

def recoverColor(color:str) -> None:
    if len(usedColors) > 0:
        if color in usedColors:
            colorsList.append(color)
            usedColors.remove(color)