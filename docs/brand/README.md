# Brand assets

| File | Use |
| --- | --- |
| `og.html` | **Canonical** Open Graph source (HTML / CSS / JS) — pill is always `beta`, never a version |
| `og.png` / `og-image.png` | Raster export (1200×630) for Pages / WhatsApp / social |
| `render-og.sh` | Chrome headless: `og.html` → `og.png` |
| `readme-header.png` | GitHub README hero |
| `intra-flow-demo-15s.gif` | 15s product demo |
| `icon-color-*.png` / `icon-color.svg` | App mark |
| `og-release-v0.1.2.*` | Legacy aliases kept for old absolute URLs |

```bash
./render-og.sh
# Live waveform: open og.html?still=0
```

**Rule:** never put `vX.Y.Z` in the OG art. Version belongs in release notes and download buttons only.

Story: [BRAND_STORY.md](../BRAND_STORY.md) · [BRAND.md](../BRAND.md) · [DESIGN.md](../DESIGN.md).
