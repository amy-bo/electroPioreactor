import { defineRouteMiddleware } from '@astrojs/starlight/route-data';

// docs/404.md is `draft: true` only so the [...slug] route skips it (it would
// clash with Starlight's /404 route). Starlight's 404 page still reads it, so
// drop the flag there, or the page shows the "this is a draft" notice.
export const onRequest = defineRouteMiddleware((context) => {
	const route = context.locals.starlightRoute;
	if (route.id === '404') route.entry.data.draft = false;
});
