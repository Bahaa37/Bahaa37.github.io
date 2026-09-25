"""One-off behavior checks for the two 2026-09-24 score-3 residuals.

Runs against the dev server (dotnet run, :5046) and asserts, in a real browser:

  back-to-top  — absent at rest, shown after ~1 viewport, clear of the contact dock,
                 works by mouse and by keyboard, instant under reduced motion
  scroll-spy   — rest state clears, correct link marks mid-page, and the marker
                 clears on client-side navigation away from home (the null-deref fix)
  chrome       — no console errors anywhere along the way

Usage: python _tools/verify_backtotop_spy.py [base-url]
"""
import sys
from playwright.sync_api import sync_playwright

BASE = (sys.argv[1] if len(sys.argv) > 1 else "http://localhost:5046").rstrip("/")
failures = []


def check(name, ok, detail=""):
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  [{detail}]" if detail else ""))
    if not ok:
        failures.append(name)


def shown(page):
    return page.evaluate(
        "() => { const b = document.querySelector('.back-to-top');"
        " return b ? getComputedStyle(b).display !== 'none' : null; }"
    )


def boxes_overlap(a, b):
    return not (a["x"] + a["width"] <= b["x"] or b["x"] + b["width"] <= a["x"]
                or a["y"] + a["height"] <= b["y"] or b["y"] + b["height"] <= a["y"])


def run(page, errors, width, height, label):
    page.set_viewport_size({"width": width, "height": height})
    page.goto(BASE + "/", wait_until="domcontentloaded")
    page.wait_for_selector(".contact-dock", state="attached", timeout=60000)

    # --- back-to-top: rest state, threshold, aria, dock clearance -------------
    check(f"{label}: back-to-top hidden at top", shown(page) is False,
          f"display={shown(page)}")

    inner_h = page.evaluate("() => window.innerHeight")
    page.evaluate(f"() => window.scrollTo(0, {inner_h} * 0.9)")
    page.wait_for_timeout(250)
    check(f"{label}: hidden at 0.9 viewport", shown(page) is False)

    page.evaluate(f"() => window.scrollTo(0, {inner_h} * 1.1)")
    page.wait_for_timeout(250)
    check(f"{label}: shown past 1 viewport", shown(page) is True)

    aria = page.get_attribute(".back-to-top", "aria-label")
    check(f"{label}: aria-label", aria == "Back to top", str(aria))

    btn = page.locator(".back-to-top").bounding_box()
    dock = page.locator(".contact-dock").bounding_box()
    check(f"{label}: clears the contact dock", btn and dock and not boxes_overlap(btn, dock),
          f"btn={btn} dock={dock}")

    page.screenshot(path=f".impeccable/review/backtotop-{label}.png")

    # --- mouse click returns to top ------------------------------------------
    page.click(".back-to-top")
    page.wait_for_function("() => window.scrollY === 0", timeout=4000)
    page.wait_for_timeout(250)
    check(f"{label}: click returns to top", page.evaluate("() => window.scrollY") == 0)
    check(f"{label}: hidden again at top", shown(page) is False)

    # --- keyboard reachability -------------------------------------------------
    page.evaluate(f"() => window.scrollTo(0, {inner_h} * 2)")
    page.wait_for_timeout(250)
    page.focus(".back-to-top")
    page.keyboard.press("Enter")
    page.wait_for_function("() => window.scrollY === 0", timeout=4000)
    check(f"{label}: keyboard Enter returns to top", page.evaluate("() => window.scrollY") == 0)

    # --- scroll-spy ------------------------------------------------------------
    page.evaluate("() => window.scrollTo(0, 0)")
    page.wait_for_timeout(250)
    spy = page.evaluate(
        "() => [...document.querySelectorAll('.site-nav a.is-current')].map(a => a.textContent)"
    )
    check(f"{label}: spy rest state empty", spy == [], str(spy))

    # Instant jump: the page's html { scroll-behavior: smooth } would otherwise put
    # the assertion mid-flight. The wait covers the reveal settle (0.7s translate)
    # plus the spy's post-settle refresh at 750ms — the state a reader ends up in.
    page.evaluate(
        "() => { const el = document.querySelector('#work');"
        " window.scrollTo(0, el.getBoundingClientRect().top + window.scrollY - 92); }"
    )
    page.wait_for_timeout(1300)
    spy = page.evaluate(
        "() => [...document.querySelectorAll('.site-nav a.is-current')].map(a => a.textContent)"
    )
    check(f"{label}: spy marks Work at #work", spy == ["Work"], str(spy))

    # --- client-side navigation away from home (the null-deref fix) ------------
    # The nav's Testimonials link renders only while a quote exists (it does not),
    # so the crossing happens through a case-study link inside the work section.
    page.click(".case-index__item")
    page.wait_for_url("**/work/**", timeout=15000)
    page.wait_for_timeout(600)
    page.mouse.wheel(0, 400)  # force scroll events on the new route
    page.wait_for_timeout(400)
    spy = page.evaluate(
        "() => [...document.querySelectorAll('.site-nav a.is-current')].map(a => a.textContent)"
    )
    check(f"{label}: spy clears on /work/*", spy == [], str(spy))

    page.goto(BASE + "/work/legacy-modernization", wait_until="domcontentloaded")
    page.wait_for_selector(".contact-dock", state="attached", timeout=60000)
    page.mouse.wheel(0, 800)
    page.wait_for_timeout(400)
    check(f"{label}: no console errors", errors == [], "; ".join(errors[:3]))

    # --- back-to-top exists on the study page too ------------------------------
    page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(300)
    check(f"{label}: shown on /work page", shown(page) is True)
    btn = page.locator(".back-to-top").bounding_box()
    dock = page.locator(".contact-dock").bounding_box()
    check(f"{label}: /work page clears the dock", btn and dock and not boxes_overlap(btn, dock))


with sync_playwright() as p:
    browser = p.chromium.launch()

    for theme in ("light", "dark"):
        errors = []
        ctx = browser.new_context(viewport={"width": 1280, "height": 900})
        page = ctx.new_page()
        page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.add_init_script(f"localStorage.setItem('theme', '{theme}')")
        run(page, errors, 1280, 900, f"desktop-{theme}")
        ctx.close()

    # mobile geometry — the dock spans the full width there, so overlap is likeliest
    errors = []
    ctx = browser.new_context(viewport={"width": 390, "height": 844})
    page = ctx.new_page()
    page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
    page.on("pageerror", lambda e: errors.append(str(e)))
    run(page, errors, 390, 844, "mobile-light")
    ctx.close()

    # reduced motion: click must be an instant jump, not an animation
    ctx = browser.new_context(viewport={"width": 1280, "height": 900}, reduced_motion="reduce")
    page = ctx.new_page()
    page.goto(BASE + "/", wait_until="domcontentloaded")
    page.wait_for_selector(".contact-dock", state="attached", timeout=60000)
    page.evaluate("() => window.scrollTo(0, document.body.scrollHeight * 0.5)")
    page.wait_for_timeout(300)
    page.click(".back-to-top")
    page.wait_for_timeout(120)  # a smooth scroll would still be far from 0 here
    check("reduced-motion: instant jump", page.evaluate("() => window.scrollY") == 0,
          f"scrollY={page.evaluate('() => window.scrollY')}")
    ctx.close()

    browser.close()

print(f"\n{len(failures)} failure(s)" + (": " + ", ".join(failures) if failures else ""))
sys.exit(1 if failures else 0)
