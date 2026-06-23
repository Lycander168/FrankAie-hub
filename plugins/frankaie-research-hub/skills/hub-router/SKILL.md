---
name: hub-router
description: >
  LYCANDER AI RESEARCH HUB — 總機 / 專案路由（總經理室）。
  當使用者給的是「一個大需求 / 一個專案 / 一個產品從頭到尾」，或明確說「召集團隊」、「不知道該找誰」、
  「幫我規劃整個流程」、「這個案子怎麼跑」、「需要哪些人」、「組一個小組」時觸發。
  負責判斷該召集哪些團隊與工具、依什麼順序協作，並產出一份「專案作戰計畫」與分工表。
---

# 總機 / 專案路由（Hub Router · 總經理室）

這是整個 HUB 的**調度中樞**。當需求跨多個團隊、或使用者不確定該找誰時，由它先拆解需求、指派對的角色與工具、排出協作順序，再交棒下去。

> 原則：先分流再執行。一個好的調度，是讓對的人在對的階段做對的事，不重工、不漏接。

---

## 何時啟動

- 需求很大 / 跨領域（例：「我想開發並上架一顆 65W GaN 充電器」）
- 使用者說「召集團隊 / 不知道找誰 / 幫我規劃整個案子」
- 需要多個 skill 接力，但不確定順序

若需求很單一（只問效率、只要一個 hook），**不必經過路由**，直接觸發對應 skill 即可。

## HUB 角色與工具地圖

### 角色團隊（完整協作用）
| Skill | 何時召集 |
|-------|----------|
| `electronics-team` | 電源/快充/電池/韌體/RF/認證等完整電子開發（5 人分工） |
| `mechanical-team` | 外觀/機構/CMF/模具/散熱完整設計（5 人分工） |
| `visual-team` | 品牌視覺/KV/動態/包裝/UI 完整視覺產出（5 人分工） |
| `marketing-team` | 品牌/廣告/社群/文案/通路完整行銷（5 人分工） |
| `operations-team` | 採購/物流/報關/庫存量產營運（5 人分工） |
| `cx-team` | 客服/RMA/口碑/會員售後（5 人分工） |
| `consumers-taiwan/usa/japan/europe` | 對概念/定價/文案/視覺做市場虛擬焦點驗證 |

### 旗艦單一專家（快速單兵諮詢用）
| Skill | 何時找 |
|-------|--------|
| `electronics-engineer` | 只需一位資深電子工程師快速判斷 / 做單一完整開發包 |
| `animation-designer` | 只需一位資深視覺/動畫師快速出 brief / 分鏡 |
| `product-manager` | 該不該做 / 做哪版 / 砍哪些功能 / 寫 PRD / 需求優先級裁決 |
| `data-analyst` | 看轉換漏斗 / ROAS / A/B / 量化評論 / 找掉量原因 / 做指標盤 |
| `security-engineer` | 含 App/韌體/連網或 DTC 站的資安、韌體/OTA 安全、資料隱私技術面 |
| `channel-sales` | marketplace 帳號健康、經銷批發/B2B 開發、通路價格與鋪貨 |
| `supply-chain-expert` | 策略採購/供應商評鑑/多源備援/TCO 降本/斷鏈風險（策略層） |
| `growth-retention` | 再購/留存/流失喚回/會員分層/LTV 成長 |
| `web-engineer` | DTC 站/落地頁/結帳優化/效能/埋點/A-B 基建（技術實作） |
| `financial-analyst` | 成本/定價/毛利/現金流/投資評估 |
| `legal-ip` | 合約/專利迴避/商標/法規合規風險 |

### 工具型 skill（執行具體產出）
| Skill | 產出 |
|-------|------|
| `listing-optimizer` | 轉換導向 Listing |
| `ad-hook-writer` | 廣告 hook + 開場分鏡 |
| `copy-humanizer` | 去 AI 味文案 |
| `review-miner` | 評論痛點/賣點萃取 |
| `pricing-calculator` | 定價/毛利/break-even |
| `email-sequence-builder` | EDM 自動化序列 |
| `competitor-comparison` | 競品比較與差異化 |
| `seo-keyword-expander` | 關鍵字地圖 |

