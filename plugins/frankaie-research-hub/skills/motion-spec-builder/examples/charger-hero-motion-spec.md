# 範例 · 動態規格 — 65W GaN 充電器 Hero（全斷點）

> 由 `motion-spec-builder` 接棒 `3d-motion-designer` 的《互動製作包》，展開成各斷點參數 + 完整微互動 + 可貼程式碼。

---

## 斷點矩陣（同一敘事，三種降載）
| 斷點 | 實作層級 | 3D | bloom | pixelRatio | scroll 旋轉 | 微互動 |
|------|----------|----|-------|-----------|-------------|--------|
| Desktop ≥1024 | Three.js 全效 | ✅ GLTF | ✅ 0.6 | ≤2 | 一圈 scrub+pin | hover bloom / 游標視差 |
| Tablet 768–1023 | Three.js 降載 | ✅ | ❌ | ≤1.5 | 一圈 scrub+pin | tap 高亮 |
| Mobile <768 | 2.5D 視差 | ❌ 靜態圖層 | ❌ | — | 視差位移 | tap 高亮 |
| reduced-motion / 無 WebGL | 純 CSS | ❌ | ❌ | — | 無 | fade-in only |

## 完整微互動清單（四軸）
| # | 元素 | 觸發 | from → to | 緩動 | 時序 | 斷點 |
|---|------|------|-----------|------|------|------|
| 1 | 產品 | 進場 | op0,y+30,scale.92 → 正常 | `power3.out` | 0.9s | all |
| 2 | 產品 | scroll | rotY 0→2π、scale .92→1 | `none`(scrub) | hero 全高 pin | ≥768 |
| 3 | 產品 | 游標 | rotY/rotX ±0.08（視差） | `power2.out` | follow, 0.4s | ≥1024 |
| 4 | 賣點卡×3 | scroll | op0,x−24 → 1,0 | `power2.out` | stagger 各 25% | all |
| 5 | 「不發燙」徽章 | hover | bloom +0.3、scale→1.04 | `power2.out` | 0.2s | ≥1024 |
| 6 | USB-C 埠 | scroll 到段3 | emissive 0.2→0.9 脈動 | `sine.inOut` | 1.2s loop | ≥768 |
| 7 | CTA | idle | scale 1→1.03→1 | `sine.inOut` | 2s loop | all |
| 8 | CTA | hover | bg shift、scale→1.05 | `power2.out` | 0.18s | pointer:fine |
| 9 | scroll 提示 | idle | y 0→8→0、op 漸隱 | `sine.inOut` | 1.5s loop，scroll 後消失 | all |

## 可貼程式碼（responsive + a11y 整合）

```js
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
gsap.registerPlugin(ScrollTrigger);

const mm = gsap.matchMedia();

// ── ≥768 且允許動態：3D scroll 敘事 ──
mm.add(
  { motion: '(prefers-reduced-motion: no-preference)', tablet: '(min-width: 768px)', desktop: '(min-width: 1024px)' },
  (ctx) => {
    const { motion, desktop } = ctx.conditions;
    if (!motion) return;

    // #2 產品旋轉 + pin
    gsap.to('#product', {
      rotateY: 360, ease: 'none', // 用 Three.js 時改寫 product.rotation.y
      scrollTrigger: { trigger: '#hero', start: 'top top', end: '+=120%', scrub: true, pin: true }
    });

    // #4 賣點卡 stagger
    gsap.utils.toArray('.sellpoint').forEach((el, i) => {
      gsap.from(el, {
        opacity: 0, x: -24, ease: 'power2.out', duration: 0.6,
        scrollTrigger: { trigger: '#hero', start: `${20 + i * 25}% top`, toggleActions: 'play none none reverse' }
      });
    });

    // #6 USB-C 脈動（段3）
    gsap.to('#port', {
      '--glow': 0.9, repeat: -1, yoyo: true, ease: 'sine.inOut', duration: 1.2,
      scrollTrigger: { trigger: '.sellpoint:nth-child(3)', start: 'top center' }
    });

    // #3 游標視差（僅 desktop + 細指標）
    if (desktop && matchMedia('(pointer:fine)').matches) {
      const hero = document.querySelector('#hero');
      hero.addEventListener('pointermove', (e) => {
        const nx = (e.clientX / innerWidth - 0.5);
        const ny = (e.clientY / innerHeight - 0.5);
        gsap.to('#product', { rotationY: `+=${nx * 4}`, rotationX: ny * 4, ease: 'power2.out', duration: 0.4, overwrite: 'auto' });
      });
    }
  }
);

// ── reduced-motion fallback：純淡入（#1 進場 + #4） ──
mm.add('(prefers-reduced-motion: reduce)', () => {
  gsap.from('#product, .sellpoint', { opacity: 0, duration: 0.5, stagger: 0.1 });
});
```

```css
/* USB-C 埠脈動用 CSS 變數驅動，方便 GSAP tween */
#port { --glow: 0.2; box-shadow: 0 0 calc(var(--glow) * 24px) rgba(110,231,255,var(--glow)); }
/* #7 CTA 微呼吸（純 CSS，reduced-motion 自動停） */
@media (prefers-reduced-motion: no-preference) {
  .cta { animation: breathe 2s ease-in-out infinite; }
  @keyframes breathe { 0%,100%{transform:scale(1)} 50%{transform:scale(1.03)} }
}
.cta { transition: transform .18s ease, background-color .18s ease; } /* #8 hover */
.cta:hover { transform: scale(1.05); }
```

## 效能 & a11y
- [x] reduced-motion 完整退場（matchMedia 分支 + CSS @media 雙保險）
- [x] 行動關 3D/bloom、`pointer:fine` 才掛游標視差（觸控不誤觸）
- [x] CTA 呼吸用純 CSS，reduced-motion 自動停
- [ ] 各斷點 FPS / LCP【需實測】；`pin` 區段建議測 CLS

> 來源製作包：`skills/3d-motion-designer/examples/charger-hero-interaction-package.md`。
