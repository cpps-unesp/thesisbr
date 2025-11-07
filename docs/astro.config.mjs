// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

// https://astro.build/config
export default defineConfig({
	integrations: [
		starlight({
			title: 'ThesisBr',
			social: [{ icon: 'github', label: 'GitHub', href: '/utilizacao/introducao' }],
			sidebar: [
				{
					label: 'Apresentação',
					autogenerate: { directory: 'thesisbr' },
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
