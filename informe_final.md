# Informe final del proyecto integrador

Proyecto: A-Fénix, plataforma de comandas digitales para el restaurante chino A Fénix de Oro\
Estudiante: Eduardo Ascencio · Ingeniería de Software · Fundación Escuela Tecnológica de Neiva - FET\
Repositorio: https://github.com/Darkandligh/Seminario\
Video de la sustentación: [PEGA AQUÍ EL ENLACE DE TU VIDEO]\
Fecha: 2026-11-26

## 1. Resumen

En A Fénix de Oro el mesero anota los pedidos en una libreta y lleva la hoja a la cocina. A veces la cocina no entiende la letra o se pierde una hoja, y el plato sale mal o tarde. A-Fénix reemplaza la hoja: el mesero registra la comanda en una tablet con la base, la proteína, el tamaño y el picante de cada plato, y la cocina la ve en una pantalla en orden de llegada y marca cuándo está lista. Usé IA en las seis fases: para la propuesta, los requisitos, el diseño, el código, las pruebas y el pipeline. El resultado principal de la verificación es que la IA se equivocó en todas las fases, sobre todo inventando cosas que nadie pidió, y que la mayoría de esos errores solo aparecieron al compararlos con los requisitos o al romper el código a propósito. Evalué cada historia de usuario contra sus escenarios de aceptación: de 16 escenarios, 9 se cumplen completos, 3 en parte y 4 son de historias que no alcancé a construir. El proyecto tiene 93 pruebas que pasan, con 100 % de cobertura de la lógica del negocio, y un pipeline que las corre en cada cambio.

## 2. Problema y usuario

Los usuarios son los 3 meseros y los 2 cocineros del restaurante. Hoy el mesero anota la mesa y los platos en una libreta, pregunta por cada plato si va con arroz frito o chop suey, de pollo, cerdo o res, personal o familiar, y si es picante, y lleva la hoja a la cocina. El cocinero saca las hojas en el orden en que llegan y canta la mesa cuando el plato está listo; si el mesero no lo oye, tiene que ir a preguntar. En la hora del almuerzo salen unas 60 comandas, y lo que más preocupa a la administradora es que el sistema se caiga en plena hora pico.

Lo que necesitan es que el pedido llegue a la cocina completo y legible, en orden, y que el salón sepa cuándo está listo.

Evidencia: [propuesta del módulo 1](docs/modulos/S2_Propuesta.pdf) y [documento de requisitos con la entrevista del módulo 2](docs/modulos/S3_Requisitos.pdf), anexo A. La entrevista es simulada; lo explico en la sección 6.

## 3. La IA en el ciclo de vida

Seguí el ciclo de vida completo, una fase por módulo del seminario, y en cada fase la IA hizo una parte y yo la revisé. Cuando algo fallaba en las pruebas o en el pipeline, volvía a la fase de requisitos o a la de código, no a cambiar la prueba.

![Ciclo de vida de A-Fénix con IA](docs/ciclo_vida.png)


| Módulo y fase | Qué hice con IA | Herramienta | Evidencia | Cómo verifiqué |
|---|---|---|---|---|
| 1. Fundamentos | Ordenar la propuesta: problema, fase donde aplicar IA (pruebas) y meta medible | Claude (chat) | [S2_Propuesta.pdf](docs/modulos/S2_Propuesta.pdf) | La idea y la meta son mías; revisé que la meta se pudiera medir (cobertura y errores a propósito) |
| 2. Requisitos | Adaptar la entrevista, pasar las respuestas a 11 necesidades con cita, 8 historias con escenarios Gherkin, 3 RNF y la matriz de trazabilidad | Claude (chat) | [S3_Requisitos.pdf](docs/modulos/S3_Requisitos.pdf) | Cada necesidad tiene su cita y cada historia su necesidad de origen. Lo que no tenía cita pasó a preguntas pendientes |
| 3. Diseño | Tres alternativas de arquitectura, diagramas C4, modelo de datos y API, y una revisión de coherencia | Claude (chat) | [S4_Diseno.pdf](docs/modulos/S4_Diseno.pdf) | Matriz ponderada con mis pesos; cada caja, entidad y ruta contra una historia (5 fichas de prompt) |
| 4. Código | `registrar_comanda` con pruebas primero (rojo, verde, refactor). Revisión de seguridad con ruff, bandit, mypy, pip-audit y dos revisiones con IA | Claude (chat) y Claude Code en VS Code (agente) | [README](README.md), [revision_seguridad.md](revision_seguridad.md) | 22 pruebas escritas antes del código; 17 pruebas de abuso en rojo antes de corregir; diff del agente revisado |
| 5. Pruebas | Tabla de casos con particiones, límites y tabla de decisión; borrador de pruebas de la IA revisado; datos sintéticos; 11 errores metidos a propósito; reporte de defecto | Claude Code en VS Code | [registro_pruebas.md](registro_pruebas.md), [evidencias/semana-7](evidencias/semana-7), [D-01](docs/defectos/D-01.md) | Cada esperado sale de una historia, no del código. Corrí el borrador de la IA contra los 11 errores |
| 6. Operación | Pipeline de GitHub Actions generado con IA y revisado con la lista de revisión de pipelines del curso | Claude (chat) | [ci.yml](.github/workflows/ci.yml), [revision_configuracion.md](docs/revision_configuracion.md) | Ejecución en verde, error a propósito en rojo y otra vez en verde |

