/* Hairline — zero-dependency motion & interaction engine (docs/spec.md §3).
   The CSS in src/*.css is the contract: every class this file drives
   (html.hl-motion, .is-visible, .is-entering, .is-active, .is-running,
   .hl-tabs--enhanced) and every keyframe exists there first.
   Visible by default: `hl-motion` lands on <html> only when an
   IntersectionObserver exists AND motion is allowed, and every hidden state
   in the CSS lives under that class, so dead JS still shows all content.
   init() is idempotent and re-scannable (data-hl-ready flags); destroy()
   undoes exactly what init() did under its root. State lives in WeakMaps and
   every timer first checks el.isConnected, so a node dropped by a re-render
   tears itself down instead of firing. Node imports must not touch the DOM. */

const version = '0.1.0';
const HAS_DOM = typeof document !== 'undefined';

/* ── bookkeeping ── */

const live = new WeakMap();     // el -> { timers, disposers, listeners }
const consoles = new WeakMap(); // [data-hl-console] -> behaviour state
const tabs = new WeakMap();     // [data-hl-tabs] -> behaviour state

function stateOf(el) {
  let s = live.get(el);
  if (!s) live.set(el, (s = { timers: new Set(), disposers: new Set(), listeners: [] }));
  return s;
}
/* One attribute can carry several features (an element may be a reveal
   target AND a console), so flags are space-separated words. */
function claim(el, what) {
  const v = el.dataset.hlReady || '';
  if (v.includes(what)) return false;
  el.dataset.hlReady = v ? `${v} ${what}` : what;
  return true;
}
function later(el, fn, ms) {
  const s = stateOf(el);
  const id = setTimeout(() => {
    s.timers.delete(id);
    if (!el.isConnected) { teardown(el); return; }
    fn();
  }, ms);
  s.timers.add(id);
  return id;
}
function listen(el, target, type, fn, opts) {
  stateOf(el).listeners.push({ target, type, fn, opts });
  target.addEventListener(type, fn, opts);
}
const setA = (el, pairs) => { for (const [k, v] of Object.entries(pairs)) el.setAttribute(k, v); };
function teardown(el) {
  const s = live.get(el);
  if (!s) return;
  s.timers.forEach((id) => clearTimeout(id));
  s.disposers.forEach((d) => d());
  s.listeners.forEach((l) => l.target.removeEventListener(l.type, l.fn, l.opts));
  consoles.delete(el);
  tabs.delete(el);
  live.delete(el);
  el.removeAttribute('data-hl-ready');
}
const fire = (el, name, detail) => el.dispatchEvent(new CustomEvent(name, { bubbles: true, detail }));
const all = (root, sel) => (root.matches && root.matches(sel) ? [root] : []).concat([...root.querySelectorAll(sel)]);

let motionQuery = null;
function reduced() {
  if (!HAS_DOM || typeof window.matchMedia !== 'function') return false;
  motionQuery ||= window.matchMedia('(prefers-reduced-motion: reduce)');
  return motionQuery.matches;
}
const motionAllowed = () => HAS_DOM && 'IntersectionObserver' in window && !reduced();

/* Autoplay pauses for the same four reasons everywhere: pointer over the
   component, focus inside it, offscreen, document hidden. */
function wirePauses(el, onHold) {
  onHold('hidden', document.hidden);
  listen(el, document, 'visibilitychange', () => onHold('hidden', document.hidden));
  for (const [type, reason, on] of [['pointerenter', 'hover', true], ['pointerleave', 'hover', false],
    ['focusin', 'focus', true], ['focusout', 'focus', false]]) {
    listen(el, el, type, () => onHold(reason, on));
  }
  if (motionAllowed() && 'IntersectionObserver' in window) {
    const io = new IntersectionObserver(([e]) => onHold('offscreen', !e.isIntersecting));
    io.observe(el);
    stateOf(el).disposers.add(() => io.disconnect());
  }
}

/* ── motion gate + reveal ── */

let revealIO = null;
/* Threshold MUST stay 0 and the fold offset lives in rootMargin: a ratio
   threshold never fires for an element taller than the viewport, which hid
   whole sections on mobile in a previous project. */
function observer() {
  revealIO ||= new IntersectionObserver(
    (entries) => { for (const e of entries) if (e.isIntersecting) show(e.target); },
    { threshold: 0, rootMargin: '0px 0px -80px 0px' });
  return revealIO;
}
function show(el) {
  if (revealIO) revealIO.unobserve(el);
  el.classList.add('is-visible');
  fire(el, 'hl:reveal', { el });
}
/* Sweep: anything whose top is already above the viewport bottom is revealed
   directly — deep links and fast scrolls can outrun the observer. */
