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

    function start() {
        if (started || typeof Blazor === "undefined") { return; }
        started = true;
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
