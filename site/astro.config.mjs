// @ts-check
import { defineConfig, passthroughImageService } from 'astro/config';
import starlight from '@astrojs/starlight';
import docsandeye from 'starlight-docsandeye';

// docs.electroPioreactor.org. The guides come from this repository's docs/ folder
// (docsandeye.config.yaml at the repository root); the AEP0.2 guide is served under
// /AEP/. Renders and media are copied verbatim, so no image service is needed.
export default defineConfig({
	site: 'https://docs.electropioreactor.org',
	image: { service: passthroughImageService() },
	integrations: [
		starlight({
			title: 'electroPioreactor',
			description: 'Assembly and training guides for the electroPioreactor, an open aseptic electro-bioreactor built on the Pioreactor.',
			plugins: [docsandeye({ projectRoot: '..' })],
			components: { ThemeSelect: '@docsandeye/themes/ThemeSelect.astro' },
			social: [{ icon: 'github', label: 'GitHub', href: 'https://github.com/amy-bo/electroPioreactor' }],
			sidebar: [
				{
					label: 'Aseptic electroPioreactor (AEP0.2)',
					items: [
						{ label: 'Assembly', link: '/AEP/' },
						{ slug: 'aep/protocol' },
						{ label: 'Bill of materials', link: 'https://github.com/amy-bo/electroPioreactor/tree/main/AsepticElectroPioreactor' },
					],
				},
				{
					label: 'Mixed-culture electroPioreactor (MEP)',
					items: [{ label: 'Assembly', link: '/MEP/' }, { slug: 'mep/protocol' }],
				},
				{ label: 'Budget aseptic electroPioreactor (BAEP)', items: [{ label: 'Assembly', link: '/BAEP/' }] },
			],
		}),
	],
});
