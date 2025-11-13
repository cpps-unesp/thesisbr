// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

// https://astro.build/config
export default defineConfig({
  integrations: [
    starlight({
      title: 'ThesisBR',
      logo: {
        src:'images/houston.webp'
		
      },
      sidebar: [
        {
          label: 'Sobre o projeto',
          items: [
            { label: 'Introdução', link: '/sobre/introducao/' },
            { label: 'Equipe', link: '/sobre/equipe/' },
            { label: 'FAQ', link: '/sobre/faq/' },
          ],
        },
        {
          label: 'Utilizando o projeto',
          autogenerate: { directory: 'utilizando' },
        },
        
        // --- 💎 NOVA SEÇÃO ADICIONADA AQUI 💎 ---
        {
          label: 'Documentação Técnica',
          // Isso irá gerar o menu para a nova pasta que você vai criar:
          // 'src/content/docs/documentacao-tecnica/'
          autogenerate: { directory: 'documentacao-tecnica' },
        },
        // --- FIM DA NOVA SEÇÃO ---

        {
          label: 'Contribuindo para o projeto',
          autogenerate: { directory: 'contribuindo' },
        },
      ],
    }),
  ],
});