function sweep() {
  if (!HAS_DOM || !motionAllowed()) return;
  const vh = window.innerHeight || document.documentElement.clientHeight;
  for (const el of document.querySelectorAll('[data-hl-reveal]:not(.is-visible)')) {
    const r = el.getBoundingClientRect();
    // An unrendered element (inside a display:none container, e.g. a framework
    // rendering offscreen before a handover) has an all-zero box: it is not
    // "above the fold", it is nowhere yet. Leave it for the observer.
    if (!r.width && !r.height) continue;
    if (r.top < vh) show(el);
  }
}
function initReveal(el) {
  if (!claim(el, 'reveal')) return;
  if (el.dataset.hlReveal === 'list') {
    let i = 0; // stagger index for the CSS 60ms steps; markup may override
    for (const child of el.children) {
      if (!child.style.getPropertyValue('--i')) child.style.setProperty('--i', String(i));
      i++;
    }
  }
  if (!motionAllowed()) return; // without hl-motion the CSS keeps it visible
  observer().observe(el);
  stateOf(el).disposers.add(() => revealIO && revealIO.unobserve(el));
}

const globals = { on: false, undo: [] };
function startGlobals() {
  if (globals.on || !HAS_DOM) return;
  globals.on = true;
  // Scroll-end: the real event where it exists, a short debounce elsewhere.
  let settle = 0;
  const onScroll = () => { clearTimeout(settle); settle = setTimeout(sweep, 180); };
  const hasEnd = 'onscrollend' in window;
  const type = hasEnd ? 'scrollend' : 'scroll';
  const handler = hasEnd ? sweep : onScroll;
  window.addEventListener(type, handler, { passive: true });
  reduced(); // cache the query before listening to it
  motionQuery.addEventListener('change', syncMotion);
  globals.undo.push(() => {
    clearTimeout(settle);
    window.removeEventListener(type, handler);
    if (motionQuery) motionQuery.removeEventListener('change', syncMotion);
  });
  syncMotion();
}
function stopGlobals() {
  globals.undo.forEach((f) => f());
  globals.undo = [];
  globals.on = false;
  if (revealIO) { revealIO.disconnect(); revealIO = null; }
  document.documentElement.classList.remove('hl-motion');
}
/* The single switch for html.hl-motion, plus what a flip means for live
   components: leaving motion completes everything in place; entering it
   restarts the machines that were running. */
function syncMotion() {
  const on = motionAllowed();
  document.documentElement.classList.toggle('hl-motion', on);
  for (const el of document.querySelectorAll('[data-hl-console]')) {
    const st = consoles.get(el);
    if (!st) continue;
    if (on) { if (st.chips.length) queueNext(el, st.active); }
    else { clearTimeout(st.wait); st.wait = 0; st.owed = false; finishTyping(el); }
  }
  for (const el of document.querySelectorAll('[data-hl-tabs]')) {
    const st = tabs.get(el);
    if (st && on && !st.stopped && !st.userPaused && st.reasons.size === 0) startCycle(el);
    else if (st && !on) pauseCycle(el);
  }
  if (on) {
    for (const el of document.querySelectorAll('[data-hl-reveal]:not(.is-visible)')) observer().observe(el);
    for (const el of document.querySelectorAll('[data-hl-marquee]')) initMarquee(el);
  } else {
    for (const el of document.querySelectorAll('[data-hl-reveal]')) show(el);
  }
}

/* ── console ── */

