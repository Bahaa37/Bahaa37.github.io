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
      * /data/... — network-first. These files are the canonical CV and decisions;
        staleness there is exactly what the app's own NoCache revalidation exists to
        prevent. The cache answers only when the network cannot (offline).
      * page navigations — network-first, cached copy as the offline fallback.
        Prerendered pages are documents whose entire purpose is being current, so
        they are never served stale while the network is reachable.

    __SW_VERSION__ is replaced at publish time by prerender.py with a hash of this
    source plus the framework file list. Any change to either produces a new cache
    name; activate() deletes the previous one. In development this file is never
    registered — the registration snippet is injected by prerender.py only.
*/
const CACHE = "cv-shell-__SW_VERSION__";

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
            return caches.match("/404.html");
        }
        throw error;
    }
}
