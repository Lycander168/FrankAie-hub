# 小露娜 LUNA — 捲動式電影感產品揭示頁

LYCANDER 官網（[www.lycander.tw](https://www.lycander.tw)，架於 SHOPLINE）的特效原型。
重製參考影片的 **scrollytelling 產品揭示**：散落元素 → 匯聚組裝 → 啟動發光 → 規格 → 品牌字卡 / CTA，
以 **小露娜 LUNA Mag Qi22 二代 25W 3-in-1 攜帶型無線充電器** 為範例。

全部使用**免費開源**工具，無需付費授權：

| 用途 | 工具 | 授權 |
|------|------|------|
| 開發 / 打包 | Vite | MIT |
| 平滑捲動 | Lenis | MIT |
| 捲動時間軸 / 文字淡入 | GSAP + ScrollTrigger | 免費（2025 起全功能免費）|
| 3D / 模型載入 | Three.js（GLTFLoader / DRACOLoader）| MIT |
| 光暈 | Three.js UnrealBloomPass | MIT |
| STEP→glb 轉檔 | cascadio（OpenCASCADE）| LGPL |

---

## 快速開始

```bash
cd web/luna-showcase
npm install
npm run dev      # http://localhost:5180
npm run build    # 產出 dist/
npm run preview  # 預覽 build 結果
```

> 需 Node 18+。`npm install` 會自行安裝上述全部免費套件。

---

## 結構（三層解耦，方便整合官網）

```
src/
├─ main.js              進入點：Lenis + GSAP + 場景 + 資料
├─ scene/               ← 動畫引擎（與內容無關，可重用）
│  ├─ scene.js          Three.js 場景、相機、燈光、Bloom、進度→特效映射
│  ├─ model.js          載入 luna.glb；exploded view 組裝/發光控制
│  └─ particles.js      星塵/能量粒子（散落↔收束、上升）
├─ scroll/timeline.js   ScrollTrigger 文字淡入 + 回報整頁進度
├─ content/copy.js      ← 文案（改字只動這裡）
├─ data/
│  ├─ shopline.js       ← 資料層（mock ↔ SHOPLINE 一行切換）
│  └─ luna.mock.json    mock 商品資料
└─ styles/style.css     深色電影感版型、響應式、reduced-motion
public/models/luna.glb  小露娜 3D 模型（由 STEP 轉檔）
```

**動線（捲動章節）**：Hero → 散落（痛點）→ 匯聚（工藝）→ 發光（體驗）→ 規格（信任）→ 品牌字卡 + 購買（轉換）。

---

## 串接 SHOPLINE（先 mock，後 live）

資料層 `src/data/shopline.js` 對外只暴露 `getProduct(handle)`，回傳正規化商品物件。
**現在**讀 `luna.mock.json`；填入憑證即自動切換到 **SHOPLINE Storefront GraphQL API**（read-only），UI / 動畫完全不動。

```bash
cp .env.example .env.local
# 填入：
#   VITE_SHOPLINE_DOMAIN=your-store.myshopline.com
#   VITE_SHOPLINE_TOKEN=<Storefront Access Token>   # guest 讀商品只需這個
```

- SHOPLINE Storefront API 為 **GraphQL**；query 已寫在 `shopline.js`（`productByHandle` 取標題/價格/變體/庫存/圖）。
- 商品 handle 設於 `src/content/copy.js` 的 `productHandle`，目前為：
  `lycander-luna-mag-qi22二代25w認證-3-in1攜帶型無線充電器`
- CTA「加入購物車」現導向官網商品頁；live 後可改接 cart API。

---

## 3D 模型：STEP → glb 轉檔

原始檔為 SolidWorks STEP（AP214，含手機/手錶示意件）。已轉成 `public/models/luna.glb`（46 個可獨立炸開的零件，用於 exploded-view 組裝動畫）。STEP 沒有材質，材質在 `model.js` 載入時套上品牌化深色金屬。

重新轉檔（若日後更新 CAD）：

```bash
pip install cascadio trimesh
python -c "import cascadio; cascadio.step_to_glb('WP302.STEP','public/models/luna.glb',0.1,0.5)"
# 第3/4參數為線性/角度容差，調小=更精細但檔案更大
```

> 原始 STEP 不入庫（見 `.gitignore`），由設計端保管；執行只需 glb。

---

## 整合進 SHOPLINE 官網

產出為可移植的 HTML/CSS/JS。整合路徑：
1. `npm run build` → `dist/`。
2. 把場景引擎（`scene/`）+ 容器 DOM 包成 SHOPLINE 自訂頁 section / theme 區塊。
3. 資料層直接走站內 Storefront API（同網域，免 CORS）。
4. 文案 / 商品由 `copy.js` + SHOPLINE 後台維護。

---

## 待辦 / 可調項（視覺驗收後微調）

- [ ] 在**真實瀏覽器**做視覺驗收：逐章節比對參考影片節奏（本開發環境無 GPU/瀏覽器，無法截圖驗證）。
- [ ] 確認模型初始朝向（CAD Z-up）；如需「站正」，於 `model.js` `_ingest` 加一行 `wrap.rotation.x = -Math.PI/2`。
- [ ] 提供 SHOPLINE Storefront token → 切 live，核對真實價格/庫存。
- [ ] 視需要 draco 壓縮 glb 進一步減重（目前 2.6 MB）。

## 無障礙 / 效能

- `prefers-reduced-motion`：關閉 Lenis、Bloom，粒子減量，僅保留淡入。
- pixelRatio 上限 2、模型 lazy-load、rAF 與 Lenis/GSAP 同一時脈。
- 行動優先（來源為直式手機錄影）；桌機自動加寬版型與運鏡距離。
