# frankaie-research-hub

LYCANDER AI RESEARCH HUB 的核心 plugin —— 收錄各領域**資深專家 AI 角色**。
設計理念：讓每個 AI 角色像一位真正的資深從業者，依固定 SOP 把工作做完、做扎實。

## 設計原則（所有角色共用）

1. **Persona 先行** — 明確的資歷、專長、思考風格與邊界（不臆造、缺資料要標註）。
2. **三階段 SOP** — 一律是「搜集市場資訊 → 驗證 → 開發 / 設計」三段，逐階段推進、逐階段確認。
3. **每階段有產出範本** — 用表格化範本確保輸出可被檢驗、可被交接。
4. **可被驗證** — 任何主張要能回溯來源或測試 / 指標；沒依據的不算數。
5. **與 LYCANDER 中心串接** — 上游取數據、下游交營運 / 行銷 / 財務 / 視覺中心。

## 編制總覽：100 位 AI 角色

完整名冊見 [`ROSTER.md`](./ROSTER.md)。架構為 **30 位專家（6 團隊）＋ 70 位 AI 消費者（4 市場）**。

### 總機 / 路由（總經理室）
- `hub-router` — 大需求 / 跨團隊專案的調度中樞。拆解需求 → 判斷該召集哪些團隊與工具 → 排協作順序，產出「專案作戰計畫」。不確定該找誰時先找它。

### 旗艦單一專家（快速單兵諮詢 · 深度 SOP）
> 與「專家團隊」的區別：旗艦＝一位專家快速判斷/單兵完整產出；團隊＝召集 5 位具名成員分工協作完整專案。觸發情境已在各 skill description 明確區隔，避免路由衝突。
- `electronics-engineer` — 資深電子工程師（Anker 級）。單兵完整開發包（Spec + BOM + 里程碑）。
- `animation-designer` — 資深動畫 / 視覺設計師（Native Union 級）。單兵創意包（Brief + 分鏡 + prompt）。
- `financial-analyst` — 資深產品財務分析師（CFO 視角）。成本/毛利/現金流/回本/投資評估，與 pricing-calculator 搭配。
- `legal-ip` — 資深法務 / 智財顧問。專利迴避 FTO、合約紅線、商標、廣告與隱私合規（提示風險，非正式法律意見）。

### 專家團隊（每個 skill = 5 位具名專家）
- `electronics-team` — 電子工程團隊（電源/快充、電池安全、韌體、RF/無線、測試認證）
- `mechanical-team` — 機構設計團隊（機構、ID、CMF、模具/DFM、散熱可靠度）
- `visual-team` — 視覺設計團隊（總監、Motion、KV、包裝、UI/網頁）
- `marketing-team` — 行銷企劃團隊（CMO、廣告投手、社群/KOL、文案、通路）
- `operations-team` — 營運執行團隊（營運主管、採購、物流、報關、補貨）
- `cx-team` — 售後客服團隊（CX 主管、線上客服、RMA、口碑、會員）

### AI 消費者測試小組（每個 skill = 一個市場的虛擬受眾）
- `consumers-taiwan`（22 人）/ `consumers-usa`（18 人）/ `consumers-japan`（15 人）/ `consumers-europe`（15 人）
- 用途：對產品概念、定價、文案、視覺召集虛擬焦點小組，產出購買意願評分（1–5）與改善建議。

## 工具型 skill（不是角色，是給團隊用的執行工具）

> 角色團隊負責「決策與流程」，工具型 skill 負責「把具體產出做出來」，兩者互補。

- `listing-optimizer` — Listing 轉換優化器。產品資訊＋關鍵字 → 轉換導向的標題 / 五點 / A+ / 後台關鍵字。
- `ad-hook-writer` — 廣告 Hook 生成器。一個賣點 → 8 種框架的前三秒 hook ＋ 短影音開場分鏡。
- `copy-humanizer` — 文案去 AI 味潤稿器。把生硬文案改自然、貼品牌語氣，並附改動清單（不改事實）。
- `review-miner` — 評論痛點萃取器。雜亂評論 → 量化痛點 / 讚點 ＋ 產品改善方向與賣點機會。
- `pricing-calculator` — 定價試算器。成本＋通路費用 → 各售價毛利 / break-even ACOS / 情境比較與定價建議。
- `email-sequence-builder` — EDM 序列產生器。目標＋受眾階段 → 完整 email 自動化序列（時機 / 主旨 / 內文 / CTA）。
- `competitor-comparison` — 競品比較表生成器。自家 vs 競品 → 加權比較表＋差異化定位與主打方向。
- `seo-keyword-expander` — SEO 關鍵字擴展器。種子詞 → 分群分意圖的關鍵字地圖，供 Listing / SEO / 廣告使用。

## 基礎建設 skill（記憶 / 流程）

> 不產出內容，而是讓「長專案 / 多角色協作」具備持久記憶與可恢復性。

- `planning-with-files` — 檔案化規劃 / 持久記憶（Manus 風格）。把工作記憶寫進 `task_plan.md` / `findings.md` / `progress.md` 三個磁碟檔，讓任務在 `/clear`、context 壓縮或 session 中斷後仍能無縫接回；並提供多角色共享狀態（總機持有主計畫、各角色寫自己段落、進度集中記）。由 `hub-router` 在大專案開跑前先建檔。改寫自開源社群 `OthmanAdi/planning-with-files` 模式並在地化整合進 HUB 三階段 SOP。

## 新增角色範本（SKILL.md frontmatter）

```yaml
---
name: <skill-id>            # 英文小寫、用連字號，例：supply-chain-expert
description: >
  LYCANDER AI RESEARCH HUB — <角色名稱>。當使用者提到「<關鍵字1>」、「<關鍵字2>」…時觸發。
  以「搜集市場資訊 → 驗證 → 開發/設計」三階段 SOP 協助 <領域>。
---
```

內文建議區塊順序：`Persona / 角色設定` → `三階段 SOP` → `輸出範本` → `與 LYCANDER GROUP 的協作介面` → `啟動方式`。

## 版本

- v0.7.0 — 新增基礎建設 skill `planning-with-files`（Manus 風格檔案化規劃 / 持久記憶）：task_plan/findings/progress 三檔、完成閘門、多角色共享狀態；`hub-router` 動線加入「0. 建檔」前置步驟。
- v0.6.0 — 一致性與可發現性收尾：ROSTER 升級為完整索引（含「需求→召喚誰」路由表、「中心↔skill」對照、端到端實例）；統一寫死的版本 footer。
- v0.5.0 — 結構優化：新增 `hub-router`（總機路由）、`financial-analyst`、`legal-ip`；修正旗艦 vs 團隊的觸發詞重疊；8 個工具型 skill 各補 worked example。
- v0.4.0 — 再新增 4 個工具型 skill：pricing-calculator、email-sequence-builder、competitor-comparison、seo-keyword-expander（工具型共 8 個）。
- v0.3.0 — 新增 4 個原創工具型 skill：listing-optimizer、ad-hook-writer、copy-humanizer、review-miner，供團隊執行具體產出。
- v0.2.0 — 擴編為 100 位 AI 角色：新增 6 個專家團隊（30 人）＋ 4 個市場 AI 消費者小組（70 人）＋ ROSTER.md 編制表。
- v0.1.0 — 初版，收錄 electronics-engineer、animation-designer 兩個角色。
