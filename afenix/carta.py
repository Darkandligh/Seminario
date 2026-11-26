"""Carta de ejemplo de A Fénix de Oro.

Sale de la entrevista real (requisitos v3): el cliente pide el plato y el
color, por ejemplo «dame un chop suey café». Los platos y los colores de cada
uno son de ejemplo hasta tener la carta completa del restaurante (P-04).
"""

COLORES = ["café", "amarillo"]

CARTA = {
    "Arroz sencillo": {"color": COLORES},
    "Arroz con todas las carnes": {"color": COLORES},
    "Arroz oriental": {"color": COLORES},
    "Arroz frito con piña": {"color": COLORES},
    "Pollo General Tso's": {"color": COLORES},
    "Chop suey": {"color": ["café"]},
    "Espaguetis": {"color": ["café"]},
    "Tortilla": {"color": ["amarillo"]},
}

MODIFICACIONES = ["color"]
