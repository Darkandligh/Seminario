# Revisión de seguridad. Semana 6

Proyecto: A-Fénix
Estudiante: Eduardo Ascencio
Código revisado: `afenix/comandas.py` y `afenix/carta.py` (HU-01 y HU-02, la funcionalidad de la semana 5)
Rama: `semana-6`
Fecha: 2026-11-23 (segunda revisión con IA: 2026-11-26)
Commit revisado: 7f1f11d (la semana 5, antes de las correcciones)

## 1. Herramientas y criterios

| Herramienta | Versión | Para qué | Configuración |
|---|---|---|---|
| ruff | 0.17.6 | Estilo, errores comunes y reglas de seguridad (`S`, las mismas de bandit) | `pyproject.toml`, reglas E, W, F, I, B, UP, S, SIM, RUF; líneas de 100 |
| bandit | 1.9.4 | Análisis estático de seguridad | `pyproject.toml`, revisa `afenix/` |
| mypy | 2.4.1 | Tipos, en modo `strict` | `pyproject.toml` |
| pip-audit | 2.10.1 | Vulnerabilidades conocidas en las dependencias | `requirements.txt` y `requirements-dev.txt` |
| pytest | 9.0.3 | Pruebas de abuso en `tests/test_abuso_comandas.py` | `pytest.ini` |

Resultados antes y después:

| Herramienta | Antes | Después |
|---|---|---|
| ruff | 2 avisos (E501 en las pruebas de la semana 5) | 2 avisos (los mismos, ver abajo) |
| bandit | 0 hallazgos | 0 hallazgos |
| mypy | 6 errores (funciones sin tipos) | 0 errores |
| pip-audit | 1 vulnerabilidad (pytest 8.3.4) | 0 vulnerabilidades |
| pruebas de abuso | 13 de 15 fallan; en la segunda revisión, 1 de 2 nuevas | 17 de 17 pasan |

Puntos de seguridad revisados:

| Punto | Qué revisé | Resultado |
|---|---|---|
| Inyección | Si algún dato del mesero llega a una consulta, a un comando o a un HTML | No hay base de datos ni HTML todavía. El único lugar donde vuelve un dato del cliente es el mensaje de error del plato que no está en la carta (H-04). |
| Secretos en el código | Busqué claves, contraseñas y tokens en el código | No hay. `.env` está en `.gitignore` y quedó `.env.example` sin valores. |
| Secretos en el historial | `git log -p --all` buscando password, secret, token, api_key, contraseña y sk- | Nada en ninguna rama. |
| Contraseñas con scrypt, bcrypt o argon2 | Si se guardan contraseñas | No aplica todavía: no hay usuarios. El inicio de sesión (`POST /api/sesiones`) está diseñado pero no hecho. Cuando se haga, las contraseñas se guardan con argon2 o bcrypt. |
| Control de acceso por rol | Que solo la cocina cambie estados (HU-07) | No aplica todavía: `registrar_comanda` no tiene roles y el cambio de estado no existe. La prueba de abuso del rol (un mesero intenta cambiar el estado y recibe 403) se escribe cuando se haga HU-07. |
| Datos de entrada | Tipos equivocados, tamaños y límites | Tres hallazgos: H-02, H-03 y H-04. |
| Dependencias | Versiones fijadas y `pip-audit` | Todas las versiones van con `==`. Un hallazgo: H-01. |

## 2. Hallazgos

