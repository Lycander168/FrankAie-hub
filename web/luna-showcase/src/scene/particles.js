import * as THREE from 'three';

// 星塵 / 光點粒子系統 —— 取代影片裡的茶葉與蒸氣。
//  - spread=1 散落漂浮（chapter 散落）
//  - spread=0 收束進機身（chapter 匯聚）
//  - rise>0 向上升起的能量場（chapter 發光，取代蒸氣）

function makeDotTexture() {
  const s = 64;
  const c = document.createElement('canvas');
  c.width = c.height = s;
  const ctx = c.getContext('2d');
  const g = ctx.createRadialGradient(s / 2, s / 2, 0, s / 2, s / 2, s / 2);
  g.addColorStop(0, 'rgba(255,255,255,1)');
  g.addColorStop(0.35, 'rgba(255,236,196,0.85)');
  g.addColorStop(1, 'rgba(255,236,196,0)');
  ctx.fillStyle = g;
  ctx.fillRect(0, 0, s, s);
  const tex = new THREE.CanvasTexture(c);
  tex.colorSpace = THREE.SRGBColorSpace;
  return tex;
}

export class Particles {
  constructor({ count = 1400 } = {}) {
    this.count = count;
    this.spread = 1; // 1 散落 → 0 收束
    this.rise = 0; // 能量上升強度
    this.opacity = 0;
    this._t = 0;

    const geo = new THREE.BufferGeometry();
    const pos = new Float32Array(count * 3);
    const dir = new Float32Array(count * 3); // 單位方向（散落用）
    const radius = new Float32Array(count); // 散落半徑
    const speed = new Float32Array(count); // 漂浮速度
    const phase = new Float32Array(count);
    const col = new Float32Array(count * 3);

    const warm = new THREE.Color('#ffd9a0');
    const gold = new THREE.Color('#ffb45a');
    const cool = new THREE.Color('#cfe0ff');

    for (let i = 0; i < count; i++) {
      // 均勻分布於球面方向
      const u = Math.random() * 2 - 1;
      const th = Math.random() * Math.PI * 2;
      const r = Math.sqrt(1 - u * u);
      dir[i * 3] = r * Math.cos(th);
      dir[i * 3 + 1] = u;
      dir[i * 3 + 2] = r * Math.sin(th);

      radius[i] = 2.2 + Math.random() * 4.5;
      speed[i] = 0.2 + Math.random() * 0.8;
      phase[i] = Math.random() * Math.PI * 2;

      const c = Math.random();
      const base = c < 0.55 ? warm : c < 0.85 ? gold : cool;
      col[i * 3] = base.r;
      col[i * 3 + 1] = base.g;
      col[i * 3 + 2] = base.b;
    }

    geo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
    geo.setAttribute('color', new THREE.BufferAttribute(col, 3));
    this._dir = dir;
    this._radius = radius;
    this._speed = speed;
    this._phase = phase;
    this._pos = pos;
    this._col = col;
    this._baseCol = col.slice(); // 原始色，能量上升時依高度衰減後可還原
    this._colDirty = false;

    const mat = new THREE.PointsMaterial({
      size: 0.07,
      map: makeDotTexture(),
      vertexColors: true,
      transparent: true,
      opacity: 0,
      depthWrite: false,
      blending: THREE.AdditiveBlending,
      sizeAttenuation: true,
    });
    this.material = mat;
    this.points = new THREE.Points(geo, mat);
    this.points.frustumCulled = false;
  }

  setState({ spread, rise, opacity }) {
    if (spread != null) this.spread = spread;
    if (rise != null) this.rise = rise;
    if (opacity != null) this.opacity = opacity;
  }

  update(dt) {
    this._t += dt;
    const t = this._t;
    const pos = this._pos;
    const dir = this._dir;
    const rad = this._radius;
    const spd = this._speed;
    const ph = this._phase;
    const spread = this.spread;
    const riseAmt = this.rise;
    const rising = riseAmt > 0.001;
    const CLIMB = 5.0; // 爬升高度（越大越往上飄）
    const col = this._col;
    const base = this._baseCol;

    for (let i = 0; i < this.count; i++) {
      const i3 = i * 3;
      // 收束時半徑趨近一個小核心；散落時拉到完整半徑
      const r = THREE.MathUtils.lerp(0.25, rad[i], spread);
      const drift = Math.sin(t * spd[i] + ph[i]) * 0.18 * spread;

      let y = dir[i3 + 1] * (r + drift);
      // 水平擴張係數（上升時略往外散，像煙柱）
      let spreadX = 1;

      if (rising) {
        const climb = (t * spd[i] * 0.7 + ph[i]) % 1.0; // 0→1 循環
        y += riseAmt * climb * CLIMB; // 向上爬升（能量/蒸氣）
        spreadX = 1 + riseAmt * climb * 0.4;
        // 越高越淡（additive blending：色值越小越透）
        const fade = 1 - riseAmt * climb;
        col[i3] = base[i3] * fade;
        col[i3 + 1] = base[i3 + 1] * fade;
        col[i3 + 2] = base[i3 + 2] * fade;
      }

      pos[i3] = dir[i3] * (r + drift) * spreadX;
      pos[i3 + 1] = y;
      pos[i3 + 2] = dir[i3 + 2] * (r + drift) * spreadX;
    }
    this.points.geometry.attributes.position.needsUpdate = true;

    if (rising) {
      this.points.geometry.attributes.color.needsUpdate = true;
      this._colDirty = true;
    } else if (this._colDirty) {
      // 上升結束 → 還原原始色（只做一次）
      col.set(base);
      this.points.geometry.attributes.color.needsUpdate = true;
      this._colDirty = false;
    }
    // 平滑 opacity
    this.material.opacity += (this.opacity - this.material.opacity) * Math.min(1, dt * 4);
    this.points.rotation.y += dt * 0.04 * (0.4 + spread);
  }

  setQuality(low) {
    this.material.size = low ? 0.058 : 0.07;
  }
}
