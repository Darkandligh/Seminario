# Registro de pruebas: tabla de casos y pruebas de la IA

Proyecto: A-Fénix, plataforma de comandas digitales para el restaurante chino A Fénix de Oro
Estudiante: Eduardo Ascencio
Fecha: 2026-11-23

Probé cuatro funciones con reglas: `registrar_comanda` (validación), `cambiar_estado` (estados y permisos), `minutos_espera` (cálculo) y `comandas_para_cocina` (orden de la pantalla). `cambiar_estado` es la que combina varias condiciones y tiene su tabla de decisión. Los esperados salen de las historias de usuario, no de correr el código.

Pruebas: `tests/test_registrar_comanda.py` (semana 5, sin cambios), `tests/test_abuso_comandas.py` (semana 6, sin cambios), y de esta semana `tests/test_comandas_datos.py`, `tests/test_estados.py`, `tests/test_cocina.py` y el fixture de `tests/conftest.py`. En total son 79 pruebas y todas pasan (`evidencias/semana-7/04_suite_final_pytest.txt`).

## 1. Tabla de casos

### Regla 1: `registrar_comanda`, la comanda se registra con mesa, platos y modificaciones de la carta

**Regla completa (el oráculo):** HU-01: como mesero, quiero registrar la comanda de una mesa con los platos de la carta para que la cocina sepa qué preparar. Si la comanda no tiene platos, el sistema no la guarda y muestra «La comanda debe tener al menos un plato». La comanda queda en estado «recibido» con la mesa, los platos y la hora de entrada. HU-02: cada plato lleva base, proteína, tamaño y picante elegidos desde la carta. Si una opción no está en la carta, el sistema no la agrega y muestra «La proteína no está en la carta» (y así con cada modificación). En el diseño de la API, lo incompleto responde 400 y lo que no está en la carta responde 422. En la semana 6 agregué los topes de 50 platos y 20 por plato.

| Técnica | Partición o límite | Entrada | Esperado | Prueba que lo cubre |
|---|---|---|---|---|
| Partición válida | Comanda normal | mesa 4, arroz frito con piña y chop suey | Estado «recibido», mesa 4, los dos platos y la hora | test_comanda_valida_queda_recibida_con_mesa_platos_y_hora |
| Partición válida | Plato con sus cuatro modificaciones | pollo General Tso's, familiar, picante medio | Las cuatro modificaciones guardadas | test_plato_guarda_sus_cuatro_modificaciones |
| Límite | Primera mesa válida | mesa 1 | Comanda de la mesa 1 | test_mesa_uno_es_valida |
| Límite | Última mesa inválida | mesa 0 | ComandaInvalida «La mesa debe ser un número mayor que cero» | test_mesa_cero_se_rechaza |
| Partición inválida | Mesa negativa, texto, vacía o booleana | -3, "4", None, True | ComandaInvalida, el mismo mensaje | test_mesa_que_no_es_entero_positivo_se_rechaza |
| Límite | Un solo plato | 1 plato | Se acepta | test_un_solo_plato_es_valido |
| Límite | Cero platos | [] y None | ComandaInvalida «La comanda debe tener al menos un plato» | test_comanda_sin_platos_se_rechaza |
| Límite | Último valor válido de platos | 50 platos | Se acepta | test_platos_en_el_tope_se_acepta |
| Límite | Primer valor inválido de platos | 51 platos | ComandaInvalida «máximo» | test_demasiados_platos_se_rechaza |
| Partición válida | Cantidad sin mandar | sin `cantidad` | cantidad 1 | test_cantidad_por_defecto_es_uno |
| Límite | Última cantidad inválida por abajo | cantidad 0 | ComandaInvalida «La cantidad debe ser un número mayor que cero» | test_cantidad_cero_se_rechaza |
| Partición inválida | Cantidad negativa o texto | -1, "2" | ComandaInvalida, el mismo mensaje | test_cantidad_que_no_es_entero_positivo_se_rechaza |
| Límite | Última cantidad válida | 20 | Se acepta | test_cantidad_en_el_tope_se_acepta (abuso) |
| Límite | Primera cantidad inválida por arriba | 21 | ComandaInvalida «La cantidad máxima por plato es 20» | test_cantidad_justo_encima_del_tope_se_rechaza |
| Partición inválida | Opción que el plato no tiene | chop suey de camarón | FueraDeCarta «La proteína no está en la carta» | test_proteina_fuera_de_la_carta_se_rechaza |
| Partición inválida | Plato que no está en la carta | «Pizza hawaiana» | FueraDeCarta «no está en la carta» | test_plato_que_no_esta_en_la_carta_se_rechaza |
| Partición inválida | Modificación vacía | base, proteína, tamaño o picante en «» | ComandaInvalida «Falta…» | test_falta_una_modificacion_se_rechaza, test_picante_vacio_dice_que_falta |
| Partición inválida | Lo incompleto no es «fuera de carta» | modificación vacía, sin platos, mesa 0 | Exactamente ComandaInvalida, no FueraDeCarta | test_lo_incompleto_no_se_marca_como_fuera_de_carta |
| Partición inválida | Un plato bueno y uno malo | chop suey bien y otro de tamaño «gigante» | FueraDeCarta: no se registra ninguno | test_un_plato_malo_rechaza_toda_la_comanda |
| Partición válida | Nombres con ñ, tilde y apóstrofo | «Arroz frito con piña», «Pollo General Tso's», camarón | El nombre y la opción quedan iguales | test_nombres_dificiles_quedan_iguales, test_camaron_con_tilde_es_la_opcion_de_la_carta |
| Partición inválida | Datos con forma equivocada | platos en texto, plato None, nombre en lista | ComandaInvalida «formato» | pruebas de `test_abuso_comandas.py` |

