# Bitácora de uso de IA

Proyecto: A-Fénix, plataforma de comandas para el restaurante chino A Fénix de Oro
Estudiante: Eduardo Ascencio
Funcionalidad: HU-01 y HU-02 (semanas 5 y 6); HU-04 a HU-07 y la suite de pruebas (semana 7)
Asistente usado: Claude (claude.ai), en el chat, en la semana 5; Claude Code dentro de VS Code en las semanas 6 y 7

## Entradas

### Entrada 1

- **Fecha:** 2026-11-23
- **Prompt o sugerencia:** «Con HU-01 y HU-02 y sus escenarios, dame las pruebas en pytest de registrar_comanda, separadas en normales, de límite y de error. Usa los mismos mensajes de error de los escenarios.»
- **Decisión:** Aceptada
- **Por qué:** Las pruebas cubrían los cuatro escenarios de las dos historias y además casos que yo no tenía anotados: la mesa en cero, la lista de platos en `None`, una modificación vacía y un plato malo dentro de una comanda buena.
- **Verificación:** Leí cada prueba y comprobé que el mensaje esperado fuera el mismo de la historia. Con la función vacía (solo lanza `NotImplementedError`) fallaron las 22, como debía ser.
- **Commit relacionado:** e76d86b «Pruebas de registrar comanda, HU-01 y HU-02 (en rojo)»

### Entrada 2

- **Fecha:** 2026-11-23
- **Prompt o sugerencia:** La primera versión que armó la IA traía también una API con FastAPI (`GET /api/platos` y `POST /api/comandas`) y un repositorio en memoria para guardar las comandas.
- **Decisión:** Rechazada
- **Por qué:** Esta semana es una sola funcionalidad con sus pruebas, y las pruebas deben correr con un solo comando sin levantar un servidor. FastAPI ya está decidido en mi diseño (ADR-001), pero lo agrego cuando la lógica esté revisada.
- **Verificación:** Sin la API las pruebas corren con `python -m pytest` en menos de un segundo y solo piden pytest.
- **Commit relacionado:** No quedó en el repositorio; la saqué antes del primer commit de la semana.

### Entrada 3

- **Fecha:** 2026-11-23
- **Prompt o sugerencia:** En el primer borrador, la clase `Comanda` traía `id`, `hora_entrega` y una lista de cambios de estado.
- **Decisión:** Rechazada
- **Por qué:** Ninguno de esos campos sale de HU-01 ni de HU-02. La hora de entrega y los cambios de estado son de HU-06, y el id lo pone la base de datos cuando exista. Si los dejaba, el código tendría datos que nadie llena.
- **Verificación:** Revisé los escenarios de HU-01 y HU-02: piden mesa, platos, modificaciones, estado «recibido» y hora de entrada, y nada más. Eso es lo que quedó en `Comanda`.
- **Commit relacionado:** e76d86b «Pruebas de registrar comanda, HU-01 y HU-02 (en rojo)»

### Entrada 4

- **Fecha:** 2026-11-23
- **Prompt o sugerencia:** «Escribe registrar_comanda para que pasen estas pruebas.» Para los mensajes de una modificación vacía, la IA armó el texto con condiciones según el género de cada palabra («es obligatoria» para la base y la proteína, «es obligatorio» para el tamaño y el picante).
- **Decisión:** Aceptada con cambios
- **Por qué:** Funcionaba, pero era difícil de leer. Lo cambié por un diccionario con el artículo de cada modificación y un solo mensaje: «Falta la base de «Chop suey»».
- **Verificación:** Las 4 pruebas de modificación vacía pasan y el mensaje se lee bien con las cuatro modificaciones.
- **Commit relacionado:** f4e6b02 «Registrar comanda: implementación, las 22 pruebas pasan (en verde)»

### Entrada 5

