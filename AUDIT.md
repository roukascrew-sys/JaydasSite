# Cramers Customlights: audit notes

## What was tested
The page was loaded in headless Chromium at desktop (1366×850) and phone (390×844) sizes, plus once with WebGL turned off.

| Check | Result |
|---|---|
| JavaScript errors | None |
| CSP script hashes (9 scripts) | All match |
| 3D viewer loads, toggles, Outside / Sit inside | Works |
| No-WebGL fallback (flat SVG car, toggles disabled) | Works |
| Quote builder: message text, sms link, Blake/Jayda switch | Works; user text is escaped |
| Empty vehicle check blocks sending | Works |
| Share button off-line message | Works |
| Horizontal scroll on phone | None |

## What was changed (and where, to edit it yourself)
1. **Square stars in "Sit inside" view** (the real bug). Headliner stars rendered as ~40px white squares because points had no texture and grew as the camera moved inside.
   - `cramers-customlights.html` line ~863: `map:glowTexture()` gives each star the round soft texture.
   - line ~986: `starMat.size = .03 - cam.blend*.016;` sets the inside star size. Make `.016` smaller for bigger stars inside, larger for tinier stars (keep it below `.03`).
2. **Color cycle smoothness**: line ~981 reuses one color object (`starC`) instead of creating 600 per frame.
3. **Both hero "Call Blake" buttons now follow CONFIG**: line ~577.

After ANY edit to a `<script>` block, run:
```
python3 refresh-csp.py cramers-customlights.html
```
If you skip it, the browser silently blocks the edited script.

## Not changed (suggestions)
- Add `og:image` (a photo of a finished car) so shared links show a picture.
- Add real install photos. See the Figma concepts.
- The small "Text instead" links are short tap targets on phones.

## UI overhaul concepts (Figma, not built yet)
https://www.figma.com/design/2b8hhoAyf5CrkLMt4oxD4X
- A. Showroom: same page, hero cut in half, controls docked in the 3D viewer, photo gallery.
- B. Build & Quote: the 3D controls ARE the quote form (scroll-craft "live surface").
- C. Climb inside: scroll drives the camera into the car and fills the roof with stars (scroll-craft filmic build).
