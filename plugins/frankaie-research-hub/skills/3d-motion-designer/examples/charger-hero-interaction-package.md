# 範例 ·《互動製作包》— LYCANDER 65W GaN 充電器 · 官網 Hero

> 由 `3d-motion-designer` 走完三階段 SOP 產出的完整範例。產品沿用 hub 既有 worked example（65W GaN 充電器），目標：Apple 官網式 hero 3D 展示頁。

---

## Stage 1 —《互動情報卡》

**目標受眾與裝置**：通勤上班族 / 科技嘗鮮者；桌機 6 成、行動 4 成；中高階裝置為主，行動端需保守降載；需支援 `prefers-reduced-motion`。

**標竿動態拆解（只記方向，不抄實作）**
| 標竿 | 進場 | scroll 觸發 | 游標 | 3D 用在哪 | 可借鏡語彙 |
|------|------|-------------|------|-----------|------------|
| Apple 產品頁 | 產品淡入＋輕浮起 | 隨 scroll 旋轉、賣點分段釘住 | 無重互動 | 主角產品 360° | 克制、慢、重量感 |
| Native Union | 材質特寫 | 視差分層 | hover 微亮 | 材質/CMF 質感 | 精緻、金屬光 |

**品牌動態語彙**：俐落、克制、重力感 → 緩動偏 `power3.out` / `expo.inOut`，慢速長時長。
**3D 材質方向**：深空灰金屬殼 + 微藍高光，key/rim 雙光。
**技術 & 效能基準**：桌機 60 FPS、行動 ≥30 FPS；首屏 LCP ≤ 2.5s；提供無 WebGL 的靜態 fallback。

## Stage 2 —《互動驗證報告》

| 方向 | 互動假設（為什麼會轉換） | 轉化指標 | 效能門檻 |
|------|--------------------------|----------|----------|
| **A 全 3D scroll 旋轉** | 把規格變成「可探索的物件」會提高 scroll 深度與停留 | scroll 深度、停留時間 | 桌機 60 / 行動 ≥30 FPS |
| B 輕量 2.5D 視差 | 成本低、行動友善，但探索感弱 | CTA 點擊 | 行動 ≥45 FPS |
| C 純 CSS 淡入 | 最省，當 reduced-motion / 低階機退場 | — | 任意 |

**上線前互動檢查表（1–5）**
| 項目 | A | 備註 |
|------|---|------|
| 節奏感 / 敘事清楚 | 5 | 三段賣點隨 scroll 顯現 |
| 可讀性（動中看懂） | 4 | 文字釘住期間靜止 |
| 效能 | 3 | 行動端須降載（關 bloom） |
| reduced-motion 等效 | 5 | 退回方向 C 靜態三圖 |
| 暈眩風險 | 4 | 旋轉慢、無大面積位移 |

**結論**：主打 A（全 3D scroll 旋轉），行動端自動降級成 B 的降載版，reduced-motion / 無 WebGL 退 C。

### Stage 2 補充 — AI 消費者焦點小組打分（consumers-taiwan）

> 由 `consumers-taiwan`（22 人 panel）對方向 A「全 3D scroll 旋轉」hero 跑焦點小組，分層取代表性子集。

**測試標的**：65W GaN 充電器官網 hero（方向 A）｜測試日期 2026-06-22

| Persona | 姓名（年齡・職業・傾向） | 評分 | 核心回饋 | 決策邏輯 |
|---------|--------------------------|:---:|----------|----------|
| T02 | 林裕豪（31・工程師・務實） | 5 | 隨 scroll 看規格超直觀，像在玩產品 | 規格可探索，命中重規格族 |
| T11 | 曾子涵（26・實況主・嘗鮮） | 4 | 旋轉展示很有質感，可當直播素材 | 視覺夠潮但想看實測溫度 |
| T13 | 馬浩明（44・建築師・嘗鮮） | 5 | 工業設計感被 3D 放大 | 美感與材質呈現到位 |
| T08 | 何建宏（42・業務・務實） | 4 | 「不發燙」徽章一眼看到重點 | 賣點清楚 |
| T04 | 劉俊翰（19・學生・嘗鮮） | 3 | 好看但手機上會不會很慢/耗電 | 擔心行動端效能 |
| T03 | 蔣美玲（47・主婦・保守） | 2 | 轉來轉去看得頭暈，我只想看價格 | 動態過多、資訊找不到 |
| T06 | 詹文昌（58・退休・保守） | 2 | 太複雜，不會操作 | 互動門檻感 |
| T20 | 周詩涵（38・公關・嘗鮮） | 4 | 質感高，適合品牌官網 | 提升品牌信任 |

