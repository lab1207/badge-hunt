# badge-hunt

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org)
[![No dependencies](https://img.shields.io/badge/deps-stdlib%20only-orange.svg)](badge_hunt.py)

**Badge progress for any GitHub user: earned wall plus exact next steps.** Achievements have no API, so the wall is parsed from the public profile page; counts come from `gh api`.

## Sample output

```
# badge-hunt: lab1207

Earned: Quickdraw
Merged PRs: 2
Top own-repo stars: AI-Website-Builder (3), laya-hands (0), lab1207 (0)

Next:
- [x] Quickdraw
- [ ] YOLO: Merge a PR on your own repo with no review.
- [ ] Pull Shark: Merge pull requests. More merges, higher tiers.
- [ ] Pair Extraordinaire: Merge PRs with Co-authored-by trailers from a partner.
- [ ] Galaxy Brain: Get discussion answers marked accepted.
- [ ] Starstruck: Earn stars on your own repos (first tier ≈16).
- [ ] Public Sponsor: Sponsor an open-source developer.
```

## Use

```bash
python badge_hunt.py <username>   # needs gh CLI authed (for counts only)
```

Wall parsing needs no auth. Tier thresholds GitHub doesn't publish are marked approximate.

## Verified against

`jaredpalmer` (8 badges + tiers), `ColeMurray` (6 + tiers), `lab1207`.

## Contributing

Small, scoped PRs. Stdlib only.

## License

[MIT](LICENSE)
