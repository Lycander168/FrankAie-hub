---
name: motion-spec-builder
description: >
  LYCANDER AI RESEARCH HUB — 網頁動態規格產生器（工具型 skill）。
  當使用者提到「動畫規格」、「scroll 動畫設定」、「GSAP / ScrollTrigger 設定」、「Three.js 場景參數」、
  「緩動曲線 easing」、「keyframe 時間軸」、「hero 動畫怎麼做」、「微互動怎麼寫」、
  「給我可貼的 3D / 動畫程式碼」時觸發。
  針對一個區塊，一次輸出 keyframe 時間軸 ＋ 緩動 ＋ 觸發點 ＋ GSAP/Three.js 可貼程式碼，並可用
  Three.js Viewer（show_threejs_scene）即時算繪預覽。
  和 `3d-motion-designer` 搭配 —— 設計師定方向，這個工具把規格與程式碼做到可直接落地。
---

# 網頁動態規格產生器（Motion Spec Builder）

這是一個**工具型 skill**。功能：把一個指定的區塊 / hero / 微互動，**爆出可直接交工程落地的動態規格 + 可貼程式碼**，並（可）即時算繪預覽。
和 `3d-motion-designer`（定方向 / 分鏡）、`visual-team`（版面）搭配 —— 角色定方向，這個工具把它變成跑得起來的設定。

> 原則：規格要能**直接貼上就動**，且自帶效能預算與 `prefers-reduced-motion` 退場；動畫不得犧牲效能與可及性。

---

## 何時用

- 已有動態方向 / 分鏡，要轉成工程可實作的規格與程式碼
- 要 scroll 驅動（ScrollTrigger）、hero 3D、或 hover / 游標微互動的具體設定
- 要在真機上先看一個 live 預覽確認節奏與效能

## 需要的輸入

1. **區塊目的**：這段要讓使用者感受到什麼、做什麼動作（scroll 到底 / 點 CTA）。
2. **素材**：產品圖 / 3D 模型 / 文案層級（主標→產品→賣點→CTA）。
3. **品牌節奏**：克制 / 俐落 / 流體…（決定緩動曲線）。
4. **目標裝置與效能預算**：桌機or行動、目標 FPS、首屏載入限制。
5. **實作偏好（可選）**：純 CSS / GSAP+ScrollTrigger / Three.js。

## 處理框架（四步）

1. **拆動態（四軸）**：把區塊拆成「進場 / scroll / 游標 / 離場」四種觸發，逐一定義 from→to。
2. **定緩動與時序**：每個動作選緩動曲線（如 `power2.out`、`expo.inOut`）與時長 / delay / stagger，對齊品牌節奏。
3. **選實作層級**：依效能預算選 純 CSS（最省）/ GSAP+ScrollTrigger（scroll 敘事）/ Three.js（真 3D）；給出對應可貼程式碼。
4. **效能 & a11y 守則**：列 draw call / 貼圖 / 懶載入建議，並一定附 `prefers-reduced-motion` 的等效靜態退場。

## Three.js Viewer / 即時算繪

- 需要 3D 預覽時，先 `learn_threejs` 取範式，再用 `show_threejs_scene` 算繪（全域：`THREE`、`OrbitControls`、`EffectComposer`、`RenderPass`、`UnrealBloomPass`、`canvas`、`width`、`height`，支援 `alpha`）。
- **⚠️ 退路**：環境無此 MCP 或呼叫未獲授權時，**退回輸出可直接貼上的程式碼 + 參數表**，不阻斷產出。安裝額外工具前先詢問使用者。

---

## 輸出範本

```
# 動態規格 | <區塊名>｜<裝置>｜<日期>

## 動態分鏡（四軸）
| 元素 | 觸發 | from → to | 緩動 easing | 時長/delay/stagger | 備註 |
|------|------|-----------|-------------|--------------------|------|
| 主標 | 進場 | y:40,op:0 → y:0,op:1 | power3.out | 0.6s | |
| 產品 | scroll | rotateY:0 → 6.28 | none(linear) | scrub | 綁 ScrollTrigger |
| CTA | 游標 | scale:1 → 1.04 | power2.out | 0.2s | hover |

## 實作層級建議
- 選用：CSS / GSAP+ScrollTrigger / Three.js（理由＋效能取捨）：

## 可貼程式碼
```js
// GSAP + ScrollTrigger 範例（節錄）
gsap.registerPlugin(ScrollTrigger);
gsap.to('#product', {
  scrollTrigger: { trigger: '#hero', start: 'top top', end: 'bottom top', scrub: true },
  rotationY: 360, ease: 'none'
});
```

## 3D 場景參數（如用 Three.js）
| 相機 fov/pos | 燈光 key/rim/ambient | 材質 metalness/roughness | bloom | draw call 上限 |
|--------------|----------------------|--------------------------|-------|----------------|

## Live 預覽
- show_threejs_scene 截圖 / 可調參數（無 MCP 時：上方程式碼自行貼跑）

## 效能 & a11y
- [ ] 目標 FPS / LCP / CLS 在預算內【需實測】
- [ ] prefers-reduced-motion：關閉位移動畫、給等效靜態
- [ ] 貼圖 / 模型懶載入、降載策略
```

---

## 實例演練（Worked Example）

**輸入**：65W GaN 充電器｜hero 區｜桌機為主｜品牌節奏「俐落克制」｜要 Apple 那種 scroll 旋轉展示。

**輸出（節錄）**：
| 元素 | 觸發 | from → to | 緩動 | 時序 |
|------|------|-----------|------|------|
| 充電器 3D | scroll | rotateY 0→360°、scale 0.9→1 | linear(scrub) | 綁定 hero 高度 |
| 賣點標註 | scroll | op 0→1，分 3 段顯現 | power2.out | stagger 0.15 |
| 「不發燙」徽章 | 游標 | bloom 微亮 | power2.out | hover 0.2s |

**3D 參數**：相機 fov 50 / z=5；key 光 (3,4,5) 強度 2.2、rim 粉光打輪廓；材質 metalness 0.9 / roughness 0.18；UnrealBloom strength 0.7、threshold 0.85；行動裝置關閉 bloom 降載。
**a11y**：`prefers-reduced-motion` 時改為靜態三張賣點圖、停用 scroll 旋轉。

## 與團隊串接

- **上游**：方向 / 分鏡由 `3d-motion-designer` 提供；版面由 `visual-team`；產品 3D 模型由 `mechanical-team`。
- **下游**：規格 + 程式碼交前端工程實作；可丟 `consumers-*` 對體驗打分；成效回 `marketing-team`。

> 提醒：規格要能直接落地且跑得順；動畫不得犧牲效能與可及性，所有實測數字標【需實測】。

---

## 範例（Worked Examples）

- [`examples/charger-hero-motion-spec.md`](examples/charger-hero-motion-spec.md) — 65W 充電器 Hero 全斷點規格（斷點矩陣 + 9 條微互動 + responsive/a11y 程式碼），接棒自 `3d-motion-designer` 的製作包。