- **Fecha:** 2026-11-23
- **Prompt o sugerencia:** La IA agregó una revisión aparte para que `True` no pase como mesa, porque en Python `True` es un entero que vale 1.
- **Decisión:** Aceptada
- **Por qué:** No lo sabía. Sin esa revisión, `registrar_comanda(True, ...)` guardaba una comanda en la mesa 1.
- **Verificación:** Hay una prueba con `True` como mesa. Quité la revisión a propósito y esa prueba falló.
- **Commit relacionado:** f4e6b02 «Registrar comanda: implementación, las 22 pruebas pasan (en verde)»

### Entrada 6

- **Fecha:** 2026-11-23
- **Prompt o sugerencia:** «Refactoriza registrar_comanda sin cambiar su comportamiento: saca los mensajes a constantes y separa las validaciones en funciones pequeñas.»
- **Decisión:** Aceptada
- **Por qué:** Quedaron `_es_entero_positivo` y `_validar_plato`, y `registrar_comanda` ahora se lee casi como la historia: revisa la mesa, revisa que haya platos y revisa cada plato.
- **Verificación:** No toqué ninguna prueba (`git diff -- tests` sale vacío) y siguen pasando las 22, con 100 % de cobertura.
- **Commit relacionado:** 8b50fad «Refactor: mensajes en constantes y validaciones en funciones pequeñas (sin tocar las pruebas)»

## Entradas de la semana 6

### Entrada 7

- **Fecha:** 2026-11-23
- **Prompt o sugerencia:** «Sigue con la semana 6.» La IA configuró ruff, bandit y mypy en `pyproject.toml` y los corrió antes de cambiar nada. Ruff marcó dos líneas largas (E501) en `tests/test_registrar_comanda.py` y la IA propuso no corregirlas.
- **Decisión:** Aceptada
- **Por qué:** Esas líneas están en las pruebas de la semana 5, que no se pueden modificar, y no son un problema de seguridad. Quedaron anotadas como avisos no corregidos en `revision_seguridad.md`.
- **Verificación:** `git diff semana-5 -- tests/test_registrar_comanda.py` sale vacío.
- **Commit relacionado:** 4bd1861 «Configura ruff, bandit y mypy en pyproject.toml»

### Entrada 8

- **Fecha:** 2026-11-23
- **Prompt o sugerencia:** La IA corrió `pip-audit` y salió que pytest 8.3.4 tiene la vulnerabilidad PYSEC-2026-1845. Propuso subir a pytest 9.0.3 y pytest-cov a 7.1.0.
- **Decisión:** Aceptada
- **Por qué:** Es la versión que corrige la falla y es un cambio de dos líneas.
- **Verificación:** Con las versiones nuevas pasan las 22 pruebas de la semana 5 y `pip-audit` sale sin vulnerabilidades.
- **Commit relacionado:** 1f7a23a «H-01: sube pytest a 9.0.3 por PYSEC-2026-1845»

### Entrada 9

- **Fecha:** 2026-11-23
- **Prompt o sugerencia:** «Revisa comandas.py como si los datos llegaran directo de la API, sin confiar en la tablet.» La IA llamó la función con datos raros (platos en texto, un plato `None`, el nombre del plato en lista, 10 000 platos, una cantidad de mil millones, un nombre de 5 000 caracteres con `<script>`) y con lo que falló armó 15 pruebas de abuso en un archivo aparte.
- **Decisión:** Aceptada
- **Por qué:** Cada prueba sale de algo que probé y falló de verdad. Además trae dos pruebas que pasan desde el principio (50 platos y cantidad 20) para que la corrección no rechace comandas buenas.
- **Verificación:** Antes de corregir fallaron 13 de las 15. Después de H-02, H-03 y H-04 pasan las 15.
- **Commit relacionado:** a2e7f85 «Pruebas de abuso de registrar comanda (en rojo)»

### Entrada 10

