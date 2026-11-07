import * as THREE from 'three';
import { mergeGeometries } from './vendor/BufferGeometryUtils.js';
import { GLTFLoader } from './vendor/GLTFLoader.js';
import { prefs } from './app.js';
import { getProgress } from './journey.js';

const host = document.querySelector('#garden');
const loading = document.querySelector('#loading');
const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
let night = prefs.get('garden-theme', 'day') === 'night';
let paused = reduced, ready = false, failed = false;
const themeButton = document.querySelector('#theme');
const motionButton = document.querySelector('#motion');
let applyLight = () => {};

function labels() {
  const en = document.documentElement.lang === 'en';
  document.body.classList.toggle('night', night);
  themeButton.innerHTML = `${night ? '☾' : '☀'} <span>${night ? (en ? 'Night' : 'Malam') : (en ? 'Day' : 'Siang')}</span>`;
  themeButton.setAttribute('aria-pressed', String(night));
  themeButton.setAttribute('aria-label', en ? (night ? 'Switch to day' : 'Switch to night') : (night ? 'Aktifkan mode siang' : 'Aktifkan mode malam'));
  motionButton.textContent = paused ? (en ? 'Resume animation' : 'Lanjutkan animasi') : (en ? 'Pause animation' : 'Jeda animasi');
  motionButton.setAttribute('aria-pressed', String(paused));
  host.setAttribute('aria-label', en ? 'A panorama and four garden viewpoints. Scroll or swipe once to visit the next view.' : 'Panorama dan empat sudut pandang taman. Scroll atau usap sekali untuk menuju spot berikutnya.');
  if (!ready) loading.textContent = failed ? (en ? '3D unavailable. Use navigation to explore all portfolio chapters.' : '3D tidak tersedia. Gunakan navigasi untuk membuka semua bagian portfolio.') : (en ? 'Growing the garden…' : 'Menumbuhkan taman…');
}
themeButton.addEventListener('click', () => { night = !night; prefs.set('garden-theme', night ? 'night' : 'day'); labels(); });
motionButton.addEventListener('click', () => { paused = !paused; labels(); });
document.addEventListener('languagechange', labels);
labels();