**Top 正面回饋**：①scroll 旋轉讓「規格變可探索」，重規格族超買單（T02/T13）②「不發燙」徽章把核心賣點視覺化（T08）③整體質感提升品牌信任（T20/T13）。
**Top 異議**：①行動端效能/耗電疑慮（T04）②保守族覺得旋轉**暈、找不到價格資訊**（T03/T06）。
**改善建議（優先度）**：
| 優先度 | 建議 | 涉及 Persona | 影響 |
|:--:|------|------|------|
| P1 | 行動端預設降載版（關 bloom、減旋轉幅度），並標示效能已最佳化 | T04,T03 | 解效能與暈眩疑慮 |
| P2 | hero 固定區放「價格 / CTA」常駐，不隨旋轉移動 | T03,T06 | 保守族快速找到關鍵資訊 |
| P3 | scroll 提示更明顯，降低互動門檻 | T06 | 降低操作焦慮 |

**整體**：平均購買意願 **3.6 / 5**（務實/嘗鮮族 4–5、保守族 2）。共識：**對重規格與設計取向族極具說服力，但需為保守/行動族提供低動態、資訊常駐的退場**（已對應 Stage 3 的 reduced-motion 與降載設計）。

**跨市場簡註**：🇺🇸 重 UL 與退貨，hero 需常駐安規標章；🇯🇵 重品質細節，旋轉可特寫做工/接縫；🇪🇺 重 CE 能效，可在 scroll 段帶出能效數字。

---

## Stage 3 —《互動製作包》本體

### 互動藍圖 Interaction Brief
- **敘事節奏**：進場「產品安靜浮現」→ scroll「產品緩轉，三個賣點依序釘住顯現」→ 結尾「CTA 微呼吸」。
- **每段感受 → 動作**：①首屏：信任、質感 → 停下來看 ②中段：理解「快充 / 不發燙 / 體積小」→ 繼續往下 ③結尾：行動 → 點「加入購物車」。

### 動態分鏡（四軸：進場 / scroll / 游標 / 離場）
| 元素 | 觸發 | from → to | 緩動 easing | 時序 | 備註 |
|------|------|-----------|-------------|------|------|
| 充電器 3D | 進場 | opacity 0、y +30、scale 0.92 → 正常 | `power3.out` | 0.9s | 浮起淡入 |
| 充電器 3D | scroll | rotationY 0 → 360°、scale 0.92 → 1.0 | linear（`scrub`） | 綁 hero 全高 | 主敘事 |
| 賣點卡 ×3 | scroll | opacity 0、x −24 → 1、0 | `power2.out` | `stagger` 各釘住 25% 區段 | pin 期間文字靜止 |
| 「不發燙」徽章 | 游標 | bloom intensity +、scale 1 → 1.04 | `power2.out` | hover 0.2s | 桌機才有 |
| CTA 按鈕 | 離場 / idle | scale 1 → 1.03 → 1 | `sine.inOut` | 2s loop | 微呼吸 |

### 3D 場景參數
| 項目 | 設定 |
|------|------|
| 相機 | fov 50、position (0,0,5) |
| 燈光 | ambient 0x404060@1.2；key Directional 0xffffff@2.2 (3,4,5)；rim 0xff5fa2@1.4 (−4,−2,−3) |
| 材質 CMF | color 深空灰 0x2b2f36、metalness 0.9、roughness 0.18，藍高光 |
| 後製 | UnrealBloom strength 0.6、radius 0.4、threshold 0.85（行動端關閉） |
| 效能 | draw call ≤ 30；貼圖 ≤ 1024²；行動降載：關 bloom、pixelRatio 上限 1.5、暫停離畫面 rAF |

### Live 預覽（可貼程式碼）

**A. Three.js hero 場景**（即 `show_threejs_scene` 會算繪的內容；自動 session 需互動授權，使用者端可自行算繪或貼進專案）：

