"""Criterios de aceptación de las historias de usuario, uno por escenario.

Cada prueba usa los datos exactos del escenario Gherkin del documento de
requisitos (docs/modulos/S3_Requisitos.pdf, sección 4) y comprueba todo el
«entonces». Las pruebas marcadas xfail son diferencias reales entre el
criterio y el código: están en la evaluación de historias del informe final.
HU-03, HU-08 y HU-09 no tienen pruebas porque todavía no están construidas.
Los criterios son los de la versión 3 del documento de requisitos, que sale
de la entrevista real con el restaurante.
"""

from datetime import datetime

import pytest

from afenix.cocina import comandas_para_cocina, minutos_espera
from afenix.comandas import RECIBIDO, ComandaInvalida, FueraDeCarta, registrar_comanda
from afenix.estados import CambioInvalido, SinPermiso, cambiar_estado

HOY = datetime(2026, 11, 28)


def hora(h, m):
    return HOY.replace(hour=h, minute=m)


def plato(nombre, base="arroz frito", proteina="pollo", tamano="personal", picante="medio"):
    return {"plato": nombre, "base": base, "proteina": proteina,
            "tamano": tamano, "picante": picante}


def comanda(mesa, h, m, estado=RECIBIDO):
    c = registrar_comanda(mesa, [plato("Chop suey")], ahora=hora(h, m))
    c.estado = estado
    return c


# ---------- HU-01. Registrar la comanda ----------

def test_hu01_e1_comanda_registrada():
    # Dado que la mesa 4 no tiene comandas abiertas,
    # cuando registro «Arroz frito con piña» y «Chop suey»,
    c = registrar_comanda(4, [plato("Arroz frito con piña"), plato("Chop suey")], ahora=hora(12, 5))
    # entonces la comanda queda «recibido» con la mesa 4, los dos platos y la hora de entrada.
    assert c.estado == RECIBIDO
    assert c.mesa == 4
    assert [p.nombre for p in c.platos] == ["Arroz frito con piña", "Chop suey"]
    assert c.hora_entrada == hora(12, 5)


def test_hu01_e2_comanda_sin_platos():
    # Dado que estoy registrando la comanda de la mesa 4,
    # cuando intento enviarla sin ningún plato,
    # entonces no se guarda y muestra «La comanda debe tener al menos un plato».
    with pytest.raises(ComandaInvalida, match=r"^La comanda debe tener al menos un plato$"):
        registrar_comanda(4, [])


# ---------- HU-02. Modificaciones desde la carta ----------
# Estas dos pruebas son del criterio de la versión 2 (base, proteína, tamaño y
# picante), que salió de la entrevista simulada. La entrevista real cambió la
# HU-02 a «plato y color»: ver las pruebas xfail de abajo.

def test_hu02_e1_plato_con_modificaciones():
    # Dado que la carta tiene «Pollo General Tso's» con arroz frito, familiar y picante medio,
    # cuando los elijo para la mesa 4,
    c = registrar_comanda(4, [plato("Pollo General Tso's", tamano="familiar", picante="medio")])
    # entonces el plato queda en la comanda con esas cuatro modificaciones.
    p = c.platos[0]
    assert (p.nombre, p.base, p.proteina, p.tamano, p.picante) == (
        "Pollo General Tso's", "arroz frito", "pollo", "familiar", "medio")


def test_hu02_e2_opcion_fuera_de_la_carta():
    # Dado que la carta no tiene camarón como proteína del chop suey,
    # cuando intento agregar «Chop suey» de camarón,
    # entonces no lo agrega y muestra «La proteína no está en la carta».
    with pytest.raises(FueraDeCarta, match=r"^La proteína no está en la carta$"):
        registrar_comanda(4, [plato("Chop suey", proteina="camarón")])


@pytest.mark.xfail(strict=True, reason="HU-02 versión 3: el cliente pide plato y color; "
                   "el código todavía pide base, proteína, tamaño y picante")
def test_hu02_v3_e1_plato_con_color():
    # Dado que la carta tiene «Chop suey» en color café, cuando lo elijo para la mesa 4,
    # entonces el plato queda en el pedido con el color café.
    c = registrar_comanda(4, [{"plato": "Chop suey", "color": "café"}])
    assert c.platos[0].color == "café"


@pytest.mark.xfail(strict=True, reason="HU-02 versión 3: falta validar el color contra la carta")
def test_hu02_v3_e2_color_que_no_existe():
    with pytest.raises(FueraDeCarta, match=r"^El color no está en la carta$"):
        registrar_comanda(4, [{"plato": "Chop suey", "color": "verde"}])


