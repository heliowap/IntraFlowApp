# Intra Flow Design Direction

## Visual Register

Primary product register: restrained precision.

Brand and onboarding moments may use stronger kinetic expression, but daily app surfaces
should remain native, calm, and fast. The user is working, not watching a campaign.

## Color Strategy

Base: graphite and off-white.

Accent: a single **electric-indigo signal**, used sparingly for active listening, ordering,
selection, and moments where language is being created. It is Intra Flow's own signature —
family-adjacent to Intrador but deliberately not the institutional petroleum-blue and not a
generic clinical blue.

**No green.** In the Intrador family green is reserved exclusively for the WhatsApp CTA; the
earlier bioelectric-green accent broke that palette law and read as a terminal/dev aesthetic.
The signal is indigo.

Tokens:

```css
:root {
  --if-graphite: oklch(18% 0.012 265);
  --if-graphite-2: oklch(25% 0.014 265);
  --if-paper: oklch(96% 0.010 90);
  --if-paper-2: oklch(91% 0.012 90);
  --if-line: oklch(18% 0.012 265 / 14%);
  --if-signal: oklch(60% 0.20 274);       /* electric indigo — the live signal / cursor */
  --if-signal-hot: oklch(72% 0.17 280);   /* brighter impulse */
  --if-signal-deep: oklch(45% 0.16 270);  /* structural / pressed */
  --if-danger: oklch(62% 0.18 28);
}
```

## Typography

Use a technical humanist sans direction.

For macOS product UI, start with:

```css
font-family: "Avenir Next", -apple-system, BlinkMacSystemFont, "SF Pro Text", system-ui, sans-serif;
```

The word `flow` should feel human and technical, not mono, not ornamental, and not a
generic geometric sans. The `I` is the **old-school I-beam cursor** (vertical stroke with
serif caps top and bottom). An I-beam reads as a serif capital `I`, so in the wordmark the
living caret *is* the letter — no separate glyph.

## Form Language

- The `I` is an old-school I-beam cursor and ordering axis.
- The flow field is technical and systemic — an **internal flow map**, not hand-drawn ridges.
- Composition is engineered: even offsets, smooth curves, no wobble, no doodly recurves.
- Use rounded corners sparingly and with macOS restraint.
- Avoid decorative blobs, generic waveforms, AI stars, and literal microphones.

### Chosen direction — Composer × Waveform

**Decided.** Canonical identity: [prototypes/intra-flow-identity.html](prototypes/intra-flow-identity.html)
(hero, app icon, Flow Bar, wordmark, system). The mark is one sentence, left → right:

1. **Waveform in** — the voice is a living, two-tone waveform (top indigo, base brighter
   periwinkle, via a vertical gradient). It swells then **tapers to nothing as it funnels into the
   cursor** — the signal being *read and consumed*, not shown for its own sake. This is what frees
   the waveform from the brand's "generic audio" ban: it is never free-floating.
2. **The I-beam** — the old-school cursor is the gate; a glow marks where speech becomes language.
3. **Text out** — plain rendered type (the word `flow`), then **ghost-word bars** (the next words
   already forming; the nearest one pulses).
4. All staged inside a **text composer** — focus ring, `COMPOSER` / `⌃ Space`, the cursor's home.

- **Logo / app icon ≠ brand surface.** The waveform is the animated *surface*. The *logo/icon* is
  the reductive **I-beam Caret** (it can't be a horizontal waveform). At large icon size a faint
  waveform funnels into the beam; at 32px and below it drops to the pure beam. Menu bar = pure
  monochrome I-beam.
- **Colour logic.** Indigo = voice + cursor; paper = the resulting text. Signal rationed. **No
  green, ever.**

Logo studies behind the icon decision: [prototypes/intra-flow-logos.html](prototypes/intra-flow-logos.html)
(Caret · Signal · Field).

### Archived explorations

Superseded, kept for reference (not the chosen mark): **A — Core** (contour field around the
cursor), **B — Composer** (breath wisps into the cursor), and the raw **pattern test**. Linked
from the chooser [prototypes/index.html](prototypes/index.html) under “explorations.”

## Motion Language

Canonical sequence:

1. The waveform funnels in from the left toward the cursor.
2. The I-beam reads it (glow at the insertion point).
3. `flow` appears as created language.
4. Ghost-word bars settle in — the next words forming.

Motion should convey state:

- idle: slow I-beam pulse; waveform asleep
- listening: the live waveform funnels toward the cursor
- transcribing: the cursor reads it; partial text appears
- done: text settles; next words ghost in
- error: signal dims and breaks, never flashes aggressively

## Application Rules

- App icon: the reductive **I-beam Caret** in a squircle (faint waveform at large size; pure beam
  at 32px and below). A **compact colour variant** (three short bars funnelling into the beam)
  is used where a small square mark should still read as voice→cursor — see
  [prototypes/intra-flow-icon-taskbar.html](prototypes/intra-flow-icon-taskbar.html).
- Menu-bar / status icon: **compact monochrome glyph** — three short waveform bars + I-beam,
  `currentColor` template (macOS tints it), ~16px tall. Reads as voice entering the cursor; the
  pure I-beam is the fallback when width is tight.

**Production assets** — built in [prototypes/assets/](prototypes/assets/) (see
[README](prototypes/assets/README.md), preview `assets/preview.html`): `IntraFlow.icns` +
`AppIcon.iconset/` (colour), `png/MenuBarTemplate*.png` (black template, set `isTemplate=true`),
and `png/frames/live-NN@2x.png` — a 14-frame loop the menu-bar app cycles while dictation is live
(animated source: `svg/icon-live.svg`). Rebuild: `node build-icons.mjs && node rasterize.mjs &&
iconutil -c icns AppIcon.iconset -o IntraFlow.icns` (rasterizes via headless Chrome).

**Wired into the app.** `App/Sources/Assets.xcassets/AppIcon.appiconset` (from the iconset) is the
bundle icon (`ASSETCATALOG_COMPILER_APPICON_NAME: AppIcon` in `App/project.yml`). The menu-bar
status item draws the identity glyph at runtime via `MenuBarGlyph` (Sources/IntraFlowKit) — idle
mark at rest, bars animating while a Dictation is live (`MenuBarController.setListening(_:)`,
driven by the Trigger edges in `IntraFlowController`). Builds into `Intra Flow.app` via `xcodegen
generate` + `xcodebuild` (a signed build needs the Apple ID account added in Xcode for the team).
- Flow Bar: canonical kinetic surface — the waveform lives here (see Motion Language).
- Onboarding: explain the shift from keyboard-first writing to voice entering the cursor.
- Future medical fork: keep the waveform → cursor → text grammar and soften the accent into
  clinical calm.

