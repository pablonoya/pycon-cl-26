---
title: Instalación
description: Clona el repositorio y prepara el entorno con uv o pip.
---

## Requisitos

- Python 3.13 o superior
- [uv](https://docs.astral.sh/uv/) (recomendado) o pip
- git

## Clona el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd app
```

## Con uv

```bash
uv sync
uv run fastapi dev
```

## Con pip

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
fastapi dev
```

La app queda en `http://127.0.0.1:8000`, con la documentación interactiva en `/docs`. `fastapi dev` recarga al guardar cambios.

## Ramas por sección

| Sección | Rama | Agrega |
| --- | --- | --- |
| 0 | `main` | Un endpoint `GET /hello` |
| 1 | `00-database` | SQLite, `POST /registrations` y validaciones |
| 2 | `01-email` | Correo de confirmación y medición del envío |
| 3 | `02-defered-execution` | Cola de tareas con varios workers |
| 4 | `03-event-driven` | Bus de eventos con consumidores |
| 5 | `04-docs` | La documentación se publica en GitHub Pages |

Cada rama incluye lo de las anteriores. La base `registrations.db` se crea sola al arrancar y está ignorada por git.
