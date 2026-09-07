/*
    Lazy Mermaid loader.

    Mermaid is ~3.5MB unminified-equivalent, which is far too much to put in front of a
    recruiter who may never open a diagram. So it is fetched only when a case study
    diagram is actually revealed, and never on first paint.

    The bundled build assigns itself to an esbuild namespace object rather than a
    documented global, so the loader probes the known candidates instead of assuming
    one. If none is found, the caller falls back to showing the diagram source.
*/

let loader = null;

function findMermaid() {
    if (window.mermaid?.render) {
        return window.mermaid;
    }

    // esbuild namespace form used by the bundled dist/mermaid.min.js.
    const ns = window.__esbuild_esm_mermaid_nm;
    if (ns?.mermaid?.render) {
        return ns.mermaid;
    }
    if (ns?.mermaid?.default?.render) {
        return ns.mermaid.default;
    }

    return null;
}

function loadScriptOnce() {
    if (loader) {
        return loader;
    }

    loader = new Promise((resolve, reject) => {
        const existing = findMermaid();
        if (existing) {
            resolve(existing);
            return;
        }

        const script = document.createElement('script');
        script.src = 'lib/mermaid/mermaid.min.js';
        script.onload = () => {
            const mermaid = findMermaid();
            if (mermaid) {
                resolve(mermaid);
            } else {
                reject(new Error('Mermaid loaded but no usable global was found.'));
            }
        };
        script.onerror = () => reject(new Error('Failed to load lib/mermaid/mermaid.min.js'));
        document.head.appendChild(script);
    });

    return loader;
}

function prefersDark() {
    return window.matchMedia?.('(prefers-color-scheme: dark)').matches ?? false;
}

/*
    Diagrams already on screen when the viewer flips their OS theme would otherwise keep
    the palette they were drawn with — a dark diagram stranded on a light page. Mermaid
    bakes theme colours into the SVG at render time, so the only fix is to redraw.
*/
const drawn = new Map();
let themeWatcherAttached = false;

function watchThemeOnce() {
    if (themeWatcherAttached || !window.matchMedia) {
        return;
    }

    themeWatcherAttached = true;
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
        for (const [element, entry] of drawn) {
            // Elements removed from the DOM (diagram collapsed) are dropped rather than redrawn.
            if (element.isConnected) {
                draw(element, entry.id, entry.definition);
            } else {
                drawn.delete(element);
            }
        }
    });
}

async function draw(element, id, definition) {
    const mermaid = await loadScriptOnce();

    mermaid.initialize({
        startOnLoad: false,
        securityLevel: 'strict',
        theme: prefersDark() ? 'dark' : 'default',
        fontFamily: 'inherit',
    });

    // innerHTML is safe here on two counts: the definition comes from cv.json, which
    // is author-controlled content committed to this repository and never user input;
    // and securityLevel 'strict' makes Mermaid sanitize its own output. If this ever
    // renders a definition supplied at runtime, it must be sanitized before this line.
    //
    // The id is suffixed because Mermaid refuses to reuse an id already in the document,
    // which a theme-change redraw would otherwise do.
    const { svg } = await mermaid.render(`mermaid-${id}-${Date.now()}`, definition);
    element.innerHTML = svg;

    const rendered = element.querySelector('svg');
    if (rendered) {
        // Let the SVG shrink to its container instead of forcing the page sideways.
        rendered.removeAttribute('width');
        rendered.style.maxWidth = '100%';
        rendered.style.height = 'auto';
    }

    drawn.set(element, { id, definition });
}

/**
 * Renders Mermaid source into the given element.
 * @returns {Promise<boolean>} true if a diagram was drawn, false if the caller should
 *          fall back to showing the source.
 */
export async function renderDiagram(element, id, definition) {
    if (!element || !definition) {
        return false;
    }

    try {
        await draw(element, id, definition);
        watchThemeOnce();
        return true;
    } catch (error) {
        console.warn('Diagram rendering unavailable:', error);
        return false;
    }
}