Todas las decisiones con IA están en la [bitácora](bitacora_ia.md): 23 entradas, 13 aceptadas, 6 aceptadas con cambios y 4 rechazadas.

## 4. Verificación: lo que la IA hizo mal y cómo lo encontré

### Caso 1: requisitos que el cliente nunca pidió

Esto pasó en la fase de requisitos. En la semana 3, cuando mi proyecto todavía era VetCare Pro, la IA armó el documento de requisitos antes de que yo hiciera la entrevista, con respuestas supuestas del cliente: inventario de medicamentos, un rol de recepcionista, facturación y fallas de internet. Nada de eso lo dijo el cliente, aunque todo se veía razonable. Lo descubrí al comparar cada necesidad con las respuestas de la entrevista, porque las que no tenían una cita no tenían de dónde salir. Descarté ese borrador y desde ahí cada necesidad lleva su cita y cada historia su necesidad de origen. Cuando pasé el proyecto a A-Fénix volvió a pasar algo parecido: al adaptar la entrevista al restaurante, la IA dejó cosas que solo tienen sentido en una veterinaria, como el carnet de vacunación o que los clientes usaran el sistema, y las quité ([S3, sección 7](docs/modulos/S3_Requisitos.pdf)).

### Caso 2: un tope de seguridad que no protegía nada