### 基礎建設 skill（記憶 / 流程 / 品質）
| Skill | 用途 |
|-------|------|
| `planning-with-files` | 長專案/多角色的持久記憶：把作戰計畫落地成 `task_plan.md` / `findings.md` / `progress.md`，防 context 流失、支援多角色共享狀態與恢復 |
| `quality-gate` | 產出品質閘門：每階段產出 / 交棒 / 結案前做對抗式審查（致命/重要/次要三級）＋ 完成前驗證，通過才放行 |
| `validation-panel` | AI 消費者驗證關卡（招牌）：用統一 1–5 購買意願 rubric 調度 4 市場 consumers-* 做概念/定價/文案/視覺驗證，產出共識/異議/跨市場對比 |

## 觸發衝突仲裁表（同一需求可能誤觸多個 skill 時）

> 多個 skill 的觸發詞會重疊。遇到下列關鍵字，依「先後 precedence」分流，避免搶答或漏接。

| 重疊關鍵字 | 可能誤觸 | 仲裁規則（precedence）|
|------------|----------|------------------------|
| 定價 / pricing / 毛利 | pricing-calculator / financial-analyst / channel-sales / marketing-team | 先 `pricing-calculator`（算 unit economics）→ 要策略/現金流找 `financial-analyst` → 各通路 MAP/價差找 `channel-sales` → 促銷機制找 `marketing-team` |
| 數據 / 分析 | data-analyst / review-miner / consumers-* | 行為/成效/漏斗/ROAS → `data-analyst`；評論文字 → `review-miner`；購買意願打分 → `consumers-*` |
| 視覺 / 設計 | animation-designer / visual-team | 快速單支 brief/分鏡 → `animation-designer`；完整多人視覺專案（KV/動態/包裝/UI）→ `visual-team` |
| 安全 / security | quality-gate / security-engineer / electronics-team / legal-ip | 產出審查 → `quality-gate`；韌體/連網/資料資安 → `security-engineer`；電氣安規 → `electronics-team`；法規合規條文 → `legal-ip` |
| 新品上市 / GTM | hub-router / product-manager / marketing-team | 整體拆解排程 → `hub-router`；做什麼產品/PRD → `product-manager`；上市執行 → `marketing-team` |
| 電子 / 硬體 | electronics-engineer / electronics-team | 一位專家快速判斷 → `electronics-engineer`；5 人分工完整開發 → `electronics-team` |

> 通則：**單兵快速** vs **團隊完整** → 看規模；**算/查/審** vs **決策/執行** → 看動作性質。仍不確定就由本路由直接指派。

## 標準調度動線（新品從 0 到上市）

> 大專案開跑前，先用 `planning-with-files` 把作戰計畫落地成 `task_plan.md`，
> 之後每階段把產出寫進 `findings.md`、進度寫進 `progress.md`，確保中斷也能無縫接回。

```
0. 建檔     → planning-with-files（建立 task_plan/findings/progress，把計畫變可勾選、可恢復）
1. 立項     → product-manager（裁決做什麼/做哪版）＋ financial-analyst（算帳）＋ validation-panel（需求驗證）＋ competitor-comparison
2. 開發     → product-manager 出 PRD → electronics-team ＋ mechanical-team（並行）→ legal-ip（專利迴避）
              ＋ security-engineer（若含 App/韌體/連網：安全需求寫進 PRD）
3. 認證量產 → electronics-team(認證) ＋ supply-chain-expert（策略採購/備援）→ operations-team（下單/量產）
4. 上市素材 → visual-team ＋ marketing-team ＋ 工具（hook/listing/seo/humanizer）
              ＋ channel-sales（選通路/鋪貨/帳號健康/B2B）＋ web-engineer（自架站/落地頁/埋點）
5. 上市前驗證→ validation-panel（素材/定價打分 + 跨市場對比）
6. 上架投放 → marketing-team ＋ channel-sales（通路鋪設）＋ operations-team（出貨）
7. 售後迭代 → cx-team ＋ review-miner ＋ data-analyst（量化成效/找問題）＋ growth-retention（再購/LTV）→（回饋 1.）

※ 驗證閘：1 與 5 一律走 validation-panel（統一 1–5 rubric）；它再去調度對應市場的 consumers-*。
※ 每階段「產出後 / 交棒前」插入 quality-gate 審查；結案前做最後總驗收，通過才標 done。
※ data-analyst 可在 1（需求量化）、4–6（投放/轉換成效）、7（掉量根因）隨時被召來提供數據洞察。
※ security-engineer 僅在產品含 App/韌體/連網或有自架 DTC 站時納入；純被動配件可略。
```