**Ambigüedades encontradas:**
- No sé cuántas mesas tiene el restaurante (P-03). No puse tope de mesas; solo pido un entero mayor que cero.
- Los topes de 50 platos y 20 por plato son míos y provisionales hasta que el restaurante responda P-01.
- La historia no dice si un plato malo rechaza toda la comanda o solo ese plato. Decidí rechazar toda la comanda, para que a la cocina no llegue un pedido incompleto sin que el mesero se entere.
- La carta real no está validada. Las pruebas usan la carta de ejemplo de `afenix/carta.py`.

### Regla 2: `cambiar_estado`, la comanda avanza paso a paso y solo la cocina la cambia (varias condiciones)

**Regla completa (el oráculo):** HU-06: la comanda pasa de «recibido» a «en preparación» y de «en preparación» a «listo», un paso a la vez. Si se intenta saltar o retroceder un estado, la API responde 409. Cuando la comanda queda lista se guarda la hora de entrega. HU-07: solo la cocina cambia el estado; si lo intenta otro rol, la API responde 403.

| Técnica | Partición o límite | Entrada (actual → nuevo, rol) | Esperado | Prueba que lo cubre |
|---|---|---|---|---|
| Partición válida | Primer paso | recibido → en preparación, cocina | Estado «en preparación», sin hora de listo | test_cocina_avanza_un_paso[recibido-en preparación], test_en_preparacion_no_guarda_hora_de_listo |
| Límite | Último paso posible | en preparación → listo, cocina | Estado «listo» y hora de listo igual a la del cambio | test_cocina_avanza_un_paso[en preparación-listo], test_al_quedar_listo_se_guarda_la_hora |
| Partición inválida | Salta un estado | recibido → listo | CambioInvalido «no puede pasar de…», el estado no cambia | test_cocina_no_puede_saltar_repetir_ni_retroceder |
| Partición inválida | Se queda igual | recibido → recibido, en preparación → en preparación, listo → listo | CambioInvalido, el estado no cambia | la misma prueba, 3 filas |
| Partición inválida | Retrocede | en preparación → recibido, listo → en preparación, listo → recibido | CambioInvalido, el estado no cambia | la misma prueba, 3 filas |
| Partición inválida | Estado que no existe | «entregado», «», «Listo» | CambioInvalido «Ese estado no existe» | test_estado_que_no_existe_se_rechaza |
| Partición inválida | Otro rol | mesero, «», «Cocina» | SinPermiso «Solo la cocina puede cambiar el estado», el estado no cambia | test_solo_la_cocina_cambia_el_estado |