try {
  const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true, powerPreference: 'high-performance' });
  renderer.setPixelRatio(Math.min(devicePixelRatio, 1.5));
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.05;
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  host.appendChild(renderer.domElement);
  const scene = new THREE.Scene();
  scene.fog = new THREE.FogExp2(0xdce7dc, .009);
  const camera = new THREE.PerspectiveCamera(43, 1, .1, 180);

  // A quiet establishing shot, then four deliberate garden compositions.
  const shots = [
    { position: [10, 10, 19], target: [0, 1.1, 0], name: 'panorama' },
    { position: [-2.6, 4.4, 9], target: [-3.6, 1.85, -.8], name: 'torii' },
    { position: [6.4, 5.7, 8.8], target: [0, 1.1, 1.2], name: 'bridge' },
    { position: [3.8, 6.8, 6.8], target: [.4, .65, 1.65], name: 'pond' },
    { position: [8.5, 5.4, 7.4], target: [2.5, 2.6, -1.6], name: 'temple' },
  ].map(s => ({ ...s, position: new THREE.Vector3(...s.position), target: new THREE.Vector3(...s.target) }));
  let selected = Math.round(getProgress());
  let position = shots[selected].position.clone(), target = shots[selected].target.clone();
  let startPosition = position.clone(), startTarget = target.clone(), travelTime = 1.05;
  document.addEventListener('journeychange', e => {
    const next = Math.round(e.detail);
    if (next === selected) return;
    startPosition.copy(position); startTarget.copy(target); selected = next; travelTime = 0;
  });

  const hemi = new THREE.HemisphereLight(0xffefdc, 0x587c62, 2.25);
  scene.add(hemi);
  const key = new THREE.DirectionalLight(0xffe3b9, 2.4);
  key.position.set(-6, 12, 7); key.castShadow = true;
  key.shadow.mapSize.set(1024, 1024);
  Object.assign(key.shadow.camera, { left: -10, right: 10, top: 10, bottom: -10, near: 1, far: 32 });
  key.shadow.bias = -.0005; key.shadow.normalBias = .025;
  scene.add(key);
  const rim = new THREE.DirectionalLight(0xb6d4e8, 1);
  rim.position.set(8, 4, -5); scene.add(rim);
  const lanterns = [];
  for (const [x, z] of [[-2.3, 2.7], [2.6, 2.3], [-4.5, -.1], [4.4, -.1]]) {
    const light = new THREE.PointLight(0xffac52, 0, 5, 2);
    light.position.set(x, 1.3, z); scene.add(light); lanterns.push(light);
  }
  const materials = new Set(), fish = [], fishTails = [], ripples = [], wakes = [], clouds = [], skySun = [], skyMoon = [], waterUniforms = [];
  let rocker = null;

  const ground = new THREE.Mesh(new THREE.PlaneGeometry(240, 240), new THREE.MeshStandardMaterial({ color: 0xa3baa1, roughness: 1 }));
  ground.rotation.x = -Math.PI / 2; ground.position.y = -1.8; ground.receiveShadow = true; scene.add(ground);
  const mountains = new THREE.Group(); scene.add(mountains);
  for (let i = 0; i < 15; i++) {
    const hill = new THREE.Mesh(new THREE.IcosahedronGeometry(1, 1), new THREE.MeshStandardMaterial({ color: i % 2 ? 0x719889 : 0x8daa98, roughness: 1 }));
    hill.scale.set(5 + i % 3, 4 + i % 4, 3);
    hill.position.set(-34 + i * 4.7, -1.8, -25 - Math.sin(i) * 4); mountains.add(hill);
  }
  const starPositions = new Float32Array(380 * 3);
  for (let i = 0; i < starPositions.length; i += 3) {
    const a = Math.random() * Math.PI * 2, elevation = .025 + Math.random() * .55;
    starPositions[i] = Math.cos(a) * 65 * Math.cos(elevation);
    starPositions[i + 1] = Math.sin(elevation) * 65;
    starPositions[i + 2] = Math.sin(a) * 65 * Math.cos(elevation);
  }
  const starGeometry = new THREE.BufferGeometry();
  starGeometry.setAttribute('position', new THREE.BufferAttribute(starPositions, 3));
  const stars = new THREE.Points(starGeometry, new THREE.PointsMaterial({ color: 0xfff3d9, size: .14, transparent: true, opacity: .9, fog: false }));
  scene.add(stars);

  let dusk = night ? 1 : 0;
  const palettes = [[hemi.color, 0xffefdc, 0x839fc7], [hemi.groundColor, 0x587c62, 0x243d40], [key.color, 0xffe3b9, 0xa4c1e9], [scene.fog.color, 0xdce7dc, 0x142632], [ground.material.color, 0xa3baa1, 0x263d3c]].map(([color, day, dark]) => [color, new THREE.Color(day), new THREE.Color(dark)]);
  applyLight = () => {
    palettes.forEach(([color, day, dark]) => color.lerpColors(day, dark, dusk));
    hemi.intensity = THREE.MathUtils.lerp(2.25, .85, dusk);
    key.intensity = THREE.MathUtils.lerp(2.4, .65, dusk); rim.intensity = 1 - dusk * .2;
    lanterns.forEach(l => l.intensity = dusk * 5);
    materials.forEach(m => { if (m.name.includes('Lantern')) m.emissiveIntensity = .2 + dusk * 2.8; });
    skySun.forEach(o => { o.material.opacity = 1-dusk; o.visible = dusk < .999; });
    skyMoon.forEach(o => { o.material.opacity = dusk; o.visible = dusk > .001; });
    clouds.forEach(o => { o.material.opacity = 1-dusk; o.visible = dusk < .999; });
    stars.material.opacity = dusk * .85;
  };

  function animateWater(material) {
    material.roughness = .22; material.metalness = .05; material.transparent = true; material.opacity = .48; material.depthWrite = false;
    material.onBeforeCompile = shader => {
      shader.uniforms.uTime = { value: 0 }; waterUniforms.push(shader.uniforms.uTime);
      shader.vertexShader = 'varying vec3 vWater;\n' + shader.vertexShader.replace('#include <worldpos_vertex>', '#include <worldpos_vertex>\nvWater = (modelMatrix * vec4(transformed, 1.0)).xyz;');
      shader.fragmentShader = 'uniform float uTime; varying vec3 vWater;\n' + shader.fragmentShader.replace('#include <color_fragment>', '#include <color_fragment>\nfloat wave = sin(vWater.x*12.0+sin(vWater.z*9.0+uTime)+uTime*.5)*sin(vWater.z*15.0-uTime*.4); diffuseColor.rgb += vec3(.09,.14,.12)*pow(max(wave,0.0),7.0); float caustic=sin(vWater.x*7.0+uTime*.6+sin(vWater.z*6.0-uTime*.3)); diffuseColor.rgb+=vec3(.025,.06,.045)*pow(max(caustic,0.0),12.0);');
    };
  }
  new GLTFLoader().load('./assets/garden.glb?v=garden-v4', gltf => {
    scene.add(gltf.scene);
    gltf.scene.traverse(o => {
      if (o.name.startsWith('FallingPetal')) o.visible = false;
      if (/^Koi_\d+$/.test(o.name)) fish.push(o);
      if (o.name.startsWith('KoiTail_')) fishTails.push(o);
      if (o.name === 'BambooRocker') rocker = o;
      if (o.name.startsWith('SkySun')) skySun.push(o);
      if (o.name.startsWith('SkyMoon')) skyMoon.push(o);
      if (o.name.startsWith('SkyCloud')) { clouds.push(o); o.userData.initialX = o.position.x; }
      if (o.name.startsWith('Ripple_')) { o.material = o.material.clone(); o.material.transparent = true; o.material.depthWrite = false; ripples.push(o); }
      if (!o.isMesh) return;
      const sky = o.name.startsWith('Sky');
      o.castShadow = !sky && !o.name.startsWith('Ripple') && !o.name.includes('pond'); o.receiveShadow = !sky;
      if (o.material) {
        if (!materials.has(o.material) && o.material.name.startsWith('Water')) animateWater(o.material);
        materials.add(o.material);
        if (sky) { o.material.fog = false; o.material.transparent = true; o.material.depthWrite = false; }
      }
    });
    fish.sort((a, b) => a.name.localeCompare(b.name, undefined, { numeric: true }));
    // Batch stationary garden pieces by material; preserve editable objects in Blender.
    gltf.scene.updateMatrixWorld(true);
    const batches = new Map(), staticObjects = [];
    gltf.scene.traverse(o => {
      if (!o.isMesh || Array.isArray(o.material) || !o.visible || o.name.startsWith('Sky') || o.name.startsWith('Ripple') || o.material.name.startsWith('Water')) return;
      for (let parent=o; parent; parent=parent.parent) if (/^Koi_|^BambooRocker/.test(parent.name)) return;
      const geometry = o.geometry.clone().applyMatrix4(o.matrixWorld);
      for (const attribute of Object.keys(geometry.attributes)) if (!['position','normal'].includes(attribute)) geometry.deleteAttribute(attribute);
      const flat = geometry.index ? geometry.toNonIndexed() : geometry;
      if (flat !== geometry) geometry.dispose();
      const key = o.material.uuid;
      if (!batches.has(key)) batches.set(key, { material: o.material, geometries: [] });
      batches.get(key).geometries.push(flat); staticObjects.push(o);
    });
    batches.forEach(({material, geometries}) => {
      const merged = mergeGeometries(geometries);
      if (!merged) throw new Error('Garden geometry could not be batched');
      const mesh = new THREE.Mesh(merged, material); mesh.castShadow = true; mesh.receiveShadow = true; scene.add(mesh);
      geometries.forEach(g => g.dispose());
    });
    staticObjects.forEach(o => o.removeFromParent());
    fish.forEach((f, i) => {
      const localBatches = new Map(), parts = [], inverse = f.matrixWorld.clone().invert();
      f.traverse(o => {
        if (!o.isMesh || o.name.startsWith('KoiTail')) return;
        const g = o.geometry.clone().applyMatrix4(new THREE.Matrix4().multiplyMatrices(inverse,o.matrixWorld));
        for (const a of Object.keys(g.attributes)) if (!['position','normal'].includes(a)) g.deleteAttribute(a);
        const flat = g.index ? g.toNonIndexed() : g;
        if(flat!==g) g.dispose();
        if(!localBatches.has(o.material.uuid)) localBatches.set(o.material.uuid,{material:o.material,geometries:[]});
        localBatches.get(o.material.uuid).geometries.push(flat); parts.push(o);
      });
      localBatches.forEach(({material,geometries}) => { const mesh=new THREE.Mesh(mergeGeometries(geometries),material); f.add(mesh); geometries.forEach(g=>g.dispose()); });
      parts.forEach(o=>o.removeFromParent());
      const direction = i%2 ? -1 : 1, phase = Math.random()*Math.PI*2;
      const points = Array.from({length: 9}, (_, j) => {
        const a=phase+direction*j/9*Math.PI*2, radius=.5+Math.random()*.45;
        return new THREE.Vector3(Math.cos(a)*1.3*radius, .535+Math.random()*.012, (i<9 ? 2.65 : -.25)+Math.sin(a)*.52*radius);
      });
      f.userData.path = new THREE.CatmullRomCurve3(points, true, 'centripetal');
      f.userData.speed = .012 + Math.random()*.012; f.userData.phase = Math.random();
      f.scale.setScalar(.78+Math.random()*.23);
      f.traverse(o => { if(o.isMesh) o.castShadow = false; });
      const wake = new THREE.Mesh(new THREE.RingGeometry(.17,.179,24), new THREE.MeshBasicMaterial({color:0xb5e4d9,transparent:true,opacity:.1,depthWrite:false,side:THREE.DoubleSide}));
      wake.rotation.x=-Math.PI/2; scene.add(wake); wakes.push(wake);
    });
    ready = true; loading.hidden = true; host.dataset.ready = 'true';
    rocker?.traverse(o => { if(o.isMesh) o.castShadow=false; });
    renderer.shadowMap.autoUpdate = false; renderer.shadowMap.needsUpdate = true;
    host.dataset.details = JSON.stringify({ koi: fish.length, ripples: ripples.length, cats: 0, staticBatches: batches.size, fountain: !!rocker, sun: skySun.length, moon: skyMoon.length, clouds: clouds.length });
    applyLight();
  }, undefined, () => { failed = true; host.dataset.error = 'model'; labels(); });

  const petalShape = new THREE.Shape();
  petalShape.moveTo(0, -.07); petalShape.bezierCurveTo(-.09, -.01, -.08, .08, -.025, .085); petalShape.lineTo(0, .06); petalShape.lineTo(.025, .085); petalShape.bezierCurveTo(.08, .08, .09, -.01, 0, -.07);
  const petals = new THREE.InstancedMesh(new THREE.ShapeGeometry(petalShape), new THREE.MeshStandardMaterial({ color: 0xf4b5bf, side: THREE.DoubleSide, roughness: .9 }), 120);
  petals.frustumCulled = false; scene.add(petals);
  const petalData = Array.from({ length: 120 }, () => ({ x: (Math.random() - .5) * 12, y: Math.random() * 5, z: (Math.random() - .5) * 9, s: .35 + Math.random() * .5, phase: Math.random() * 6.28 }));
  const dummy = new THREE.Object3D();
  // Fountain droplets run from the hollow bamboo outlet into the stone basin.
  const drops = new THREE.InstancedMesh(new THREE.SphereGeometry(.025, 8, 6), new THREE.MeshStandardMaterial({ color: 0xbce7e5, transparent: true, opacity: .7, roughness: .1 }), 12);
  drops.frustumCulled = false; scene.add(drops);

  let mobile = false, width = 1, height = 1, framing = selected === 0 ? 0 : 1;
  function resize() {
    const w = host.clientWidth, h = host.clientHeight;
    width = w; height = h; mobile = w <= 900; renderer.setSize(w, h); camera.aspect = w / h;
    camera.updateProjectionMatrix();
  }
  new ResizeObserver(resize).observe(host); resize(); applyLight();
  let last = 0, time = 0;
  const effectivePosition = new THREE.Vector3(), swimAhead = new THREE.Vector3();
  renderer.setAnimationLoop(t => {
    if (document.hidden) { last = t; return; }
    const dt = Math.min((t - last) / 1000, .05); last = t;
    if (!paused) time += dt;
    dusk = THREE.MathUtils.damp(dusk, night ? 1 : 0, reduced ? 1000 : 2.8, dt); applyLight();
    framing = THREE.MathUtils.damp(framing, selected === 0 ? 0 : 1, 5, dt);
    camera.setViewOffset(width, height, mobile ? 0 : -width*.18*framing, mobile ? height*.20*framing : 0, width, height);
    travelTime = Math.min(1.05, travelTime + dt);
    const p = reduced ? 1 : travelTime / 1.05;
    const ease = p * p * p * (p * (p * 6 - 15) + 10);
    position.lerpVectors(startPosition, shots[selected].position, ease);
    position.y += Math.sin(Math.PI * ease) * .25;
    target.lerpVectors(startTarget, shots[selected].target, ease);
    effectivePosition.copy(position);
    if (mobile) effectivePosition.sub(target).multiplyScalar(1.55).add(target);
    camera.position.copy(effectivePosition); camera.lookAt(target);
    host.dataset.shot = shots[selected].name; host.dataset.transition = p.toFixed(2);
    if (!paused || time === 0) {
      petalData.forEach((v, i) => {
        dummy.position.set(v.x + Math.sin(time * .4 + v.phase) * .45, .65 + (v.y - time * (.22 + v.s * .14) + 600) % 5, v.z + Math.sin(time * .2 + v.phase) * .3);
        dummy.rotation.set(time * .7 + v.phase, Math.sin(time + v.phase), time * .4); dummy.scale.setScalar(v.s); dummy.updateMatrix(); petals.setMatrixAt(i, dummy.matrix);
      });
      petals.instanceMatrix.needsUpdate = true;
      fish.forEach((f, i) => {
        const u=(f.userData.phase+time*f.userData.speed)%1;
        f.userData.path.getPointAt(u, f.position);
        f.userData.path.getPointAt((u+.003)%1, swimAhead);
        swimAhead.sub(f.position); f.rotation.set(0, Math.atan2(swimAhead.x, swimAhead.z), 0);
        const wake=wakes[i], cycle=(time*.35+i*.31)%1;
        wake.position.set(f.position.x,.658,f.position.z);
        wake.scale.setScalar(.5+cycle*1.25);wake.material.opacity=(1-cycle)*.12;
      });
      fishTails.forEach((f, i) => f.rotation.y = Math.sin(time * (5+i%4) + i) * .24);
      ripples.forEach((r, i) => { const phase = (time * .27 + i * .21) % 1; r.scale.setScalar(.35 + phase * 1.1); r.material.opacity = (1 - phase) * .27; });
      if (rocker) rocker.rotation.x = Math.max(0, Math.sin(time * .7)) * .40;
      for (let i = 0; i < 12; i++) {
        const f = (time * 1.4 + i / 12) % 1;
        dummy.position.set(2.95 + Math.sin(i) * .015, 1.8 - f * 1.08, 2.75 + Math.sin(i * 2) * .015);
        dummy.rotation.set(0, 0, 0); dummy.scale.set(.65, 1.4, .65); dummy.updateMatrix(); drops.setMatrixAt(i, dummy.matrix);
      }
      drops.instanceMatrix.needsUpdate = true;
      clouds.forEach(o => o.position.x = o.userData.initialX + Math.sin(time * .025) * 1.3);
      stars.material.opacity = dusk * (.8 + Math.sin(time * .4) * .12);
      waterUniforms.forEach(u => u.value = time);
    }
    renderer.render(scene, camera);
    host.dataset.drawCalls = String(renderer.info.render.calls);
    host.dataset.triangles = String(renderer.info.render.triangles);
  });
  renderer.domElement.addEventListener('webglcontextlost', e => { e.preventDefault(); failed = true; ready = false; loading.hidden = false; labels(); });
} catch (error) { failed = true; host.dataset.error = 'webgl'; labels(); console.error(error); }
