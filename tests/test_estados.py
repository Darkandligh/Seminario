"""Pruebas de cambiar_estado (HU-06 y HU-07). Casos de registro_pruebas.md, regla 2."""

from datetime import datetime

import pytest

from afenix.estados import CambioInvalido, SinPermiso, cambiar_estado

HORA_LISTO = datetime(2026, 11, 28, 12, 25)
CAMINO = ["recibido", "en preparación", "listo"]


def llevar_a(comanda, estado):
    for paso in CAMINO[1:CAMINO.index(estado) + 1]:
        cambiar_estado(comanda, paso, "cocina")
    return comanda


@pytest.mark.parametrize("actual, nuevo", [
    ("recibido", "en preparación"),  # R3: primer paso
    ("en preparación", "listo"),     # R3: último paso posible
])
def test_cocina_avanza_un_paso(turno, actual, nuevo):
    comanda = llevar_a(turno[0], actual)
    assert cambiar_estado(comanda, nuevo, "cocina", ahora=HORA_LISTO).estado == nuevo


def test_al_quedar_listo_se_guarda_la_hora(turno):
    comanda = llevar_a(turno[0], "en preparación")
    cambiar_estado(comanda, "listo", "cocina", ahora=HORA_LISTO)
    assert comanda.hora_listo == HORA_LISTO


def test_en_preparacion_no_guarda_hora_de_listo(turno):
    comanda = cambiar_estado(turno[0], "en preparación", "cocina", ahora=HORA_LISTO)
    assert comanda.hora_listo is None


@pytest.mark.parametrize("actual, nuevo", [
    ("recibido", "listo"),                # R4: salta en preparación
    ("recibido", "recibido"),             # R5: se queda igual al inicio
    ("en preparación", "en preparación"), # R5: se queda igual en medio
    ("listo", "listo"),                   # R5: se queda igual al final
    ("en preparación", "recibido"),       # R6: retrocede un paso
    ("listo", "en preparación"),          # R6: devuelve un pedido listo (P-06)
    ("listo", "recibido"),                # R6: retrocede dos pasos
])
def test_cocina_no_puede_saltar_repetir_ni_retroceder(turno, actual, nuevo):
    comanda = llevar_a(turno[0], actual)
    with pytest.raises(CambioInvalido, match=f"no puede pasar de «{actual}» a «{nuevo}»"):
        cambiar_estado(comanda, nuevo, "cocina")
    assert comanda.estado == actual


@pytest.mark.parametrize("nuevo", [
    "entregado",  # R2: estado que no está en el flujo
    "",           # R2: texto vacío
    "Listo",      # R2: con mayúscula no es el mismo estado
])
def test_estado_que_no_existe_se_rechaza(turno, nuevo):
    comanda = llevar_a(turno[0], "en preparación")
    with pytest.raises(CambioInvalido, match="Ese estado no existe"):
        cambiar_estado(comanda, nuevo, "cocina")
    assert comanda.estado == "en preparación"


@pytest.mark.parametrize("rol, nuevo", [
    ("mesero", "en preparación"),  # R1: el salón con un paso válido
    ("mesero", "listo"),           # R1: el salón con un paso inválido; el paso no importa
    ("mesero", "entregado"),       # R1: el salón con un estado que no existe
    ("", "en preparación"),        # R1: sin rol
    ("Cocina", "en preparación"),  # R1: con mayúscula no es el rol cocina
])
def test_solo_la_cocina_cambia_el_estado(turno, rol, nuevo):
    comanda = turno[0]
    with pytest.raises(SinPermiso, match="Solo la cocina puede cambiar el estado"):
        cambiar_estado(comanda, nuevo, rol)
    assert comanda.estado == "recibido"
