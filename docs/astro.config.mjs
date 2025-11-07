// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

// https://astro.build/config
export default defineConfig({
	site: 'https://cpps-unesp.github.io',
	base: '/thesisbr/',
	integrations: [
		starlight({
			title: 'ThesisBr',
			social: [{ icon: 'github', label: 'GitHub', href: '/utilizacao/introducao' }],
			sidebar: [
				{
					label: 'Sobre',
					autogenerate: { directory: 'sobre' },
				},
				{
					label: 'Utilizando o projeto',
					autogenerate: { directory: 'utilizacao' },
				},
				{
					label: 'Contribuindo para o Projeto',
					autogenerate: { directory: 'contribuindo' },
				},
				{
					label: 'Guides',
					items: [
						// Each item here is one entry in the navigation menu.
						{ label: 'Example Guide', slug: 'guides/example' },
					],
				},
				{
					label: 'Reference',
					autogenerate: { directory: 'reference' },
				},
				
			],
		}),
	],
});