# ---------- HU-04. Cocina en orden de llegada ----------

def test_hu04_e1_orden_por_llegada():
    # Dado que la mesa 2 pidió a las 12:05 y la mesa 6 a las 12:01,
    comandas = [comanda(2, 12, 5), comanda(6, 12, 1)]
    # cuando abro la pantalla de cocina, entonces la mesa 6 aparece primero.
    assert [c.mesa for c in comandas_para_cocina(comandas)] == [6, 2]


def test_hu04_e2_comanda_lista_no_aparece():
    # Dado que la comanda de la mesa 6 está «Listo»,
    comandas = [comanda(2, 12, 5), comanda(6, 12, 1, estado="listo")]
    # cuando abro la pantalla de cocina, entonces no aparece entre las pendientes.
    assert [c.mesa for c in comandas_para_cocina(comandas)] == [2]


# ---------- HU-05. Tiempo de espera ----------

def test_hu05_e1_tiempo_a_la_vista():
    # Dado que la comanda de la mesa 2 entró a las 12:05,
    # cuando son las 12:17, entonces muestra 12 minutos de espera.
    assert minutos_espera(hora(12, 5), hora(12, 17)) == pytest.approx(12)


def test_hu05_e2_no_muestra_tiempo_negativo():
    # Dado que la comanda entró a las 12:05, cuando el equipo marca las 11:50,
    # entonces el sistema no muestra un tiempo negativo.
    with pytest.raises(ValueError):
        minutos_espera(hora(12, 5), hora(11, 50))


@pytest.mark.xfail(strict=True, reason="El código dice «La hora actual no puede ser anterior "
                   "a la hora de entrada»; el criterio pide «Revisa la hora del equipo»")
def test_hu05_e2_mensaje_del_criterio():
    with pytest.raises(ValueError, match=r"^Revisa la hora del equipo$"):
        minutos_espera(hora(12, 5), hora(11, 50))


# ---------- HU-06. Cambio de estado paso a paso ----------

def test_hu06_e1_pedido_listo():
    # Dado que la comanda de la mesa 2 está «En preparación»,
    c = comanda(2, 12, 5, estado="en preparación")
    # cuando la marco como lista a las 12:24,
    cambiar_estado(c, "listo", "cocina", ahora=hora(12, 24))
    # entonces queda «Listo» con 12:24 como hora de entrega.
    assert c.estado == "listo"
    assert c.hora_listo == hora(12, 24)


def test_hu06_e2_salto_de_estado_no_cambia():
    # Dado que la comanda de la mesa 2 está «Recibido»,
    c = comanda(2, 12, 5)
    # cuando intento marcarla como lista, entonces el estado no cambia.
    with pytest.raises(CambioInvalido):
        cambiar_estado(c, "listo", "cocina")
    assert c.estado == RECIBIDO


@pytest.mark.xfail(strict=True, reason="El código dice «La comanda no puede pasar de «recibido» "
                   "a «listo»»; el criterio pide «El pedido debe pasar primero por en preparación»")
def test_hu06_e2_mensaje_del_criterio():
    with pytest.raises(CambioInvalido, match=r"^El pedido debe pasar primero por en preparación$"):
        cambiar_estado(comanda(2, 12, 5), "listo", "cocina")


# ---------- HU-07. Solo la cocina cambia el estado ----------

def test_hu07_e1_la_cocina_cambia_el_estado():
    # Dado que entré con mi usuario de cocinero,
    # cuando paso la comanda de la mesa 2 a «En preparación»,
    c = comanda(2, 12, 5)
    cambiar_estado(c, "en preparación", "cocina", ahora=hora(12, 8))
    # entonces el cambio queda guardado.
    assert c.estado == "en preparación"


@pytest.mark.xfail(strict=True, reason="El cambio no guarda quién lo hizo ni a qué hora: falta "
                   "la entidad CambioEstado del modelo de datos")
def test_hu07_e1_guarda_nombre_y_hora():
    c = comanda(2, 12, 5)
    cambiar_estado(c, "en preparación", "cocina", ahora=hora(12, 8))
    assert c.cambios[-1] == ("cocina", "en preparación", hora(12, 8))


def test_hu07_e2_el_salon_no_cambia_el_estado():
    # Dado que entré a la tablet con usuario de mesero,
    c = comanda(2, 12, 5)
    # cuando intento cambiar el estado de la comanda de la mesa 2,
    # entonces no lo permite y muestra que solo la cocina puede cambiar el estado.
    with pytest.raises(SinPermiso, match="Solo la cocina puede cambiar el estado"):
        cambiar_estado(c, "en preparación", "mesero")
    assert c.estado == RECIBIDO
