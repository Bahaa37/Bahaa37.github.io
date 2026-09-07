/*
    Scroll-triggered section reveals.

    Each section fades up once, on first entry, and is never replayed — a reveal that
    re-fires every time you scroll past turns into noise on the second read.

    The `js-reveal` class is added to <html> from here rather than sitting in the markup,
    so the hiding CSS only ever applies when this script has actually run. Without that
    guard, a failed script load would leave the page permanently blank.
*/

let observer = null;

export function start() {
    // Honour the OS setting: do nothing at all rather than animate and immediately undo.
    if (window.matchMedia?.('(prefers-reduced-motion: reduce)').matches) {
        return;
    }

    if (!('IntersectionObserver' in window)) {
        return;
    }

    document.documentElement.classList.add('js-reveal');

    observer ??= new IntersectionObserver(
        (entries) => {
            for (const entry of entries) {
                if (entry.isIntersecting) {
                    entry.target.classList.add('is-visible');
                    observer.unobserve(entry.target);
                }
            }
        },
        { threshold: 0.12, rootMargin: '0px 0px -40px 0px' },
    );

    observe();
}

/** Claims any not-yet-observed .reveal elements. Blazor renders sections after start(). */
export function observe() {
    if (!observer) {
        return;
    }

    for (const element of document.querySelectorAll('.reveal:not(.is-visible)')) {
        observer.observe(element);
    }
}
