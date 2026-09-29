import { defineCollection } from 'astro:content';
import { docsLoader, i18nLoader } from '@astrojs/starlight/loaders';
import { docsSchema, i18nSchema } from '@astrojs/starlight/schema';
import { stepFrontmatterExtension } from 'starlight-docsandeye/schema';

export const collections = {
	docs: defineCollection({ loader: docsLoader(), schema: docsSchema({ extend: stepFrontmatterExtension }) }),
	// Starlight warns at build when this collection is missing or empty, hence the
	// empty src/content/i18n/en.json (English needs no string overrides).
	i18n: defineCollection({ loader: i18nLoader(), schema: i18nSchema() }),
};
