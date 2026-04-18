"""Download Valorant map splash images from valorant-api.com.

All images are copyright Riot Games and are not covered by this project's MIT license.
Run this script once after cloning to populate assets/maps/.

Usage:
    uv run python scripts/download_maps.py
"""

import json
import time
import urllib.request
from pathlib import Path

API_URL = "https://valorant-api.com/v1/maps"
DEST = Path(__file__).parent.parent / "assets" / "maps"

# Map display name -> local filename (must match MAP_IMAGE_FILES in cogs/map_roulette.py)
TARGETS: dict[str, str] = {
    # Standard
    "Ascent": "ascent.png",
    "Abyss": "abyss.png",
    "Bind": "bind.png",
    "Breeze": "breeze.png",
    "Fracture": "fracture.png",
    "Haven": "haven.png",
    "Icebox": "icebox.png",
    "Lotus": "lotus.png",
    "Pearl": "pearl.png",
    "Split": "split.png",
    "Sunset": "sunset.png",
    # Team Deathmatch
    "District": "district.png",
    "Drift": "drift.png",
    "Kasbah": "kasbah.png",
    "Piazza": "piazza.png",
    # Skirmish (A/B/C share the same splash image)
    "Skirmish A": "skirmish_a.png",
}


def main() -> None:
    """Fetch and save map splash images."""
    DEST.mkdir(parents=True, exist_ok=True)

    print("Fetching map list from valorant-api.com ...")
    with urllib.request.urlopen(API_URL) as resp:
        data = json.loads(resp.read())

    api_map: dict[str, str] = {
        m["displayName"]: m["splash"]
        for m in data["data"]
        if m.get("displayName") and m.get("splash")
    }

    ok = skipped = failed = 0
    for name, filename in TARGETS.items():
        dest_path = DEST / filename
        if dest_path.exists():
            print(f"  SKIP  {filename} (already exists)")
            skipped += 1
            continue

        url = api_map.get(name)
        if not url:
            print(f"  MISS  {name} (not found in API)")
            failed += 1
            continue

        try:
            urllib.request.urlretrieve(url, dest_path)
            size_kb = dest_path.stat().st_size // 1024
            print(f"  OK    {filename} ({size_kb} KB)")
            ok += 1
        except Exception as e:
            print(f"  FAIL  {filename}: {e}")
            failed += 1

        time.sleep(0.1)

    print(f"\nDone — {ok} downloaded, {skipped} skipped, {failed} failed")


if __name__ == "__main__":
    main()
