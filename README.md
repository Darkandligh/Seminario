# A-Fénix

Plataforma de comandas digitales para el restaurante chino A Fénix de Oro, en Neiva.

## 1. Qué es

Con A-Fénix el mesero registra la comanda en una tablet y la cocina la recibe en una pantalla en orden de llegada. El diseño completo está en mis documentos de requisitos y de diseño: Python con FastAPI y SQLite en un mini PC del restaurante (ADR-001). En este repositorio voy construyendo el proyecto por semanas, empezando por la lógica de negocio. Por ahora no hay API ni base de datos: las comandas viven en memoria.

Funciones con reglas de negocio:

| Archivo | Función | Historia |
|---|---|---|
| `afenix/comandas.py` | `registrar_comanda` | HU-01 y HU-02 (contrato abajo) |
| `afenix/estados.py` | `cambiar_estado`: recibido → en preparación → listo, un paso a la vez; solo la cocina | HU-06 y HU-07 |
| `afenix/cocina.py` | `minutos_espera`: minutos desde la hora de entrada | HU-05 |
| `afenix/cocina.py` | `comandas_para_cocina`: pendientes por hora de entrada | HU-04 |

Las reglas y la tabla de casos de cada una están en [`registro_pruebas.md`](registro_pruebas.md).

### Historias de usuario

**HU-01. Registrar la comanda** (prioridad Must, necesidades N-01 y N-03)

Como mesero, quiero registrar la comanda de una mesa con los platos de la carta para que la cocina sepa qué preparar.

- **Escenario 1 (comanda registrada):** dado que la mesa 4 no tiene comandas abiertas, cuando registro «Arroz frito con piña» y «Chop suey», entonces la comanda queda en estado «recibido» con la mesa 4, los dos platos y la hora de entrada.
- **Escenario 2 (error: comanda sin platos):** dado que estoy registrando la comanda de la mesa 4, cuando intento enviarla sin ningún plato, entonces el sistema no la guarda y muestra «La comanda debe tener al menos un plato».

**HU-02. Plato y color** (prioridad Must, necesidades N-01 y N-03, versión 3 de los requisitos)

Como mesero, quiero elegir el plato y su color desde la carta para que el pedido llegue a la cocina tal como lo pidió el cliente.

- **Escenario 1 (plato con color):** dado que la carta tiene «Chop suey» en color café, cuando lo elijo para la mesa 4, entonces el plato queda en el pedido con el color café.
- **Escenario 2 (error: color que no existe):** dado que el plato no se prepara en un color, cuando intento pedirlo en ese color, entonces el sistema no lo agrega y muestra «El color no está en la carta».

Hasta el 26 de noviembre esta historia pedía base, proteína, tamaño y picante, porque salió de una entrevista simulada. La entrevista real mostró que el cliente solo dice el plato y el color («dame un chop suey café»), y la historia, el código y las pruebas se cambiaron.

### Contrato de la función

Archivo: `afenix/comandas.py`

```python
def registrar_comanda(
    mesa: int,
    items: list[dict[str, str | int]],
    ahora: datetime | None = None,
) -> Comanda
```

**Qué recibe:**

- `mesa`: número entero de la mesa.
- `items`: lista de platos. Cada plato es un diccionario con `plato`, `color` y, si se quiere, `cantidad`.
- `ahora`: hora de entrada. Si no se manda, se usa la hora del equipo. Sirve para que las pruebas no dependan del reloj.

**Qué devuelve:** un objeto `Comanda` con `mesa`, `platos` (lista de `Plato` con sus cuatro modificaciones y la cantidad), `hora_entrada` y `estado = "recibido"`.

**Qué lanza:**

| Excepción | Mensaje | Cuándo |
|---|---|---|
| `ComandaInvalida` | «La mesa debe ser un número mayor que cero» | La mesa es 0, negativa, texto, `None` o `True`. |
| `ComandaInvalida` | «El restaurante tiene 12 mesas» | La mesa es mayor que 12. Sale de la entrevista real (P-03). |
| `ComandaInvalida` | «La comanda debe tener al menos un plato» | La lista de platos está vacía o es `None`. |
| `ComandaInvalida` | «La comanda tiene un formato incorrecto» | Los platos no vienen en lista, un plato no es diccionario o su nombre no es texto. |
| `ComandaInvalida` | «Una comanda tiene máximo 50 platos» | Vienen más de 50 platos, contando las cantidades: 3 filas de 20 son 60. |
| `ComandaInvalida` | «Falta el color de «Chop suey»» | El color viene vacío o no viene. |
| `ComandaInvalida` | «La cantidad debe ser un número mayor que cero» | La cantidad es 0, negativa o texto. |
| `ComandaInvalida` | «La cantidad máxima por plato es 20» | La cantidad pasa de 20. |
| `FueraDeCarta` | «El plato «...» no está en la carta» | El plato no existe en la carta. El nombre se recorta a 40 caracteres. |
| `FueraDeCarta` | «El color no está en la carta» | El plato no se prepara en ese color. |

`FueraDeCarta` hereda de `ComandaInvalida`. Las separé para que más adelante la API pueda responder 400 a lo que está incompleto y 422 a lo que no existe en la carta, como dice la tabla de la API del documento de diseño.

**Supuestos:**

