"""Datos sintéticos de un turno de almuerzo en A Fénix de Oro.

No son datos de personas reales: las comandas solo llevan mesa, platos y hora.
La carta es la de ejemplo de afenix/carta.py.
"""

from datetime import datetime

import pytest

from afenix.comandas import registrar_comanda

SABADO = datetime(2026, 11, 28)


def plato(nombre, color="café", **extra):
    return {"plato": nombre, "color": color, **extra}


# (mesa, hora, minuto, platos). Están en el orden en que se registraron.
TURNO = [
    (7, 12, 10, [plato("Pollo General Tso's", "amarillo")]),
    (3, 12, 0, [plato("Arroz frito con piña", "amarillo"),
                plato("Arroz con todas las carnes", "café")]),
    (9, 12, 4, [plato("Chop suey", "café", cantidad=3)]),
    (2, 12, 4, [plato("Chop suey", "café")]),
    (12, 12, 1, [plato("Arroz oriental", "café")]),
]


@pytest.fixture
def turno():
    """Las comandas del turno, recién registradas y en estado recibido."""
    return [registrar_comanda(mesa, platos, ahora=SABADO.replace(hour=h, minute=m))
            for mesa, h, m, platos in TURNO]


@pytest.fixture
def platos_dificiles():
    """Platos con tildes, ñ, apóstrofo, cantidad alta y color vacío."""
    return {
        "ñ y tilde": plato("Arroz frito con piña", "café"),
        "apóstrofo": plato("Pollo General Tso's", "amarillo"),
        "cantidad en el tope": plato("Chop suey", "café", cantidad=20),
        "color vacío": plato("Chop suey", ""),
    }
