# Informe final del proyecto integrador

Proyecto: A-Fénix, plataforma de comandas digitales para el restaurante chino A Fénix de Oro\
Estudiante: Eduardo Ascencio · Ingeniería de Software · Fundación Escuela Tecnológica de Neiva - FET\
Repositorio: https://github.com/Darkandligh/Seminario\
Fecha: 2026-11-26

## 1. Resumen

En A Fénix de Oro el mesero anota los pedidos en una libreta y lleva la hoja a la cocina. A veces la cocina no entiende la letra o se pierde una hoja, y el plato sale mal o tarde. A-Fénix reemplaza la hoja: el mesero registra la comanda en una tablet con la base, la proteína, el tamaño y el picante de cada plato, y la cocina la ve en una pantalla en orden de llegada y marca cuándo está lista. Usé IA en las seis fases: para la propuesta, los requisitos, el diseño, el código, las pruebas y el pipeline. El resultado principal de la verificación es que la IA se equivocó en todas las fases, sobre todo inventando cosas que nadie pidió, y que la mayoría de esos errores solo aparecieron al compararlos con los requisitos o al romper el código a propósito. Hoy el proyecto tiene 81 pruebas con 100 % de cobertura de la lógica del negocio y un pipeline que las corre en cada cambio.

## 2. Problema y usuario

Los usuarios son los 3 meseros y los 2 cocineros del restaurante. Hoy el mesero anota la mesa y los platos en una libreta, pregunta por cada plato si va con arroz frito o chop suey, de pollo, cerdo o res, personal o familiar, y si es picante, y lleva la hoja a la cocina. El cocinero saca las hojas en el orden en que llegan y canta la mesa cuando el plato está listo; si el mesero no lo oye, tiene que ir a preguntar. En la hora del almuerzo salen unas 60 comandas, y lo que más preocupa a la administradora es que el sistema se caiga en plena hora pico.

Lo que necesitan es que el pedido llegue a la cocina completo y legible, en orden, y que el salón sepa cuándo está listo.

Evidencia: [propuesta del módulo 1](docs/modulos/S2_Propuesta.pdf) y [documento de requisitos con la entrevista del módulo 2](docs/modulos/S3_Requisitos.pdf), anexo A. La entrevista es simulada; lo explico en la sección 6.

## 3. La IA en el ciclo de vida

| Módulo y fase | Qué hice con IA | Herramienta | Evidencia | Cómo verifiqué |
|---|---|---|---|---|
| 1. Fundamentos | Ordenar la propuesta: problema, fase donde aplicar IA (pruebas) y meta medible | Claude (chat) | [S2_Propuesta.pdf](docs/modulos/S2_Propuesta.pdf) | La idea y la meta son mías; revisé que la meta se pudiera medir (cobertura y errores a propósito) |
| 2. Requisitos | Adaptar la entrevista, pasar las respuestas a 11 necesidades con cita, 8 historias con escenarios Gherkin, 3 RNF y la matriz de trazabilidad | Claude (chat) | [S3_Requisitos.pdf](docs/modulos/S3_Requisitos.pdf) | Cada necesidad tiene su cita y cada historia su necesidad de origen. Lo que no tenía cita pasó a preguntas pendientes |
| 3. Diseño | Tres alternativas de arquitectura, diagramas C4, modelo de datos y API, y una revisión de coherencia | Claude (chat) | [S4_Diseno.pdf](docs/modulos/S4_Diseno.pdf) | Matriz ponderada con mis pesos; cada caja, entidad y ruta contra una historia (5 fichas de prompt) |
| 4. Código | `registrar_comanda` con pruebas primero (rojo, verde, refactor). Revisión de seguridad con ruff, bandit, mypy, pip-audit y dos revisiones con IA | Claude (chat) y Claude Code en VS Code (agente) | [README](README.md), [revision_seguridad.md](revision_seguridad.md) | 22 pruebas escritas antes del código; 17 pruebas de abuso en rojo antes de corregir; diff del agente revisado |
| 5. Pruebas | Tabla de casos con particiones, límites y tabla de decisión; borrador de pruebas de la IA revisado; datos sintéticos; 11 errores metidos a propósito; reporte de defecto | Claude Code en VS Code | [registro_pruebas.md](registro_pruebas.md), [evidencias/semana-7](evidencias/semana-7), [D-01](docs/defectos/D-01.md) | Cada esperado sale de una historia, no del código. Corrí el borrador de la IA contra los 11 errores |
| 6. Operación | Pipeline de GitHub Actions generado con IA y revisado con la lista de la semana 9 | Claude (chat) | [ci.yml](.github/workflows/ci.yml), [revision_configuracion.md](docs/revision_configuracion.md) | Ejecución en verde, error a propósito en rojo y otra vez en verde |

