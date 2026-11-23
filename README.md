# A-Fénix

Plataforma de comandas digitales para el restaurante chino A Fénix de Oro.

Proyecto final del Seminario de Inteligencia Artificial Aplicada al Ciclo de Vida del Software (FET).
Eduardo Ascencio, Ingeniería de Software, Fundación Escuela Tecnológica de Neiva - FET.

Con A-Fénix el mesero registra la comanda en una tablet y la cocina la recibe en una pantalla en orden de llegada. El diseño completo está en mis documentos de requisitos y de diseño: Python con FastAPI y SQLite en un mini PC del restaurante (ADR-001). En este repositorio voy construyendo el proyecto por semanas, empezando por la lógica de negocio. Por ahora no hay API ni base de datos: las comandas viven en memoria.

## Funcionalidad de la semana 5

### Historias de usuario

**HU-01. Registrar la comanda** (prioridad Must, necesidades N-01 y N-03)

Como mesero, quiero registrar la comanda de una mesa con los platos de la carta para que la cocina sepa qué preparar.

- **Escenario 1 (comanda registrada):** dado que la mesa 4 no tiene comandas abiertas, cuando registro «Arroz frito con piña» y «Chop suey», entonces la comanda queda en estado «recibido» con la mesa 4, los dos platos y la hora de entrada.
- **Escenario 2 (error: comanda sin platos):** dado que estoy registrando la comanda de la mesa 4, cuando intento enviarla sin ningún plato, entonces el sistema no la guarda y muestra «La comanda debe tener al menos un plato».

**HU-02. Modificaciones de cada plato** (prioridad Must, necesidades N-02 y N-03)

Como mesero, quiero elegir la base, la proteína, el tamaño y el picante de cada plato desde la carta para que el pedido llegue a la cocina tal como lo pidió el cliente.

- **Escenario 1 (plato con modificaciones):** dado que la carta tiene «Pollo General Tso's» con base arroz frito, tamaño familiar y picante medio, cuando los elijo para la mesa 4, entonces el plato queda en la comanda con esas cuatro modificaciones.
- **Escenario 2 (error: opción fuera de la carta):** dado que la carta no tiene camarón como proteína del chop suey, cuando intento agregar «Chop suey» de camarón, entonces el sistema no lo agrega y muestra «La proteína no está en la carta».

### Contrato de la función

Archivo: `afenix/comandas.py`

```python
def registrar_comanda(mesa, items, ahora=None) -> Comanda
```

**Qué recibe:**

- `mesa`: número entero de la mesa.
- `items`: lista de platos. Cada plato es un diccionario con `plato`, `base`, `proteina`, `tamano`, `picante` y, si se quiere, `cantidad`.
- `ahora`: hora de entrada. Si no se manda, se usa la hora del equipo. Sirve para que las pruebas no dependan del reloj.

**Qué devuelve:** un objeto `Comanda` con `mesa`, `platos` (lista de `Plato` con sus cuatro modificaciones y la cantidad), `hora_entrada` y `estado = "recibido"`.

**Qué lanza:**

| Excepción | Mensaje | Cuándo |
|---|---|---|
| `ComandaInvalida` | «La mesa debe ser un número mayor que cero» | La mesa es 0, negativa, texto, `None` o `True`. |
| `ComandaInvalida` | «La comanda debe tener al menos un plato» | La lista de platos está vacía o es `None`. |
| `ComandaInvalida` | «Falta la base de «Chop suey»» (y así con cada modificación) | Una modificación viene vacía. |
| `ComandaInvalida` | «La cantidad debe ser un número mayor que cero» | La cantidad es 0, negativa o texto. |
| `FueraDeCarta` | «El plato «...» no está en la carta» | El plato no existe en la carta. |
| `FueraDeCarta` | «La proteína no está en la carta» (y así con cada modificación) | La opción no está entre las de ese plato. |

`FueraDeCarta` hereda de `ComandaInvalida`. Las separé para que más adelante la API pueda responder 400 a lo que está incompleto y 422 a lo que no existe en la carta, como dice la tabla de la API del documento de diseño.

**Supuestos:**

- Si un plato está mal se rechaza toda la comanda, para que nada incompleto llegue a la cocina.
- Las cuatro modificaciones son obligatorias en cada plato.
- La cantidad es 1 si no se manda.
- La mesa solo tiene que ser un entero mayor que cero. Cuántas mesas tiene el restaurante está pendiente (P-03).
- La carta de `afenix/carta.py` es de ejemplo. La real la tiene que validar el restaurante.

**Casos límite:**

- Mesa 1: se acepta. Mesa 0: error.
- Un solo plato: se acepta. Ningún plato: error.
- Cantidad 0: error.
- `True` como mesa: error. En Python `True` es un entero que vale 1, así que hubo que descartarlo aparte.

**Ejemplos:**

| Entrada | Salida |
|---|---|
| `registrar_comanda(4, [{"plato": "Chop suey", "base": "arroz frito", "proteina": "res", "tamano": "familiar", "picante": "medio"}])` | `Comanda(mesa=4, platos=[Plato("Chop suey", ...)], estado="recibido")` |
| `registrar_comanda(4, [])` | lanza `ComandaInvalida`: «La comanda debe tener al menos un plato» |
| `registrar_comanda(4, [{"plato": "Chop suey", ..., "proteina": "camarón"}])` | lanza `FueraDeCarta`: «La proteína no está en la carta» |
| `registrar_comanda(0, [...])` | lanza `ComandaInvalida`: «La mesa debe ser un número mayor que cero» |

### Cómo ejecutar las pruebas

Necesitas Python 3.12 o más reciente.

```bash
python -m venv .venv
source .venv/bin/activate        # en Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m pytest -v
```

Salen 22 pruebas: 3 normales, 4 de límite y 15 de error. Para ver la cobertura: `python -m pytest --cov=afenix`.

## Bitácora de uso de IA

Está en [`bitacora_ia.md`](bitacora_ia.md).

## Estructura

```
afenix/carta.py       carta de ejemplo con los platos y sus opciones
afenix/comandas.py    la función registrar_comanda
tests/                pruebas con pytest
bitacora_ia.md        registro de lo que sugirió la IA y qué decidí
```
