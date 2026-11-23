"""Datos sintéticos de un turno de almuerzo en A Fénix de Oro.

No son datos de personas reales: las comandas solo llevan mesa, platos y hora.
La carta es la de ejemplo de afenix/carta.py.
"""

from datetime import datetime

import pytest

from afenix.comandas import registrar_comanda

SABADO = datetime(2026, 11, 28)


def plato(nombre, base, proteina, tamano="personal", picante="medio", **extra):
    return {"plato": nombre, "base": base, "proteina": proteina,
            "tamano": tamano, "picante": picante, **extra}


# (mesa, hora, minuto, platos). Están en el orden en que se registraron.
TURNO = [
    (7, 12, 10, [plato("Pollo General Tso's", "chop suey", "pollo", picante="picante")]),
    (3, 12, 0, [plato("Arroz frito con piña", "arroz frito", "camarón", "familiar"),
                plato("Cerdo agridulce", "arroz blanco", "cerdo", picante="sin picante")]),
    (9, 12, 4, [plato("Chop suey", "arroz blanco", "res", cantidad=3)]),
    (2, 12, 4, [plato("Chop suey", "arroz frito", "pollo")]),
    (12, 12, 1, [plato("Arroz frito con piña", "arroz frito", "pollo")]),
]


@pytest.fixture
def turno():
    """Las comandas del turno, recién registradas y en estado recibido."""
    return [registrar_comanda(mesa, platos, ahora=SABADO.replace(hour=h, minute=m))
            for mesa, h, m, platos in TURNO]


@pytest.fixture
def platos_dificiles():
    """Platos con tildes, ñ, apóstrofo, cantidad alta y picante vacío."""
    return {
        "ñ y tilde": plato("Arroz frito con piña", "arroz frito", "camarón"),
        "apóstrofo": plato("Pollo General Tso's", "arroz frito", "pollo"),
        "cantidad en el tope": plato("Chop suey", "arroz frito", "res", cantidad=20),
        "picante vacío": plato("Chop suey", "arroz frito", "res", picante=""),
    }
