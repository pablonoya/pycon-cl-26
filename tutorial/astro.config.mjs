// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

// https://astro.build/config
export default defineConfig({
	// GitHub Pages sirve el sitio en https://pablonoya.github.io/pycon-cl-26/
	site: 'https://pablonoya.github.io',
	base: '/pycon-cl-26',
	trailingSlash: 'always',
	integrations: [
		starlight({
			title: '¿Qué tanto debe hacer mi endpoint? - PyCon Chile 2026',
			description: 'Taller de FastAPI para PyCon Chile 2026',
			locales: { root: { label: 'Español', lang: 'es' } },
			sidebar: [
				{
					label: 'Empezar',
					items: [{ label: 'Inicio', link: '/' }, 'setup'],
				},
				{
					label: 'Secciones',
					items: [
						'secciones/00-main',
						'secciones/01-database',
						'secciones/02-email',
						'secciones/03-deferred',
						'secciones/04-events',
						'secciones/05-docs',
					],
				},
			],
		}),
	],
});
