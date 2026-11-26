"""Pruebas de registrar_comanda (HU-01 y HU-02).

Actualizadas el 2026-11-26: la entrevista real cambió la HU-02. El cliente pide
el plato y el color, no base, proteína, tamaño y picante. Las pruebas comprueban
lo mismo que antes (normales, límite y error), con los datos del requisito real.

Están separadas en normales, de límite y de error. Cada una dice de qué
escenario sale cuando viene directo de una historia.
"""

from datetime import datetime

import pytest

from afenix.comandas import RECIBIDO, ComandaInvalida, FueraDeCarta, registrar_comanda

HORA = datetime(2026, 11, 23, 12, 5)


def plato(nombre="Chop suey", color="café", **extra):
    return {"plato": nombre, "color": color, **extra}


# ---------- Normales ----------

def test_comanda_valida_queda_recibida_con_mesa_platos_y_hora():
    # HU-01, escenario 1
    comanda = registrar_comanda(4, [plato("Arroz frito con piña"), plato("Chop suey")], ahora=HORA)

    assert comanda.mesa == 4
    assert [p.nombre for p in comanda.platos] == ["Arroz frito con piña", "Chop suey"]
    assert comanda.estado == RECIBIDO
    assert comanda.hora_entrada == HORA


def test_plato_guarda_su_color():
    # HU-02, escenario 1
    comanda = registrar_comanda(4, [plato("Arroz con todas las carnes", color="café")], ahora=HORA)
    p = comanda.platos[0]

    assert (p.nombre, p.color) == ("Arroz con todas las carnes", "café")


def test_cantidad_por_defecto_es_uno():
    assert registrar_comanda(4, [plato()], ahora=HORA).platos[0].cantidad == 1


# ---------- Límite ----------

def test_mesa_uno_es_valida():
    assert registrar_comanda(1, [plato()], ahora=HORA).mesa == 1


def test_mesa_cero_se_rechaza():
    with pytest.raises(ComandaInvalida, match="La mesa debe ser un número mayor que cero"):
        registrar_comanda(0, [plato()], ahora=HORA)


def test_un_solo_plato_es_valido():
    assert len(registrar_comanda(4, [plato()], ahora=HORA).platos) == 1


def test_cantidad_cero_se_rechaza():
    with pytest.raises(ComandaInvalida, match="La cantidad debe ser un número mayor que cero"):
        registrar_comanda(4, [plato(cantidad=0)], ahora=HORA)


# ---------- Error ----------

@pytest.mark.parametrize("platos", [[], None])
def test_comanda_sin_platos_se_rechaza(platos):
    # HU-01, escenario 2
    with pytest.raises(ComandaInvalida, match="La comanda debe tener al menos un plato"):
        registrar_comanda(4, platos, ahora=HORA)


@pytest.mark.parametrize("mesa", [-3, "4", None, True])
def test_mesa_que_no_es_entero_positivo_se_rechaza(mesa):
    with pytest.raises(ComandaInvalida, match="La mesa debe ser un número mayor que cero"):
        registrar_comanda(mesa, [plato()], ahora=HORA)


def test_color_fuera_de_la_carta_se_rechaza():
    # HU-02, escenario 2
    with pytest.raises(FueraDeCarta, match="El color no está en la carta"):
        registrar_comanda(4, [plato("Chop suey", color="verde")], ahora=HORA)


def test_plato_que_no_esta_en_la_carta_se_rechaza():
    with pytest.raises(FueraDeCarta, match="no está en la carta"):
        registrar_comanda(4, [plato("Pizza hawaiana")], ahora=HORA)


@pytest.mark.parametrize("color", ["", None])
def test_falta_el_color_se_rechaza(color):
    with pytest.raises(ComandaInvalida, match="Falta el color de «Chop suey»"):
        registrar_comanda(4, [plato(color=color)], ahora=HORA)


def test_un_plato_malo_rechaza_toda_la_comanda():
    with pytest.raises(FueraDeCarta):
        registrar_comanda(4, [plato(), plato(color="verde")], ahora=HORA)


@pytest.mark.parametrize("cantidad", [-1, "2"])
def test_cantidad_que_no_es_entero_positivo_se_rechaza(cantidad):
    with pytest.raises(ComandaInvalida, match="La cantidad debe ser un número mayor que cero"):
        registrar_comanda(4, [plato(cantidad=cantidad)], ahora=HORA)