| Id | Archivo y línea | Problema | Categoría OWASP 2025 | Severidad | Corrección | Commit |
|---|---|---|---|---|---|---|
| H-01 | `requirements.txt:1` | pytest 8.3.4 tiene la vulnerabilidad PYSEC-2026-1845: en Unix usa carpetas `/tmp/pytest-of-{usuario}` que otro usuario del equipo puede usar para tumbar las pruebas o subir privilegios. | A03 Fallas en la cadena de suministro de software | Baja (solo se usa al correr pruebas) | Subí pytest a 9.0.3 y pytest-cov a 7.1.0. | 1f7a23a |
| H-02 | `afenix/comandas.py:70` y `:110` | Si los platos no venían en lista, si un plato no era diccionario o si el nombre no era texto, la función reventaba con `AttributeError` o `TypeError` en vez de `ComandaInvalida`. Cuando esté la API, eso es un error 500 que muestra detalles internos en lugar de un 400. | A10 Manejo incorrecto de condiciones excepcionales | Media | Reviso el formato antes de validar y lanzo `ComandaInvalida` con «La comanda tiene un formato incorrecto». | d761de7 |
| H-03 | `afenix/comandas.py:88` y `:112` | No había tope: se aceptaba una cantidad de mil millones y una comanda de 10 000 platos. Con una sola petición se llena la pantalla de la cocina y la memoria del mini PC. | A06 Diseño inseguro | Media | Tope de 50 platos por comanda y 20 por plato. Son provisionales hasta confirmar con el restaurante (P-01). | 06f1eb1 |
| H-04 | `afenix/comandas.py:75` | El mensaje «El plato «...» no está en la carta» repetía el nombre completo que mandó el cliente, así fueran 5 000 caracteres o un `<script>`. Si la tablet pinta el mensaje sin escapar, es una puerta a XSS. | A05 Inyección | Baja | Recorto el nombre a 40 caracteres en el mensaje. Escapar el HTML le toca a la pantalla cuando exista. | c22890f |
| H-05 | `afenix/comandas.py:112` | El tope de H-03 contaba filas, no platos: una comanda de 50 filas con cantidad 20 pasaba con 1000 platos, así que el tope no servía. | A06 Diseño inseguro | Media | El tope de 50 ahora suma las cantidades. Prueba de abuso nueva con 3 filas de 20. | 3556eef (prueba en rojo), affc4b8 |
| H-06 | `README.md`, contrato de la función | La firma del contrato no tenía tipos, aunque el código ya los tiene. | Documentación | Baja | Firma con tipos en el README. | 872e714 (rama semana-5) y 69f0f40 |

Avisos del linter que no corregí:

| Aviso | Dónde | Por qué no lo corregí |
|---|---|---|
| E501 línea de 114 caracteres | `tests/test_registrar_comanda.py:36` | Es una prueba de la semana 5 y esas pruebas no se modifican. No es un problema de seguridad. |
| E501 línea de 101 caracteres | `tests/test_registrar_comanda.py:39` | La misma razón. |

## 3. Revisión con IA

Herramienta: Claude Code (Claude Opus 5.5), dentro de VS Code.

Prompt usado (le pedí a Claude Code que siguiera con la semana 6; la revisión del código la hizo con este criterio):

> «Revisa afenix/comandas.py como si fuera a recibir los datos directo de la API, sin confiar en la tablet. Busca entradas que hagan fallar la función con un error que no sea ComandaInvalida, valores sin límite y datos del cliente que vuelvan en los mensajes. Comprueba cada cosa corriendo la función, no solo leyendo el código.»

Lo que encontró la IA:

| Hallazgo de la IA | ¿Real? | Cómo lo verifiqué |
|---|---|---|
| Platos en texto, en diccionario o en número revientan con `AttributeError` o `TypeError` | Real (H-02) | Llamé la función con esos datos y salió el error de Python. Quedó en las pruebas de abuso. |
| Un plato `None` o en lista dentro de la lista revienta | Real (H-02) | Igual que el anterior. |
| Un nombre de plato en lista da `TypeError: unhashable type` | Real (H-02) | Igual que el anterior. |
| Cantidad y número de platos sin tope | Real (H-03) | Pasaron una cantidad de 10⁹ y una comanda de 10 000 platos. |
| El mensaje de error repite el nombre completo del plato | Real (H-04) | Mandé un nombre de 5 000 caracteres con `<script>` y volvió entero. |
| Una base o proteína en lista o en diccionario podría colarse | Falso positivo | La probé y sale `FueraDeCarta` como debe ser, porque el valor no está en la lista de la carta. |
| El parámetro `ahora` acepta cualquier cosa | Falso positivo por ahora | Es cierto, pero `ahora` no viene del cliente: lo usan las pruebas, y en la API guardada en `_guardado/api.py` no se pasa. Si algún día viene de afuera, hay que validarlo. |
| La mesa no tiene tope (se acepta la mesa 10³⁰) | Real, pero no lo corregí | Lo probé y la acepta. No le puse tope porque no sé cuántas mesas hay (P-03). Quedó en pendientes. |
| pytest 8.3.4 vulnerable | Real (H-01) | Lo dio `pip-audit` y lo confirmé con la descripción de PYSEC-2026-1845. |

