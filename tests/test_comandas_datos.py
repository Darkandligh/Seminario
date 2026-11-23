"""Casos de registrar_comanda que faltaban en la tabla de la semana 7 (regla 1)."""

import pytest

from afenix.comandas import ComandaInvalida, registrar_comanda


@pytest.mark.parametrize("caso, nombre", [
    ("ñ y tilde", "Arroz frito con piña"),  # el nombre con ñ no se daña
    ("apóstrofo", "Pollo General Tso's"),   # el apóstrofo no se pierde
])
def test_nombres_dificiles_quedan_iguales(platos_dificiles, caso, nombre):
    comanda = registrar_comanda(4, [platos_dificiles[caso]])
    assert comanda.platos[0].nombre == nombre


def test_camaron_con_tilde_es_la_opcion_de_la_carta(platos_dificiles):
    assert registrar_comanda(4, [platos_dificiles["ñ y tilde"]]).platos[0].proteina == "camarón"


def test_cantidad_en_el_tope_se_acepta(platos_dificiles):
    # límite: 20 es el último valor válido
    assert registrar_comanda(4, [platos_dificiles["cantidad en el tope"]]).platos[0].cantidad == 20


def test_cantidad_justo_encima_del_tope_se_rechaza(platos_dificiles):
    # límite: 21 es el primer valor inválido
    plato = {**platos_dificiles["cantidad en el tope"], "cantidad": 21}
    with pytest.raises(ComandaInvalida, match="La cantidad máxima por plato es 20"):
        registrar_comanda(4, [plato])


def test_picante_vacio_dice_que_falta(platos_dificiles):
    with pytest.raises(ComandaInvalida, match="Falta el picante de «Chop suey»"):
        registrar_comanda(4, [platos_dificiles["picante vacío"]])


def test_turno_completo_queda_recibido(turno):
    assert [(c.mesa, c.estado, len(c.platos)) for c in turno] == [
        (7, "recibido", 1), (3, "recibido", 2), (9, "recibido", 1),
        (2, "recibido", 1), (12, "recibido", 1),
    ]