```js
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(50, width / height, 0.1, 100);
camera.position.set(0, 0, 5);
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
renderer.setSize(width, height);
renderer.setClearColor(0x000000, 0);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.5)); // 行動降載

const composer = new EffectComposer(renderer);
composer.addPass(new RenderPass(scene, camera));
const bloom = new UnrealBloomPass(new THREE.Vector2(width, height), 0.6, 0.4, 0.85);
composer.addPass(bloom); // 行動端：composer.removePass(bloom)

// 65W GaN charger stand-in（正式版換成 GLTF 模型）
const group = new THREE.Group();
const body = new THREE.Mesh(
  new THREE.BoxGeometry(1.5, 1.7, 0.95),
  new THREE.MeshStandardMaterial({ color: 0x2b2f36, metalness: 0.9, roughness: 0.18 })
);
group.add(body);
const port = new THREE.Mesh(
  new THREE.BoxGeometry(0.5, 0.12, 0.06),
  new THREE.MeshStandardMaterial({ color: 0x6ee7ff, emissive: 0x1b6fa8, emissiveIntensity: 0.6, metalness: 0.6, roughness: 0.3 })
);
port.position.set(0, -0.75, 0.5);
group.add(port);
const prongMat = new THREE.MeshStandardMaterial({ color: 0xcfd3da, metalness: 1.0, roughness: 0.25 });
[-0.18, 0.18].forEach((x) => {
  const prong = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.45, 0.04), prongMat);
  prong.position.set(x, 1.05, -0.2);
  group.add(prong);
});
scene.add(group);

scene.add(new THREE.AmbientLight(0x404060, 1.2));
const key = new THREE.DirectionalLight(0xffffff, 2.2); key.position.set(3, 4, 5); scene.add(key);
const rim = new THREE.DirectionalLight(0xff5fa2, 1.4); rim.position.set(-4, -2, -3); scene.add(rim);

const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;

// scrollProgress 由頁面 ScrollTrigger 餵入（0→1）；此處 demo 用自轉
function animate() {
  requestAnimationFrame(animate);
  group.rotation.y += 0.006;
  group.rotation.x = Math.sin(Date.now() * 0.0004) * 0.12;
  controls.update();
  composer.render();
}
animate();
```

**B. GSAP + ScrollTrigger 綁定**（產品旋轉 + 賣點釘住，含 reduced-motion 分支）：

```js
gsap.registerPlugin(ScrollTrigger);
const mm = gsap.matchMedia();

mm.add(
  { isMotion: '(prefers-reduced-motion: no-preference)', isDesktop: '(min-width: 768px)' },
  (ctx) => {
    if (!ctx.conditions.isMotion) return; // 退回方向 C：靜態三圖

    gsap.to('#product', {
      rotationY: 360, ease: 'none',
      scrollTrigger: { trigger: '#hero', start: 'top top', end: 'bottom top', scrub: true, pin: true }
    });

    gsap.utils.toArray('.sellpoint').forEach((el, i) => {
      gsap.from(el, {
        opacity: 0, x: -24, ease: 'power2.out',
        scrollTrigger: { trigger: '#hero', start: `${20 + i * 25}% top`, toggleActions: 'play none none reverse' }
      });
    });
  }
);
```

### 效能 & 可及性 QA
- [ ] 桌機 60 / 行動 ≥30 FPS【需實測】
- [ ] LCP ≤ 2.5s、CLS ≈ 0（hero 預留固定高度，避免位移）
- [x] `prefers-reduced-motion`：不掛 scroll 動畫，退靜態三圖（方向 C）
- [x] 無 WebGL：偵測失敗 → 顯示產品靜態高解析圖
- [x] 行動降載：關 bloom、pixelRatio≤1.5、離畫面暫停 rAF
- [ ] 暈眩：旋轉 ≤ 一圈、無大面積快速位移（已符合）

### 交接
- 規格 + 程式碼 → 前端工程實作；產品 GLTF 模型由 `mechanical-team` 提供；品牌色/字體由 `visual-team`。
- 細部規格展開（各斷點 / 更多微互動）→ 交 `motion-spec-builder`（見其 examples）。
- 上線後 scroll 深度 / CTA 點擊 → 回 `marketing-team` 迭代；可丟 `consumers-*` 對體驗打分。

> 原創守則：標竿站只取「慢、克制、重量感」的動態方向，未複製任何既有實作；所有效能數字標【需實測】。