- Si un plato está mal se rechaza toda la comanda, para que nada incompleto llegue a la cocina.
- Las cuatro modificaciones son obligatorias en cada plato.
- La cantidad es 1 si no se manda.
- Los topes de 50 platos y 20 por plato son provisionales hasta confirmarlos con el restaurante (P-01).
- La mesa solo tiene que ser un entero mayor que cero. Cuántas mesas tiene el restaurante está pendiente (P-03).
- La carta de `afenix/carta.py` es de ejemplo. La real la tiene que validar el restaurante.

**Casos límite:**

- Mesa 1: se acepta. Mesa 0: error.
- Un solo plato: se acepta. Ningún plato: error. 50 platos: se acepta. 51: error.
- Cantidad 20: se acepta. Cantidad 0 o 21: error.
- `True` como mesa: error. En Python `True` es un entero que vale 1, así que hubo que descartarlo aparte.

**Ejemplos:**

| Entrada | Salida |
|---|---|
| `registrar_comanda(4, [{"plato": "Chop suey", "color": "café"}])` | `Comanda(mesa=4, platos=[Plato("Chop suey", "café", 1)], estado="recibido")` |
| `registrar_comanda(4, [])` | lanza `ComandaInvalida`: «La comanda debe tener al menos un plato» |
| `registrar_comanda(4, [{"plato": "Chop suey", "color": "verde"}])` | lanza `FueraDeCarta`: «El color no está en la carta» |
| `registrar_comanda(0, [...])` | lanza `ComandaInvalida`: «La mesa debe ser un número mayor que cero» |

## 2. Requisitos

- Python 3.12 o más reciente.
- Las dependencias van con versión fijada en `requirements.txt` (pruebas) y `requirements-dev.txt` (linter y auditoría).

## 3. Instalación

```bash
python -m venv .venv
source .venv/bin/activate        # en Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
```

Si solo vas a correr las pruebas basta con `pip install -r requirements.txt`. Por ahora la aplicación no usa variables de entorno; `.env.example` queda como plantilla.

## 4. Ejecución

Todavía no hay servidor. La función se usa desde Python:

```python
from afenix.comandas import registrar_comanda

registrar_comanda(4, [{"plato": "Chop suey", "color": "café"}])
```

## 5. Pruebas

```bash
python -m pytest -v
python -m pytest --cov=afenix
```

Salen 93 pruebas que pasan, con 100 % de cobertura: las 20 de la semana 5 (`tests/test_registrar_comanda.py`, adaptadas a plato y color), las 17 de abuso de la semana 6 (`tests/test_abuso_comandas.py`), 42 de la semana 7 (`test_estados.py`, `test_cocina.py` y `test_comandas_datos.py`, con los datos sintéticos de `tests/conftest.py`) , 12 de aceptación, una por escenario de las historias (`tests/test_aceptacion.py`), y 2 de la entrevista real (`tests/test_entrevista_real.py`). Además hay 3 pruebas de aceptación marcadas `xfail`: son diferencias reales entre el criterio y el código, explicadas en la evaluación de historias del informe final.

Las mismas pruebas, el linter, mypy, bandit y pip-audit corren solos en GitHub Actions cada vez que se sube un cambio (`.github/workflows/ci.yml`). La revisión de ese pipeline está en [`docs/revision_configuracion.md`](docs/revision_configuracion.md).

Análisis estático y auditoría de dependencias:

```bash
ruff check afenix tests
bandit -c pyproject.toml -r afenix
mypy
pip-audit -r requirements-dev.txt
```

El resultado de cada uno está en [`revision_seguridad.md`](revision_seguridad.md).

## 6. Estructura

```
afenix/carta.py              carta de ejemplo con los platos y sus opciones
afenix/comandas.py           la función registrar_comanda
afenix/estados.py            cambio de estado de la comanda
afenix/cocina.py             tiempo de espera y lista de la pantalla de cocina
tests/                       pruebas normales, de límite, de error, de abuso y de aceptación
docs/ciclo_vida.png          diagrama del ciclo de vida con IA
tests/conftest.py            datos sintéticos de un turno de almuerzo
evidencias/semana-7/         borrador de pruebas de la IA y salidas de pytest
evidencias/entrega-final/         borrador del pipeline que generó la IA
.github/workflows/ci.yml     pipeline de integración continua
docs/modulos/                propuesta, requisitos y diseño (módulos 1 a 3)
docs/revision_configuracion.md  revisión del pipeline
docs/defectos/D-01.md        reporte de defecto
pyproject.toml               configuración de ruff, bandit y mypy
requirements.txt             dependencias para las pruebas
requirements-dev.txt         dependencias del linter y la auditoría
bitacora_ia.md               registro de lo que sugirió la IA y qué decidí
revision_seguridad.md        informe de seguridad de la semana 6
registro_pruebas.md          tabla de casos, revisión de las pruebas de la IA y mutaciones
```

## 7. Uso de IA

Usé un asistente de IA para escribir las pruebas, la implementación y la revisión de seguridad. Lo que sugirió, lo que acepté o rechacé y cómo lo verifiqué está en [`bitacora_ia.md`](bitacora_ia.md). La revisión de seguridad con IA está en la sección 3 de [`revision_seguridad.md`](revision_seguridad.md).

## 8. Autor y licencia

Eduardo Ascencio, Ingeniería de Software, Fundación Escuela Tecnológica de Neiva - FET.
Proyecto final del Seminario de Inteligencia Artificial Aplicada al Ciclo de Vida del Software.

Uso académico. Sin licencia de código abierto por ahora.