Lo que la primera revisión no encontró: puso el tope de 50 platos (H-03), pero contando filas y no unidades. Con 50 filas de cantidad 20 entraban 1000 platos y el tope no protegía nada. Se vio en la segunda revisión, al llamar la función con esa comanda (H-05). Tampoco revisó control de acceso, contraseñas ni inyección en base de datos, porque nada de eso existe todavía en el código; eso queda en pendientes.

### Segunda revisión con IA (prompt de la semana)

Herramienta: Claude (claude.ai), en el chat. Fecha: 2026-11-26.

> «Actúa como revisor de código y de seguridad. Revisa afenix/comandas.py y afenix/carta.py de la rama semana-6 con estos criterios: corrección y pruebas, diseño y legibilidad, y seguridad (inyección, secretos, contraseñas, control de acceso, dependencias y validación de entradas). Entrega una tabla con archivo y línea, problema y severidad (alta, media o baja), y separa los problemas seguros de las sospechas. Comprueba cada problema seguro llamando la función.»

| Hallazgo de la IA | Tipo | ¿Real o falso positivo? | Cómo lo verifiqué |
|---|---|---|---|
| `comandas.py:112`: el tope de 50 cuenta filas, no platos | Seguro, media | Real (H-05) | 50 filas de cantidad 20 se aceptaron: 1000 platos en una comanda. |
| `README.md`: la firma del contrato no tiene tipos | Seguro, baja | Real (H-06) | Comparé el README con la firma de `registrar_comanda` en el código. |
| `comandas.py:106`: la mesa no tiene tope | Seguro, baja | Real, sin corregir | La mesa 10³⁰ se aceptó. Falta saber cuántas mesas hay (P-03). |
| `comandas.py:108`: si los platos llegan como `0` o `""`, el mensaje dice «al menos un plato» y no «formato incorrecto» | Sospecha | Falso positivo | Igual lanza `ComandaInvalida` y no revienta. El mensaje no es exacto, pero no es un problema. |
| `comandas.py:116`: la hora de entrada no tiene zona horaria | Sospecha | Falso positivo | Todo corre en un solo equipo del restaurante (ADR-001), así que todas las horas son de la misma zona. |
| `comandas.py:57`: `_es_entero_positivo` no tiene docstring | Seguro, baja | Real, sin corregir | Es una función auxiliar privada y tiene un comentario que explica el caso de `True`. Las funciones principales sí tienen docstring. |

## 4. Pendientes

- Tope de mesas cuando el restaurante diga cuántas tiene (P-03).
- Confirmar los topes de 50 platos y 20 por plato (P-01).
- Escapar el HTML en la tablet y en la pantalla de cocina cuando se hagan.
- Control de acceso por rol con su prueba de abuso cuando se haga HU-07 (un mesero que intenta cambiar el estado debe recibir 403).
- Guardar las contraseñas con argon2 o bcrypt cuando se haga el inicio de sesión.
- Volver a correr `pip-audit` cuando se agreguen FastAPI y las demás dependencias.

Claves expuestas: ninguna. Revisé el código y todo el historial de Git y no hay claves, contraseñas ni tokens.
