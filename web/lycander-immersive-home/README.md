# LYCANDER 沈浸式滾動品牌首頁(Shopline 可上架版)

一頁式沈浸式滾動網頁,為 www.lycander.tw 官網優化製作。
**單一檔案 `index.html`,零外部依賴**(不載入任何 CDN / 外部字型 / 外部圖片),
可直接貼入 Shopline 後台的自訂頁面 HTML 編輯器。

## 頁面內容(6 個滾動場景)

| # | 場景 | 沈浸式手法 |
|---|------|-----------|
| 0 | Hero 品牌開場(LYCANDER wordmark + 雙語標語) | 滿版開場 + 背景網格視差(支援的瀏覽器) |
| 1 | 品牌故事三段敘事 | 桌機左欄視覺釘住(sticky)、右欄文字捲過 |
| 2 | 精選產品 ×4(Contrastin / OLIKA W3 / HALFTER / iSlim) | **翻卡堆疊**:往下捲動新卡覆蓋前卡 |
| 3 | 周邊配件(GaN 充電器 / HDMI 8K / Mini PC 座) | 手機橫向滑動卡帶(scroll-snap),桌機三欄 |
| 4 | 永續與品牌價值三柱 | 進場浮現動畫 |
| 5 | CTA 導購 + 聯絡資訊 | 深色收尾面板 |

## 上架步驟(Shopline 後台)

1. 進入 **Shopline 後台 → 網店設計(或「頁面管理」)→ 新增自訂頁面**。
2. 編輯器切換到 **HTML 原始碼模式**(`<>` 圖示)。
3. 打開 `index.html`,**全選複製、整份貼上**(含最上方註解、`<style>`、內容、`<script>`)。
4. 先以**隱藏/未發布狀態**儲存並預覽,確認顯示正常後再發布。
5. 若貴店主題頁首高度不是 64px,調整 CSS 開頭的 `--lyc-header-h`(見下方客製化)。

> **若編輯器移除了 `<script>` 也沒關係**:頁面設計為優雅降級,
> 所有內容照常完整顯示、翻卡沈浸效果照常運作,只會少了「進場浮現」小動畫。

## 換圖清單(搜尋 `[換圖]` 註解)

程式碼內所有圖片目前為內嵌 SVG 佔位圖(標明用途與建議尺寸)。
請在 Shopline 後台「檔案管理/媒體庫」上傳實際產品圖後,複製圖片網址,替換對應 `<img>` 的 `src`:

| 位置 | 佔位標籤 | 建議尺寸(比例) |
|------|---------|----------------|
| 品牌故事 | 品牌形象照 | 1000×1250(4:5 直式) |
| 產品卡 1 | CONTRASTIN 產品圖 | 1200×900(4:3) |
| 產品卡 2 | OLIKA W3 產品圖 | 1200×900(4:3) |
| 產品卡 3 | HALFTER 產品圖 | 1200×900(4:3) |
| 產品卡 4 | iSlim 產品圖 | 1200×900(4:3) |
| 配件帶 1 | GaN 充電器圖 | 800×600(4:3) |
| 配件帶 2 | HDMI 8K 線材圖 | 800×600(4:3) |
| 配件帶 3 | Mini PC 擴充座圖 | 800×600(4:3) |

替換時保留 `alt` 與 `width`/`height` 屬性(維持無障礙與版面穩定),例如:

```html
<img src="https://cdn.shoplineapp.com/......jpg"
     alt="Contrastin 筆電支架包" width="1200" height="900"
     loading="lazy" decoding="async">
```

## 換連結清單(搜尋 `[換連結]` 註解)

| 位置 | 目前連結 | 建議替換為 |
|------|---------|-----------|
| Contrastin 卡片 | `https://www.lycander.tw/contrastin` | 實際商品頁 |
| OLIKA W3 卡片 | `https://www.lycander.tw/shop` | 實際商品頁 |
| HALFTER 卡片 | `https://www.lycander.tw/store/products/k1` | 實際商品頁 |
| iSlim 卡片 | `https://www.lycander.tw/shop` | 實際商品頁 |
| CTA 主按鈕 | `https://www.lycander.tw/shop` | 商店/分類頁 |