Todas las decisiones con IA están en la [bitácora](bitacora_ia.md): 23 entradas, 13 aceptadas, 6 aceptadas con cambios y 4 rechazadas.

## 4. Verificación: lo que la IA hizo mal y cómo lo encontré

### Caso 1: requisitos que el cliente nunca pidió

- **Fase:** requisitos.
- **Qué propuso la IA:** en la semana 3, cuando mi proyecto todavía era VetCare Pro, la IA armó el documento de requisitos antes de que yo hiciera la entrevista, con respuestas supuestas del cliente: inventario de medicamentos, un rol de recepcionista, facturación y fallas de internet. Cuando pasé el proyecto a A-Fénix volvió a pasar algo parecido: al adaptar la entrevista al restaurante, dejó cosas que solo tienen sentido en una veterinaria, como el carnet de vacunación o que los clientes usaran el sistema.
- **Qué estaba mal:** eran requisitos que el cliente nunca dijo, aunque se veían razonables.
- **Cómo lo detecté:** comparé cada necesidad con las respuestas de la entrevista; las que no tenían una cita no tenían de dónde salir.
- **Qué hice:** descarté el borrador y armé el documento solo con necesidades que tienen su cita, y cada historia con su necesidad de origen. En A-Fénix quité lo que no aplicaba a un restaurante ([S3, sección 7](docs/modulos/S3_Requisitos.pdf)).

### Caso 2: un tope de seguridad que no protegía nada

