---
title: "Sección 5: Publicar la documentación"
description: Las docs se publican como sitio estático en GitHub Pages.
---

El build de las docs es un sitio estático. En vez de servirlo desde la app, lo publicamos en GitHub Pages con la acción oficial de Astro.

El proyecto Astro vive en `tutorial/` y ya tiene Starlight configurado. Para publicar en un subpath de GitHub Pages (`https://pablonoya.github.io/pycon-cl-26/`) hay que declarar `site` y `base`:

```js title="tutorial/astro.config.mjs"
export default defineConfig({
	site: 'https://pablonoya.github.io',
	base: '/pycon-cl-26',
	trailingSlash: 'always',
	integrations: [starlight({ /* ... */ })],
});
```

`base` es el nombre del repositorio: Astro lo antepone a todos los links internos, a los assets y a la búsqueda de Pagefind.

El deploy lo hace un workflow que buildea el sitio y sube el artefacto a Pages:

```yaml title=".github/workflows/deploy.yml"
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout your repository using git
        uses: actions/checkout@v7
      - name: Install, build, and upload your site output
        uses: withastro/action@v6
        with:
          path: ./tutorial

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v5
```

`withastro/action` detecta el package manager por el lockfile (`bun.lock` → Bun), instala, corre `astro build` y sube `tutorial/dist` como artefacto de Pages. `path` le dice dónde está el proyecto Astro dentro del repo.

Y en el repo, en **Settings → Pages**, el *Source* tiene que ser **GitHub Actions**.

En local, el mismo build se prueba con:

```bash
cd tutorial
bun install
bun astro build
bun astro preview
```

La app no participa: la documentación es un sitio estático, y publicarlo no debería obligar a la app a servir archivos.

Rama: `04-docs`
