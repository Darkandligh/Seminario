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


def test_cantidad_justo_encima_del_tope_se_rechaza(platos_dificiles):
    # límite: 21 es el primer valor inválido; el 20 lo cubre test_abuso_comandas.py
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


@pytest.mark.parametrize("mesa, items", [
    (4, [{"plato": "Chop suey", "base": "", "proteina": "res",
          "tamano": "personal", "picante": "medio"}]),   # falta la base
    (4, [{"plato": "Chop suey", "base": "arroz frito", "proteina": "",
          "tamano": "personal", "picante": "medio"}]),   # falta la proteína
    (4, []),                                             # sin platos
    (0, [{"plato": "Chop suey", "base": "arroz frito", "proteina": "res",
          "tamano": "personal", "picante": "medio"}]),   # mesa 0
])
def test_lo_incompleto_no_se_marca_como_fuera_de_carta(mesa, items):
    # Lo incompleto es 400 en la API y lo que no está en la carta es 422
    with pytest.raises(ComandaInvalida) as error:
        registrar_comanda(mesa, items)
    assert type(error.value) is ComandaInvalida
