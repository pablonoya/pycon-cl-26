---
title: "Sección 0: Hola, FastAPI"
description: Punto de partida del taller.
---

`Crea un archivo src/app/main.py`

```py title="src/app/main.py"
from fastapi import FastAPI

app = FastAPI()


@app.get("/hello")
def hello(name: str | None = None):
    return {"message": f"Hello {name or 'World'}!"}
```

`name` es opcional: sin parámetro responde `Hello World!`.

Apunta a la app de en main.py
```toml title=pyproject.toml
[tool.fastapi]
entrypoint = "app.main:app"
```

```sh
uv run fastapi dev
```

`/docs` muestra el esquema generado y permite probar el endpoint desde el navegador.

Rama: `main`