function initConsole(el) {
  if (!claim(el, 'console')) return;
  const log = el.querySelector('.hl-window__log');
  if (!log) return;
  // chip order is the autoplay order; templates hold one run each
  const st = { log, chips: [...el.querySelectorAll('[data-hl-run]')], templates: new Map(),
    interval: parseInt(el.dataset.hlInterval, 10) || 6000,
    active: null, typing: null, wait: 0, owed: false, reasons: new Set() };
  for (const t of el.querySelectorAll('template[data-hl-run-id]')) st.templates.set(t.dataset.hlRunId, t);
  consoles.set(el, st);
  markChip(el, st.chips[0] && st.chips[0].dataset.hlRun); // the static log already shows run #1
  log.setAttribute('aria-live', 'off'); // an autoplaying live region would chatter
  for (const chip of st.chips) {
    listen(el, chip, 'click', (e) => {
      // Modifier clicks keep native link behaviour ("open in new tab").
      if (e.ctrlKey || e.metaKey || e.shiftKey || e.altKey || e.button === 1) return;
      e.preventDefault(); // the result line carries the real link
      runConsole(el, chip.dataset.hlRun, 'user');
    });
  }
  wirePauses(el, (r, a) => holdConsole(el, r, a));
  if (motionAllowed() && st.chips.length) queueNext(el, st.chips[0].dataset.hlRun);
}
function markChip(el, id) {
  const st = consoles.get(el);
  if (!st) return;
  st.active = id;
  for (const c of st.chips) {
    const on = c.dataset.hlRun === id;
    c.classList.toggle('is-active', on);
    setA(c, { 'aria-pressed': String(on) });
  }
}
function holdConsole(el, reason, active) {
  const st = consoles.get(el);
  if (!st) return;
  if (active) {
    st.reasons.add(reason);
    if (st.wait) { clearTimeout(st.wait); st.wait = 0; st.owed = true; }
  } else {
    st.reasons.delete(reason);
    if (st.owed && st.reasons.size === 0) { st.owed = false; queueNext(el, st.active); }
  }
}
function queueNext(el, fromId) {
  const st = consoles.get(el);
  if (!st || !st.chips.length) return;
  clearTimeout(st.wait);
  const i = Math.max(0, st.chips.findIndex((c) => c.dataset.hlRun === fromId));
  const next = st.chips[(i + 1) % st.chips.length];
  st.wait = later(el, () => { st.wait = 0; runConsole(el, next.dataset.hlRun, 'auto'); }, st.interval);
}
function runConsole(el, id, source) {
  const st = consoles.get(el);
  const tpl = st && st.templates.get(id);
  if (!tpl) return;
  finishTyping(el); // a run already typing completes instantly first
  markChip(el, id);
  st.log.setAttribute('aria-live', source === 'user' ? 'polite' : 'off');
  fire(el, 'hl:console-run', { id, source });
  // Frameworks that build DOM node by node (Blazor, some Angular paths) put a
  // template's lines in as direct children, never into .content; read either.
  const lines = [...(tpl.content.children.length ? tpl.content.children : tpl.children)];
  if (!motionAllowed()) { // reduced motion: swap in the complete run at once
    for (const node of lines) appendLine(el, node);
    return;
  }
  let i = 0;
  const step = () => {
    appendLine(el, lines[i]);
    i++;
    if (i < lines.length) st.typing = { lines, at: i, timer: later(el, step, 450) };
    else {
      st.typing = null;
      if (st.reasons.size) st.owed = true; // paused mid-cycle: resume later
      else queueNext(el, st.active);
    }
  };
  step(); // the first line lands immediately
}
function appendLine(el, node) {
  const line = node.cloneNode(true); // templates run repeatedly
  line.classList.add('is-entering'); // state hook; the CSS animates insertion itself
  const log = consoles.get(el).log;
  log.appendChild(line);
  /* The log is bottom-anchored: old lines leave through the top, cap at 12. */
  while (log.children.length > 12) log.firstElementChild.remove();
}
function finishTyping(el) {
  const st = consoles.get(el);
  if (!st || !st.typing) return;
  clearTimeout(st.typing.timer);
  for (const node of st.typing.lines.slice(st.typing.at)) appendLine(el, node);
  st.typing = null;
}

/* ── tabs ── */