- **Fase:** código.
- **Qué propuso la IA:** en la revisión de seguridad el agente puso un tope de 50 platos por comanda (H-03), comparando el número de filas de la lista.
- **Qué estaba mal:** cada fila tiene su cantidad, así que 50 filas de cantidad 20 eran 1000 platos. El tope se saltaba repartiendo los platos en filas.
- **Cómo lo detecté:** en la segunda revisión, con el prompt de la semana que pide separar problemas seguros de sospechas y comprobar cada uno llamando la función. Con 3 filas de 20 la comanda quedó «recibido» con 60 platos.
- **Qué hice:** primero escribí la prueba de abuso en rojo ([3556eef](https://github.com/Darkandligh/Seminario/commit/3556eef)) y después la corrección, que suma las cantidades ([affc4b8](https://github.com/Darkandligh/Seminario/commit/affc4b8)). Quedó como H-05 en el informe de seguridad y como el defecto [D-01](docs/defectos/D-01.md).

### Caso 3: pruebas que pasaban aunque el código estuviera mal

- **Fase:** pruebas.
- **Qué propuso la IA:** un borrador de pruebas para el cambio de estado y la pantalla de cocina. Incluía `assert len(resultado) == 3` para revisar el orden de la pantalla, `assert c.hora_listo is not None` para la hora de entrega y una prueba de que un «admin» puede cambiar el estado.
- **Qué estaba mal:** las dos primeras son débiles: pasan con el orden al revés y con cualquier hora. La tercera es una regla inventada: A-Fénix no tiene rol de administrador y HU-07 dice que solo la cocina cambia el estado.
- **Cómo lo detecté:** la del admin falló y revisé HU-07 antes de tocar el código. Para las débiles metí 11 errores a propósito: el borrador no habría detectado 7.
- **Qué hice:** descarté o corregí 11 pruebas del borrador y agregué las que faltaban. La suite revisada atrapó 10 de los 11 errores; el que se escapó (una modificación vacía marcada como «fuera de carta») me llevó a agregar una prueba del tipo exacto de la excepción ([registro_pruebas.md, secciones 2 y 3](registro_pruebas.md), commit [911442f](https://github.com/Darkandligh/Seminario/commit/911442f)).

### Caso 4: un pipeline que parecía bien

- **Fase:** operación.
- **Qué propuso la IA:** un workflow que corre `pytest` en cada push a `main`, con Python «3.x» y `pip install pytest` sin versión ([borrador](evidencias/semana-9/ci_borrador_ia.yml)).
- **Qué estaba mal:** no revisaba las ramas por semana donde trabajo, no limitaba los permisos, usaba versiones que cambian solas y solo corría las pruebas. actionlint no marcó nada, porque el archivo es válido.
- **Cómo lo detecté:** con la lista de revisión de la semana 9, línea por línea.
- **Qué hice:** corregí los 6 problemas ([revision_configuracion.md](docs/revision_configuracion.md)) y comprobé que un error a propósito lo pone en rojo.

## 5. Estado final del sistema

- **Arquitectura:** monolito web en Python con FastAPI y SQLite, instalado en un mini PC del restaurante y sin depender de internet, con la pantalla de cocina conectada por cable. Ganó la matriz ponderada con 103 puntos contra 69 de la nube y 65 de microservicios. Ver el [documento de diseño y el ADR-001](docs/modulos/S4_Diseno.pdf).
- **Funcionalidades terminadas (lógica del negocio):**

| Historia | Prioridad | Estado |
|---|---|---|
| HU-01 Registrar la comanda | Must | Terminada (`afenix/comandas.py`) |
| HU-02 Modificaciones desde la carta | Must | Terminada |
| HU-03 La comanda llega a la cocina al enviarla | Must | Pendiente: necesita la API y el WebSocket |
| HU-04 Cocina ordenada por hora de entrada | Must | Terminada (`afenix/cocina.py`) |
| HU-05 Tiempo de espera | Should | Terminada (`afenix/cocina.py`) |
| HU-06 Cambio de estado paso a paso | Should | Terminada (`afenix/estados.py`) |
| HU-07 Solo la cocina cambia el estado | Should | Terminada, con prueba de abuso del rol |
| HU-08 El mesero consulta el estado de una mesa | Could | Pendiente |

- **Pruebas:** 81 pruebas (normales, de límite, de error y de abuso) con 100 % de cobertura de `afenix/`. El pipeline también corre ruff, mypy, bandit y pip-audit. [Última ejecución del pipeline](https://github.com/Darkandligh/Seminario/actions).
- **Pendientes:** la API con FastAPI, SQLite y las pantallas no alcanzaron: el seminario se centró en la lógica y su verificación, y preferí terminar bien 6 historias que dejar 8 a medias. También quedan las preguntas al restaurante: cuántas mesas tiene (P-03), si los topes de 50 platos y 20 por plato sirven (P-01) y si un pedido marcado listo por error se puede devolver (P-06).

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

- Bitácora de uso de IA: [bitacora_ia.md](bitacora_ia.md)
- Módulo 1, propuesta: [docs/modulos/S2_Propuesta.pdf](docs/modulos/S2_Propuesta.pdf)
- Módulo 2, requisitos y entrevista: [docs/modulos/S3_Requisitos.pdf](docs/modulos/S3_Requisitos.pdf)
- Módulo 3, diseño, C4, ADR, modelo y API: [docs/modulos/S4_Diseno.pdf](docs/modulos/S4_Diseno.pdf)
- Módulo 4, código y revisión de seguridad: [README.md](README.md), [revision_seguridad.md](revision_seguridad.md)
- Módulo 5, pruebas: [registro_pruebas.md](registro_pruebas.md), [evidencias/semana-7](evidencias/semana-7), [docs/defectos/D-01.md](docs/defectos/D-01.md)
- Módulo 6, operación: [.github/workflows/ci.yml](.github/workflows/ci.yml), [docs/revision_configuracion.md](docs/revision_configuracion.md)
- Ramas por semana: `semana-5`, `semana-6`, `semana-7` y `semana-9`, unidas en `main`
