import * as THREE from 'three';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
import { LunaModel } from './model.js';
import { Particles } from './particles.js';

// 線性插值關鍵格：stops = [[pos, value], ...]，pos 為 0..1 的捲動進度。
function kf(p, stops) {
  if (p <= stops[0][0]) return stops[0][1];
  const last = stops[stops.length - 1];
  if (p >= last[0]) return last[1];
  for (let i = 1; i < stops.length; i++) {
    const [p1, v1] = stops[i];
    if (p <= p1) {
      const [p0, v0] = stops[i - 1];
      const t = (p - p0) / (p1 - p0);
      return v0 + (v1 - v0) * t;
    }
  }
  return last[1];
}

export class Scene {
  constructor(canvas, { reducedMotion = false } = {}) {
    this.canvas = canvas;
    this.reduced = reducedMotion;
    this.progress = 0;
    this._target = 0;
    this.clock = new THREE.Clock();

    this.renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true, powerPreference: 'high-performance' });
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    this.renderer.toneMapping = THREE.ACESFilmicToneMapping;
    this.renderer.toneMappingExposure = 1.05;
    this.renderer.outputColorSpace = THREE.SRGBColorSpace;

    this.scene = new THREE.Scene();
    this.scene.fog = new THREE.FogExp2(0x05060a, 0.045);

    this.camera = new THREE.PerspectiveCamera(42, 1, 0.1, 100);
    this.camera.position.set(0, 0.2, 8.5);

    // 環境光照（用 RoomEnvironment 讓金屬材質有反射）
    const pmrem = new THREE.PMREMGenerator(this.renderer);
    this.scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;

    const key = new THREE.DirectionalLight(0xfff0d8, 2.0);
    key.position.set(3, 4, 5);
    const rim = new THREE.DirectionalLight(0x9fc0ff, 1.2);
    rim.position.set(-4, 1, -3);
    const amb = new THREE.AmbientLight(0x404a66, 0.6);
    this.scene.add(key, rim, amb);

    // 中央暖光點（發光時加強）
    this.glowLight = new THREE.PointLight(0xffcf8a, 0, 12, 2);
    this.glowLight.position.set(0, 0, 1.2);
    this.scene.add(this.glowLight);

    this.group = new THREE.Group();
    this.scene.add(this.group);

    this.model = new LunaModel();
    this.group.add(this.model.root);

    this.particles = new Particles({ count: reducedMotion ? 500 : 1400 });
    this.group.add(this.particles.points);

    // 後製：Bloom 光暈
    this.composer = new EffectComposer(this.renderer);
    this.composer.addPass(new RenderPass(this.scene, this.camera));
    this.bloom = new UnrealBloomPass(new THREE.Vector2(1, 1), 0.6, 0.85, 0.2);
    this.bloom.strength = 0.5;
    if (!reducedMotion) this.composer.addPass(this.bloom);

    this.resize();
    window.addEventListener('resize', () => this.resize());
  }

  async init() {
    await this.model.load();
  }

  // 由 main.js 餵入 0..1 的整體捲動進度
  setProgress(p) {
    this._target = THREE.MathUtils.clamp(p, 0, 1);
  }

  resize() {
    const w = window.innerWidth;
    const h = window.innerHeight;
    this.camera.aspect = w / h;
    this.camera.updateProjectionMatrix();
    this.renderer.setSize(w, h, false);
    this.composer.setSize(w, h);
    // 直式（手機）把模型拉近一點，桌機拉遠
    this.camera.position.z = w < 760 ? 9.8 : 8.5;
  }

  render() {
    const dt = Math.min(this.clock.getDelta(), 0.05);
    // 平滑追進度（即使 Lenis 已平滑，再補一層讓 3D 更柔）
    this.progress += (this._target - this.progress) * Math.min(1, dt * 6);
    const p = this.progress;

    // ── 把整體進度映射到各特效參數（對應影片 6 節點）──
    // 散落程度：hero 微散 → scatter 全散 → assemble 收合 → 之後保持組裝
    const assembly = kf(p, [
      [0.0, 0.35],
      [0.18, 0.9],
      [0.32, 1.0],
      [0.58, 0.0],
      [1.0, 0.0],
    ]);
    // 粒子散落（與模型炸開同步，發光後淡出）
    const spread = kf(p, [
      [0.0, 0.55],
      [0.3, 1.0],
      [0.58, 0.12],
      [0.78, 0.05],
      [1.0, 0.0],
    ]);
    const pOpacity = kf(p, [
      [0.0, 0.5],
      [0.3, 0.95],
      [0.62, 0.6],
      [0.72, 0.9],
      [0.85, 0.25],
      [1.0, 0.1],
    ]);
    // 發光：assemble 末段啟動 → glow 章節達峰 → 之後維持微亮
    const glow = kf(p, [
      [0.5, 0.0],
      [0.66, 1.0],
      [0.78, 0.7],
      [1.0, 0.55],
    ]);
    // 能量上升（取代蒸氣）
    const rise = kf(p, [
      [0.6, 0.0],
      [0.7, 0.5],
      [0.8, 0.25],
      [1.0, 0.0],
    ]);

    this.model.setAssembly(assembly);
    this.model.setGlow(glow);
    this.particles.setState({ spread, rise, opacity: pOpacity });

    // 相機 / 群組運鏡
    const spin = this.reduced ? 0 : 1;
    this.group.rotation.y = kf(p, [
      [0, -0.5],
      [0.32, 0.4],
      [0.6, Math.PI * 0.9],
      [1.0, Math.PI * 1.15],
    ]) * spin;
    this.group.rotation.x = Math.sin(p * Math.PI) * 0.12;
    this.camera.position.y = 0.2 + Math.sin(p * Math.PI) * 0.3;

    this.glowLight.intensity = glow * 3.2;
    this.bloom.strength = 0.45 + glow * 0.9;

    this.model.update(dt);
    this.particles.update(dt);

    if (this.reduced) this.renderer.render(this.scene, this.camera);
    else this.composer.render();
  }
}
