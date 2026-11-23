"""Registrar la comanda de una mesa (HU-01 y HU-02)."""

from dataclasses import dataclass
from datetime import datetime

from afenix.carta import CARTA, MODIFICACIONES

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
    if isinstance(mesa, bool) or not isinstance(mesa, int) or mesa < 1:
        raise ComandaInvalida("La mesa debe ser un número mayor que cero")
    if not items:
        raise ComandaInvalida("La comanda debe tener al menos un plato")

    nombres = {"base": "la base", "proteina": "la proteína", "tamano": "el tamaño", "picante": "el picante"}
    platos = []
    for item in items:
        nombre = item.get("plato")
        if nombre not in CARTA:
            raise FueraDeCarta(f"El plato «{nombre}» no está en la carta")
        for mod in MODIFICACIONES:
            valor = item.get(mod)
            if not valor:
                raise ComandaInvalida(f"Falta {nombres[mod]} de «{nombre}»")
            if valor not in CARTA[nombre][mod]:
                raise FueraDeCarta(f"{nombres[mod].capitalize()} no está en la carta")
        cantidad = item.get("cantidad", 1)
        if isinstance(cantidad, bool) or not isinstance(cantidad, int) or cantidad < 1:
            raise ComandaInvalida("La cantidad debe ser un número mayor que cero")
        platos.append(Plato(nombre, item["base"], item["proteina"], item["tamano"], item["picante"], cantidad))

    return Comanda(mesa=mesa, platos=platos, hora_entrada=ahora or datetime.now())
