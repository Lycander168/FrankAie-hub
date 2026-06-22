# 範例 ·《互動製作包》— LYCANDER 無線充電盤（MagSafe 相容）· 官網 Hero

> 第二個範例，刻意換一個「核心動態語彙不同」的產品：無線充電盤的靈魂是**磁吸吸附感**，用帶 overshoot 的緩動（`back.out`）表現磁力——與充電器的「克制旋轉」形成對照。

---

## Stage 1 —《互動情報卡》
- **受眾/裝置**：桌面族（辦公桌情境）＋ iPhone 用戶；桌機 5 / 行動 5；質感取向高。
- **標竿語彙**：俯視 45° 產品擺拍、手機「啪」一聲吸附的磁吸動作、充電光環呼吸。
- **品牌動態語彙**：磁吸「吸附感」是核心 → 用帶輕微 overshoot 的緩動（`back.out(1.4)`）表現磁力。
- **3D 材質**：霧面矽膠盤面 + 鋁合金邊框；中央充電圈會發光（bloom 主角）。
- **效能基準**：桌機 60 / 行動 ≥30 FPS；LCP ≤ 2.5s。

## Stage 2 —《互動驗證報告》
| 方向 | 假設 | 指標 | 效能門檻 |
|------|------|------|----------|
| **A 手機磁吸吸附動畫**（主打） | 演示「一放就吸、自動對位」最能傳達 MagSafe 價值 → 提高 CTA | CTA 點擊、停留 | 桌機60/行動≥30 |
| B 純產品旋轉 | 質感夠但沒講到磁吸賣點 | scroll 深度 | — |
| C 靜態圖 | reduced-motion / 低階退場 | — | — |

**檢查表重點**：吸附動作要短促有力（overshoot）但不暈；充電光環脈動要慢。**結論主打 A**。

---

## Stage 3 —《互動製作包》本體

### 互動藍圖
進場「盤面浮現」→ scroll 段1「手機從上方滑入、磁吸吸附對位」→ 段2「充電光環亮起呼吸 + 電量數字跳動」→ 段3「CTA」。

### 動態分鏡（四軸）
| 元素 | 觸發 | from → to | 緩動 | 時序 | 備註 |
|------|------|-----------|------|------|------|
| 充電盤 | 進場 | op0,scale.9 → 1 | `power3.out` | 0.8s | |
| 手機 | scroll 段1 | y −180,rot −8° → 吸附位,0° | **`back.out(1.4)`** | scrub 後段 snap | 磁吸 overshoot 是靈魂 |
| 吸附瞬間 | scroll 段1 末 | 盤面微縮 0.98→1（受力反彈） | `elastic.out(1,0.5)` | 0.4s | 力回饋 |
| 充電光環 | scroll 段2 | op 0.3→1 脈動、scale 1→1.06 | `sine.inOut` | 1.6s loop | bloom 主角 |
| 電量數字 | scroll 段2 | 0% → 35% 跳動 | `power1.out` | 1.2s | counter |
| 手機 | 游標 | 輕微 tilt 視差 ±5° | `power2.out` | 0.4s | 桌機 only |
| CTA | idle/hover | 同充電器規格（微呼吸 / hover） | `sine.inOut`/`power2.out` | | 複用 |

### 3D 場景參數
| 項目 | 設定 |
|------|------|
| 相機 | fov 45、俯視 position (0, 2.4, 4.5)、lookAt(0,0,0) |
| 燈光 | ambient 0x3a3a4a@1.0；key 0xffffff@2.0 (2,5,4)；rim 冷藍 0x6ee7ff@1.2 (−3,1,−3) |
| 材質 | 盤面霧面矽膠 color 0x1f2228 roughness 0.7；鋁框 metalness 1.0 roughness 0.3 |
| 光環 | emissive 0x6ee7ff、UnrealBloom strength 0.8、threshold 0.8 |
| 效能 | draw call ≤ 25；行動關 bloom、光環改用貼圖發光 |

### Live 預覽（可貼程式碼 — 磁吸吸附是重點）

```js
// 手機磁吸：scrub 進來 + 末段 overshoot snap（GSAP timeline 綁 ScrollTrigger）
const tl = gsap.timeline({
  scrollTrigger: { trigger: '#pad-hero', start: 'top top', end: '+=140%', scrub: 0.5, pin: true }
});
tl.fromTo('#phone',
  { y: -180, rotateZ: -8, opacity: 0 },
  { y: 0, rotateZ: 0, opacity: 1, ease: 'back.out(1.4)' }, 0)                              // 吸附 overshoot
  .fromTo('#pad', { scale: 0.98 }, { scale: 1, ease: 'elastic.out(1,0.5)', duration: 0.4 }, '>-0.1') // 受力反彈
  .to('#ring', { '--glow': 1, scale: 1.06, repeat: -1, yoyo: true, ease: 'sine.inOut', duration: 1.6 }, '>') // 充電呼吸
  .to('#battery', { innerText: 35, snap: { innerText: 1 }, ease: 'power1.out', duration: 1.2 }, '<'); // 電量跳動
```

### 效能 & a11y QA
- [x] reduced-motion：手機直接定位、光環靜態亮、電量顯示終值（無跳動/吸附）
- [x] 無 WebGL：俯視靜態產品圖 + 靜態光環
- [x] 行動：關 bloom、光環用貼圖、pixelRatio≤1.5
- [ ] 吸附 overshoot 幅度實測不致暈眩【需實測】
- [ ] FPS / LCP / CLS【需實測】

### 交接
模型 → `mechanical-team`；品牌資產 → `visual-team`；斷點展開 → `motion-spec-builder`；成效 → `marketing-team`／`consumers-*` 打分。

> 對照重點：充電器靠「克制旋轉（power3/linear）」、充電盤靠「磁吸 overshoot（back.out / elastic）」——同一 skill，依產品價值選不同的緩動語彙。
