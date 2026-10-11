/*
    The style guide's runtime layer (/styleguide).

    The page renders statically with names, swatches and samples; this module adds
    everything only the live cascade can answer: the resolved value of every --hl-*
    token under the CURRENT theme, re-read when the theme changes, the easing plots
    re-derived from the token's live value, the Replay buttons for the entrance
    animations, and the log of every hl:* event the kit's engine fires.

    Fetched by bare path from StyleGuide.razor — the same accepted exception as
    js/motion.js (see CLAUDE.md): a file that changes rarely, traded against the
    manual cache-busting a ?v= stamp would require.

    init() is idempotent: Blazor renders once, but the theme toggle re-renders the
    layout, and a second binding would double every listener. Values are written
    into Blazor-owned elements only as textContent of nodes whose render tree never
    changes — the same contract motion.js's counters already honour.
*/

const HL_EVENTS = ['hl:reveal', 'hl:console-run', 'hl:tab-change', 'hl:autoplay'];

let bound = false;

const readVar = (name) => getComputedStyle(document.documentElement).getPropertyValue(name).trim();

/** Fills every [data-sg-token] span with the token's value under the current theme. */
function fillTokenValues() {
    for (const cell of document.querySelectorAll('[data-sg-token]')) {
        const value = readVar(cell.dataset.sgToken);
        // Never blank a filled cell: a token that resolves to nothing leaves the
        // static name showing rather than an empty box.
        if (value) cell.textContent = value;
    }
}

/*
 * Re-derives each easing plot from the token's live value, so a vendored kit
 * update changes the drawn curve on the next visit even before the static path
 * constants in StyleGuide.razor/prerender.py are re-synced. Same sampler as the
 * kit's own demo: 41 samples, y flipped, one decimal.
 */
function plotEases() {
    for (const card of document.querySelectorAll('[data-sg-ease]')) {
        const [x1, y1, x2, y2] = (readVar(card.dataset.sgEase).match(/-?[\d.]+/g) || []).map(Number);
        if (![x1, y1, x2, y2].every(Number.isFinite)) continue;
        const bez = (a, b, t) => 3 * (1 - t) ** 2 * t * a + 3 * (1 - t) * t ** 2 * b + t ** 3;
        const pts = Array.from({ length: 41 }, (_, i) => {
            const t = i / 40;
            return `${(bez(x1, x2, t) * 100).toFixed(1)},${(100 - bez(y1, y2, t) * 100).toFixed(1)}`;
        }).join(' L ');
        const path = card.querySelector('path');
        if (path) path.setAttribute('d', `M ${pts}`);
    }
}

/*
 * Replay: class out, forced reflow, class in — the same re-trigger trick
 * hairline.js uses. Under reduced motion the buttons are relabelled and
 * aria-disabled instead, which is honest: there is nothing to replay.
 */
function wireReplay() {
    const reduced = window.matchMedia?.('(prefers-reduced-motion: reduce)').matches === true;
    for (const button of document.querySelectorAll('[data-sg-replay]')) {
        if (reduced) {
            button.textContent = 'Motion reduced';
            button.setAttribute('aria-disabled', 'true');
            continue;
        }
        button.addEventListener('click', () => {
            const target = document.getElementById(button.dataset.sgTarget);
            const cls = button.dataset.sgClass;
            if (!target || !cls) return;
            target.classList.remove(cls);
            void target.offsetWidth;
            target.classList.add(cls);
        });
    }
}

/*
 * The events log. hl:* events bubble, so one document-level listener per event
 * type sees everything the engine does on this page — reveals, console runs, tab
 * changes, autoplay pauses — with the detail serialized as JSON (DOM nodes, the
 * one thing JSON cannot say, render as <tag#id>).
 */
function wireEventLog() {
    const log = document.getElementById('sg-eventlog');
    if (!log) return;

    const t0 = performance.now();
    const asJson = (detail) => {
        if (!detail) return '{}';
        const replacer = (key, value) =>
            value && value.nodeType === 1
                ? `<${value.tagName.toLowerCase()}${value.id ? `#${value.id}` : ''}>`
                : value;
        return JSON.stringify(detail, replacer);
    };

    for (const type of HL_EVENTS) {
        document.addEventListener(type, (event) => {
            log.querySelector('[data-sg-log-placeholder]')?.remove();
            const line = document.createElement('p');
            line.className = 'sg-eventlog__line';
            line.textContent = `+${Math.round(performance.now() - t0)}ms  ${type}  ${asJson(event.detail)}`;
            log.prepend(line);
            while (log.children.length > 40) log.lastElementChild.remove();
        });
    }
}

export function init() {
    fillTokenValues();
    plotEases();
    if (bound) return;
    bound = true;

    wireReplay();
    wireEventLog();

    // A theme switch flips --hl-* values on the root; both switch paths must
    // re-read: the explicit data-theme attribute (tap or drag on the switch)
    // and the OS-level scheme change, which applies while no attribute is set.
    // The switch commits through a View Transition when available; the observer
    // fires after the DOM change lands, so the values read are the new theme's.
    const repaint = () => { fillTokenValues(); plotEases(); };
    new MutationObserver(repaint).observe(document.documentElement, {
        attributes: true,
        attributeFilter: ['data-theme'],
    });
    window.matchMedia?.('(prefers-color-scheme: dark)').addEventListener?.('change', repaint);
}
