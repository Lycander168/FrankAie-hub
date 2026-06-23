import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { DRACOLoader } from 'three/addons/loaders/DRACOLoader.js';

// 小露娜模型控制器。
//  - 嘗試載入 public/models/luna.glb（由使用者 STEP 轉檔而來）。
//  - 載不到時，建一個程式化 placeholder（3C 配件量感），動線仍可完整運作。
//  - 提供 setAssembly(0..1)：0 完全組裝、1 完全炸開（exploded view）。
//  - 提供 setGlow(0..1)：控制發光部位的 emissive 強度。

export class LunaModel {
  constructor() {
    this.root = new THREE.Group();
    this.parts = []; // { mesh, base:Vector3, dir:Vector3, dist:number, phase:number }
    this.emissives = [];
    this.assembly = 0;
    this.glow = 0;
    this.ready = false;
    this._t = 0;
  }

  async load(url = './models/luna.glb') {
    try {
      const loader = new GLTFLoader();
      const draco = new DRACOLoader();
      draco.setDecoderPath('https://www.gstatic.com/draco/v1/decoders/');
      loader.setDRACOLoader(draco);
      const gltf = await loader.loadAsync(url);
      this._ingest(gltf.scene);
      this._buildParts();
      this.ready = true;
      return true;
    } catch (e) {
      console.warn('[luna] GLB 載入失敗，改用 placeholder：', e?.message || e);
      this._buildPlaceholder();
      this._buildParts();
      this.ready = true;
      return false;
    }
  }

  _ingest(scene) {
    // 置中 + 等比縮放到適合視野的尺寸
    const box = new THREE.Box3().setFromObject(scene);
    const size = box.getSize(new THREE.Vector3());
    const center = box.getCenter(new THREE.Vector3());
    const maxDim = Math.max(size.x, size.y, size.z) || 1;
    const scale = 3.2 / maxDim;
    scene.position.sub(center);
    const wrap = new THREE.Group();
    wrap.add(scene);
    wrap.scale.setScalar(scale);

    // STEP/CAD 沒有材質 → 套上品牌化深色金屬材質，避免一片灰。
    // 用零件 z 範圍當啟發式：較靠正面/小體積者當作「發光指示區」。
    const bodyMat = () =>
      new THREE.MeshStandardMaterial({
        color: '#171a22',
        metalness: 0.9,
        roughness: 0.32,
        emissive: new THREE.Color('#ffcf8a'),
        emissiveIntensity: 0,
        envMapIntensity: 1.2,
      });

    scene.traverse((o) => {
      if (o.isMesh) {
        o.castShadow = false;
        o.receiveShadow = false;
        const m = bodyMat();
        // 名稱含 shouji（手機）等示意配件略微透亮，與主機身區分
        if (/shouji|phone|watch|pod/i.test(o.name)) {
          m.color = new THREE.Color('#0e1118');
          m.roughness = 0.5;
          m.metalness = 0.4;
        }
        m.userData.glowMax = /shouji|phone|watch|pod/i.test(o.name) ? 0.25 : 0.55;
        o.material = m;
        this.emissives.push(m); // 全部可隨 glow 微微暖亮
      }
    });
    this.root.add(wrap);
  }

  _buildPlaceholder() {
    const body = new THREE.Group();
    const matBody = new THREE.MeshStandardMaterial({ color: '#1b1e27', metalness: 0.85, roughness: 0.28 });
    const matRing = new THREE.MeshStandardMaterial({
      color: '#10131a',
      metalness: 0.4,
      roughness: 0.5,
      emissive: new THREE.Color('#ffcf8a'),
      emissiveIntensity: 0,
    });
    const matDome = new THREE.MeshStandardMaterial({
      color: '#0e1118',
      metalness: 0.2,
      roughness: 0.15,
      emissive: new THREE.Color('#bcd2ff'),
      emissiveIntensity: 0,
    });
    matRing.userData.glowMax = 2.4;
    matDome.userData.glowMax = 1.8;
    this.emissives.push(matRing, matDome);

    // 機身（圓角盤）
    const slab = new THREE.Mesh(new THREE.CylinderGeometry(1.1, 1.1, 0.34, 64), matBody);
    slab.rotation.x = Math.PI / 2;
    body.add(slab);

    // 發光環（MagSafe 對位環）
    const ring = new THREE.Mesh(new THREE.TorusGeometry(0.72, 0.05, 24, 80), matRing);
    ring.position.z = 0.18;
    body.add(ring);

    // 中央柔光點
    const dome = new THREE.Mesh(new THREE.SphereGeometry(0.34, 48, 48), matDome);
    dome.position.z = 0.16;
    body.add(dome);

    // 折疊支架
    const stand = new THREE.Mesh(new THREE.BoxGeometry(1.6, 0.9, 0.06), matBody);
    stand.position.set(0, -0.1, -0.22);
    stand.rotation.x = -0.5;
    body.add(stand);

    // 兩側充電墊（3-in-1）
    const padGeo = new THREE.CylinderGeometry(0.42, 0.42, 0.1, 48);
    const padL = new THREE.Mesh(padGeo, matBody.clone());
    padL.rotation.x = Math.PI / 2;
    padL.position.set(-1.4, 0, 0);
    const padR = padL.clone();
    padR.position.set(1.4, 0, 0);
    body.add(padL, padR);

    this.root.add(body);
  }

  _buildParts() {
    // 收集所有 mesh 當作可炸開的零件
    const meshes = [];
    this.root.traverse((o) => o.isMesh && meshes.push(o));
    const center = new THREE.Vector3();

    meshes.forEach((m, i) => {
      const base = m.position.clone();
      // 炸開方向：由整體中心指向零件位置；太靠中心者給隨機方向
      m.getWorldPosition(center);
      let dir = center.clone().sub(this.root.position).normalize();
      if (!isFinite(dir.x) || dir.lengthSq() < 0.001) {
        dir = new THREE.Vector3(Math.random() - 0.5, Math.random() - 0.5, Math.random() - 0.5).normalize();
      }
      this.parts.push({
        mesh: m,
        base,
        dir,
        dist: 2.4 + (i % 5) * 0.6,
        phase: Math.random() * Math.PI * 2,
      });
    });
  }

  setAssembly(a) {
    this.assembly = THREE.MathUtils.clamp(a, 0, 1);
  }
  setGlow(g) {
    this.glow = THREE.MathUtils.clamp(g, 0, 1);
  }

  update(dt) {
    if (!this.ready) return;
    this._t += dt;
    const a = this.assembly;

    for (const p of this.parts) {
      const float = Math.sin(this._t * 0.8 + p.phase) * 0.12 * a;
      const offX = p.dir.x * p.dist * a;
      const offY = p.dir.y * p.dist * a + float;
      const offZ = p.dir.z * p.dist * a;
      p.mesh.position.set(p.base.x + offX, p.base.y + offY, p.base.z + offZ);
      // 炸開時零件自轉一點，增加散落感
      p.mesh.rotation.z = p.phase + a * 1.2;
    }

    // 發光
    const gi = this.glow;
    for (const m of this.emissives) {
      const target = gi * (m.userData.glowMax ?? 1.0);
      m.emissiveIntensity += (target - m.emissiveIntensity) * Math.min(1, dt * 4);
    }
  }
}