**Tabla de decisión.** C1: ¿lo pide la cocina? C2: ¿el estado nuevo existe? C3: ¿cómo es el paso frente al estado actual? El guion (–) indica que esa condición no importa.

| Regla | C1 cocina | C2 existe | C3 paso | Resultado | Prueba |
|---|---|---|---|---|---|
| R1 | No | – | – | SinPermiso, el estado no cambia | test_solo_la_cocina_cambia_el_estado (paso válido, paso inválido y estado que no existe) |
| R2 | Sí | No | – | CambioInvalido «Ese estado no existe» | test_estado_que_no_existe_se_rechaza |
| R3 | Sí | Sí | Siguiente | Cambia el estado; si queda listo guarda la hora | test_cocina_avanza_un_paso, test_al_quedar_listo_se_guarda_la_hora |
| R4 | Sí | Sí | Salta | CambioInvalido, el estado no cambia | [recibido-listo] |
| R5 | Sí | Sí | Igual | CambioInvalido, el estado no cambia | [recibido-recibido], [en preparación-en preparación], [listo-listo] |
| R6 | Sí | Sí | Retrocede | CambioInvalido, el estado no cambia | [en preparación-recibido], [listo-en preparación], [listo-recibido] |

Las combinaciones completas son 2 × 2 × 4 = 16 y quedan en 6 reglas: si no es la cocina, nada más importa, y si el estado no existe, el paso no se puede medir. Con la cocina probé las 9 parejas posibles de estado actual y estado nuevo. En R1 probé un paso válido, uno inválido y un estado que no existe, para comprobar que de verdad no importan.

**Ambigüedades encontradas:**
- P-06: no está definido si la cocina puede devolver una comanda que marcó lista por error. Con la regla tal como está, no se puede (fila listo → en preparación). Queda por confirmar con el restaurante.
- La regla habla de hora de entrega, pero no hay un estado «entregado». Tomé la hora en que queda lista como la hora de entrega.
- La regla no dice cómo se escriben los roles. Decidí que solo «cocina», tal cual, tiene permiso; «Cocina» o un rol vacío se rechazan. Es más seguro negar por defecto.
- Si un mesero manda un estado que no existe, ¿qué error recibe? Decidí que primero se revisa el permiso, así quien no es cocina siempre recibe 403 y no puede averiguar qué estados existen.

### Regla 3: `minutos_espera`, cuánto lleva esperando la comanda

**Regla completa (el oráculo):** HU-05: la pantalla de cocina muestra cuánto lleva esperando cada comanda, contado desde su hora de entrada.

| Técnica | Partición o límite | Entrada | Esperado | Prueba que lo cubre |
|---|---|---|---|---|
| Límite | Recién entra, primer valor válido | 0 segundos | 0.0 | test_minutos_de_espera[transcurrido0-0.0] |
| Límite | Primer segundo de espera | 1 segundo | 1/60 (pytest.approx) | test_minutos_de_espera[transcurrido1-…] |
| Partición válida | Con decimales | 90 segundos | 1.5 (pytest.approx) | test_minutos_de_espera[transcurrido2-1.5] |
| Partición válida | Más de una hora | 1 hora y 5 minutos | 65.0 (pytest.approx) | test_minutos_de_espera[transcurrido3-65.0] |
| Límite | Último valor inválido | hora actual 1 segundo antes de la entrada | ValueError «no puede ser anterior a la hora de entrada» | test_hora_actual_anterior_a_la_entrada_se_rechaza[antes0] |
| Partición inválida | Hora actual muy anterior | 2 horas antes | ValueError, el mismo mensaje | test_hora_actual_anterior_a_la_entrada_se_rechaza[antes1] |

