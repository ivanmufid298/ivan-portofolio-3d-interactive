# Ivan Mufid — Digital Garden

Full-screen Japanese garden journey with Indonesian / English content and persistent day / night modes. The document does not scroll: wheel, touch gestures on the garden, keyboard arrows, and chapter buttons advance a camera route. Professional content is based on Ivan's supplied resume.

## Run locally

`python3 -m http.server 4173`

Open http://localhost:4173. No build step or API keys required. Vercel serves this static repository directly.

## Editable Blender source

Open `blender/Ivan-Japanese-Garden.blend` in Blender. It contains original, individually editable geometry, materials, lighting, and a camera. `blender/create_garden.py` regenerates it using Blender in a separate background process. The script clears that process's scene: do not run in an unsaved working scene.

The website loads the actual exported `assets/garden.glb`. After editing the Blender file, export glTF Binary to that path with cameras/lights disabled. Web lighting is controlled in `scene.js`.

## Controls

- Each wheel gesture or vertical swipe selects one stop: panorama, torii, bridge, pond, temple. The panorama opens without a content panel and invites visitors to scroll into the garden. A 1.05-second quintic eased transition moves the camera between shots, with a subtle elevated arc. Trackpad momentum cannot skip several viewpoints. On phones, swipe over the garden or use chapter buttons.
- Arrow keys / Page Up / Page Down navigate chapters; Home / End jump to endpoints. Navigation links and the five route markers also work.
- Pause animation stops falling petals, koi, ripples, water shimmer and the bamboo fountain. Reduced-motion preference pauses ambient animation and makes camera navigation immediate.
- Enjoy the garden hides the content overlay; the same control restores it.
- Day / Night and ID / EN preferences persist locally.
- Project buttons open accessible detail dialogs. Escape closes them. Japanese garden journals use a mountain illustration, paper texture, vermilion seal, and eased opening/closing animation.

The portfolio text and navigation remain usable if WebGL fails. Animation sleeps when the tab is hidden. Pixel ratio is capped for mobile performance. Long profile content can scroll inside its panel without moving the page; wheel input advances the journey at the panel boundary.

## Scene details

Fourteen koi below the water surface with integrated color patches, independent randomized closed swimming paths, varied speeds, directional swimming and tail movement; notched lily pads and layered lotus blossoms; a bamboo shishi-odoshi fountain with a stone basin, rocking tube and flowing water; bamboo window shades with pull cords; shoji latticework; connected gravel paths, curved stepping stones and bridge abutments; varied low-poly river stones, shrubs, green trees and five bamboo groves; falling sakura; pond ripples, faint koi wakes and animated water shimmer; soft shadows and distant hills.

The sun, moon, clouds and stars are world-space objects, never camera children or fixed HTML overlays. Day shows sun and moving clouds; night shows moon, a surrounding starfield and lantern light. The garden uses low-poly organic meshes and restrained wood bevels; koi retain smooth normals. Static garden meshes are batched by material at runtime to reduce drawing overhead while the Blender source keeps each object editable. Day/night illumination and sky visibility blend gradually.

The Blender timeline (frames 1–240) includes editable koi, fountain and falling-petal animation previews. Four named cameras and timeline markers preserve the composed viewpoints. GLB exports static geometry, and `scene.js` animates named roots in the browser. `journey.js` owns navigation; `journey.css` owns the fixed viewport layout. Bump the model URL version in `scene.js` when changing the GLB so returning visitors receive the latest model.

Three.js 0.170.0 is vendored under `vendor/` (MIT license). Google Fonts: DM Sans and Manrope, with system fallbacks. No client confidential screenshots, source code, phone number, or full resume PDF is published.
