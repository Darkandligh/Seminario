"""Pantalla de cocina: orden de llegada (HU-04) y tiempo de espera (HU-05)."""

from datetime import datetime

from afenix.comandas import Comanda

LISTO = "listo"
HORA_ANTERIOR = "La hora actual no puede ser anterior a la hora de entrada"


def minutos_espera(hora_entrada: datetime, ahora: datetime) -> float:
    """Calcula cuánto lleva esperando una comanda.

    Recibe la hora de entrada de la comanda y la hora actual.
    Devuelve los minutos con decimales: 90 segundos son 1.5.
    Lanza ValueError si la hora actual es anterior a la de entrada.
    """
    if ahora < hora_entrada:
        raise ValueError(HORA_ANTERIOR)
    return (ahora - hora_entrada).total_seconds() / 60


def comandas_para_cocina(comandas: list[Comanda]) -> list[Comanda]:
    """Arma la lista de la pantalla de cocina.

    Recibe todas las comandas del turno.
    Devuelve las que no están listas, de la más antigua a la más reciente.
    Si dos entraron a la misma hora queda primero la que se registró primero.
    No lanza errores.
    """
    pendientes = [c for c in comandas if c.estado != LISTO]
    return sorted(pendientes, key=lambda c: c.hora_entrada)
