# Ivan Mufid — Digital Garden

Full-screen Japanese garden journey with Indonesian / English content and persistent day / night modes. The document does not scroll: wheel, touch gestures on the garden, keyboard arrows, and chapter buttons advance a camera route. Professional content is based on Ivan's supplied resume.

## Run locally

`python3 -m http.server 4173`

Open http://localhost:4173. No build step or API keys required. Vercel serves this static repository directly.

## Editable Blender source

Open `blender/Ivan-Japanese-Garden.blend` in Blender. It contains original, individually editable geometry, materials, lighting, and a camera. `blender/create_garden.py` regenerates it using Blender in a separate background process. The script clears that process's scene: do not run in an unsaved working scene.

The website loads the actual exported `assets/garden.glb`. After editing the Blender file, export glTF Binary to that path with cameras/lights disabled. Web lighting is controlled in `scene.js`.

## Controls

- Each wheel gesture or vertical swipe selects exactly one composed viewpoint: torii, bridge, pond, temple. A 1.8-second quintic eased transition moves the camera between shots, with an elevated arc to keep clear of foreground objects. Trackpad momentum cannot skip several viewpoints. On phones, swipe over the garden or use chapter buttons.
- Arrow keys / Page Up / Page Down navigate chapters; Home / End jump to endpoints. Navigation links and the four route markers also work.
- Pause animation stops falling petals, koi, ripples, water shimmer, and the cat's tail. Reduced-motion preference pauses ambient animation and makes camera navigation immediate.
- Enjoy the garden hides the content overlay; the same control restores it.
- Day / Night and ID / EN preferences persist locally.
- Project buttons open accessible detail dialogs. Escape closes them.

The portfolio text and navigation remain usable if WebGL fails. Animation sleeps when the tab is hidden. Pixel ratio is capped for mobile performance. Long profile content can scroll inside its panel without moving the page; wheel input advances the journey at the panel boundary.

## Scene details

Six smoothly modeled koi with integrated color patches, directional swimming and tail movement; notched lily pads and layered lotus blossoms; a walking four-legged cat with whiskers and a moving tail; a bamboo shishi-odoshi fountain with a stone basin, rocking tube and flowing water; bamboo window shades with pull cords; shoji latticework; connected gravel paths and bridge abutments; varied rounded river stones, shrubs and green trees; falling sakura; pond ripples and water shimmer; soft shadows and distant hills.

The sun, moon, clouds and stars are world-space objects, never camera children or fixed HTML overlays. Day shows sun and moving clouds; night shows moon, a surrounding starfield and lantern light. Organic meshes use smooth normals and additional geometry, and woodwork has softened bevels.

The Blender timeline (frames 1–240) includes editable koi, cat walking/legs/tail, fountain and falling-petal animation previews. Four named cameras and timeline markers preserve the composed viewpoints. GLB exports static geometry, and `scene.js` animates named roots in the browser. `journey.js` owns navigation; `journey.css` owns the fixed viewport layout. Bump the model URL version in `scene.js` when changing the GLB so returning visitors receive the latest model.

Three.js 0.170.0 is vendored under `vendor/` (MIT license). Google Fonts: DM Sans and Manrope, with system fallbacks. No client confidential screenshots, source code, phone number, or full resume PDF is published.
