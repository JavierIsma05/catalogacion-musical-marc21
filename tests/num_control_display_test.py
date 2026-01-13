# Script de prueba: visualización de num_control sin la letra inicial
# No modifica el código del proyecto, demostración local.
import re

examples = [
    "M000009",
    "I000123",
    "M000001",
    "I999999",
    "000008",  # caso sin prefijo
    "X000010",
]

def display_without_prefix(num_control: str) -> str:
    """Elimina cualquier prefijo no numérico al inicio y devuelve el resto.
    Si no hay dígitos, devuelve la cadena original.
    """
    m = re.search(r"(\d+)", num_control)
    return m.group(1) if m else num_control

if __name__ == '__main__':
    print("Demostración: mostrar num_control sin letra de tipo (solo números):\n")
    for n in examples:
        print(f"Original: {n}  -> Mostrar: {display_without_prefix(n)}")
