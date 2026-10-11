/*
    Offline-first caching for the published site.

    The point of this file is the repeat visit. The host (GitHub Pages) caps HTTP
    caching at ten minutes, so without it every returning visitor re-downloads the
    ~2 MB WebAssembly runtime. With it, the runtime is fetched from Cache Storage
    on every visit after the first, and booting takes seconds on any connection.

    Strategy per request (GET, same-origin only; everything else passes through):

      * /_framework/... and anything with a ?v= content hash — cache-first. These
        URLs are immutable by construction: the framework files carry a build
        fingerprint, the ?v= hashes are computed from file contents by prerender.py.
        A new deploy changes the URLs, so stale entries are simply never asked for.
      * /data/... — network-first. These files are the canonical data documents;
        staleness there is exactly what the app's own NoCache revalidation exists to
        prevent. The cache answers only when the network cannot (offline).
      * page navigations — network-first, cached copy as the offline fallback.
        Prerendered pages are documents whose entire purpose is being current, so
        they are never served stale while the network is reachable.

    Install precaches the pages an installed app must open offline without having been
    visited first: the home page it launches into, the CV, the PDF, and the 404 page
    networkFirst() falls back to. Before the site was installable, "offline" only meant
    "a page you already read"; an app icon that opens onto the browser's error page is
    a broken app. Precaching changes nothing online — navigations stay network-first.

    __SW_VERSION__ is replaced at publish time by prerender.py with a hash of this
    source plus the framework file list. Any change to either produces a new cache
    name; activate() deletes the previous one. In development this file is never
    registered — the registration snippet is injected by prerender.py only.
*/
const CACHE = "cv-shell-__SW_VERSION__";

const PRECACHE = ["/", "/cv/", "/Bahaa-Aldeen-Mohamed-CV.pdf", "/404.html"];

self.addEventListener("install", (event) => {
    // One by one, never addAll: addAll rejects as a whole, and a single failed fetch
    // would then fail the install and leave visitors on the previous worker.
    event.waitUntil(
        caches.open(CACHE).then((cache) =>
            Promise.all(PRECACHE.map((url) => cache.add(url).catch(() => undefined)))
        )
    );
});

self.addEventListener("activate", (event) => {
    event.waitUntil(
        caches.keys()
            .then((keys) =>
                Promise.all(
                    keys.filter((key) => key !== CACHE).map((key) => caches.delete(key))
                )
            )
            .then(() => self.clients.claim())
    );
});

self.addEventListener("fetch", (event) => {
    const request = event.request;
    if (request.method !== "GET") { return; }

    const url = new URL(request.url);
    if (url.origin !== self.location.origin) { return; }

    if (url.pathname.startsWith("/data/") || request.mode === "navigate") {
        event.respondWith(networkFirst(request));
        return;
    }

    if (url.pathname.startsWith("/_framework/") || url.search.includes("?v=")) {
        event.respondWith(cacheFirst(request));
    }
});

async function cacheFirst(request) {
    const cached = await caches.match(request);
    if (cached) { return cached; }

    const response = await fetch(request);
    if (response.ok) {
        const cache = await caches.open(CACHE);
        cache.put(request, response.clone());
    }
    return response;
}

async function networkFirst(request) {
    try {
        const response = await fetch(request);
        if (response.ok) {
            const cache = await caches.open(CACHE);
            cache.put(request, response.clone());
        }
        return response;
    } catch (error) {
        const cached = await caches.match(request);
        if (cached) { return cached; }
        if (request.mode === "navigate") {
            // The site links to "/cv"; GitHub Pages redirects that to "/cv/", and only
            // the redirect target is ever cached. Without this lookup the static page's
            // CV link would open the 404 page offline.
            const url = new URL(request.url);
            if (!url.pathname.endsWith("/")) {
                url.pathname += "/";
                const slashed = await caches.match(url.href);
                if (slashed) { return slashed; }
            }
            return caches.match("/404.html");
        }
        throw error;
    }
}
