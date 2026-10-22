// @ts-check
import { defineConfig, passthroughImageService } from 'astro/config';
import starlight from '@astrojs/starlight';
import docsandeye from 'starlight-docsandeye';
import { globSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

// Docs&I reads docs/ once at startup, so `astro dev` restarts whenever one of its files
// changes. Astro restarts only for files registered with addWatchFile, and only hears about
// them from Vite's watcher, which covers site/ alone: hence both. A new file is picked up
// after the next restart.
const repoRoot = fileURLToPath(new URL('..', import.meta.url));
const reloadOnDocs = {
	name: 'reload-on-docs',
	hooks: {
		'astro:config:setup'({ addWatchFile, updateConfig, command }) {
			if (command !== 'dev') return;
			const files = ['docsandeye.config.yaml', ...globSync('docs/**/*.{yaml,yml,md,mdx}', { cwd: repoRoot })].map((f) => repoRoot + f);
			for (const f of files) addWatchFile(f);
			updateConfig({ vite: { plugins: [{ name: 'reload-on-docs', configureServer(server) { server.watcher.add(files); } }] } });
		},
	},
};

// docs.electroPioreactor.org. The guides come from this repository's docs/ folder
// (docsandeye.config.yaml at the repository root); the AEP0.2 guide is served under
// /AEP/. Renders and media are copied verbatim, so no image service is needed.
export default defineConfig({
	site: 'https://docs.electropioreactor.org',
	image: { service: passthroughImageService() },
	vite: {
		build: {
			// The 3D model viewer is one ~1 MB chunk, loaded only when a reader opens a
			// model (a dynamic import in docsandeye's docsi-model), so the size warning is noise.
			chunkSizeWarningLimit: 1100,
			rolldownOptions: {
				// Astro marks MDX pages that import components with this directive and strips
				// it itself; the bundler's warning about it is noise.
				onwarn(warning, warn) {
					if (warning.code === 'MODULE_LEVEL_DIRECTIVE' && warning.message.includes('astro:head-inject')) return;
					warn(warning);
				},
			},
		},
	},
	integrations: [
		starlight({
			routeMiddleware: './src/routeData.ts',
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
						{ slug: 'AEP/protocol' },
						{ label: 'Bill of materials', link: 'https://github.com/amy-bo/electroPioreactor/tree/main/AsepticElectroPioreactor' },
					],
				},
				{
					label: 'Mixed-culture electroPioreactor (MEP)',
					items: [{ label: 'Assembly', link: '/MEP/' }, { slug: 'MEP/protocol' }],
				},
				{ label: 'Budget aseptic electroPioreactor (BAEP)', items: [{ label: 'Assembly', link: '/BAEP/' }] },
			],
		}),
		reloadOnDocs,
	],
});
