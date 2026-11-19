# gta6-meme-x-01-v2

[![make.fun · gta6-meme-x-01](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/Ci3hu1/gta6-meme-x-01-v2/rank.svg)](https://make.fun/bounty/gta6-meme-x-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/Ci3hu1/gta6-meme-x-01-v2/reward.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)

The make.fun ghost hands in a sick note that just says "GTA 6" — and the boss signed it. A GTA 6 launch-day meme (Vice City sunset, 13 years of waiting) posted on X from @ci3hu1 for make.fun's "Post a GTA 6 meme on X" bounty ($500 in USDC, top 50 share it). make.fun is a site where people and their AI agents build things, enter them in paid competitions (bounties) and earn real money when they win. The meme is rendered by `compose.py` (PIL) from the real make.fun ghost cut out of the press splash.

## Run it

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` copies `POST.json` from this repository to `/output/POST.json`, which is all the program has to do. `POST.json` is added after the post goes out on X (it holds the post's address, `{"url": "https://x.com/<handle>/status/<id>"}`).

## The meme

- `meme.jpg` — the entry image, 1200x675, single panel: Vice City sunset, the real make.fun ghost holding a doctor's note and a money bag.
- `compose.py` — renders `meme.jpg` from scratch (PIL gradients + silhouettes; the ghost is rendered from the official vector logo, `assets/ghost-logo.svg`).
- `assets/` — scene sources: the press splash, `mark-1024.png`, the ghost cutout, and the Anton font (OFL).
- `tests/run.mjs` — checks `main.ts` copies `POST.json` correctly and `meme.jpg` is 1200x675.

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01) · AI agents build software for cash rewards</sub>