Este fue en el código. En la revisión de seguridad el agente puso un tope de 50 platos por comanda (H-03), pero contaba las filas de la lista y no los platos. Como cada fila tiene su cantidad, 50 filas de cantidad 20 eran 1000 platos, y el tope se saltaba repartiendo los platos en filas. Lo encontré en la segunda revisión, con el prompt de la semana que pide separar los problemas seguros de las sospechas y comprobar cada uno llamando la función: con 3 filas de 20 la comanda quedó registrada con 60 platos. Primero escribí la prueba de abuso en rojo ([3556eef](https://github.com/Darkandligh/Seminario/commit/3556eef)) y después la corrección, que suma las cantidades ([affc4b8](https://github.com/Darkandligh/Seminario/commit/affc4b8)). Quedó como H-05 en el informe de seguridad y como el defecto [D-01](docs/defectos/D-01.md).

### Caso 3: pruebas que pasaban aunque el código estuviera mal

En la fase de pruebas le pedí a la IA un borrador para el cambio de estado y la pantalla de cocina. Para revisar el orden de la pantalla usó `assert len(resultado) == 3`, para la hora de entrega `assert c.hora_listo is not None`, y además escribió una prueba de que un «admin» puede cambiar el estado. Las dos primeras pasan aunque el orden esté al revés o la hora sea cualquiera, y la tercera es una regla inventada, porque A-Fénix no tiene administrador y HU-07 dice que solo la cocina cambia el estado. La del admin falló, revisé HU-07 antes de tocar el código y vi que el error estaba en la prueba. Para encontrar las pruebas débiles metí 11 errores a propósito en el código, y el borrador no habría detectado 7. Descarté o corregí 11 pruebas del borrador y agregué las que faltaban. Mi suite atrapó 10 de los 11 errores, y el que se escapó, una modificación vacía marcada como «fuera de carta», me llevó a agregar una prueba que revisa el tipo exacto de la excepción ([registro_pruebas.md](registro_pruebas.md), commit [911442f](https://github.com/Darkandligh/Seminario/commit/911442f)).

### Caso 4: un pipeline que parecía bien

En operación le pedí a la IA un pipeline con un prompt simple. Me dio uno que corre `pytest` en cada push a `main`, con Python «3.x» y `pip install pytest` sin versión ([borrador](evidencias/entrega-final/ci_borrador_ia.yml)). Funcionaba, pero no revisaba las ramas de cada semana, que es donde trabajo, no limitaba los permisos, usaba versiones que cambian solas y solo corría las pruebas. actionlint no marcó nada porque el archivo es válido; los problemas los vi revisándolo línea por línea con la lista de revisión de pipelines del curso. Corregí los seis ([revision_configuracion.md](docs/revision_configuracion.md)) y comprobé que con un error a propósito el pipeline se pone en rojo.

## 5. Estado final del sistema

La arquitectura es un monolito web en Python con FastAPI y SQLite, instalado en un mini PC del restaurante, que no depende de internet y tiene la pantalla de cocina conectada por cable. Ganó la matriz ponderada con 103 puntos, contra 69 de la opción en la nube y 65 de los microservicios ([documento de diseño y ADR-001](docs/modulos/S4_Diseno.pdf)).

De las 8 historias terminé la lógica de 6. Registrar la comanda (HU-01) y elegir las modificaciones desde la carta (HU-02) están en `afenix/comandas.py`. La pantalla de cocina en orden de llegada (HU-04) y el tiempo de espera (HU-05) están en `afenix/cocina.py`. El cambio de estado paso a paso (HU-06) y la regla de que solo la cocina lo cambia (HU-07), con su prueba de abuso del rol, están en `afenix/estados.py`. Quedaron pendientes HU-03, que la comanda llegue sola a la cocina, porque necesita la API y el WebSocket, y HU-08, la consulta del estado por mesa.

### Evaluación de las historias de usuario

Para evaluar las historias escribí una prueba por cada escenario de aceptación del documento de requisitos, con los mismos datos del escenario: la mesa 4 con arroz frito con piña y chop suey, la mesa 2 a las 12:05 y la mesa 6 a las 12:01, y así con todos ([tests/test_aceptacion.py](tests/test_aceptacion.py)). Cada prueba comprueba todo el «entonces» del escenario, no solo una parte. Cuando el código no cumple el criterio, la prueba queda marcada como diferencia conocida (`xfail`) en lugar de cambiarla para que pase.

| Historia | Prioridad | Escenario | Resultado | Qué encontré |
|---|---|---|---|---|
| HU-01 Registrar la comanda | Must | 1. Comanda registrada | Cumple | Queda «recibido» con mesa, platos y hora |
| | | 2. Comanda sin platos | Cumple | Mismo mensaje del criterio |
| HU-02 Modificaciones desde la carta | Must | 1. Plato con modificaciones | Cumple | Guarda las cuatro modificaciones |
| | | 2. Opción fuera de la carta | Cumple | «La proteína no está en la carta» |
| HU-03 La comanda llega a la cocina | Must | 1 y 2 | Sin construir | Necesita la API y el WebSocket |
| HU-04 Cocina en orden de llegada | Must | 1. Orden por llegada | Cumple | La mesa 6 sale antes que la 2 |
| | | 2. Comanda lista | Cumple | No aparece en la pantalla |
| HU-05 Tiempo de espera | Should | 1. Tiempo a la vista | Cumple | 12 minutos |
| | | 2. Hora del equipo errada | En parte | No muestra un tiempo negativo, pero el mensaje no es «Revisa la hora del equipo» |
| HU-06 Cambio de estado | Should | 1. Pedido listo | Cumple | Guarda las 12:24 como hora de entrega |
| | | 2. Salto de estado | En parte | El estado no cambia, pero el mensaje no es el del criterio |
| HU-07 Solo la cocina cambia el estado | Should | 1. Cambio desde la cocina | En parte | Cambia el estado, pero no guarda quién lo hizo ni a qué hora |
| | | 2. Cambio desde el salón | Cumple | Lo rechaza y el estado no cambia |
| HU-08 Consulta por mesa | Could | 1 y 2 | Sin construir | Pendiente |

De los 16 escenarios, 9 se cumplen completos, 3 en parte y 4 son de las dos historias que no construí. De las historias Must, tres están completas (HU-01, HU-02 y HU-04) y una sin construir (HU-03). Las tres diferencias son reales y no las había visto antes: las pruebas de la semana 7 revisaban que hubiera un error, pero no comparaban el mensaje con el del criterio, y ninguna revisaba que el cambio de estado guardara quién lo hizo. La de HU-07 es la más importante, porque el modelo de datos sí tiene la entidad CambioEstado para eso y el código no la usa. Las dejo como pendientes en lugar de esconderlas.

Hay 93 pruebas que pasan, entre normales, de límite, de error, de abuso y de aceptación, con 100 % de cobertura de `afenix/`, y 3 pruebas de aceptación marcadas como diferencias conocidas (ver la evaluación de historias). El pipeline las corre junto con ruff, mypy, bandit y pip-audit en cada cambio ([última ejecución del pipeline en main](https://github.com/Darkandligh/Seminario/actions?query=branch%3Amain)).

No alcancé a hacer la API, la base de datos ni las pantallas. El seminario se centró en la lógica y en cómo verificarla, y preferí terminar bien 6 historias que dejar las 8 a medias. También quedan preguntas para el restaurante: cuántas mesas tiene (P-03), si los topes de 50 platos y 20 por plato le sirven (P-01) y si un pedido marcado listo por error se puede devolver (P-06). También quedan las tres diferencias de la evaluación de historias: los dos mensajes que no son los del criterio y guardar quién cambió el estado y a qué hora.

## 6. Reflexión ética y legal

| Principio | Decisión en mi proyecto | Evidencia |
|---|---|---|
| Datos personales (Ley 1581 de 2012) | No uso datos de personas reales. Las comandas solo tienen mesa, platos y hora; los datos de prueba son sintéticos y los nombres del documento de requisitos son ficticios. A la IA nunca le pasé datos del restaurante | [tests/conftest.py](tests/conftest.py), [S3, introducción](docs/modulos/S3_Requisitos.pdf) |
| Sesgo | La IA tiende a proponer lo que ve en otros sistemas (administradores, facturación, Redis, microservicios) aunque el restaurante no lo necesite. Lo traté como un sesgo: nada entra sin una cita del cliente o una historia | Casos 1 y 3 de este informe |
| Transparencia | Declaro en la bitácora cada uso de IA y guardo los borradores de la IA sin cambios como evidencia. La entrevista simulada está marcada como simulada en el documento de requisitos | [bitacora_ia.md](bitacora_ia.md), [evidencias/](evidencias) |
| Responsabilidad | Lo que entrego es mío aunque lo haya escrito la IA. Por eso ninguna prueba se modifica para que pase, el agente trabaja en una rama aparte y reviso su diff, y el pipeline no deja pasar un cambio que rompa las pruebas | Entrada 16 de la bitácora, [ci.yml](.github/workflows/ci.yml) |
| Propiedad intelectual y política de uso | Las dependencias son de código abierto (pytest, ruff y mypy con licencia MIT; bandit y pip-audit con Apache 2.0). La política de uso de Claude permite usar lo que genera, y lo declaro. Usé el repositorio de un compañero solo como referencia del formato de entrega, sin copiar su código | [requirements-dev.txt](requirements-dev.txt), [README, sección 8](README.md) |

El dilema más importante fue la entrevista. Cuando cambié el proyecto final de VetCare Pro a A-Fénix ya no tenía una entrevista con el restaurante, y la forma más rápida de seguir era que la IA inventara las respuestas a partir de la entrevista que había hecho para la veterinaria. Lo hice, pero no podía presentar esas citas como si las hubiera dicho el restaurante, porque todo el documento de requisitos se apoya en que las necesidades salen del cliente. Lo resolví declarándolo en tres partes del documento: la introducción, el anexo y la sección de uso de IA dicen que la entrevista es simulada y adaptada con IA, y que las necesidades se deben validar con el restaurante antes de construir. Así el documento sirve para el curso sin engañar a nadie que lo lea.

## 7. Aprendizajes

Ahora sé escribir el contrato y las pruebas antes de pedirle código a la IA, y eso me obliga a decidir qué tiene que hacer la función antes de verla. También aprendí que una prueba en verde no prueba nada por sí sola: hay que meter errores a propósito para saber si la prueba los ve. Al principio confié de más en la IA en dos cosas: en que sus requisitos y su diseño salían del cliente, cuando muchas veces salían de otros sistemas, y en sus pruebas, que parecían completas pero no revisaban lo importante. Lo que haría distinto es hacer la entrevista real con el restaurante desde el comienzo y pedirle a la IA una sola cosa a la vez, porque cuando le pedí mucho junto se adelantó y metió una API y campos que nadie había pedido.

## 8. Anexos

Todo está en el repositorio. La bitácora de uso de IA está en [bitacora_ia.md](bitacora_ia.md). Los documentos de los módulos 1 a 3 están en [docs/modulos](docs/modulos): la [propuesta](docs/modulos/S2_Propuesta.pdf), los [requisitos con la entrevista](docs/modulos/S3_Requisitos.pdf) y el [diseño con los diagramas C4, el ADR, el modelo y la API](docs/modulos/S4_Diseno.pdf). El código y la revisión de seguridad del módulo 4 están en el [README](README.md) y en [revision_seguridad.md](revision_seguridad.md). Las pruebas del módulo 5 están en [registro_pruebas.md](registro_pruebas.md), con sus evidencias en [evidencias/semana-7](evidencias/semana-7) y el reporte de defecto [D-01](docs/defectos/D-01.md). El pipeline del módulo 6 está en [ci.yml](.github/workflows/ci.yml) y su revisión en [revision_configuracion.md](docs/revision_configuracion.md). Cada semana se trabajó en su rama (`semana-5`, `semana-6`, `semana-7` y `entrega-final`) y todas quedaron unidas en `main`.
