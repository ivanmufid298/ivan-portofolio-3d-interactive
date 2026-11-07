# Ivan Mufid — Digital Garden

Interactive Japanese garden portfolio with Indonesian / English content and persistent day / night modes. Professional content is based on Ivan's supplied resume; project illustrations are explicitly illustrative, not client screenshots.

## Run locally

`python3 -m http.server 4173`

Open http://localhost:4173. No build step or API keys required. Vercel serves this static repository directly.

## Editable Blender source

Open `blender/Ivan-Japanese-Garden.blend` in Blender. It contains original, individually editable geometry, materials, lighting, and a camera. `blender/create_garden.py` regenerates it using Blender in a separate background process. The script clears that process's scene: do not run in an unsaved working scene.

The website loads the actual exported `assets/garden.glb`. After editing the Blender file, export glTF Binary to that path with cameras/lights disabled. Web lighting is controlled in `scene.js`.

## Controls

- Drag garden to orbit; arrow keys when focused also rotate.
- Plus / minus zoom; Reset restores the initial view.
- Pause animation stops drifting petals and star pulsing. Reduced-motion preference pauses by default.
- Day / Night and ID / EN preferences persist locally.
- Project buttons open accessible detail dialogs. Escape closes them.

The portfolio text and navigation remain usable if WebGL fails. Animation sleeps when the scene is offscreen or the tab is hidden. Pixel ratio is capped for mobile performance.

Three.js 0.170.0 is vendored under `vendor/` (MIT license). Google Fonts: DM Sans and Manrope, with system fallbacks. No client confidential screenshots, source code, phone number, or full resume PDF is published.
