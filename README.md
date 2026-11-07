# Ivan Mufid — Digital Garden

Full-screen Japanese garden journey with Indonesian / English content and persistent day / night modes. The document does not scroll: wheel, touch gestures on the garden, keyboard arrows, and chapter buttons advance a camera route. Professional content is based on Ivan's supplied resume.

## Run locally

`python3 -m http.server 4173`

Open http://localhost:4173. No build step or API keys required. Vercel serves this static repository directly.

## Editable Blender source

Open `blender/Ivan-Japanese-Garden.blend` in Blender. It contains original, individually editable geometry, materials, lighting, and a camera. `blender/create_garden.py` regenerates it using Blender in a separate background process. The script clears that process's scene: do not run in an unsaved working scene.

The website loads the actual exported `assets/garden.glb`. After editing the Blender file, export glTF Binary to that path with cameras/lights disabled. Web lighting is controlled in `scene.js`.

## Controls

- Scroll to walk from the entrance across the bridge, past the koi pond, toward the temple. On phones, swipe vertically over the garden or use chapter buttons.
- Arrow keys / Page Up / Page Down navigate chapters; Home / End jump to endpoints. Navigation links and the four route markers also work.
- Pause animation stops falling petals, koi, ripples, water shimmer, and the cat's tail. Reduced-motion preference pauses ambient animation and makes camera navigation immediate.
- Enjoy the garden hides the content overlay; the same control restores it.
- Day / Night and ID / EN preferences persist locally.
- Project buttons open accessible detail dialogs. Escape closes them.

The portfolio text and navigation remain usable if WebGL fails. Animation sleeps when the tab is hidden. Pixel ratio is capped for mobile performance. Long profile content can scroll inside its panel without moving the page; wheel input advances the journey at the panel boundary.

## Scene details

Six swimming koi, notched lily pads and layered lotus blossoms, a cream cat with whiskers and a moving tail, bamboo window shades with pull cords, shoji latticework, stone steps, bamboo, fallen petals, instanced airborne sakura, expanding pond ripples, water shimmer, soft shadows, distant mountains, and night lanterns.

The Blender timeline (frames 1–240) includes editable koi, cat-tail and falling-petal animation previews. GLB exports static geometry, and `scene.js` animates named roots in the browser. `journey.js` owns navigation; `journey.css` owns the fixed viewport layout.

Three.js 0.170.0 is vendored under `vendor/` (MIT license). Google Fonts: DM Sans and Manrope, with system fallbacks. No client confidential screenshots, source code, phone number, or full resume PDF is published.
