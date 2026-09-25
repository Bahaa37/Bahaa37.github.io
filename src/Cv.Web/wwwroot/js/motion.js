/*
    The site's motion system.

    Three things live here: the orchestrated hero sequence, the scroll reveals, and the
    stat counters.

    Three rules govern everything in this file:

    1. Motion is ADDITIVE. Every hiding rule in the stylesheet is gated behind the
       `js-motion` class, which is added from here and only here. If this module fails
       to load, is blocked, or throws, no element is ever hidden and the page reads
       exactly as it would without JavaScript. Putting the hiding class in the markup
       instead would make a script failure indistinguishable from a blank page.

    2. Reduced motion is honoured by doing NOTHING rather than by animating and undoing.
       We return before adding `js-motion` at all, so the starting states never apply.

    3. Motion never replays over a reader. The hero sequence exists for the visitor who
       landed fast and is still on their first look. A visitor who has scrolled, or who
       has already seen it this session, gets the static hero — the runtime arrives
       seconds late on a cold connection, and hiding what someone is mid-way through
       reading is the one defect this site must never commit.
*/

const REDUCED_MOTION = '(prefers-reduced-motion: reduce)';

// The sequence only starts when the runtime has booted this soon after navigation.
// Past this point the visitor has been reading the static hero for seconds, and
// replaying it would blank exactly what they are looking at.
const HERO_PLAY_DEADLINE_MS = 1500;

const HERO_SCROLL_THRESHOLD = 40;

let observer = null;
let sweepQueued = false;
let sweepBound = false;

/**
 * Reveals anything that has ended up above the viewport without ever intersecting.
 *
 * An IntersectionObserver only reports a CHANGE in intersection. Every anchor in the
 * site nav jumps the reader over whole sections, and a section that goes straight from
 * "below the viewport" to "above the viewport" in one jump is never intersecting at any
 * sampled frame — so no callback fires for it at all and it stays at opacity:0 for the
 * rest of the visit, blank if the reader scrolls back up.
 *
 * Cheap by construction: rAF-throttled, and the selector stops matching once everything
 * has been revealed, at which point the listener detaches itself.
 */
function sweepScrolledPast() {
    if (sweepQueued) {
        return;
    }

    sweepQueued = true;

    requestAnimationFrame(() => {
        sweepQueued = false;

        const pending = document.querySelectorAll('.reveal:not(.is-visible)');

        for (const element of pending) {
            if (element.getBoundingClientRect().bottom < 0) {
                element.classList.add('is-visible');
                observer?.unobserve(element);
            }
        }

        if (pending.length === 0 && sweepBound) {
            window.removeEventListener('scroll', sweepScrolledPast);
            sweepBound = false;
        }
    });
}

function prefersReducedMotion() {
    return window.matchMedia?.(REDUCED_MOTION).matches === true;
}

export function start() {
    // Scroll-spy is STATE, not motion — it marks which section the reader is in, so
    // it runs regardless of reduced motion, exactly like the header's is-scrolled.
    startScrollSpy();

    // Counters carry their final value in the markup, so under reduced motion the
    // figures are simply present and nothing else needs doing.
    if (prefersReducedMotion() || !('IntersectionObserver' in window)) {
        return;
    }

    document.documentElement.classList.add('js-motion');

    maybePlayHero();
    observe();
}

/*
    Current-section state for the header nav (the two heuristics the 2026-09-24
    critique scored 2/4 both traced here: on a page this tall, nothing told you
    where you were).

    Scope is deliberately tiny: only the home page has the four sections the nav's
    section anchors point at, so the spy arms only when both sides exist — nav links
    matching /#<id> and a section with that id. It never removes anything from the
    page: the class ADDS emphasis to one link and nothing is ever hidden, which
    keeps this file's additive-only rule intact. The static shell has no marker
    (pre-boot there is no scroll state worth claiming), so prerender.py needs no
    mirror of this.
*/
const SPY_TOP_OFFSET = 120; // just below the capsule, so a section counts as "reached" once its heading clears the chrome

let spyTick = false;
let spyUpdate = null; // the armed spy's throttled update, or null while disarmed

/*
    A reveal lifts its section the last 26px as it settles (translate 26 → 0 over
    .7s), and settling fires no scroll event — so a spy sample taken mid-settle
    reads the just-reached section ~26px below where it will rest and can leave the
    previous link marked. Every reveal therefore schedules one extra spy pass past
    the transition window; without it the marker waits for the reader's next scroll.
*/
function refreshSpyAfterSettle() {
    if (!spyUpdate) {
        return;
    }

    setTimeout(spyUpdate, 750);
}