function initTabs(el) {
  if (!claim(el, 'tabs')) return;
  const list = el.querySelector('.hl-tabs__list');
  if (!list) return;
  const st = { list, tabs: [...list.querySelectorAll('[data-hl-tab]')], panels: new Map(),
    count: el.querySelector('.hl-tabs__count'), ringBtn: el.querySelector('.hl-ring__btn'),
    bar: el.querySelector('.hl-ring__bar'), interval: parseInt(el.dataset.hlAutoplay, 10) || 7000,
    index: 0, timer: 0, reasons: new Set(), userPaused: false, stopped: false };
  tabs.set(el, st);
  // Enhance: reveal the pre-rendered chrome and hide the inactive panels —
  // the one place the kit hides statically-visible content.
  const controls = el.querySelector('.hl-tabs__controls');
  list.removeAttribute('hidden');
  if (controls) controls.removeAttribute('hidden');
  el.classList.add('hl-tabs--enhanced');
  setA(list, { role: 'tablist' });
  st.tabs.forEach((tab, i) => {
    const id = tab.dataset.hlTab;
    const panel = el.querySelector(`[data-hl-panel="${id}"]`);
    if (!panel) return;
    st.panels.set(tab, panel);
    if (!tab.id) tab.id = `hl-tab-${id}`;
    if (!panel.id) panel.id = `hl-panel-${id}`;
    setA(tab, { role: 'tab', 'aria-controls': panel.id });
    setA(panel, { role: 'tabpanel', 'aria-labelledby': tab.id, tabindex: '0' });
    listen(el, tab, 'click', () => selectTab(el, i, 'user'));
  });
  listen(el, list, 'keydown', (e) => {
    const n = st.tabs.length;
    const moves = { ArrowRight: (st.index + 1) % n, ArrowLeft: (st.index - 1 + n) % n, Home: 0, End: n - 1 };
    const i = e.key in moves ? moves[e.key] : -1;
    if (i < 0 || !st.tabs[i]) return;
    e.preventDefault();
    selectTab(el, i, 'user'); // focus follows selection
    st.tabs[i].focus();
  });
  if (st.ringBtn) {
    listen(el, st.ringBtn, 'click', () => {
      if (st.stopped || !motionAllowed()) return;
      st.userPaused = !st.userPaused;
      if (st.userPaused) pauseCycle(el); else startCycle(el);
      syncRingBtn(el);
      fire(el, 'hl:autoplay', { el, playing: !st.userPaused });
    });
  }
  wirePauses(el, (r, a) => holdTabs(el, r, a));
  selectTab(el, 0, 'init');
  syncRingBtn(el);
  if (motionAllowed() && st.interval) startCycle(el);
}
function selectTab(el, i, source) {
  const st = tabs.get(el);
  const tab = st && st.tabs[i];
  if (!tab) return;
  st.index = i;
  for (const t of st.tabs) {
    const on = t === tab;
    setA(t, { 'aria-selected': String(on) });
    t.tabIndex = on ? 0 : -1; // roving tabindex
    const panel = st.panels.get(t);
    if (panel) panel.hidden = !on;
  }
  const panel = st.panels.get(tab);
  if (source !== 'init' && panel) {
    panel.classList.remove('is-entering'); // retrigger the scene swap:
    void panel.offsetWidth;                // class out, reflow, class in
    panel.classList.add('is-entering');
  }
  if (st.count) st.count.textContent = `${i + 1} / ${st.tabs.length}`;
  // Horizontal only, never the page: scrollIntoView would move the viewport.
  const view = st.list;
  const within = tab.getBoundingClientRect().left - view.getBoundingClientRect().left + view.scrollLeft;
  view.scrollTo({ left: Math.max(0, within - (view.clientWidth - tab.offsetWidth) / 2) });
  if (source !== 'init') fire(el, 'hl:tab-change', { index: i, id: tab.dataset.hlTab, source });
  if (source === 'user') stopCycle(el); // first manual pick ends autoplay for good
}
/* The ring's custom property cannot interpolate (unregistered), so the arc is
   driven directly on stroke-dashoffset with an inline transition matching the
   slot duration; the property is kept in sync as a declarative mirror. */
function drawRing(el, restart) {
  const st = tabs.get(el);
  if (!st || !st.bar) return;
  const bar = st.bar;
  bar.style.transition = 'none';
  if (!restart) return; // freeze wherever the arc is
  bar.style.strokeDashoffset = '100';
  bar.style.setProperty('--hl-ring-progress', '0');
  void bar.getBoundingClientRect(); // commit the reset before transitioning
  bar.style.transition = `stroke-dashoffset ${st.interval}ms linear`;
  bar.style.strokeDashoffset = '0';
  bar.style.setProperty('--hl-ring-progress', '1');
}
function startCycle(el) {
  const st = tabs.get(el);
  if (!st || st.stopped || st.userPaused || st.reasons.size || !st.tabs.length) return;
  clearTimeout(st.timer);
  drawRing(el, true);
  st.timer = later(el, () => {
    st.timer = 0;
    selectTab(el, (st.index + 1) % st.tabs.length, 'auto');
    if (!st.stopped) startCycle(el);
  }, st.interval);
}
function pauseCycle(el) {
  const st = tabs.get(el);
  if (!st) return;
  clearTimeout(st.timer);
  st.timer = 0;
  drawRing(el, false);
}
function stopCycle(el) {
  const st = tabs.get(el);
  if (!st || st.stopped) return;
  pauseCycle(el);
  st.stopped = true;
  if (st.ringBtn) st.ringBtn.setAttribute('aria-disabled', 'true');
}
function holdTabs(el, reason, active) {
  const st = tabs.get(el);
  if (!st) return;
  if (active) {
    st.reasons.add(reason);
    pauseCycle(el);
  } else {
    st.reasons.delete(reason);
    if (st.timer === 0 && !st.userPaused && !st.stopped && st.reasons.size === 0 && motionAllowed()) startCycle(el);
  }
}
function syncRingBtn(el) {
  const st = tabs.get(el);
  if (!st || !st.ringBtn) return;
  const playing = !st.userPaused && !st.stopped && motionAllowed();
  setA(st.ringBtn, { 'aria-label': playing ? 'Pause autoplay' : 'Play autoplay', 'aria-pressed': String(!playing) });
  const pause = st.ringBtn.querySelector('.hl-ring__icon--pause');
  const play = st.ringBtn.querySelector('.hl-ring__icon--play');
  if (pause) pause.hidden = !playing;
  if (play) play.hidden = playing;
}