## 客製化(CSS 開頭的 brand tokens)

所有品牌參數集中在 `.lyc-page { ... }` 的 CSS 變數,改一處全頁生效:

| 變數 | 預設值 | 用途 |
|------|--------|------|
| `--lyc-header-h` | `64px` | **貴店主題頁首高度**;若頁首較高(如 80px)請改此值,sticky 場景與 hero 高度都會自動修正 |
| `--lyc-bg` / `--lyc-surface` | `#fafafa` / `#fff` | 頁面底色 / 卡片底色 |
| `--lyc-ink` / `--lyc-ink-soft` | `#1a1a1a` / `#595959` | 主文字 / 次要文字 |
| `--lyc-dark` | `#1d1d1f` | CTA 深色收尾區底色 |
| `--lyc-max-w` | `1200px` | 內容最大寬度 |
| `--lyc-radius` | `20px` | 卡片圓角 |

文案直接在 HTML 內修改即可(繁中為主、英文點綴的結構已排好)。

## 瀏覽器支援

| 體驗層 | 技術 | 支援範圍 |
|--------|------|---------|
| 基底(完整內容 + 翻卡堆疊 + 橫向滑動) | `position: sticky`、scroll-snap | 所有現代瀏覽器(含 iOS Safari、Firefox) |
| 進場浮現動畫 | IntersectionObserver(內嵌 ~25 行 JS) | 所有現代瀏覽器;被移除時自動全顯示 |
| 視差 / 卡片縮放加強 | CSS scroll-driven animations(`@supports` 包裹) | Chrome / Edge 115+;其他瀏覽器自動忽略 |
| 減少動態 | `prefers-reduced-motion` | 系統開啟時關閉全部動畫 |

## 疑難排解

- **翻卡效果沒有出現(卡片不會釘住)**:代表主題把貼上的內容包進了設有
  `overflow: hidden / auto` 的容器(這會停用 `position: sticky`)。
  請確認自訂頁面容器沒有這類設定,或聯絡 Shopline 客服詢問該頁面版型;
  即使 sticky 失效,頁面仍會以一般滾動完整顯示,不會破版。
- **Hero 開場高度不對(太高或被頁首蓋住)**:調整 `--lyc-header-h` 為貴店
  主題實際頁首高度。
- **手機橫向或矮螢幕沒有翻卡效果**:這是刻意設計——視窗高度不足 700px 時
  改為一般滾動,避免卡片內容被蓋住無法閱讀。

## 驗證紀錄(2026-07)

- Playwright + Chromium 實測 8 種情境:直開/模擬 Shopline 殼(60px sticky 頁首+全域主題樣式干擾)× 手機 390×844 / 桌機 1440×900 × JS 停用 × 減少動態 —— 全數通過:無 console 錯誤、無水平溢出、no-JS 內容完整、reduced-motion 正常。另補測 320×568 / 375×667 極窄與短視窗:無溢出、卡片正確降級。
- 4 向工程交叉審查(Shopline 相容性 / RWD 正確性 / 無障礙 / 效能體積)發現並已修正:
  - CTA 按鈕文字被內部 reset 蓋色(特異度)→ 元件 selector 加 `.lyc-page` 前綴
  - 小字對比不足(WCAG AA):產品型號、故事編號 → `#767676`,hero 英文標語 → `#6e6e6e`
  - 四個「了解更多」連結文字相同 → 各加 `aria-label` 區分
  - 品牌故事區缺自己的 `<h2>` → 補上標題
  - hero 字級/字距在 ≤320px 可能溢出 → 調降 `clamp()` 下限
  - 短視窗(<700px 高)sticky 卡片底部內容會被蓋住 → 降級為一般滾動
  - 8 張圖片加 `loading="lazy" decoding="async"`
  - heading/段落 margin 防主題覆寫、`:focus-visible` 焦點框、英文標語 `lang="en"`