- **Fecha:** 2026-11-23
- **Prompt o sugerencia:** Para H-03 la IA puso un tope de 50 platos por comanda y 20 por plato. A la mesa no le puso tope.
- **Decisión:** Aceptada
- **Por qué:** Sin tope cualquiera llena la pantalla de cocina con una sola petición. Los números son provisionales hasta que el restaurante diga cuántas comandas tiene en hora pico (P-01). A la mesa no le puse tope porque no sé cuántas mesas hay (P-03) y prefiero no inventarlo.
- **Verificación:** Las pruebas de 51 platos y cantidad de mil millones fallan con el mensaje nuevo, y las de 50 platos y cantidad 20 pasan.
- **Commit relacionado:** 06f1eb1 «H-03: pone tope de 50 platos por comanda y 20 por plato»

### Entrada 11

- **Fecha:** 2026-11-23
- **Prompt o sugerencia:** Para que mypy en modo estricto no diera errores, la primera versión de la IA repetía `isinstance(valor, int)` antes de cada llamada a `_es_entero_positivo`.
- **Decisión:** Aceptada con cambios
- **Por qué:** Repetir la misma revisión en dos sitios es fácil de olvidar en uno. Lo cambié para que `_es_entero_positivo` devuelva `TypeGuard[int]`, y así mypy sabe que el valor es entero sin repetir nada.
- **Verificación:** `mypy` sale sin errores, ruff sin avisos en `afenix/` y pasan las 37 pruebas con 100 % de cobertura.
- **Commit relacionado:** 2678ccb «Tipos y docstrings en comandas.py, mypy sin errores»

### Entrada 12

- **Fecha:** 2026-11-23
- **Prompt o sugerencia:** En la revisión la IA marcó que el parámetro `ahora` acepta cualquier cosa, por ejemplo un texto, y lo guarda como hora de entrada.
- **Decisión:** Rechazada
- **Por qué:** Es cierto, pero `ahora` no viene del cliente: lo usan las pruebas para no depender del reloj, y en la API guardada (`_guardado/api.py`) no se pasa. Validarlo sería código que hoy no protege de nada.
- **Verificación:** Revisé `_guardado/api.py`: llama `registrar_comanda(datos.get("mesa"), datos.get("platos"))`, sin `ahora`.
- **Commit relacionado:** Ninguno; quedó como falso positivo en `revision_seguridad.md`.

### Entrada 13

- **Fecha:** 2026-11-26
- **Prompt o sugerencia:** Segunda revisión con el prompt de la semana: criterios de corrección, diseño y seguridad, tabla con archivo, línea y severidad, y los problemas seguros separados de las sospechas. Claude encontró 6 cosas.
- **Decisión:** Aceptada con cambios
- **Por qué:** De las 6, corregí dos (H-05 y H-06) y dejé una en pendientes (la mesa sin tope). Las dos sospechas eran falsos positivos: el mensaje con `0` o `""` igual lanza `ComandaInvalida`, y la hora sin zona no importa porque todo corre en un solo equipo. Tampoco le puse docstring a `_es_entero_positivo`, porque es auxiliar y ya tiene un comentario.
- **Verificación:** Llamé la función con cada caso. Quedó la tabla en la sección 3 de `revision_seguridad.md`.
- **Commit relacionado:** Ninguno; los cambios están en las entradas 14 y 15.

### Entrada 14

- **Fecha:** 2026-11-26
- **Prompt o sugerencia:** Para H-05 la IA propuso sumar las cantidades de todos los platos y comparar el total con el tope de 50, con una prueba de abuso de 3 filas de 20.
- **Decisión:** Aceptada
- **Por qué:** El tope de H-03 se podía saltar repartiendo los platos en filas. Mantuve el mismo número, 50, para no inventar otro hasta que el restaurante confirme (P-01), y agregué una prueba de 5 filas de 10 para no rechazar comandas buenas.
- **Verificación:** La prueba nueva falló antes de la corrección y después pasan las 39. Las pruebas de la semana 5 no cambiaron (`git diff 7f1f11d -- tests/test_registrar_comanda.py` sale vacío).
- **Commit relacionado:** 3556eef «Prueba de abuso: más de 50 platos sumando las cantidades (en rojo)» y affc4b8 «H-05: el tope de 50 platos suma las cantidades de cada plato»

