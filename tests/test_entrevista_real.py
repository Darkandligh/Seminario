"""Reglas que salen de la entrevista real con el restaurante (P-03).

Respuesta 10 de la entrevista: «12 mesas».
"""

import pytest

from afenix.comandas import ComandaInvalida, registrar_comanda

PLATO = {"plato": "Chop suey", "color": "café"}


def test_la_mesa_12_es_valida():
    assert registrar_comanda(12, [PLATO]).mesa == 12


def test_la_mesa_13_no_existe():
    with pytest.raises(ComandaInvalida, match="El restaurante tiene 12 mesas"):
        registrar_comanda(13, [PLATO])
