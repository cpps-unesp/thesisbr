// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

// https://astro.build/config
export default defineConfig({
	integrations: [
		starlight({
			title: 'My Docs',
			social: [{ icon: 'github', label: 'GitHub', href: 'https://github.com/withastro/starlight' }],
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
				{
					label: 'Apresentação',
					autogenerate: { directory: 'thesisbr' },
				},
			],
		}),
	],
});