/* ── marquee ── */

function initMarquee(el) {
  if (!claim(el, 'marquee')) return;
  if (!motionAllowed()) return; // no clones: the reduced-motion row wraps once
  const track = el.querySelector('.hl-marquee__track');
  if (!track || track.dataset.hlCloned) return;
  track.dataset.hlCloned = '1';
  for (const child of [...track.children]) {
    const clone = child.cloneNode(true);
    setA(clone, { 'aria-hidden': 'true', 'data-hl-clone': '' });
    // Clones are scenery: keep anything focusable out of the tab order.
    for (const f of clone.querySelectorAll('a, button, input, select, textarea, [tabindex]')) {
      f.setAttribute('tabindex', '-1');
    }
    track.appendChild(clone);
  }
  track.classList.add('is-running');
  const pace = () => {
    if (!el.isConnected) { teardown(el); return; }
    const speed = parseFloat(el.dataset.hlSpeed) || 40; // px per second
    const loop = track.scrollWidth / 2; // two copies: one copy is the travel
    track.style.animationDuration = `${Math.max(8, Math.round(loop / speed))}s`;
  };
  pace();
  let t = 0;
  const repace = () => { clearTimeout(t); t = setTimeout(() => (el.isConnected ? pace() : teardown(el)), 200); };
  listen(el, window, 'resize', repace, { passive: true });
  stateOf(el).disposers.add(() => clearTimeout(t));
}

/* ── api ── */

/* Entrances (.hl-enter) play once per page load. After they have had time to
   finish, html.hl-entered switches them off, so a framework re-rendering the
   same markup (Blazor replacing #app, an Angular route re-entering) shows it
   settled instead of blinking it out and animating it in a second time. */
const ENTRANCE_MS = 2000;
let enteredTimer = 0;
function scheduleEntered() {
  const html = document.documentElement;
  if (enteredTimer || html.classList.contains('hl-entered')) return;
  enteredTimer = setTimeout(() => html.classList.add('hl-entered'), motionAllowed() ? ENTRANCE_MS : 0);
}

/* For handovers: a framework has just swapped a pre-rendered page for its own
   render of the same content. Everything already on screen must simply be there,
   so reveals at or above the fold are shown with transitions suppressed for one
   frame, and entrances are marked as already played. */
function settle(root = document) {
  if (!HAS_DOM) return;
  const html = document.documentElement;
  clearTimeout(enteredTimer); enteredTimer = 1;
  html.classList.add('hl-entered', 'hl-instant');
  init(root);
  void html.offsetHeight; // commit the instant styles before transitions return
  requestAnimationFrame(() => requestAnimationFrame(() => html.classList.remove('hl-instant')));
}

function init(root = document) {
  if (!HAS_DOM) return;
  startGlobals();
  scheduleEntered();
  for (const el of all(root, '[data-hl-reveal]')) initReveal(el);
  for (const el of all(root, '[data-hl-console]')) initConsole(el);
  for (const el of all(root, '[data-hl-tabs]')) initTabs(el);
  for (const el of all(root, '[data-hl-marquee]')) initMarquee(el);
  sweep();
}
function destroy(root = document) {
  if (!HAS_DOM) return;
  for (const el of all(root, '[data-hl-ready]')) teardown(el);
  if (root === document) stopGlobals();
}

const Hairline = { init, destroy, settle, version };

if (HAS_DOM) {
  globalThis.Hairline = Hairline;
  // Blazor reaches globalThis.Hairline; Angular sets data-hl-manual on <html>
  // and calls init itself after its own bootstrap.
  const auto = () => { if (!document.documentElement.hasAttribute('data-hl-manual')) init(document); };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', auto, { once: true });
  else auto();
}

export { init, destroy, settle, version };