**Ambigüedades encontradas:** la historia no dice si el tiempo va en minutos enteros o con segundos. La función devuelve minutos con decimales y la pantalla decide cómo mostrarlos. HU-05 también habla de comandas atrasadas, pero no se sabe desde cuántos minutos una comanda es «tarde» (P-02), así que no programé esa alerta para no inventar el número.

### Regla 4: `comandas_para_cocina`, la cocina ve las comandas en orden de llegada

**Regla completa (el oráculo):** HU-04: la cocina ve las comandas en una pantalla en orden de llegada, por hora de entrada, para preparar primero lo que llegó primero.

| Técnica | Partición o límite | Entrada | Esperado | Prueba que lo cubre |
|---|---|---|---|---|
| Partición válida | Comandas desordenadas | turno del fixture: mesas 7 (12:10), 3 (12:00), 9 (12:04), 2 (12:04), 12 (12:01) | Orden 3, 12, 9, 2, 7 | test_pantalla_ordena_por_hora_de_entrada |
| Límite | Misma hora de entrada | mesas 9 y 2 a las 12:04, la 9 registrada antes | La 9 antes que la 2 | test_misma_hora_queda_primero_la_registrada_primero |
| Partición válida | Comanda en preparación | la mesa 3 pasa a en preparación | Sigue en la pantalla | test_en_preparacion_sigue_en_pantalla |
| Partición válida | Comanda lista | la mesa 3 queda lista | Sale: quedan 12, 9, 2, 7 | test_las_listas_salen_de_la_pantalla |
| Partición válida | No hay comandas | [] | [] | test_pantalla_vacia[False] |
| Partición válida | Todas están listas | las cinco del turno listas | [] | test_pantalla_vacia[True] |
| Partición válida | La lista del turno no se toca | turno del fixture | El turno queda en el mismo orden | test_no_cambia_la_lista_original |

**Ambigüedades encontradas:** la historia no dice qué pasa con las comandas listas. Decidí que salen de la pantalla de cocina, porque la cocina ya terminó con ellas; el mesero las sigue consultando por HU-08. Tampoco dice qué hacer si dos comandas entran a la misma hora. Decidí dejar primero la que se registró primero.

## 2. Pruebas de la IA descartadas o corregidas

**Prompt usado:** le di a la IA las reglas de HU-04 a HU-07, las firmas de las funciones y sus excepciones, y le pedí pruebas en pytest con `@pytest.mark.parametrize` y un comentario por fila, `pytest.approx` para decimales, `pytest.raises` con el tipo exacto y esperados fijos, sin modificar mi código. El prompt está en `evidencias/semana-7/borrador_ia/prompt.md` y el borrador sin cambios en `evidencias/semana-7/borrador_ia/test_borrador_ia.py`. Es la entrada 18 de `bitacora_ia.md`. El borrador tenía 18 pruebas y 1 falló (`evidencias/semana-7/01_borrador_ia_pytest.txt`). Antes de tocar nada revisé la regla: la falla venía de una regla inventada por la IA, no de un defecto del código.

