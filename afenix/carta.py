"""Carta de ejemplo de A Fénix de Oro.

Son datos de prueba, no la carta real del restaurante. Cada plato dice qué
opciones acepta en cada modificación: base, proteína, tamaño y picante.
"""

TAMANOS = ["personal", "familiar"]
PICANTES = ["sin picante", "medio", "picante"]

CARTA = {
    "Pollo General Tso's": {
        "base": ["arroz frito", "arroz blanco", "chop suey"],
        "proteina": ["pollo"],
        "tamano": TAMANOS,
        "picante": PICANTES,
    },
    "Chop suey": {
        "base": ["arroz frito", "arroz blanco"],
        "proteina": ["pollo", "cerdo", "res"],
        "tamano": TAMANOS,
        "picante": PICANTES,
    },
    "Arroz frito con piña": {
        "base": ["arroz frito"],
        "proteina": ["pollo", "cerdo", "camarón"],
        "tamano": TAMANOS,
        "picante": PICANTES,
    },
    "Cerdo agridulce": {
        "base": ["arroz frito", "arroz blanco", "chop suey"],
        "proteina": ["cerdo"],
        "tamano": TAMANOS,
        "picante": PICANTES,
    },
}

MODIFICACIONES = ["base", "proteina", "tamano", "picante"]
