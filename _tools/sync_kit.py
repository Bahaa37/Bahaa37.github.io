"""Vendor the Hairline design-system kit into the site.

The kit is developed in its own private repository (bahaa37/hairline-kit) so it can be reused in
other projects. The site cannot pull from a private repo in CI, so the built files are copied here
and committed: they are served publicly anyway, so vendoring exposes nothing new.

    python _tools/sync_kit.py ../hairline-kit

Never hand-edit src/Cv.Web/wwwroot/kit/. Change the kit, rebuild it, then run this again; the
VERSION file records which kit commit the copy came from, so drift is visible in review.
"""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEST = ROOT / "src" / "Cv.Web" / "wwwroot" / "kit"
FILES = {"dist/hairline.css": "hairline.css", "src/hairline.js": "hairline.js"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("kit", type=Path, help="path to the hairline-kit checkout")
    kit = parser.parse_args().kit.resolve()

    # Build first so a stale dist/ can never be vendored. The build also enforces the kit's own
    # guards (size budget, no color-mix, no "</" that would break the inlined <style>).
    subprocess.run(["node", "scripts/build.mjs"], cwd=kit, check=True)

    DEST.mkdir(parents=True, exist_ok=True)
    for src, dst in FILES.items():
        shutil.copyfile(kit / src, DEST / dst)

    sha = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=kit,
                         capture_output=True, text=True).stdout.strip() or "uncommitted"
    dirty = subprocess.run(["git", "status", "--porcelain"], cwd=kit,
                           capture_output=True, text=True).stdout.strip()
    (DEST / "VERSION").write_text(f"{sha}{'+dirty' if dirty else ''}\n", encoding="utf-8")
    print(f"kit {sha}{' (dirty)' if dirty else ''} -> {DEST.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