## 端到端 worked example（一顆 65W GaN 充電器跑完全程）

| # | 召喚 | 做什麼 | 產出 |
|---|------|--------|------|
| 0 | `planning-with-files` | 建 task_plan/findings/progress | 可恢復的作戰計畫 |
| 1 | `product-manager`＋`financial-analyst`＋`validation-panel`＋`competitor-comparison` | 裁決做不做、算帳、測需求、比競品 | Go 決策 + 差異化方向（主打「不發燙」）|
| 2 | `electronics-team`∥`mechanical-team`→`legal-ip`（＋`security-engineer` 視連網） | 開發電子/機構、查專利 | Spec＋BOM＋外殼＋FTO |
| 3 | `electronics-team`(認證)＋`supply-chain-expert`→`operations-team` | 認證、策略採購/備援、量產 | 認證包＋採購策略＋量產方案 |
| 4 | `seo-keyword-expander`→`listing-optimizer`＋`ad-hook-writer`＋`visual-team`＋`web-engineer` | 關鍵字→素材→落地頁 | 上架投放素材包＋DTC 落地頁 |
| 5 | `validation-panel`＋`copy-humanizer` | 素材/定價跨市場打分、文案去 AI 味 | 上市前驗證報告 |
| 6 | `marketing-team`＋`channel-sales`＋`operations-team` | 投放＋鋪通路＋出貨 | 上市 |
| 7 | `cx-team`＋`review-miner`＋`data-analyst`＋`growth-retention` | 服務、評論回饋、量化成效、做再購 | 迭代輸入＋LTV 成長 →（回饋 1.）|

> 每一步交棒前由 `quality-gate` 審查，狀態寫回 `planning-with-files`。

## 第一次使用（給新用戶）

1. 給一個大需求（例：「我想開發並上架一顆 65W GaN 充電器」）→ 本路由先產《專案作戰計畫》。
2. 不確定該找誰？直接呼叫 `hub-router`；只要單點產出？直接點對應 skill（看上方表）。
3. 要驗證「會不會被買」？呼叫 `validation-panel`。要把產出把關？呼叫 `quality-gate`。

---

## 輸出範本：專案作戰計畫

```
# 專案作戰計畫 | <需求>｜<日期>

## 需求拆解
- 目標 / 範圍 / 已知限制：

## 召集名單（誰、做什麼、為什麼）
| 階段 | 召集角色/工具 | 任務 | 產出 | 依賴前置 |
|------|----------------|------|------|----------|
| 1 | | | | |

## 協作順序（含並行）
<簡單流程圖或編號步驟>

## 第一步建議
- 現在馬上該啟動的 1–2 個角色/工具：
- 需要使用者先補的資訊：
```

---

## 啟動方式

收到大需求後，預設先產出「專案作戰計畫」，列出召集名單與順序，再詢問是否從第一步開始。
使用者可隨時插隊指定（例：「先跳到定價」），路由會直接交棒給對應 skill。

> 提醒：路由只負責「分流與排序」，不替專業角色下技術結論；實際內容由被召集的團隊/工具產出，並沿用各自的防臆造守則。
