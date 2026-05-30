# CLAUDE.md — Радко speech-therapy game

Project brief for continuing this work in Claude Code. Read `radko_level1.html`
alongside this file; it is heavily commented and the architecture is meant to be
self-explanatory once you have this context.

## What this is

A Bulgarian speech-therapy point-and-click game — **"Приключенията на Радко"**.
Audience: a young, pre-literate child practicing the **Р** sound. Single
self-contained HTML file (vanilla JS, inline CSS, no build step, no external JS
libraries).

**Two engines live in the repo:**
- **`radko.html` — the current game.** Image-backed: each scene is a full-bleed
  16:9 illustration with invisible tap-**hotspots** over the things drawn into the
  art. Covers **Level 1** (voiced) + **Level 2** (silent, baked questions); Level 3
  is locked ("идва скоро"). Edit this one going forward.
- `radko_level1.html` — the original SVG prototype (drawn art + choice cards),
  kept for reference. Superseded.

### Hard constraint
The assignment requires the game be **created using Canva**. The delivery path is:
develop the HTML here → paste the whole file into **Canva Code** ("Use exactly
this code, no changes") → publish via my.canva.site. Canva is the delivery
target, not the engine. Practical consequences that shape every decision:
- Keep it a **single file**, vanilla JS, **no external JS libraries** (Canva
  Code's runtime has unreliable CDNs).
- Stay well under Canva Code's **~1700-line budget** (currently ~600 lines) to
  avoid its truncation bug.
- No `localStorage`/`sessionStorage`.

## Pedagogical design (do not "improve" these away)

- **The rule:** Radko may only pass through things whose name contains **Р**.
- **No scoring, no timer, no fail state.** This is deliberate for the audience.
  Correct tap → advance. Wrong tap → gentle wiggle + re-play narration, no
  penalty, stays on the scene.
- Six sequential correct choices: река, дърво, дракон, пещера, врата, корона.
  Wrong options must **not** contain Р: пътека, камък, змия, водопад, капак, меч.
  - NOTE: Scene 2's wrong option was changed from "горска пътека" (which contains
    Р in "горска") to **"пътека"**. Keep it Р-free.
- Correct/wrong cards are **equal visual weight**, and the correct card's
  **side is randomized** each render so position can't be pattern-matched.

## Architecture

### `radko.html` (current — image + hotspots)
Data-driven. To change content you edit the `SCENES` array, not logic.
- **CONFIG** (top of `<script>`): `DEBUG` (true, or press **"d"** in-browser, to
  outline every hotspot for tuning); `ART_BASE`/`AUDIO_BASE` (local dev ↔ jsDelivr);
  `NAR` (audio-file map); `SCRIPT` (L1 narration = recording script).
- **`SCENES`**: each `{id, type, img, audio, hotspots:[…]}`. Types: `menu`,
  `title`, `choice`, `win`. Hotspots are % of the frame `{x,y,w,h}` plus one of:
  `correct:true + next` (the Р answer → advances), bare (a wrong answer → gentle
  nudge), `goto` (navigation), `locked:"msg"` (toast). Add levels by appending.
- **Engine**: `go(id)` cross-fades scenes; `buildScene` renders the image +
  hotspots + controls + progress pips; `onHotspot` handles correct/wrong/nav;
  synth `chimeOk`/`chimeNudge`; `playKey` plays a hosted MP3 only where a scene
  has an `audio` key; an idle "tap here" hint; confetti on win.
- **Asset pipeline**: `tools/build_web_assets.py` turns the raw `scene/*.png`
  into slugged, compressed `scene/web/*.jpg`. `/tmp/calib.py` (regenerate as
  needed) overlays the hotspot boxes onto the art to verify coordinates.

### `radko_level1.html` (legacy — inline SVG)
Original prototype. Everything in the rest of this section describes it; data-driven,
edit data not logic. Kept for reference.

- **CONFIG block (top of `<script>`)** — the only block normally edited:
  - `ART_SOURCE`   = `"svg"` (inline drawn art, baked in — current) or `"image"`
    (load PNGs from `IMAGE_BASE`).
  - `AUDIO_SOURCE` = `"files"` (hosted MP3s — current) or `"tts"` (browser
    text-to-speech, for offline testing).
  - `AUDIO_BASE`   = `https://cdn.jsdelivr.net/gh/myAlexD/radko-game@main/audio/`
  - `IMAGE_BASE`   = same repo, `images/` (only used if `ART_SOURCE==="image"`).
  - `IMG`, `NAR`   = filename maps. `LANDING_AUDIO = "0-1.mp3"`.
  - `SCRIPT`       = per-scene Bulgarian narration text. Doubles as the recording
    script AND the TTS fallback.
- **`SCENES` array** — the whole game. Each scene: `id`, `type`
  (`start`|`choice`|`win`), `bg`, and for choices a `step` (1–6) + `choices`
  (each `{key,label,correct,next}`). Add Level 2 by appending scenes.
- **`ICON`** — inline SVG for the 14 items + Radko + castle (`ART_SOURCE==="svg"`).
- **`BG`** — inline SVG full-scene backgrounds, keyed by `bg` suffix
  (`bg-forest` → `BG.forest`).
- **Audio engine** — `buildAudioCache()` preloads all clips; `playNarration()`,
  `playSequence()` (start screen plays `landing` → `s1`), synth `chimeOk`/
  `chimeNudge`. First playback unlocked by a user tap (autoplay-safe); start
  screen has a 🔊 button as the reliable trigger.
- **State machine** — `go(id)` swaps scenes with a fade; `buildScene(s)` renders;
  `onChoice()` handles correct/wrong; `burstConfetti()` on win.

## Assets

- **Audio:** GitHub repo **`myAlexD/radko-game`**, `audio/` folder, served via
  jsDelivr. Files: `s1.mp3`…`s8.mp3` (per-scene narration) + `0-1.mp3` (landing/
  welcome clip). All verified public, 256 kbps mono MP3.
  - jsDelivr caches `@main` for ~24h. While iterating on recordings, pin a tag
    (`@v1`) or purge via `https://purge.jsdelivr.net/gh/myAlexD/radko-game@main/...`.
- **Images (current engine):** the user's own illustrated scenes. Raw Canva PNG
  exports live in `scene/` (1920×1080, 2–5 MB, Cyrillic filenames). The build
  script slugs + compresses them to **`scene/web/*.jpg`** (~250 KB, 1600×900, ~5.4 MB
  total) — that folder is what gets hosted and referenced by `ART_BASE` (jsDelivr,
  same as audio). The old "don't re-host" caveat applied to licensed Canva **stock**;
  these are the user's own art and are fine to host.
- `radko_level1.html` (legacy) uses inline SVG only — no image hosting.

## Local dev

Serve over HTTP (not `file://`) for clean audio/autoplay behavior:
```
python -m http.server      # or VS Code Live Server
```
For local audio, set `AUDIO_BASE` to `"audio/"` (relative). **Flip it back to the
jsDelivr URL before publishing** — localhost isn't reachable by anyone else.

## Open tasks (radko.html)

1. **Record Level 2 narration.** L2 scenes are currently **silent** (the question is
   baked into the art). Add `l2-*.mp3` files, extend `NAR`, and set each L2 scene's
   `audio` key. Words: крепост, крокодил, брадва, дракон, врата, принцеса.
2. **Fix the broken L2 beat.** `Ниво 2 - 2. Намира оръжие` has **no Р-word** in its
   art (rock / broom / tulip), so the engine **skips it** (l2-1 → l2-3). Re-illustrate
   with a real Р vs non-Р pair, then insert an `l2-2` scene.
3. **Build Level 3 — "Над българската земя".** Different mechanic (a Bulgarian-culture
   quiz, e.g. holidays), and only 2 of its screens are illustrated. Needs more art +
   design. Menu entry is currently `locked`.
4. **Publish.** `git add scene/web && git commit && git push`; flip `ART_BASE` +
   `AUDIO_BASE` to the jsDelivr URLs (commented in CONFIG); paste `radko.html` into
   Canva Code. (~480 lines — well under the budget.)
5. **Tune hotspots if needed.** Open with `DEBUG=true` (or press "d"); regenerate
   `/tmp/calib.py` overlays to check boxes against the art.

## Conventions

- Bulgarian for all in-game text; code comments in English.
- Flat-storybook visual style, warm folk palette (see CSS `:root` variables).
- Keep additions lean and dependency-free for Canva Code compatibility.
