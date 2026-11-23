"""Cambio de estado de la comanda (HU-06 y HU-07)."""

from datetime import datetime

from afenix.comandas import Comanda

ESTADOS = ("recibido", "en preparación", "listo")
COCINA = "cocina"

SOLO_COCINA = "Solo la cocina puede cambiar el estado"
ESTADO_DESCONOCIDO = "Ese estado no existe"


class SinPermiso(PermissionError):
    """Quien pidió el cambio no es la cocina."""


class CambioInvalido(ValueError):
    """El cambio salta, repite o retrocede un estado."""


def cambiar_estado(
    comanda: Comanda, nuevo: str, rol: str, ahora: datetime | None = None
) -> Comanda:
    """Pasa la comanda al estado siguiente.

    Recibe la comanda, el estado al que se quiere pasar, el rol de quien lo
    pide y la hora del cambio; si no llega la hora se usa la del equipo.
    Devuelve la misma comanda con el estado nuevo. Al quedar «listo» guarda
    la hora en hora_listo.
    Lanza SinPermiso si el rol no es la cocina, y CambioInvalido si el estado
    no existe o no es el siguiente del actual.
    """
    if rol != COCINA:
        raise SinPermiso(SOLO_COCINA)
    if nuevo not in ESTADOS:
        raise CambioInvalido(ESTADO_DESCONOCIDO)

    actual = comanda.estado
    if ESTADOS.index(nuevo) != ESTADOS.index(actual) + 1:
        raise CambioInvalido(f"La comanda no puede pasar de «{actual}» a «{nuevo}»")

    comanda.estado = nuevo
    if nuevo == ESTADOS[-1]:
        comanda.hora_listo = ahora or datetime.now()
    return comanda