| Prueba generada | Decisión | Por qué | En su lugar |
|---|---|---|---|
| test_cocina_avanza (2 filas) | Corregida | Solo revisaba el estado final. No comprobaba que «en preparación» deja la hora de listo vacía | test_cocina_avanza_un_paso y test_en_preparacion_no_guarda_hora_de_listo |
| test_listo_guarda_hora: `assert c.hora_listo is not None` | Corregida | Débil: pasa con cualquier hora. Lo comprobé con la mutación 10 (se guarda la hora del equipo en vez de la del cambio) y el borrador no falló | test_al_quedar_listo_se_guarda_la_hora compara con la hora exacta del cambio |
| test_cambio_invalido con «listo» y «recibido» | Corregida | No revisaba el mensaje ni que el estado siguiera igual, y faltaban los otros pasos inválidos | test_cocina_no_puede_saltar_repetir_ni_retroceder con las 7 parejas inválidas, `match` y `assert comanda.estado == actual` |
| test_retroceder_de_listo_a_preparacion | Corregida | El esperado sí sale de la regla, pero era una prueba suelta y sin mensaje | Quedó como fila [listo-en preparación] del parametrize, marcada con P-06 |
| test_solo_cocina[mesero] | Corregida | No revisaba el mensaje ni que el estado siguiera igual, y solo probaba un paso válido | test_solo_la_cocina_cambia_el_estado con paso válido, paso inválido y estado que no existe (R1) |
| test_solo_cocina[admin] | Descartada | Regla inventada: A-Fénix no tiene rol de administrador, solo mesero y cocina | Las filas «» y «Cocina», que son errores que sí pueden llegar |
| test_admin_puede_cambiar_estado | Descartada | Regla inventada que contradice HU-07 y contradice la fila anterior del mismo borrador. Fue la prueba que falló; revisé HU-07 y el código está bien | Ninguna: HU-07 ya está cubierta |
| test_minutos_espera con 0, 60, 300, 90 y 3600 segundos y `==` | Corregida | Comparaba decimales con `==`, y 60, 300 y 3600 son la misma partición | 0 s, 1 s, 90 s y 65 min con `pytest.approx` |
| test_minutos_espera_devuelve_numero: `isinstance(..., float)` | Descartada | Débil: pasa aunque el cálculo esté mal | Las filas con `pytest.approx` ya comprueban el valor |
| test_hora_anterior | Corregida | Sin mensaje y sin el límite: probaba 1 minuto antes, no 1 segundo | test_hora_actual_anterior_a_la_entrada_se_rechaza con 1 segundo y 2 horas, con `match` |
| test_orden_de_llegada: `assert len(resultado) == 3` | Corregida | Débil: no revisa el orden, que es justo la regla. Con las mutaciones 6 y 8 (orden al revés, empate por mesa) no falló | test_pantalla_ordena_por_hora_de_entrada compara la lista de mesas |
| test_cocina_sin_comandas | Conservada | El esperado sale de la regla y cubre la partición sin comandas | Agregué el caso de todas listas en test_pantalla_vacia |
| No existía | Agregada | Al borrador le faltaban las comandas listas que salen de la pantalla, la que está en preparación, el empate de hora, el estado que no existe y que la función no desordene el turno | test_las_listas_salen_de_la_pantalla, test_en_preparacion_sigue_en_pantalla, test_misma_hora_queda_primero_la_registrada_primero, test_estado_que_no_existe_se_rechaza, test_no_cambia_la_lista_original |
| test_cantidad_en_el_tope_se_acepta en `test_comandas_datos.py` (de la suite revisada) | Descartada | Redundante: es igual a la prueba de abuso de la semana 6 con cantidad 20 | Dejé solo el límite de 21 y un comentario que apunta a la prueba de la semana 6 |

## 3. Romper el código a propósito

Hice cada cambio, corrí `pytest`, guardé la salida en `evidencias/semana-7/03_mutacion_N.txt` y deshice el cambio con `git restore`. Corrí sin la caché de Python (`PYTHONDONTWRITEBYTECODE=1`). También corrí el borrador de la IA: sin cambios ya tenía 1 falla, así que lo comparo contra ese número.