### Entrada 15

- **Fecha:** 2026-11-26
- **Prompt o sugerencia:** La IA vio que la firma del contrato en el README no tenía tipos (H-06). Lo corregí en `semana-5` y traje ese cambio a `semana-6` con un merge.
- **Decisión:** Aceptada
- **Por qué:** El contrato tiene que coincidir con el código, y el código ya tenía los tipos desde la entrada 11.
- **Verificación:** El merge no tuvo conflictos y pasan las 39 pruebas.
- **Commit relacionado:** 872e714 (en `semana-5`) y 69f0f40 «Trae de semana-5 la firma con tipos y la reflexión final»

### Entrada 16

- **Fecha:** 2026-11-26
- **Prompt o sugerencia:** Revisión del trabajo del agente. Claude Code hizo las correcciones de la semana 6 como agente, trabajando en la rama `semana-6`, separada de `semana-5`.
- **Decisión:** Aceptada
- **Por qué:** Antes de entregar revisé su diff completo en GitHub (comparación `7f1f11d...semana-6`): los topes en `comandas.py`, la revisión de formato, el recorte del nombre en el mensaje y las pruebas de abuso.
- **Verificación:** En el diff no aparece `tests/test_registrar_comanda.py`, así que el agente no tocó las pruebas de la semana 5. Pasan las 39 pruebas.
- **Commit relacionado:** Todos los de la rama `semana-6`, desde 4bd1861 hasta este.

## Entradas de la semana 7

### Entrada 17

- **Fecha:** 2026-11-23
- **Prompt o sugerencia:** «Con las reglas de HU-01, HU-02 y HU-04 a HU-07, propón la tabla de casos de cada función con particiones de equivalencia, valores límite y tabla de decisión para la que combina condiciones.» La IA armó las cuatro tablas y la tabla de decisión de `cambiar_estado`, con 6 reglas.
- **Decisión:** Aceptada con cambios
- **Por qué:** Revisé la propuesta con las cinco preguntas. Las particiones y los límites estaban, y cada esperado salía de una historia. Lo que cambié fueron las reglas inventadas: HU-05 habla de comandas atrasadas, pero no hay un número para decir cuándo una comanda va tarde (P-02), así que no se programa la alerta y queda como ambigüedad. También anoté las decisiones que no salen de la regla: que una comanda lista sale de la pantalla, que en un empate de hora va primero la que se registró primero, y que solo el rol «cocina», escrito tal cual, tiene permiso.
- **Verificación:** Cada fila de `registro_pruebas.md` dice de qué historia sale su esperado. Las decisiones que no salen de una historia quedaron en «Ambigüedades encontradas».
- **Commit relacionado:** 0003ad0 «Registro de pruebas de la semana 7»

### Entrada 18

- **Fecha:** 2026-11-23
- **Prompt o sugerencia:** El prompt de `evidencias/semana-7/borrador_ia/prompt.md`: las reglas, las firmas de las funciones y el pedido de usar parametrize con un comentario por fila, `pytest.approx`, `pytest.raises` con el tipo exacto y esperados fijos, sin tocar mi código. La IA entregó 18 pruebas y 1 falló.
- **Decisión:** Aceptada con cambios
- **Por qué:** La que falló esperaba que un «admin» pudiera cambiar el estado. Revisé HU-07 antes de tocar nada: solo la cocina cambia el estado y A-Fénix no tiene administrador, así que el error era de la prueba y la descarté. Con las tres preguntas corregí 9 pruebas, descarté 3 (dos con el rol inventado y una débil que solo miraba el tipo del resultado) y agregué 5 que faltaban. Todo está en la sección 2 de `registro_pruebas.md`.
- **Verificación:** Corrí el borrador contra los 11 errores a propósito: no habría detectado 7. La suite revisada atrapó 10 a la primera.
- **Commit relacionado:** 029ce2b «Suite de pruebas de estados y cocina, datos sintéticos y borrador de la IA como evidencia»

