import { defineCollection } from 'astro:content';
import { docsLoader } from '@astrojs/starlight/loaders';
import { docsSchema } from '@astrojs/starlight/schema';
import { stepFrontmatterExtension } from 'starlight-docsandeye/schema';

export const collections = {
	docs: defineCollection({ loader: docsLoader(), schema: docsSchema({ extend: stepFrontmatterExtension }) }),
};