function startScrollSpy() {
    const links = [...document.querySelectorAll('.site-nav a[href^="/#"]')]
        .filter((link) => document.querySelector(link.hash));

    if (links.length === 0) {
        spyUpdate = null;
        return;
    }

    const update = () => {
        spyTick = false;

        // The binding survives client-side navigation away from the home page — only
        // the sections don't. A missing section is skipped, not dereferenced: a bare
        // call threw on every scrolled frame of every other route, and left the last
        // .is-current stranded on the nav. Skipping it clears the marker instead, and
        // navigation itself scrolls to top, so the next scrolled frame fires at once.
        const current = links
            .map((link) => document.querySelector(link.hash))
            .filter((section) => section && section.getBoundingClientRect().top <= SPY_TOP_OFFSET)
            .pop();

        for (const link of links) {
            const isCurrent = link.hash === `#${current?.id}`;
            link.classList.toggle('is-current', isCurrent);
            // The class alone is invisible to assistive tech — aria-current is what a
            // screen reader announces as the section you are in.
            if (isCurrent) {
                link.setAttribute('aria-current', 'true');
            } else {
                link.removeAttribute('aria-current');
            }
        }
    };

    const requestUpdate = () => {
        if (!spyTick) {
            spyTick = true;
            requestAnimationFrame(update);
        }
    };

    spyUpdate = requestUpdate;

    window.addEventListener('scroll', requestUpdate, { passive: true });

    update();
}

/*
    Back-to-top: the floating control in MainLayout.razor (.back-to-top) that appears
    after roughly one viewport of scroll and returns the reader to the top.

    The scroll logic lives here rather than in a new module because this file is the
    accepted bare-path import (CLAUDE.md) — a newly fetched JS file would inherit the
    manual cache-busting problem the warning describes. The button is runtime chrome
    with no static-shell copy on purpose: the footer's "Back to top" hash link is the
    no-script path to the same place, so a visitor the runtime never reaches loses an
    affordance, never an ability. The stylesheet keeps the button display:none and
    .is-shown — the only visibility class — is applied from here and nowhere else,
    which keeps this file's additive-only rule intact: the button contains no content,
    so a failure here leaves an enhancement absent, never content invisible.
*/
const BACK_TO_TOP_VIEWPORTS = 1; // viewports of scroll before the control earns its place

let backToTopTick = false;

export function initBackToTop() {
    const button = document.querySelector('.back-to-top');

    // Idempotent: MainLayout owns the wiring and re-runs its first render only once
    // per layout instance, but a second binding against the same button would double
    // every scroll callback for the life of the page.
    if (!button || button.dataset.backToTopBound) {
        return;
    }

    button.dataset.backToTopBound = '1';

    const update = () => {
        backToTopTick = false;
        const y = window.scrollY || window.pageYOffset || 0;
        button.classList.toggle('is-shown', y > window.innerHeight * BACK_TO_TOP_VIEWPORTS);
    };

    button.addEventListener('click', () => {
        // Reduced motion gets the instant jump the user asked for, and so does any
        // browser without scroll-behavior — a coerced ScrollToOptions object would
        // scroll nowhere predictable there.
        if (!prefersReducedMotion() && 'scrollBehavior' in document.documentElement.style) {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        } else {
            window.scrollTo(0, 0);
        }
    });

    window.addEventListener('scroll', () => {
        if (!backToTopTick) {
            backToTopTick = true;
            requestAnimationFrame(update);
        }
    }, { passive: true });

    // Deep links such as /#work land already scrolled; the control must not wait for
    // the reader's first scroll event to learn that.
    update();
}

/**
 * Plays the hero as one sequence. Arming applies the hidden starting states; the
 * class is never added on the skip path, so a visitor who does not get the sequence
 * gets the fully visible static hero, not an invisible one.
 *
 * Removing the playing class and reading offsetWidth forces a reflow, which is what
 * actually restarts the animations; without that read the browser coalesces the
 * remove/add and nothing replays.
 */
export function playHero() {
    const hero = document.querySelector('.hero');

    if (!hero || prefersReducedMotion()) {
        return;
    }

    hero.classList.add('is-armed');
    hero.classList.remove('is-playing');
    void hero.offsetWidth;
    hero.classList.add('is-playing');

    runCounters();
}

/**
 * Decides whether this visit gets the sequence at all.
 *
 * Three independent reasons to skip, any one of which means the visitor already has
 * eyes on the static hero: they scrolled while the runtime was arriving, they have
 * seen the sequence earlier in this session, or the boot itself took longer than the
 * play deadline. The flag is per session, so a second page view never replays it.
 */
function maybePlayHero() {
    const hero = document.querySelector('.hero');

    if (!hero) {
        return;
    }

    let played = false;
    try { played = sessionStorage.getItem('heroPlayed') === '1'; } catch (e) { }

    const scrolled = (window.scrollY || window.pageYOffset || 0) > HERO_SCROLL_THRESHOLD;
    const bootedLate = performance.now() > HERO_PLAY_DEADLINE_MS;

    if (played || scrolled || bootedLate) {
        return;
    }

    try { sessionStorage.setItem('heroPlayed', '1'); } catch (e) { }

    playHero();
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
                    // The section now settles upward into place; give the spy one
                    // post-settle sample so the current-section marker agrees with
                    // where the section finally rests.
                    refreshSpyAfterSettle();
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

    if (!sweepBound) {
        window.addEventListener('scroll', sweepScrolledPast, { passive: true });
        sweepBound = true;
    }

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
        // Short enough that a glancing reader never settles on the "before" figure:
        // the count-down dramatizes 7 → 3, but 900ms of visible "7" read as the number.
        const duration = 550;

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