### Entrada 19

- **Fecha:** 2026-11-23
- **Prompt o sugerencia:** «Genera datos sintéticos para las pruebas: comandas de un turno de almuerzo de A Fénix de Oro, sin personas reales, con casos difíciles como tildes, ñ, apóstrofo, texto vacío y valores en cero. Ponlos en un fixture de pytest.» La IA armó el fixture `turno`, con cinco comandas de un sábado entre las 12:00 y las 12:10, y el fixture `platos_dificiles`.
- **Decisión:** Aceptada
- **Por qué:** Las comandas solo llevan mesa, platos y hora, así que no hacen falta nombres ni teléfonos. Me sirvió que en el empate de las 12:04 la mesa 9 se registre antes que la 2: así, si alguien ordena por número de mesa, la prueba lo nota.
- **Verificación:** Revisé que todos los platos y opciones estén en la carta de ejemplo y que no haya nombres de personas. La mutación 8 (ordenar el empate por mesa) hizo fallar la prueba del empate.
- **Commit relacionado:** 029ce2b «Suite de pruebas de estados y cocina, datos sintéticos y borrador de la IA como evidencia»

### Entrada 20

- **Fecha:** 2026-11-23
- **Prompt o sugerencia:** La IA propuso como mutación 11 que una modificación vacía lanzara `FueraDeCarta` en vez de `ComandaInvalida`, y las 76 pruebas pasaron. Propuso agregar una prueba que revise el tipo exacto del error.
- **Decisión:** Aceptada
- **Por qué:** `pytest.raises(ComandaInvalida)` también acepta `FueraDeCarta`, porque hereda de ella. En la API eso sería un 422 donde la tabla del diseño pide un 400. Es justo lo que la tarea pide: si ninguna prueba falla, falta un caso.
- **Verificación:** Con la prueba nueva volví a meter el error y fallaron 2 filas. Lo deshice con `git restore` y pasaron las 79.
- **Commit relacionado:** 911442f «Mutaciones 1 a 11 con evidencias; caso agregado tras la mutación 11»

### Entrada 21

- **Fecha:** 2026-11-23
- **Prompt o sugerencia:** En la suite revisada, la IA escribió `test_cantidad_en_el_tope_se_acepta` en `tests/test_comandas_datos.py`.
- **Decisión:** Rechazada
- **Por qué:** Es redundante: prueba lo mismo que la prueba de abuso de la semana 6 con cantidad 20. En la mutación 9 fallaron las dos a la vez, así que la segunda no aporta nada.
- **Verificación:** La quité y la mutación 9 sigue cubierta por la prueba de la semana 6.
- **Commit relacionado:** 911442f «Mutaciones 1 a 11 con evidencias; caso agregado tras la mutación 11»

## Entradas de la semana 9

### Entrada 22

- **Fecha:** 2026-11-26
- **Prompt o sugerencia:** «Escribe un workflow de GitHub Actions para mi proyecto de Python con pytest.» La IA entregó un pipeline que corre `pytest` en cada push y pull request a `main`.
- **Decisión:** Aceptada con cambios
- **Por qué:** La base servía y no tenía claves ni `continue-on-error`, pero al revisarlo con la lista de la semana 9 salieron 6 problemas: solo revisaba `main`, no limitaba los permisos, usaba Python «3.x» y paquetes sin versión, solo corría pytest y no tenía tiempo límite. Los corregí todos; el detalle está en `docs/revision_configuracion.md`.
- **Verificación:** El pipeline revisado salió en verde en GitHub. Cambié el tope de platos a 49 a propósito y salió en rojo en el paso de pruebas; lo revertí y volvió a verde. actionlint no encontró ninguno de los 6 problemas.
- **Commit relacionado:** 2ddd140 «Borrador del pipeline generado por la IA, sin cambios (evidencia)» y 6daf173 «Pipeline de CI revisado…»

