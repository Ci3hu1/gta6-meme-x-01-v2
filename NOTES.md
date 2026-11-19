# Notes — gta6-meme-x-01 v2

## Bounty

- "Post a GTA 6 meme on X", $500, FREE, 50 paid places.
- Closes 23 Nov 2026 21:00 WIB / 14:00 UTC. Results 8 Dec 2026.
- Play code: `makefun-mole-gorilla-geyser`. Post from @ci3hu1 (public).
- Kit level 20, fresh download 19 Nov 2026. Transcripts go via kit BUNDLE
  (harness program/v1), not the strict-transcripts record route.

## Live top 10 (fresh, 19 Nov ~23:45 WIB, field 566, judge score = dev win rate)

1. meongs123 — "TOTAL DUE: /bin/bash.00 — Leonida Mart Receipt" — 857,650
2. rapid-badger-53 — "Marine Corona" — 848,244
3. tak-attack — "Lucia Wasn't the Only One Released Today" — 828,964
4. gaiaoagoaia-art — "Waited 13 years for GTA VI. Called in sick. My boss is 3 spots ahead of me in line." — 826,313
5. nimble-badger-62 — "Leonida Fever" — 803,262
6. andryrohul — "WAITED 13 YEARS. CALLED IN SICK. STILL DOWNLOADING." — 803,092
7. leeseo — "99% SINCE 2013" — 802,740
8. sampurna00123 — "After 13 Years, the Bill Arrives — My Agent Won It on make.fun" — 800,629
9. raphael — "WAITED 13 YEARS FOR GTA VI — DIED WAITING. CAME BACK FOR LAUNCH DAY." — 789,945
10. luhut — "Cardinal Sonar" — 787,584

Pattern: the judge rewards ONE sharp joke. Sick-note ranks 4 and 6;
receipt/bill 1 and 8; "99% since 2013" 7; agent-won-it 8; died-waiting 9.

## v1 live state

- Submitted 19 Nov ~22:58 WIB (repo Ci3hu1/gta6-meme-x-01, submission
  01a1f487-92b7-772c-846a-7ef2b530e56f, round 1): stage scored, no failing
  checks, dev grade provisional win rate 0.591 (3W/2D/7L), NOT in the live
  top 10. Joke was a tombstone ("WE GOT PAID BEFORE GTA 6") — too diffuse.

## v2 direction

- Sick-note angle, original punchline: "MY SICK NOTE SAYS GTA 6 / MY BOSS
  SIGNED IT." Ghost prominent (real ghost from the press splash), money bag
  for the paid angle, Vice City sunset, GTA 6-true, clean.
- Quota at build time: day cap 3, taken 1, left 2 (UTC day resets 07:00 WIB
  20 Nov); max 5 submissions per competition, 1 used. Quota check only in
  this job — no post, no submit.
- Status: built, NOT posted, NOT submitted. Posting + submitting wait for
  Joni's 'Setuju' on this exact v2 meme + post text.

## Ghost fix (20 Nov ~00:30 WIB)

- Joni: "Perbaiki dulu gambar ghostnya" — the v2 ghost's right edge was a
  flat vertical cut (compose.py flood-fill cut the splash at x > 625) and
  the ghost was cropped at the frame edge.
- Fix: ghost now rendered at high resolution from the official vector logo
  (assets/ghost-logo.svg, light variant; magenta coin removed — the money
  bag already carries the paid angle and the coin would collide with it).
  Rendered with cairosvg at 2400 px, cropped to the opaque bbox + margin,
  stored as assets/ghost.png (1909x1971). compose.py no longer cuts the
  splash — it loads the pre-rendered ghost. Full figure, clean outline on
  every side, fully inside the frame. Everything else unchanged: same joke
  text, scene, note, money bag, watermark, layout.
- Verified visually at 1200x675 and at judge shrink 768x480: ghost outline
  clean, no flat cut, no crop, text sharp, make.fun clear.
- Kit check (fresh kit level 20): 0 failures. Quota re-checked, NOT submitted.
