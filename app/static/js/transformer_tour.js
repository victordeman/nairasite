import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

export function initTransformerTour(containerId) {
  const container = document.getElementById(containerId);
  if (!container) return;

  // Ensure container has relative positioning for absolute UI elements
  if (getComputedStyle(container).position === 'static') {
    container.style.position = 'relative';
  }
  container.style.overflow = 'hidden';

  // Scene setup
  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0x050a18);
  scene.fog = new THREE.FogExp2(0x050a18, 0.035);

  const camera = new THREE.PerspectiveCamera(70, container.clientWidth / container.clientHeight, 0.1, 500);
  camera.position.set(0, 2, 10);

  const renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(container.clientWidth, container.clientHeight);
  renderer.setPixelRatio(window.devicePixelRatio);
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  container.appendChild(renderer.domElement);

  // Controls
  const controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.dampingFactor = 0.08;
  controls.enableZoom = true;
  controls.autoRotate = false;

  // Lighting
  const ambientLight = new THREE.AmbientLight(0x0a1a3a, 1.5);
  scene.add(ambientLight);

  const dirLight = new THREE.DirectionalLight(0x4488ff, 2.5);
  dirLight.position.set(10, 20, 10);
  dirLight.castShadow = true;
  scene.add(dirLight);

  const pointLight1 = new THREE.PointLight(0x00aaff, 3, 40);
  pointLight1.position.set(-8, 5, 0);
  scene.add(pointLight1);

  const pointLight2 = new THREE.PointLight(0x8844ff, 3, 40);
  pointLight2.position.set(8, 5, 0);
  scene.add(pointLight2);

  // ─── Data ───────────────────────────────────────────────────────────────────
  const tourStops = [
    {
      id: 'input_embedding',
      label: 'Input Embedding',
      color: 0x00d4ff,
      emissive: 0x003d66,
      position: new THREE.Vector3(0, -6, 0),
      shape: 'slab',
      description: 'Raw tokens are converted into dense numeric vectors (embeddings). Each word/token is mapped to a high-dimensional space where semantic similarity is encoded as geometric proximity.',
      detail: 'Dimension: d_model (e.g. 512 or 768). Learned during training via an embedding matrix of size [vocab_size × d_model].'
    },
    {
      id: 'pos_encoding',
      label: 'Positional Encoding',
      color: 0x00ffaa,
      emissive: 0x003322,
      position: new THREE.Vector3(0, -4, 0),
      shape: 'wave',
      description: 'Since transformers have no recurrence, sinusoidal (or learned) signals are added to embeddings to inject order information. Without this, the model would be permutation-invariant.',
      detail: 'PE(pos,2i) = sin(pos/10000^(2i/d_model)). Each dimension oscillates at a different frequency, creating a unique fingerprint per position.'
    },
    {
      id: 'multi_head_attn',
      label: 'Multi-Head Attention',
      color: 0xff6600,
      emissive: 0x331500,
      position: new THREE.Vector3(0, -1.5, 0),
      shape: 'sphere_cluster',
      description: 'The heart of the transformer. Each token attends to every other token via scaled dot-product attention, learning which words are contextually relevant to each other.',
      detail: 'Q, K, V projections split into h heads. Attention(Q,K,V) = softmax(QKᵀ/√d_k)·V. Multiple heads capture different relationship types simultaneously.'
    },
    {
      id: 'add_norm1',
      label: 'Add & Norm (1)',
      color: 0xffdd00,
      emissive: 0x332500,
      position: new THREE.Vector3(0, 0.8, 0),
      shape: 'ring',
      description: 'A residual connection adds the input directly to the attention output, preventing gradient vanishing. Layer normalization then stabilizes activations across the feature dimension.',
      detail: 'LayerNorm(x + Sublayer(x)). Residuals allow gradients to flow unchanged through depth. LN normalizes mean=0, variance=1 per token.'
    },
    {
      id: 'ffn',
      label: 'Feed-Forward Network',
      color: 0xff44aa,
      emissive: 0x330022,
      position: new THREE.Vector3(0, 2.5, 0),
      shape: 'box',
      description: 'A position-wise two-layer MLP applied identically to each token. This adds non-linearity and dramatically expands representational capacity after attention.',
      detail: 'FFN(x) = max(0, xW₁+b₁)W₂+b₂. Inner dimension is 4× d_model (e.g. 2048). ReLU or GELU activation. Applied independently per position.'
    },
    {
      id: 'add_norm2',
      label: 'Add & Norm (2)',
      color: 0xffdd00,
      emissive: 0x332500,
      position: new THREE.Vector3(0, 4.0, 0),
      shape: 'ring',
      description: 'A second residual + LayerNorm wraps the FFN sublayer, mirroring the first. This dual-residual pattern is repeated N times (typically 6–24 layers) to build depth.',
      detail: 'Same formula: LayerNorm(x + FFN(x)). Stacking encoder layers extracts increasingly abstract representations from the raw tokens.'
    },
    {
      id: 'encoder_stack',
      label: 'Encoder Stack (×N)',
      color: 0xaa88ff,
      emissive: 0x220044,
      position: new THREE.Vector3(0, 5.8, 0),
      shape: 'stack',
      description: 'The full encoder is N identical layers, each with a self-attention + FFN sublayer pair. Context is progressively distilled into rich hidden representations.',
      detail: 'N=6 in original "Attention is All You Need". Modern LLMs use up to 96 layers. Output: sequence of contextual embeddings [seq_len × d_model].'
    },
    {
      id: 'output_linear',
      label: 'Output Projection & Softmax',
      color: 0xff3344,
      emissive: 0x330008,
      position: new THREE.Vector3(0, 7.8, 0),
      shape: 'pyramid',
      description: 'The final encoder output is projected to vocabulary size via a linear layer, then softmax converts raw logits to a probability distribution over all tokens.',
      detail: 'Linear: [d_model → vocab_size]. Often shares weights with the input embedding matrix (weight tying). Softmax: p_i = e^(z_i) / Σe^(z_j).'
    }
  ];

  // ─── Particle Field ──────────────────────────────────────────────────────────
  const particleCount = 2000;
  const pGeo = new THREE.BufferGeometry();
  const pPos = new Float32Array(particleCount * 3);
  const pColors = new Float32Array(particleCount * 3);
  for (let i = 0; i < particleCount; i++) {
    pPos[i * 3] = (Math.random() - 0.5) * 60;
    pPos[i * 3 + 1] = (Math.random() - 0.5) * 40;
    pPos[i * 3 + 2] = (Math.random() - 0.5) * 60;
    const c = new THREE.Color().setHSL(Math.random() * 0.3 + 0.55, 1, 0.6);
    pColors[i * 3] = c.r; pColors[i * 3 + 1] = c.g; pColors[i * 3 + 2] = c.b;
  }
  pGeo.setAttribute('position', new THREE.BufferAttribute(pPos, 3));
  pGeo.setAttribute('color', new THREE.BufferAttribute(pColors, 3));
  const pMat = new THREE.PointsMaterial({ size: 0.08, vertexColors: true, transparent: true, opacity: 0.6 });
  const particles = new THREE.Points(pGeo, pMat);
  particles.name = 'particles';
  scene.add(particles);

  // ─── Build Component Meshes ──────────────────────────────────────────────────
  const componentMeshes = [];

  function buildMesh(stop) {
    const group = new THREE.Group();
    group.name = stop.id + '_group';
    const mat = new THREE.MeshStandardMaterial({
      color: stop.color,
      emissive: stop.emissive,
      emissiveIntensity: 0.8,
      metalness: 0.4,
      roughness: 0.3,
      transparent: true,
      opacity: 0.88
    });

    let mesh;
    if (stop.shape === 'slab') {
      mesh = new THREE.Mesh(new THREE.BoxGeometry(4.5, 0.5, 1.2), mat);
    } else if (stop.shape === 'wave') {
      const wGeo = new THREE.BoxGeometry(4.5, 0.4, 1.2, 30, 1, 1);
      const pos = wGeo.attributes.position;
      for (let i = 0; i < pos.count; i++) {
        pos.setY(i, pos.getY(i) + Math.sin(pos.getX(i) * 1.5) * 0.18);
      }
      pos.needsUpdate = true;
      mesh = new THREE.Mesh(wGeo, mat);
    } else if (stop.shape === 'sphere_cluster') {
      mesh = new THREE.Group();
      mesh.name = stop.id + '_cluster';
      for (let i = 0; i < 8; i++) {
        const s = new THREE.Mesh(new THREE.SphereGeometry(0.28 + Math.random() * 0.18, 16, 16), mat.clone());
        s.name = stop.id + '_sphere_' + i;
        const angle = (i / 8) * Math.PI * 2;
        s.position.set(Math.cos(angle) * 1.6, (Math.random() - 0.5) * 0.5, Math.sin(angle) * 0.5);
        mesh.add(s);
      }
      const center = new THREE.Mesh(new THREE.SphereGeometry(0.5, 24, 24), mat);
      center.name = stop.id + '_center';
      mesh.add(center);
    } else if (stop.shape === 'ring') {
      mesh = new THREE.Mesh(new THREE.TorusGeometry(1.8, 0.22, 16, 80), mat);
      mesh.rotation.x = Math.PI / 2;
      mesh.name = stop.id + '_torus';
    } else if (stop.shape === 'box') {
      mesh = new THREE.Mesh(new THREE.BoxGeometry(4.2, 0.8, 1.2), mat);
    } else if (stop.shape === 'stack') {
      mesh = new THREE.Group();
      mesh.name = stop.id + '_stack';
      for (let i = 0; i < 3; i++) {
        const layer = new THREE.Mesh(new THREE.BoxGeometry(4.0, 0.28, 1.1), mat.clone());
        layer.name = stop.id + '_layer_' + i;
        layer.position.y = i * 0.42 - 0.42;
        mesh.add(layer);
      }
    } else if (stop.shape === 'pyramid') {
      mesh = new THREE.Mesh(new THREE.ConeGeometry(1.8, 1.2, 6), mat);
      mesh.name = stop.id + '_cone';
    } else {
      mesh = new THREE.Mesh(new THREE.BoxGeometry(3, 0.6, 1), mat);
    }

    if (!mesh.name) mesh.name = stop.id + '_mesh';
    group.add(mesh);

    // Glow halo
    const haloMat = new THREE.MeshBasicMaterial({
      color: stop.color,
      transparent: true,
      opacity: 0.07,
      side: THREE.BackSide
    });
    const halo = new THREE.Mesh(new THREE.SphereGeometry(2.6, 16, 16), haloMat);
    halo.name = stop.id + '_halo';
    group.add(halo);

    group.position.copy(stop.position);
    scene.add(group);
    return { group, mesh, mat, stop };
  }

  tourStops.forEach(stop => {
    componentMeshes.push(buildMesh(stop));
  });

  // ─── Connector Lines ─────────────────────────────────────────────────────────
  for (let i = 0; i < tourStops.length - 1; i++) {
    const from = tourStops[i].position;
    const to = tourStops[i + 1].position;
    const mid = new THREE.Vector3().lerpVectors(from, to, 0.5);
    mid.x += 0.0;
    const curve = new THREE.CatmullRomCurve3([from.clone(), mid, to.clone()]);
    const pts = curve.getPoints(40);
    const geo = new THREE.BufferGeometry().setFromPoints(pts);
    const mat = new THREE.LineBasicMaterial({ color: tourStops[i].color, transparent: true, opacity: 0.3 });
    const line = new THREE.Line(geo, mat);
    line.name = 'connector_' + i;
    scene.add(line);
  }

  // ─── Flow Particles Along Spine ──────────────────────────────────────────────
  const flowCount = 80;
  const flowSpheres = [];
  for (let i = 0; i < flowCount; i++) {
    const s = new THREE.Mesh(
      new THREE.SphereGeometry(0.06, 8, 8),
      new THREE.MeshBasicMaterial({ color: 0x00d4ff, transparent: true, opacity: 0.7 })
    );
    s.name = 'flow_' + i;
    s.userData.t = Math.random();
    s.userData.speed = 0.0015 + Math.random() * 0.001;
    scene.add(s);
    flowSpheres.push(s);
  }

  const spinePositions = tourStops.map(s => s.position.clone());
  const spineCurve = new THREE.CatmullRomCurve3(spinePositions);

  // ─── UI ──────────────────────────────────────────────────────────────────────
  const style = document.createElement('style');
  style.textContent = `
    .trans-hud-title {
      position: absolute; top: 20px; left: 50%; transform: translateX(-50%);
      text-align: center; pointer-events: none; z-index: 100;
    }
    .trans-hud-title h1 {
      font-size: 18px; font-weight: 600; letter-spacing: 0.12em;
      color: #e0eeff; text-transform: uppercase;
    }
    .trans-hud-title p {
      font-size: 11px; color: #4488aa; letter-spacing: 0.08em; margin-top: 3px;
    }

    .trans-info-panel {
      position: absolute; bottom: 24px; left: 50%; transform: translateX(-50%);
      width: min(560px, calc(100% - 32px));
      background: rgba(5,10,24,0.88);
      border: 1px solid rgba(0,180,255,0.25);
      border-radius: 12px;
      padding: 18px 22px 16px;
      z-index: 100;
      transition: opacity 0.4s ease;
      pointer-events: auto;
    }
    .trans-info-panel .stop-num {
      font-size: 10px; font-weight: 600; letter-spacing: 0.15em;
      color: #0088bb; text-transform: uppercase; margin-bottom: 4px;
    }
    .trans-info-panel .stop-name {
      font-size: 17px; font-weight: 700; color: #eef6ff; margin-bottom: 8px;
    }
    .trans-info-panel .stop-desc {
      font-size: 13px; color: #8ab8d8; line-height: 1.65; margin-bottom: 10px;
    }
    .trans-info-panel .stop-detail {
      font-size: 11.5px; color: #4a7a99; line-height: 1.6;
      border-top: 1px solid rgba(0,150,255,0.12); padding-top: 8px;
    }

    .trans-nav-bar {
      position: absolute; bottom: 24px; right: 24px;
      display: flex; flex-direction: column; gap: 8px; z-index: 100;
    }
    .trans-nav-btn {
      width: 40px; height: 40px;
      background: rgba(5,10,24,0.85);
      border: 1px solid rgba(0,180,255,0.3);
      border-radius: 8px;
      color: #88ccee;
      font-size: 18px;
      cursor: pointer;
      display: flex; align-items: center; justify-content: center;
      transition: background 0.2s, border-color 0.2s, color 0.2s;
    }
    .trans-nav-btn:hover { background: rgba(0,100,180,0.35); border-color: rgba(0,200,255,0.6); color: #fff; }

    .trans-stop-dots {
      position: absolute; left: 20px; top: 50%; transform: translateY(-50%);
      display: flex; flex-direction: column; gap: 10px; z-index: 100;
    }
    .trans-dot {
      width: 9px; height: 9px; border-radius: 50%;
      background: rgba(0,140,200,0.25);
      border: 1px solid rgba(0,180,255,0.4);
      cursor: pointer;
      transition: background 0.25s, transform 0.25s;
    }
    .trans-dot.active { background: #00aaff; transform: scale(1.5); border-color: #00d4ff; }

    .trans-auto-btn {
      position: absolute; top: 20px; right: 20px;
      background: rgba(5,10,24,0.85);
      border: 1px solid rgba(0,180,255,0.25);
      border-radius: 8px; padding: 7px 14px;
      color: #66aacc; font-size: 11px; letter-spacing: 0.08em;
      cursor: pointer;
      transition: background 0.2s;
      z-index: 100;
    }
    .trans-auto-btn:hover { background: rgba(0,80,160,0.4); color: #fff; }
    .trans-auto-btn.active { border-color: rgba(0,255,180,0.5); color: #00ffaa; }
  `;
  container.appendChild(style);

  // Title
  const hudTitle = document.createElement('div');
  hudTitle.className = 'trans-hud-title';
  hudTitle.innerHTML = `<h1>Transformer Architecture</h1><p>Immersive Component Tour</p>`;
  container.appendChild(hudTitle);

  // Info panel
  const infoPanel = document.createElement('div');
  infoPanel.className = 'trans-info-panel';
  container.appendChild(infoPanel);

  // Nav bar
  const navBar = document.createElement('div');
  navBar.className = 'trans-nav-bar';
  navBar.innerHTML = `
    <button class="trans-nav-btn" id="trans-btn-prev">↑</button>
    <button class="trans-nav-btn" id="trans-btn-next">↓</button>
  `;
  container.appendChild(navBar);

  // Stop dots
  const dotsContainer = document.createElement('div');
  dotsContainer.className = 'trans-stop-dots';
  tourStops.forEach((s, i) => {
    const d = document.createElement('div');
    d.className = 'trans-dot';
    d.dataset.idx = i;
    d.title = s.label;
    dotsContainer.appendChild(d);
  });
  container.appendChild(dotsContainer);

  // Auto-tour button
  const autoBtn = document.createElement('button');
  autoBtn.className = 'trans-auto-btn';
  autoBtn.textContent = 'AUTO TOUR';
  container.appendChild(autoBtn);

  // ─── Tour State ───────────────────────────────────────────────────────────────
  let currentStop = 0;
  let autoTour = false;
  let autoTimer = 0;
  const AUTO_INTERVAL = 5.5;

  function goToStop(idx) {
    currentStop = (idx + tourStops.length) % tourStops.length;
    updateUI();
    animateCamera();
  }

  function updateUI() {
    const stop = tourStops[currentStop];
    infoPanel.innerHTML = `
      <div class="stop-num">Component ${currentStop + 1} / ${tourStops.length}</div>
      <div class="stop-name" style="color:#${stop.color.toString(16).padStart(6,'0')}">${stop.label}</div>
      <div class="stop-desc">${stop.description}</div>
      <div class="stop-detail">${stop.detail}</div>
    `;
    container.querySelectorAll('.trans-dot').forEach((d, i) => {
      d.classList.toggle('active', i === currentStop);
    });
  }

  function animateCamera() {
    const target = tourStops[currentStop].position.clone();
    const camTarget = target.clone().add(new THREE.Vector3(0, 0.5, 7.5));
    gsapTo(camera.position, camTarget, 1.4);
    gsapTo(controls.target, target, 1.4);
  }

  // Mini tween helper
  function gsapTo(obj, target, duration) {
    const start = { x: obj.x, y: obj.y, z: obj.z };
    const end = { x: target.x, y: target.y, z: target.z };
    const startTime = performance.now();
    const ms = duration * 1000;
    function tick() {
      const t = Math.min((performance.now() - startTime) / ms, 1);
      const e = t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t; // ease in-out quad
      obj.x = start.x + (end.x - start.x) * e;
      obj.y = start.y + (end.y - start.y) * e;
      obj.z = start.z + (end.z - start.z) * e;
      if (t < 1) requestAnimationFrame(tick);
    }
    tick();
  }

  // Events
  container.querySelector('#trans-btn-next').addEventListener('click', () => { autoTimer = 0; goToStop(currentStop + 1); });
  container.querySelector('#trans-btn-prev').addEventListener('click', () => { autoTimer = 0; goToStop(currentStop - 1); });
  container.querySelectorAll('.trans-dot').forEach(d => {
    d.addEventListener('click', () => { autoTimer = 0; goToStop(parseInt(d.dataset.idx)); });
  });
  autoBtn.addEventListener('click', () => {
    autoTour = !autoTour;
    autoBtn.classList.toggle('active', autoTour);
    autoBtn.textContent = autoTour ? 'PAUSE TOUR' : 'AUTO TOUR';
    autoTimer = 0;
  });

  // Handle keys only when mouse is over container
  let isMouseOver = false;
  container.addEventListener('mouseenter', () => isMouseOver = true);
  container.addEventListener('mouseleave', () => isMouseOver = false);

  window.addEventListener('keydown', e => {
    if (!isMouseOver) return;
    if (e.key === 'ArrowDown' || e.key === 's') { autoTimer = 0; goToStop(currentStop + 1); }
    if (e.key === 'ArrowUp' || e.key === 'w') { autoTimer = 0; goToStop(currentStop - 1); }
  });

  goToStop(0);

  // ─── Animation Loop ───────────────────────────────────────────────────────────
  const clock = new THREE.Clock();

  function animate() {
    const dt = clock.getDelta();
    const elapsed = clock.getElapsedTime();

    // Auto tour
    if (autoTour) {
      autoTimer += dt;
      if (autoTimer >= AUTO_INTERVAL) {
        autoTimer = 0;
        goToStop(currentStop + 1);
      }
    }

    // Animate particles
    particles.rotation.y = elapsed * 0.012;

    // Animate component meshes
    componentMeshes.forEach(({ group, mat, stop }, i) => {
      const isActive = i === currentStop;
      const dist = Math.abs(i - currentStop);
      const targetOpacity = isActive ? 1.0 : Math.max(0.25, 1 - dist * 0.22);
      mat.opacity += (targetOpacity - mat.opacity) * 0.08;
      mat.emissiveIntensity = isActive ? 1.4 + Math.sin(elapsed * 2) * 0.3 : 0.4;

      // Pulse active component
      if (isActive) {
        const pulse = 1 + Math.sin(elapsed * 2.5) * 0.04;
        group.scale.setScalar(pulse);
      } else {
        group.scale.lerp(new THREE.Vector3(1, 1, 1), 0.1);
      }

      // Gentle rotation for some shapes
      if (stop.shape === 'sphere_cluster') group.rotation.y = elapsed * 0.5;
      if (stop.shape === 'ring') group.rotation.z = elapsed * 0.3;
      if (stop.shape === 'pyramid') group.rotation.y = elapsed * 0.4;
    });

    // Flow particles along spine
    flowSpheres.forEach(s => {
      s.userData.t = (s.userData.t + s.userData.speed) % 1;
      const pt = spineCurve.getPoint(s.userData.t);
      pt.x += Math.sin(elapsed + s.userData.t * 30) * 0.3;
      pt.z += Math.cos(elapsed * 0.7 + s.userData.t * 20) * 0.3;
      s.position.copy(pt);
      // Color based on progress
      const c = new THREE.Color().setHSL(s.userData.t * 0.3 + 0.55, 1, 0.65);
      s.material.color.copy(c);
      s.material.opacity = 0.4 + Math.sin(elapsed * 3 + s.userData.t * 20) * 0.3;
    });

    // Pulse lights
    pointLight1.intensity = 2.5 + Math.sin(elapsed * 1.2) * 0.8;
    pointLight2.intensity = 2.5 + Math.cos(elapsed * 0.9) * 0.8;

    controls.update();
    renderer.render(scene, camera);
  }
  renderer.setAnimationLoop(animate);

  const resizeObserver = new ResizeObserver(() => {
    camera.aspect = container.clientWidth / container.clientHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(container.clientWidth, container.clientHeight);
  });
  resizeObserver.observe(container);
}
