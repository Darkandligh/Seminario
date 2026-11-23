from datetime import datetime, timedelta

import pytest

from afenix.cocina import comandas_para_cocina, minutos_espera
from afenix.comandas import registrar_comanda
from afenix.estados import CambioInvalido, SinPermiso, cambiar_estado

HORA = datetime(2026, 11, 28, 12, 0)
PLATO = {"plato": "Chop suey", "base": "arroz frito", "proteina": "pollo",
         "tamano": "personal", "picante": "medio"}


def nueva(mesa=4, hora=HORA):
    return registrar_comanda(mesa, [PLATO], ahora=hora)


@pytest.mark.parametrize("pasos, esperado", [
    (["en preparación"], "en preparación"),  # primer paso
    (["en preparación", "listo"], "listo"),  # segundo paso
])
def test_cocina_avanza(pasos, esperado):
    c = nueva()
    for paso in pasos:
        c = cambiar_estado(c, paso, "cocina", ahora=HORA)
    assert c.estado == esperado


def test_listo_guarda_hora():
    c = nueva()
    cambiar_estado(c, "en preparación", "cocina", ahora=HORA)
    cambiar_estado(c, "listo", "cocina", ahora=HORA + timedelta(minutes=20))
    assert c.hora_listo is not None


@pytest.mark.parametrize("nuevo", [
    "listo",     # salta en preparación
    "recibido",  # se queda igual
])
def test_cambio_invalido(nuevo):
    with pytest.raises(CambioInvalido):
        cambiar_estado(nueva(), nuevo, "cocina")


def test_retroceder_de_listo_a_preparacion():
    c = nueva()
    cambiar_estado(c, "en preparación", "cocina")
    cambiar_estado(c, "listo", "cocina")
    with pytest.raises(CambioInvalido):
        cambiar_estado(c, "en preparación", "cocina")


@pytest.mark.parametrize("rol", [
    "mesero",  # el salón solo consulta
    "admin",   # el administrador
])
def test_solo_cocina(rol):
    with pytest.raises(SinPermiso):
        cambiar_estado(nueva(), "en preparación", rol)


def test_admin_puede_cambiar_estado():
    c = cambiar_estado(nueva(), "en preparación", "admin")
    assert c.estado == "en preparación"


@pytest.mark.parametrize("segundos, minutos", [
    (0, 0),        # recién entra
    (60, 1),       # un minuto
    (300, 5),      # cinco minutos
    (90, 1.5),     # minuto y medio
    (3600, 60),    # una hora
])
def test_minutos_espera(segundos, minutos):
    assert minutos_espera(HORA, HORA + timedelta(seconds=segundos)) == minutos


def test_minutos_espera_devuelve_numero():
    assert isinstance(minutos_espera(HORA, HORA + timedelta(minutes=3)), float)


def test_hora_anterior():
    with pytest.raises(ValueError):
        minutos_espera(HORA, HORA - timedelta(minutes=1))


def test_orden_de_llegada():
    a = nueva(1, HORA + timedelta(minutes=10))
    b = nueva(2, HORA)
    c = nueva(3, HORA + timedelta(minutes=5))
    resultado = comandas_para_cocina([a, b, c])
    assert len(resultado) == 3


def test_cocina_sin_comandas():
    assert comandas_para_cocina([]) == []
