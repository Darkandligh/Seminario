"""Registrar la comanda de una mesa (HU-01 y HU-02)."""

from dataclasses import dataclass
from datetime import datetime

RECIBIDO = "recibido"


class ComandaInvalida(ValueError):
    """La comanda no cumple las reglas y no se guarda."""


class FueraDeCarta(ComandaInvalida):
    """El plato o una de sus modificaciones no existe en la carta."""


@dataclass
class Plato:
    nombre: str
    base: str
    proteina: str
    tamano: str
    picante: str
    cantidad: int = 1


@dataclass
class Comanda:
    mesa: int
    platos: list[Plato]
    hora_entrada: datetime
    estado: str = RECIBIDO


def registrar_comanda(mesa, items, ahora=None):
    raise NotImplementedError
