# 範例 · 動態規格 — 小露娜 Luna 無線充電盤 Hero（全斷點）

> 由 `motion-spec-builder` 接棒 `3d-motion-designer` 的《小露娜互動製作包》，展開成各斷點參數 + 完整微互動 + 可貼程式碼。核心語彙：磁吸 `back.out` overshoot ＋ 月光環呼吸。

---

## 斷點矩陣（同一敘事，三種降載）
| 斷點 | 實作層級 | 3D | bloom | pixelRatio | 磁吸吸附 | 月光環 | 微互動 |
|------|----------|----|-------|-----------|----------|--------|--------|
| Desktop ≥1024 | Three.js 全效 | ✅ GLTF | ✅ 0.8 | ≤2 | scrub+pin snap | 呼吸發光 | 游標 tilt 視差 / hover |
| Tablet 768–1023 | Three.js 降載 | ✅ | ❌ | ≤1.5 | scrub+pin snap | 貼圖發光 | tap 高亮 |
| Mobile <768 | 2.5D 視差 | ❌ 靜態圖層 | ❌ | — | 手機圖層滑入吸附 | 貼圖呼吸（CSS） | tap 高亮 |
| reduced-motion / 無 WebGL | 純 CSS | ❌ | ❌ | — | 手機直接定位 | 靜態亮 | fade-in only |

## 完整微互動清單（四軸）
| # | 元素 | 觸發 | from → to | 緩動 | 時序 | 斷點 |
|---|------|------|-----------|------|------|------|
| 1 | 充電盤 | 進場 | op0,scale.9 → 1 | `power3.out` | 0.8s | all |
| 2 | 手機 | scroll 段1 | y−180,rotZ−8° → 0,0 | **`back.out(1.4)`** | scrub snap | ≥768（行動：圖層滑入） |
| 3 | 盤面 | 吸附末 | scale .98→1（反彈） | `elastic.out(1,0.5)` | 0.4s | ≥768 |
| 4 | 月光環 | scroll 段2 | --glow .3→1、scale 1→1.06 | `sine.inOut` | 1.6s loop | all（行動用 CSS） |
| 5 | 規格字卡 | scroll 段2 | op0,y+16 → 1,0 | `power2.out` | 0.5s | all（焦點小組 P1）|
| 6 | 電量數字 | scroll 段2 | 0 → 35（counter） | `power1.out` | 1.2s | ≥768 |
| 7 | 手機 | 游標 | tilt ±5° 視差 | `power2.out` | 0.4s | ≥1024 pointer:fine |
| 8 | CTA | idle/hover | scale 1→1.03→1 / →1.05 | `sine.inOut`/`power2.out` | 2s loop / .18s | all |
| 9 | 低動態開關 | UI | 一鍵停動畫（保守族） | — | — | all（焦點小組 P2）|

## 可貼程式碼（responsive + a11y 整合）

```js
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
gsap.registerPlugin(ScrollTrigger);

const mm = gsap.matchMedia();

// ── ≥768 且允許動態：磁吸吸附 + 月光呼吸敘事 ──
mm.add(
  { motion: '(prefers-reduced-motion: no-preference)', tablet: '(min-width: 768px)', desktop: '(min-width: 1024px)' },
  (ctx) => {
    const { motion, desktop } = ctx.conditions;
    if (!motion) return;

    const tl = gsap.timeline({
      scrollTrigger: { trigger: '#luna-hero', start: 'top top', end: '+=140%', scrub: 0.5, pin: true }
    });
    tl.fromTo('#phone', { y: -180, rotateZ: -8, opacity: 0 },
                        { y: 0, rotateZ: 0, opacity: 1, ease: 'back.out(1.4)' }, 0)          // #2 吸附 overshoot
      .fromTo('#pad', { scale: 0.98 }, { scale: 1, ease: 'elastic.out(1,0.5)', duration: 0.4 }, '>-0.1') // #3 反彈
      .to('#ring', { '--glow': 1, scale: 1.06, repeat: -1, yoyo: true, ease: 'sine.inOut', duration: 1.6 }, '>') // #4 月光呼吸
      .from('#spec-card', { opacity: 0, y: 16, ease: 'power2.out', duration: 0.5 }, '<')      // #5 規格字卡
      .to('#battery', { innerText: 35, snap: { innerText: 1 }, ease: 'power1.out', duration: 1.2 }, '<'); // #6 電量

    // #7 游標 tilt 視差（desktop + 細指標）
    if (desktop && matchMedia('(pointer:fine)').matches) {
      const hero = document.querySelector('#luna-hero');
      hero.addEventListener('pointermove', (e) => {
        const nx = (e.clientX / innerWidth - 0.5), ny = (e.clientY / innerHeight - 0.5);
        gsap.to('#phone', { rotationY: nx * 5, rotationX: -ny * 5, ease: 'power2.out', duration: 0.4, overwrite: 'auto' });
      });
    }
  }
);

// ── reduced-motion fallback：手機定位、月光靜態、電量終值 ──
mm.add('(prefers-reduced-motion: reduce)', () => {
  gsap.set('#phone', { y: 0, rotateZ: 0, opacity: 1 });
  gsap.set('#ring', { '--glow': 1 });
  document.querySelector('#battery').textContent = '35';
});
```

```css
/* 月光環呼吸（行動 / 無 JS 用純 CSS；reduced-motion 自動停） */
#ring { --glow: 0.3; box-shadow: 0 0 calc(var(--glow) * 40px) rgba(188,212,255,var(--glow)); }
@media (prefers-reduced-motion: no-preference) and (max-width: 767px) {
  #ring { animation: luna-breathe 1.6s ease-in-out infinite; }
  @keyframes luna-breathe { 0%,100%{--glow:.4} 50%{--glow:1} }
}
.cta { transition: transform .18s ease; }
.cta:hover { transform: scale(1.05); }
```

## 效能 & a11y
- [x] reduced-motion 完整退場（matchMedia + CSS 雙保險）；提供「低動態開關」給保守族（焦點小組 P2）
- [x] 行動關 3D/bloom、月光環改 CSS/貼圖、`pointer:fine` 才掛游標視差
- [x] 規格字卡常駐補足務實/保守族信任（焦點小組 P1）
- [ ] 吸附 overshoot 幅度 / 各斷點 FPS / LCP / CLS【需實測】

> 來源製作包：`skills/3d-motion-designer/examples/wireless-pad-interaction-package.md`（小露娜 Luna）。
