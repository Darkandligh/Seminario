"""Pruebas de abuso de registrar_comanda (revisión de seguridad, semana 6).

Mandan datos que un mesero no mandaría pero que sí puede llegar a la API:
tipos equivocados, cantidades enormes y textos largos o con HTML.
"""

import pytest

from afenix.comandas import ComandaInvalida, FueraDeCarta, registrar_comanda

BIEN = {"plato": "Chop suey", "color": "café"}


# H-02: datos con forma equivocada deben dar ComandaInvalida, no un error de Python

@pytest.mark.parametrize("items", ["Chop suey", {"plato": "Chop suey"}, 42])
def test_platos_que_no_vienen_en_lista_se_rechazan(items):
    with pytest.raises(ComandaInvalida, match="formato"):
        registrar_comanda(4, items)


@pytest.mark.parametrize("item", [None, "Chop suey", ["Chop suey"], 7])
def test_plato_que_no_es_diccionario_se_rechaza(item):
    with pytest.raises(ComandaInvalida, match="formato"):
        registrar_comanda(4, [item])


@pytest.mark.parametrize("nombre", [["Chop suey"], {"a": 1}, 5])
def test_nombre_de_plato_que_no_es_texto_se_rechaza(nombre):
    with pytest.raises(ComandaInvalida, match="formato"):
        registrar_comanda(4, [{**BIEN, "plato": nombre}])


# H-03: sin topes, una sola petición puede llenar la pantalla de cocina

def test_cantidad_exagerada_se_rechaza():
    with pytest.raises(ComandaInvalida, match="La cantidad"):
        registrar_comanda(4, [{**BIEN, "cantidad": 10**9}])


def test_cantidad_en_el_tope_se_acepta():
    assert registrar_comanda(4, [{**BIEN, "cantidad": 20}]).platos[0].cantidad == 20


def test_demasiados_platos_se_rechaza():
    with pytest.raises(ComandaInvalida, match="máximo"):
        registrar_comanda(4, [BIEN] * 51)


def test_platos_en_el_tope_se_acepta():
    assert len(registrar_comanda(4, [BIEN] * 50).platos) == 50


# H-04: el mensaje de error no debe repetir completo lo que mandó el cliente

def test_mensaje_no_repite_un_nombre_larguisimo():
    with pytest.raises(FueraDeCarta) as error:
        registrar_comanda(4, [{**BIEN, "plato": "<script>" + "A" * 5000}])
    assert len(str(error.value)) < 100


# H-05: el tope de 50 contaba filas, no unidades; 50 filas de 20 eran 1000 platos

def test_mas_de_50_unidades_en_total_se_rechaza():
    with pytest.raises(ComandaInvalida, match="máximo 50 platos"):
        registrar_comanda(4, [{**BIEN, "cantidad": 20}] * 3)


def test_50_unidades_repartidas_en_varias_filas_se_acepta():
    comanda = registrar_comanda(4, [{**BIEN, "cantidad": 10}] * 5)
    assert sum(p.cantidad for p in comanda.platos) == 50