### Entrada 23

- **Fecha:** 2026-11-26
- **Prompt o sugerencia:** Le pedí a la IA que redactara el reporte de defecto D-01 con la plantilla de la semana 8, a partir de H-05.
- **Decisión:** Aceptada
- **Por qué:** El reporte sigue la plantilla y el caso mínimo es una sola llamada. Revisé que los pasos, el commit y el resultado fueran los reales y no inventados.
- **Verificación:** Seguí los pasos en el commit 69f0f40, antes de la corrección: la comanda de 3 filas de 20 quedó «recibido» con 60 platos, como dice el reporte.
- **Commit relacionado:** el de `docs/defectos/D-01.md`.

## Resumen

| Decisión | Cantidad |
|---|---|
| Aceptadas | 13 |
| Aceptadas con cambios | 6 |
| Rechazadas | 4 |

## Errores que atraparon las pruebas

La implementación pasó las 22 pruebas en la primera corrida, así que para saber si las pruebas de verdad sirven metí errores a propósito en el código, uno a la vez, y las corrí:

| Error metido | Pruebas que fallaron |
|---|---|
| Aceptar la mesa 0 y la cantidad 0 (`>= 0` en vez de `>= 1`) | 2 |
| Aceptar una comanda con la lista de platos vacía | 1 |
| No revisar las opciones contra la carta | 2 |
| Dejar pasar `True` como mesa | 1 |
| Saltarse los platos malos en vez de rechazar toda la comanda | 10 |

Las pruebas detectaron los cinco. Después dejé el código como estaba y volvieron a pasar las 22. El más peligroso era el último: con ese error la comanda se guardaba sin el plato malo y el mesero no se enteraba, así que a la cocina llegaba un pedido incompleto.

## Errores que atrapó la revisión de la semana 6

Las 22 pruebas de la semana 5 pasaban, pero solo probaban lo que manda un mesero normal. La revisión encontró cinco problemas que esas pruebas no veían:

| Id | Qué pasaba | Cómo se vio |
|---|---|---|
| H-01 | pytest 8.3.4 tenía una vulnerabilidad conocida | `pip-audit` |
| H-02 | Platos en texto, un plato `None` o un nombre en lista reventaban con `AttributeError` o `TypeError`, que en la API sería un error 500 | 10 pruebas de abuso en rojo |
| H-03 | Se aceptaba una comanda de 10 000 platos y una cantidad de mil millones | 2 pruebas de abuso en rojo |
| H-04 | El mensaje de error devolvía entero un nombre de 5 000 caracteres con `<script>` | 1 prueba de abuso en rojo |
| H-05 | El tope de 50 platos contaba filas: 50 filas de cantidad 20 eran 1000 platos | 1 prueba de abuso en rojo, en la segunda revisión |

El más serio era H-02: la función prometía lanzar `ComandaInvalida` cuando algo estaba mal, y con datos de otro tipo no lo cumplía. Lo corregí sin tocar las pruebas de la semana 5 y siguen pasando las 22.

## Reflexión final

Lo que más me ayudó del asistente fue que pensó en ejemplos que yo no había considerado, por ejemplo pasarle True como número de mesa o meter un plato malo en medio de una comanda buena. Mi implementación pasaba las 22 pruebas al primer intento, así que no sabía si eran realmente útiles. Metí algunos errores intencionales en el código. El que más me preocupó fue el de omitir los platos malos: hizo fallar 10 pruebas, y sin ellas el sistema podría haber enviado un pedido incompleto a la cocina sin que el mesero se enterara. Además tuve que detener al asistente en dos ocasiones: primero porque creó una API, y luego porque agregó campos de otras historias que nadie había pedido. En la próxima funcionalidad voy a pedirle una sola cosa a la vez y le voy a preguntar al restaurante cuántas mesas tiene antes de programar.
