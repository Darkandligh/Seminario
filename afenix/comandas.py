"""Registrar la comanda de una mesa (HU-01 y HU-02)."""

from dataclasses import dataclass
from datetime import datetime

from afenix.carta import CARTA, MODIFICACIONES

RECIBIDO = "recibido"

MESA_INVALIDA = "La mesa debe ser un número mayor que cero"
SIN_PLATOS = "La comanda debe tener al menos un plato"
CANTIDAD_INVALIDA = "La cantidad debe ser un número mayor que cero"
FORMATO_INVALIDO = "La comanda tiene un formato incorrecto"

NOMBRES_MODIFICACION = {
    "base": "la base",
    "proteina": "la proteína",
    "tamano": "el tamaño",
    "picante": "el picante",
}


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


def _es_entero_positivo(valor):
    # bool es subclase de int en Python: sin esto, True pasaría como mesa 1
    return not isinstance(valor, bool) and isinstance(valor, int) and valor >= 1


def _validar_plato(item):
    if not isinstance(item, dict) or not isinstance(item.get("plato"), str):
        raise ComandaInvalida(FORMATO_INVALIDO)

    nombre = item["plato"]
    if nombre not in CARTA:
        raise FueraDeCarta(f"El plato «{nombre}» no está en la carta")

    for mod in MODIFICACIONES:
        valor = item.get(mod)
        texto = NOMBRES_MODIFICACION[mod]
        if not valor:
            raise ComandaInvalida(f"Falta {texto} de «{nombre}»")
        if valor not in CARTA[nombre][mod]:
            raise FueraDeCarta(f"{texto.capitalize()} no está en la carta")

    cantidad = item.get("cantidad", 1)
    if not _es_entero_positivo(cantidad):
        raise ComandaInvalida(CANTIDAD_INVALIDA)

    return Plato(nombre, item["base"], item["proteina"], item["tamano"], item["picante"], cantidad)


def registrar_comanda(mesa, items, ahora=None):
    """Valida la comanda de una mesa y la devuelve en estado recibido.

    Si un solo plato está mal se rechaza toda la comanda, para que nada
    incompleto llegue a la cocina.
    """
    if not _es_entero_positivo(mesa):
        raise ComandaInvalida(MESA_INVALIDA)
    if not items:
        raise ComandaInvalida(SIN_PLATOS)
    if not isinstance(items, list):
        raise ComandaInvalida(FORMATO_INVALIDO)

    platos = [_validar_plato(item) for item in items]
    return Comanda(mesa=mesa, platos=platos, hora_entrada=ahora or datetime.now())
