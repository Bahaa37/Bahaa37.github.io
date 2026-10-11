/*
    Boots the WebAssembly runtime late, on purpose.

    The page a person reads is prerendered HTML with its stylesheet inlined: it is
    complete — navigable, themable, downloadable — before any of this runs. What the
    runtime adds is the app's own rendering, motion reveals and the architecture
    diagrams, so it is started once the browser is idle instead of ahead of first
    paint. Nothing on the page is waiting for it.

    On a connection that asks to save data, or that reports 2G, the runtime is never
    started. A visitor on such a connection gets the whole site as static pages —
    which is everything a CV reader needs — instead of a ~2 MB download they did
    not ask for. The site's own bar is that content is visible in under a second;
    this file exists to keep that true while the runtime loads behind it.
*/
(function () {
    "use strict";

    var started = false;

    /*
        The handover. Blazor renders into #app, and its first render of any page is a
        "Loading…" placeholder while the CV data is fetched: a visitor who had been
        reading the static page for seconds watched it vanish, then come back. So the
        static page is moved out of #app into a sibling before the runtime starts,
        Blazor renders into a hidden #app, and only once that render has real content
        (a page heading and no loading placeholder) does one synchronous swap happen,
        before the next paint. If the runtime never gets there, the static page simply
        stays: it is the product, not a placeholder.

        The nodes are MOVED, not cloned, so the console, tabs and theme switch keep
        their listeners while the runtime loads behind them.
    */
    function holdStaticPage() {
        var app = document.getElementById("app");
        if (!app || !app.querySelector(".prerendered")) { return; } // dev server: nothing to hold

        var shell = document.createElement("div");
        shell.id = "app-static";
        var nodes = Array.prototype.slice.call(app.childNodes);
        for (var i = 0; i < nodes.length; i++) {
            var node = nodes[i];
            // The loading spinner stays behind in #app; it never shows, #app is hidden.
            if (node.nodeType === 1 && /\bloading-progress/.test(node.getAttribute("class") || "")) { continue; }
            shell.appendChild(node);
        }
        app.parentNode.insertBefore(shell, app);
        app.hidden = true;

        function rendered() {
            return app.querySelector("h1") && !app.querySelector(".booting, .loading");
        }

        var observer = new MutationObserver(function () {
            if (!rendered()) { return; }
            observer.disconnect();
            var y = window.scrollY || window.pageYOffset || 0;
            app.hidden = false;
            shell.parentNode.removeChild(shell);
            window.scrollTo(0, y);
            // Everything already on screen must simply be there: no fade-ins, no replayed entrance.
            if (window.Hairline && window.Hairline.settle) { window.Hairline.settle(document); }
        });
        observer.observe(app, { childList: true, subtree: true });
    }

    function start() {
        if (started || typeof Blazor === "undefined") { return; }
        started = true;
        holdStaticPage();
        Blazor.start();
    }

    function dataSaverActive() {
        var connection = navigator.connection
            || navigator.mozConnection
            || navigator.webkitConnection;
        if (!connection) { return false; }
        if (connection.saveData) { return true; }
        // Matches "2g" and "slow-2g".
        return (connection.effectiveType || "").indexOf("2g") !== -1;
    }

    window.addEventListener("load", function () {
        if (dataSaverActive()) { return; }

        if (typeof window.requestIdleCallback === "function") {
            window.requestIdleCallback(start, { timeout: 4000 });
        } else {
            window.setTimeout(start, 1200);
        }
    });
})();
