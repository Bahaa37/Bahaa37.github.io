/*
    The site's motion system.

    Supersedes reveal.js, which only handled scroll reveals. Three things live here now:
    the orchestrated hero sequence, the scroll reveals, and the stat counters.

    Two rules govern everything in this file:

    1. Motion is ADDITIVE. Every hiding rule in the stylesheet is gated behind the
       `js-motion` class, which is added from here and only here. If this module fails
       to load, is blocked, or throws, no element is ever hidden and the page reads
       exactly as it would without JavaScript. Putting the hiding class in the markup
       instead would make a script failure indistinguishable from a blank page.

    2. Reduced motion is honoured by doing NOTHING rather than by animating and undoing.
       We return before adding `js-motion` at all, so the starting states never apply.
*/

const REDUCED_MOTION = '(prefers-reduced-motion: reduce)';

let observer = null;

function prefersReducedMotion() {
    return window.matchMedia?.(REDUCED_MOTION).matches === true;
}

export function start() {
    // Counters carry their final value in the markup, so under reduced motion the
    // figures are simply present and nothing else needs doing.
    if (prefersReducedMotion() || !('IntersectionObserver' in window)) {
        return;
    }

    document.documentElement.classList.add('js-motion');

    playHero();
    observe();
}

/**
 * Plays the hero as one sequence. Exported so the component can replay it.
 *
 * Removing the class and reading offsetWidth forces a reflow, which is what actually
 * restarts the animations; without that read the browser coalesces the remove/add and
 * nothing replays.
 */
export function playHero() {
    const hero = document.querySelector('.hero');

    if (!hero || prefersReducedMotion()) {
        return;
    }

    hero.classList.remove('is-playing');
    void hero.offsetWidth;
    hero.classList.add('is-playing');

    runCounters();
}

/** Claims any not-yet-observed .reveal elements. Blazor renders sections after start(). */
export function observe() {
    if (prefersReducedMotion()) {
        return;
    }

    observer ??= new IntersectionObserver(
        (entries) => {
            for (const entry of entries) {
                if (entry.isIntersecting) {
                    entry.target.classList.add('is-visible');
                    observer.unobserve(entry.target);
                }
            }
        },
        /*
            threshold MUST stay 0.

            A ratio threshold is a function of element height, so a section taller than
            roughly 8x the viewport can never satisfy it and stays at opacity:0 forever —
            its text selectable but invisible. That is not hypothetical: at 390x844 the
            "Selected work" section is 6533px tall, so at most 0.093 of it is ever on
            screen. The previous 0.12 threshold could never fire and the section was
            blank on every phone while looking fine on every desktop.

            Triggering on the leading edge is height-independent. The negative bottom
            margin stops it firing before the section has really been scrolled to.
        */
        { threshold: 0, rootMargin: '0px 0px -80px 0px' },
    );

    for (const element of document.querySelectorAll('.reveal:not(.is-visible)')) {
        /*
            Anything already scrolled past is shown at once instead of being observed.

            An IntersectionObserver only ever reports what is intersecting NOW, so a
            section sitting above the viewport when the observer arms will never fire.
            That is not rare: browsers restore scroll position on reload, and a deep
            link such as /#work loads part-way down the page. In both cases every
            section above the entry point would stay at opacity:0 forever — present in
            the DOM, its text selectable, but invisible.

            Blazor arms this after its own async boot, so the window is wide enough for
            a reader to have already scrolled.
        */
        if (element.getBoundingClientRect().bottom < 0) {
            element.classList.add('is-visible');
            continue;
        }

        observer.observe(element);
    }
}

/**
 * Counts each [data-count-to] element up to its final value.
 *
 * The element's markup already contains the final text, so a failure here leaves the
 * correct figure on screen rather than a zero.
 */
function runCounters() {
    const counters = document.querySelectorAll('[data-count-to]');

    for (const element of counters) {
        const to = Number.parseFloat(element.dataset.countTo);
        const from = element.dataset.countFrom ? Number.parseFloat(element.dataset.countFrom) : 0;
        const decimals = Number.parseInt(element.dataset.decimals ?? '0', 10);
        const delay = Number.parseInt(element.dataset.countDelay ?? '2150', 10);

        if (Number.isNaN(to)) {
            continue;
        }

        const started = performance.now();
        const duration = 900;

        const step = (now) => {
            const progress = Math.min(1, Math.max(0, (now - started - delay) / duration));
            const eased = 1 - Math.pow(1 - progress, 3);

            element.textContent = (from + (to - from) * eased).toFixed(decimals);

            if (progress < 1) {
                requestAnimationFrame(step);
            }
        };

        requestAnimationFrame(step);
    }
}
