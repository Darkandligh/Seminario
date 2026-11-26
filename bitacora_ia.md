# Bitácora de uso de IA

Proyecto: A-Fénix, plataforma de comandas para el restaurante chino A Fénix de Oro
Estudiante: Eduardo Ascencio
Funcionalidad: HU-01 Registrar la comanda y HU-02 Modificaciones de cada plato
Asistente usado: Claude (claude.ai), en el chat

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

## Resumen

| Decisión | Cantidad |
|---|---|
| Aceptadas | 3 |
| Aceptadas con cambios | 1 |
| Rechazadas | 2 |

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

## Reflexión final

Lo que más me ayudó del asistente fue que pensó en ejemplos que yo no había considerado, por ejemplo pasarle True como número de mesa o meter un plato malo en medio de una comanda buena. Mi implementación pasaba las 22 pruebas al primer intento, así que no sabía si eran realmente útiles. Metí algunos errores intencionales en el código. El que más me preocupó fue el de omitir los platos malos: hizo fallar 10 pruebas, y sin ellas el sistema podría haber enviado un pedido incompleto a la cocina sin que el mesero se enterara. Además tuve que detener al asistente en dos ocasiones: primero porque creó una API, y luego porque agregó campos de otras historias que nadie había pedido. En la próxima funcionalidad voy a pedirle una sola cosa a la vez y le voy a preguntar al restaurante cuántas mesas tiene antes de programar.
