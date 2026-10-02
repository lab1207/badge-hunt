"""Badge progress for any GitHub user: earned wall plus exact next steps.

Usage:
    python badge_hunt.py lab1207

Achievements have no API, so the earned wall is parsed from the public
profile page (no auth needed). Counts that drive badges (own-repo stars,
merged PRs) come from `gh api`. Tier thresholds GitHub does not publish
are marked approximate.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import urllib.request

WALL = "https://github.com/{user}?tab=achievements"

GUIDE = [
    ("Quickdraw", "Close an issue or PR within 5 minutes of opening it."),
    ("YOLO", "Merge a PR on your own repo with no review."),
    ("Pull Shark", "Merge pull requests. More merges, higher tiers."),
    ("Pair Extraordinaire", "Merge PRs with Co-authored-by trailers from a partner."),
    ("Galaxy Brain", "Get discussion answers marked accepted."),
    ("Starstruck", "Earn stars on your own repos (first tier ~16)."),
    ("Public Sponsor", "Sponsor an open-source developer."),
]


def fetch_wall(user: str) -> dict:
    req = urllib.request.Request(WALL.format(user=user), headers={"User-Agent": "badge-hunt"})
    try:
        html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")
    except Exception as exc:
        return {"error": str(exc)}
    found: dict = {}
    for name in re.findall(r"Achievement: ([A-Za-z ]+)", html):
        found[name] = found.get(name, 0) + 1
    tiers: dict = {}
    for name, mult in re.findall(r'alt="Achievement: ([^"]+)"[^>]*/><span[^>]*>x(\d)</span>', html):
        tiers[name] = max(tiers.get(name, 0), int(mult))
    return {"badges": found, "tiers": tiers}


def api(path: str):
    out = subprocess.run(["gh", "api", path], capture_output=True, check=False)
    if out.returncode != 0:
        return None
    try:
        return json.loads(out.stdout.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None


def numbers(user: str) -> dict:
    repos = api(f"users/{user}/repos?per_page=100&type=owner") or []
    own = [r for r in repos if isinstance(r, dict) and not r.get("fork")]
    stars = sorted(
        ((r.get("stargazers_count", 0), r.get("name")) for r in own), reverse=True
    )
    merged = 0
    page = 1
    while True:
        items = api(
            f"search/issues?q=author:{user}+type:pr&per_page=100&page={page}"
        )
        if not items or not items.get("items"):
            break
        merged += sum(1 for i in items["items"] if i.get("pull_request", {}).get("merged_at"))
        if len(items["items"]) < 100 or page >= 3:
            break
        page += 1
    return {"top_stars": stars[:5], "merged_prs": merged}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="GitHub badge progress.")
    ap.add_argument("user")
    args = ap.parse_args(argv)
    wall = fetch_wall(args.user)
    if "error" in wall:
        print(f"wall fetch failed: {wall['error']}")
        return 1
    earned = wall["badges"]
    print(f"# badge-hunt: {args.user}\n")
    print("Earned: " + (", ".join(sorted(earned)) if earned else "none yet"))
    nums = numbers(args.user)
    print(f"Merged PRs: {nums['merged_prs']}")
    print("Top own-repo stars: " + ", ".join(f"{n} ({s})" for s, n in nums["top_stars"] or [("—", 0)]))
    print("\nNext:")
    for name, how in GUIDE:
        if name not in earned:
            print(f"- [ ] {name}: {how}")
        else:
            tier = wall["tiers"].get(name)
            print(f"- [x] {name}" + (f" (x{tier})" if tier else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
