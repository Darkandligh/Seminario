# Revisión del pipeline

Proyecto: A-Fénix
Estudiante: Eduardo Ascencio
Fecha: 2026-11-26

## 1. Cómo se generó

**Herramienta de IA:** Claude (claude.ai), en el chat.
**Prompt del pipeline:** «Escribe un workflow de GitHub Actions para mi proyecto de Python con pytest». Es el mismo prompt simple del código de práctica del curso. El borrador quedó sin cambios en [`evidencias/entrega-final/ci_borrador_ia.yml`](../evidencias/entrega-final/ci_borrador_ia.yml) y la versión revisada en [`.github/workflows/ci.yml`](../.github/workflows/ci.yml). Entrada 22 de la bitácora.
**Prompt del Dockerfile:** no se generó. El diseño (ADR-001) instala A-Fénix directo en un mini PC del restaurante, sin contenedores, y todavía no hay un servidor que empaquetar.

## 2. Hallazgos

Revisé el borrador línea por línea con la lista de revisión de pipelines del curso: eventos, permisos, secretos, versiones, dependencias y si un fallo de las pruebas hace fallar el pipeline.

| Archivo y línea | Problema | Riesgo | Corrección |
|---|---|---|---|
| ci_borrador_ia.yml:6-10 | Solo corre con `push` y `pull_request` a `main` | El trabajo se hace en ramas por semana (`semana-5`, `semana-6`...). Esas ramas nunca se revisaban y un error solo se veía al unir con `main` | `push` sin filtro de ramas; `pull_request` hacia `main` |
| ci_borrador_ia.yml (falta) | No declara `permissions` | El token del pipeline queda con los permisos por defecto del repositorio, que pueden ser de escritura. El pipeline solo necesita leer | `permissions: contents: read` |
| ci_borrador_ia.yml:20 | `python-version: "3.x"` | Toma la versión más nueva que exista ese día, no la 3.12 del proyecto (`pyproject.toml`). Un día puede fallar sin que el código haya cambiado | `python-version: "3.12"` |
| ci_borrador_ia.yml:23-25 | `pip install --upgrade pip` y `pip install pytest` sin versión | Instala lo último que haya. En la semana 6 justo pytest 8.3.4 tenía una vulnerabilidad (H-01). Lo que pasa en mi equipo puede no pasar en el pipeline | `pip install -r requirements-dev.txt`, con todas las versiones fijadas |
| ci_borrador_ia.yml:26-27 | Solo corre `pytest` | No revisa el linter, los tipos, la seguridad ni las dependencias, que configuré en la semana 6. Tampoco mide la cobertura | Pasos para ruff, mypy, bandit y pip-audit, y `--cov-fail-under=95` |
| ci_borrador_ia.yml:14 | `ubuntu-latest` y sin tiempo límite | La imagen cambia sin aviso, y si algo se cuelga el trabajo sigue hasta 6 horas | `ubuntu-24.04` y `timeout-minutes: 10` |

Lo que estaba bien en el borrador: no tiene claves ni secretos, y no tiene `continue-on-error`, así que una prueba que falla sí hace fallar el pipeline. Lo comprobé con la ejecución en rojo de la sección 4.

Un ajuste que salió al correr el pipeline revisado: `ruff check .` revisaba también `evidencias/`, donde está el borrador de pruebas de la IA de la semana 7 sin cambios, y daba 7 avisos. Excluí esa carpeta en `pyproject.toml` porque no es código del proyecto. También dejé por archivo la excepción E501 de las pruebas de la semana 5, que ya estaba justificada en `revision_seguridad.md`.

## 3. Lo que encontraron las herramientas

| Herramienta | Avisos | ¿Coinciden con mis hallazgos? | ¿Qué no encontró? |
|---|---|---|---|
| actionlint 1.7 | 0 en el borrador | No encontró ninguno | Ninguno de los 6. El borrador es YAML válido; los problemas son de permisos, versiones y lo que falta revisar, y eso actionlint no lo juzga |
| hadolint | No aplica | No hay Dockerfile | — |

## 4. Verificación

- [x] El pipeline corregido se ejecutó en GitHub y salió en verde: [ejecución 45827540623](https://github.com/Darkandligh/Seminario/actions/runs/45827540623).
- [x] Hice fallar una prueba a propósito y el pipeline salió en rojo: cambié `MAX_PLATOS` de 50 a 49 y falló el paso de pruebas ([ejecución 45827692474](https://github.com/Darkandligh/Seminario/actions/runs/45827692474)). Revertí el cambio y volvió a verde ([ejecución 45828006219](https://github.com/Darkandligh/Seminario/actions/runs/45828006219)).
- [ ] La imagen se construye: no aplica, no hay Dockerfile (ver sección 1).
- [x] No hay claves en `ci.yml` ni en el historial de Git. Lo revisé con `git log -p --all` buscando password, secret, token y key.
