"""Pruebas de la pantalla de cocina (HU-04 y HU-05). Casos de registro_pruebas.md, reglas 3 y 4."""

from datetime import datetime, timedelta

import pytest

from afenix.cocina import comandas_para_cocina, minutos_espera
from afenix.estados import cambiar_estado

ENTRADA = datetime(2026, 11, 28, 12, 0)


@pytest.mark.parametrize("transcurrido, esperado", [
    (timedelta(0), 0.0),                     # límite: recién entra
    (timedelta(seconds=1), 1 / 60),          # límite: primer segundo de espera
    (timedelta(seconds=90), 1.5),            # minutos con decimales
    (timedelta(hours=1, minutes=5), 65.0),   # más de una hora
])
def test_minutos_de_espera(transcurrido, esperado):
    assert minutos_espera(ENTRADA, ENTRADA + transcurrido) == pytest.approx(esperado)


@pytest.mark.parametrize("antes", [
    timedelta(seconds=1),  # límite: un segundo antes de la entrada
    timedelta(hours=2),    # hora actual muy anterior
])
def test_hora_actual_anterior_a_la_entrada_se_rechaza(antes):
    with pytest.raises(ValueError, match="no puede ser anterior a la hora de entrada"):
        minutos_espera(ENTRADA, ENTRADA - antes)


def test_pantalla_ordena_por_hora_de_entrada(turno):
    # 12:00 mesa 3, 12:01 mesa 12, 12:04 mesas 9 y 2, 12:10 mesa 7
    assert [c.mesa for c in comandas_para_cocina(turno)] == [3, 12, 9, 2, 7]


def test_misma_hora_queda_primero_la_registrada_primero(turno):
    # La 9 y la 2 entran a las 12:04 y la 9 se registró antes, aunque su número es mayor
    mesas = [c.mesa for c in comandas_para_cocina(turno)]
    assert mesas.index(9) < mesas.index(2)


def test_en_preparacion_sigue_en_pantalla(turno):
    cambiar_estado(turno[1], "en preparación", "cocina")
    assert 3 in [c.mesa for c in comandas_para_cocina(turno)]


def test_las_listas_salen_de_la_pantalla(turno):
    mesa_3 = turno[1]
    cambiar_estado(mesa_3, "en preparación", "cocina")
    cambiar_estado(mesa_3, "listo", "cocina")
    assert [c.mesa for c in comandas_para_cocina(turno)] == [12, 9, 2, 7]


@pytest.mark.parametrize("hay_comandas", [
    False,  # no hay comandas en el turno
    True,   # las cinco del turno están listas
])
def test_pantalla_vacia(turno, hay_comandas):
    comandas = turno if hay_comandas else []
    for c in comandas:
        cambiar_estado(c, "en preparación", "cocina")
        cambiar_estado(c, "listo", "cocina")
    assert comandas_para_cocina(comandas) == []


def test_no_cambia_la_lista_original(turno):
    mesas = [c.mesa for c in turno]
    comandas_para_cocina(turno)
    assert [c.mesa for c in turno] == mesas
