"""Registrar la comanda de una mesa (HU-01 y HU-02)."""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, TypeGuard

from afenix.carta import CARTA, MODIFICACIONES

RECIBIDO = "recibido"

# Topes provisionales hasta confirmar con el restaurante (P-01)
MAX_PLATOS = 50
# Respuesta 10 de la entrevista real (P-03)
MAX_MESAS = 12
MAX_CANTIDAD = 20
LARGO_NOMBRE = 40

MESA_INVALIDA = "La mesa debe ser un número mayor que cero"
MESA_INEXISTENTE = f"El restaurante tiene {MAX_MESAS} mesas"
SIN_PLATOS = "La comanda debe tener al menos un plato"
CANTIDAD_INVALIDA = "La cantidad debe ser un número mayor que cero"
FORMATO_INVALIDO = "La comanda tiene un formato incorrecto"
DEMASIADOS_PLATOS = f"Una comanda tiene máximo {MAX_PLATOS} platos"
CANTIDAD_EXAGERADA = f"La cantidad máxima por plato es {MAX_CANTIDAD}"

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
    hora_listo: datetime | None = None


def _es_entero_positivo(valor: object) -> TypeGuard[int]:
    # bool es subclase de int en Python: sin esto, True pasaría como mesa 1
    return not isinstance(valor, bool) and isinstance(valor, int) and valor >= 1


def _validar_plato(item: object) -> Plato:
    """Revisa un plato contra la carta.

    Recibe el diccionario de un plato tal como llega del mesero.
    Devuelve el Plato ya validado.
    Lanza ComandaInvalida si falta algo o tiene mal formato, y FueraDeCarta
    si el plato o una opción no existe en la carta.
    """
    if not isinstance(item, dict) or not isinstance(item.get("plato"), str):
        raise ComandaInvalida(FORMATO_INVALIDO)

    nombre = item["plato"]
    if nombre not in CARTA:
        raise FueraDeCarta(f"El plato «{nombre[:LARGO_NOMBRE]}» no está en la carta")

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
    if cantidad > MAX_CANTIDAD:
        raise ComandaInvalida(CANTIDAD_EXAGERADA)

    return Plato(nombre, item["base"], item["proteina"], item["tamano"], item["picante"], cantidad)


def registrar_comanda(mesa: Any, items: Any, ahora: datetime | None = None) -> Comanda:
    """Valida la comanda de una mesa y la devuelve en estado recibido.

    Recibe el número de la mesa, la lista de platos (diccionarios con plato,
    base, proteina, tamano, picante y, si se quiere, cantidad) y la hora de
    entrada; si no llega la hora se usa la del equipo.
    Devuelve la Comanda con sus platos, la hora de entrada y estado recibido.
    Lanza ComandaInvalida si la mesa no es un número de 1 a MAX_MESAS, si los
    platos o la cantidad no sirven, o si
    la comanda pasa de MAX_PLATOS platos sumando las cantidades, y
    FueraDeCarta (que hereda de ComandaInvalida) si algo no está en la carta.
    Si un solo plato está mal se rechaza toda la comanda, para que nada
    incompleto llegue a la cocina.
    """
    if not _es_entero_positivo(mesa):
        raise ComandaInvalida(MESA_INVALIDA)
    if mesa > MAX_MESAS:
        raise ComandaInvalida(MESA_INEXISTENTE)
    if not items:
        raise ComandaInvalida(SIN_PLATOS)
    if not isinstance(items, list):
        raise ComandaInvalida(FORMATO_INVALIDO)
    if len(items) > MAX_PLATOS:
        raise ComandaInvalida(DEMASIADOS_PLATOS)

    platos = [_validar_plato(item) for item in items]
    if sum(plato.cantidad for plato in platos) > MAX_PLATOS:
        raise ComandaInvalida(DEMASIADOS_PLATOS)
    return Comanda(mesa=mesa, platos=platos, hora_entrada=ahora or datetime.now())