| Cambio introducido | Archivo y línea | ¿Alguna prueba falló? | Qué hice |
|---|---|---|---|
| 1. `!=` por `>`: se puede repetir y retroceder | afenix/estados.py:40 | Sí, 6: las filas de repetir y retroceder de test_cocina_no_puede_saltar_repetir_ni_retroceder. El borrador también lo notó | Nada |
| 2. `rol != COCINA` por `not rol`: cualquier rol cambia el estado | afenix/estados.py:34 | Sí, 4 filas de test_solo_la_cocina_cambia_el_estado. El borrador también | Nada |
| 3. Guarda la hora de listo en cualquier cambio | afenix/estados.py:44 | Sí: test_en_preparacion_no_guarda_hora_de_listo. El borrador no lo notó | Nada |
| 4. `/ 60` por `// 60`: se pierden los decimales | afenix/cocina.py:20 | Sí: test_minutos_de_espera con 1 s y con 90 s. El borrador también | Nada |
| 5. `<` por `<=`: se rechaza la comanda que recién entra | afenix/cocina.py:18 | Sí: test_minutos_de_espera con 0 s. El borrador también | Nada |
| 6. La pantalla ordena de la más reciente a la más antigua | afenix/cocina.py:32 | Sí: test_pantalla_ordena_por_hora_de_entrada y test_las_listas_salen_de_la_pantalla. El borrador no lo notó, porque solo contaba las comandas | Nada |
| 7. La pantalla muestra también las comandas listas | afenix/cocina.py:31 | Sí: test_las_listas_salen_de_la_pantalla y test_pantalla_vacia[True]. El borrador no lo notó | Nada |
| 8. Con la misma hora ordena por número de mesa | afenix/cocina.py:32 | Sí: test_misma_hora_queda_primero_la_registrada_primero y 2 más. El borrador no lo notó | Nada |
| 9. `>` por `>=` en el tope: se rechaza la cantidad 20 | afenix/comandas.py:89 | Sí: test_cantidad_en_el_tope_se_acepta (la de abuso y la que después descarté por redundante). El borrador no lo notó | Nada |
| 10. Guarda la hora del equipo en vez de la hora del cambio | afenix/estados.py:45 | Sí: test_al_quedar_listo_se_guarda_la_hora. El borrador no lo notó: su `is not None` pasa con cualquier hora | Nada |
| 11. Una modificación vacía lanza FueraDeCarta en vez de ComandaInvalida | afenix/comandas.py:82 | No. Pasaron las 76 (`03_mutacion_11_antes.txt`): `pytest.raises(ComandaInvalida)` también acepta FueraDeCarta, que hereda de ella. En la API eso sería un 422 donde va un 400 | Agregué test_lo_incompleto_no_se_marca_como_fuera_de_carta, que revisa el tipo exacto. Volví a meter el error y fallaron 2 filas (`03_mutacion_11.txt`). Deshice el error con `git restore` |

La suite atrapó 10 de los 11 errores a la primera, y el que faltaba quedó cubierto con el caso nuevo. El borrador de la IA no habría detectado 7 de los 11: el 3, el 6, el 7, el 8, el 9, el 10 y el 11.

## 4. Datos de prueba

**Origen:** sintéticos generados con IA y revisados por mí, en `tests/conftest.py`: el fixture `turno` (cinco comandas de un almuerzo de sábado en el restaurante, el 28/11/2026 entre las 12:00 y las 12:10, que es la hora pico) y el fixture `platos_dificiles`. Confirmo que no hay datos de personas reales. Las funciones solo manejan mesas, platos y horas, así que no hay nombres de clientes, meseros ni teléfonos. La carta es de ejemplo, no la carta real de A Fénix de Oro.

**Casos difíciles incluidos:**
- Tildes y ñ: «Arroz frito con piña», «camarón», «en preparación».
- Apóstrofo: «Pollo General Tso's».
- Texto vacío: picante vacío, rol vacío y estado vacío.
- Mayúsculas: rol «Cocina» y estado «Listo», que no son los valores de la regla.
- Valores en cero y bordes: 0 segundos de espera, mesa 0, lista de platos vacía, cantidad 20 y 21.
- Empate: dos comandas a las 12:04, con la de número mayor (mesa 9) registrada primero, para que ordenar por mesa no dé lo mismo por casualidad.
- Una comanda con dos platos y otra con cantidad 3.
