# Bitácora de uso de IA

Proyecto: A-Fénix, plataforma de comandas para el restaurante chino A Fénix de Oro
Estudiante: Eduardo Ascencio
Funcionalidad: HU-01 Registrar la comanda y HU-02 Modificaciones de cada plato
Asistente usado: Claude (claude.ai), en el chat, en la semana 5; Claude Code dentro de VS Code en la semana 6

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

## Resumen

| Decisión | Cantidad |
|---|---|
| Aceptadas | 7 |
| Aceptadas con cambios | 2 |
| Rechazadas | 3 |

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

Las 22 pruebas de la semana 5 pasaban, pero solo probaban lo que manda un mesero normal. La revisión encontró cuatro problemas que esas pruebas no veían:

| Id | Qué pasaba | Cómo se vio |
|---|---|---|
| H-01 | pytest 8.3.4 tenía una vulnerabilidad conocida | `pip-audit` |
| H-02 | Platos en texto, un plato `None` o un nombre en lista reventaban con `AttributeError` o `TypeError`, que en la API sería un error 500 | 10 pruebas de abuso en rojo |
| H-03 | Se aceptaba una comanda de 10 000 platos y una cantidad de mil millones | 2 pruebas de abuso en rojo |
| H-04 | El mensaje de error devolvía entero un nombre de 5 000 caracteres con `<script>` | 1 prueba de abuso en rojo |

El más serio era H-02: la función prometía lanzar `ComandaInvalida` cuando algo estaba mal, y con datos de otro tipo no lo cumplía. Lo corregí sin tocar las pruebas de la semana 5 y siguen pasando las 22.

## Reflexión final

Lo que más me ayudó del asistente fue que pensó en ejemplos que yo no había considerado, por ejemplo pasarle True como número de mesa o meter un plato malo en medio de una comanda buena. Mi implementación pasaba las 22 pruebas al primer intento, así que no sabía si eran realmente útiles. Metí algunos errores intencionales en el código. El que más me preocupó fue el de omitir los platos malos: hizo fallar 10 pruebas, y sin ellas el sistema podría haber enviado un pedido incompleto a la cocina sin que el mesero se enterara. Además tuve que detener al asistente en dos ocasiones: primero porque creó una API, y luego porque agregó campos de otras historias que nadie había pedido. En la próxima funcionalidad voy a pedirle una sola cosa a la vez y le voy a preguntar al restaurante cuántas mesas tiene antes de programar.
