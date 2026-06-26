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
- `product-manager` — 資深產品經理。產品決策者：機會評估 → Go/No-Go → PRD + 功能優先級 + 路線圖。與 hub-router 分工（它排「召集誰」，PM 裁「做什麼產品」）。
- `data-analyst` — 資深資料 / 數據分析師。把流量/轉換/ROAS/留存/評論情緒等數據變成可決策洞察與監控指標盤。與 financial-analyst 分工（財務看錢，數據看行為成效）。
- `security-engineer` — 資深資安 / 裝置安全工程師。含 App/韌體/連網產品或 DTC 站的威脅建模、韌體/OTA 安全、資料隱私技術面（防禦性用途）。與 legal-ip 分工（它做法律合規條文，本角色做技術防護）。
- `channel-sales` — 資深通路 / B2B 業務。marketplace 帳號健康、經銷批發與 B2B 開發、通路價格體系與鋪貨。與 marketing-team 分工（行銷拉需求/流量，本角色鋪通路/談條件）。
- `supply-chain-expert` — 資深供應鏈 / 策略採購。供應商評鑑、多源備援、TCO 降本、斷鏈韌性。與 operations-team 分工（它做策略層選誰/佈局，operations 做執行層下單/跟料）。
- `growth-retention` — 資深成長 / 再購。留存、流失喚回、會員分層、LTV 提升。與 marketing-team（獲取）、cx-team（服務）分工，專攻既有客成長。
- `web-engineer` — 資深前端 / DTC 站工程。官網/落地頁、結帳優化、效能(Core Web Vitals)、追蹤埋點、A/B 基建。與 visual-team（設計稿）、data-analyst（分析）分工。
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
- `ig-carousel-factory` — IG 輪播工廠。一個賣點 → 一整組品牌一致的 IG 輪播（共享 BASE 風格 + 逐頁 prompt + caption + 發文時段）＋ 程式化批量生成樣板（一鍵換 BASE 切風格）。
- `copy-humanizer` — 文案去 AI 味潤稿器。把生硬文案改自然、貼品牌語氣，並附改動清單（不改事實）。
- `review-miner` — 評論痛點萃取器。雜亂評論 → 量化痛點 / 讚點 ＋ 產品改善方向與賣點機會。
- `pricing-calculator` — 定價試算器。成本＋通路費用 → 各售價毛利 / break-even ACOS / 情境比較與定價建議。
- `email-sequence-builder` — EDM 序列產生器。目標＋受眾階段 → 完整 email 自動化序列（時機 / 主旨 / 內文 / CTA）。
- `competitor-comparison` — 競品比較表生成器。自家 vs 競品 → 加權比較表＋差異化定位與主打方向。
- `seo-keyword-expander` — SEO 關鍵字擴展器。種子詞 → 分群分意圖的關鍵字地圖，供 Listing / SEO / 廣告使用。

## 基礎建設 skill（記憶 / 品質 / 驗證）

> 不產出內容，而是讓「長專案 / 多角色協作」具備持久記憶、品質把關與標準化驗證。

- `planning-with-files` — 檔案化規劃 / 持久記憶（Manus 風格）。把工作記憶寫進 `task_plan.md` / `findings.md` / `progress.md` 三個磁碟檔，讓任務在 `/clear`、context 壓縮或 session 中斷後仍能無縫接回；並提供多角色共享狀態（總機持有主計畫、各角色寫自己段落、進度集中記）。由 `hub-router` 在大專案開跑前先建檔。改寫自開源社群 `OthmanAdi/planning-with-files` 模式並在地化整合進 HUB 三階段 SOP。
- `quality-gate` — 產出品質閘門 / 對抗式審查。對每份產出（情報卡 / 驗證報告 / Spec / Listing / 文案 / 視覺 brief…）以「致命 / 重要 / 次要」三級審查，跑「完成前驗證」檢核表，通過才放行；含 HUB 專用審查維度（防臆造、可回溯、可量測、邏輯一致、風險揭露…）與「收到審查意見的回應法」。由 `hub-router` 在每階段交棒前與結案前插入。改寫自開源社群 superpowers 的 code-review / verification-before-completion 方法（`obra/superpowers`）並在地化。
- `validation-panel` — AI 消費者驗證關卡（**HUB 招牌**）。用統一「購買意願 1–5 rubric」調度 4 市場 `consumers-*` 對概念/定價/文案/視覺做低成本驗證，產出共識/異議/改善建議與跨市場對比；是 `hub-router` 動線中固定的「驗證閘」。產出為虛擬受眾模擬推估，非真實市場數據。

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

## 格式選用指南（Pattern A / B / C）

本 hub 依 skill 類型有三套內文格式，新增時請對號入座，保持一致：

| Pattern | 適用 | 內文骨架 | 範例 |
|---------|------|----------|------|
| **A 專家型** | 單一資深專家（深度諮詢） | Persona → 三階段 SOP → 輸出範本 → 協作介面 → 啟動方式 | `product-manager`、`security-engineer`、`channel-sales` |
| **B 工具型** | 執行具體產出的工具 | 何時用 → 需要的輸入 → 運作流程 → 輸出範本 → 實例演練 → 與團隊串接 | `listing-optimizer`、`pricing-calculator`、`ad-hook-writer` |
| **C 團隊型** | 5 人具名團隊 | 團隊總覽(表) → 成員檔案(深描) → 三階段 SOP → 指名調用 → 協作介面 | `electronics-team`、`visual-team`、`cx-team` |

> 基礎建設型（`planning-with-files`、`quality-gate`、`hub-router`）為特例：以「何時啟動 → 機制/守則 → 範本 → 協作 → 啟動」描述流程而非角色。

共同必備（所有 Pattern）：
1. frontmatter `description` 要有**明確觸發關鍵字**，並用 `⚠️` 標出與相近 skill 的分界（避免路由衝突）。
2. 至少一份**輸出範本**。
3. **防臆造守則**：無一手資料的主張一律標 `【需查證】`／`【需數據】`／`【假設】`。
4. 引用其他 skill 時，名稱必須是**真實存在**的 skill（CI 會檢查）。

## 版本

- v0.13.0 — 新增工具型 skill `ig-carousel-factory`（IG 輪播工廠）：把「程式化批量 IG 輪播生成」工作流（一個檔案＝一整組輪播企劃、共享 `BASE` 風格一鍵換皮、並行批量生圖＋自動 caption）在地化整合進 HUB；串接 `ad-hook-writer`（封面 hook）/`copy-humanizer`（caption 去 AI 味）/`visual-team`·`animation-designer`（風格分鏡）/`validation-panel`（虛擬受眾打分）/`marketing-team`（發文日曆）。ROSTER 工具型 8→9、路由表與「行銷中心」對照同步、skill 數 33→34。
- v0.12.0 — 衝刺品質分數（WS1–WS4）：① hub-router 加端到端 worked example ＋「第一次使用」指引；② CI `check_skills.py` 升級為**結構強制**（name=資料夾、description、輸出範本、防臆造守則）＋ 新增 `skills/_TEMPLATE/`（Pattern A/B/C 範本）；③ 補 3 垂直角色 `supply-chain-expert`/`growth-retention`/`web-engineer`；④ 招牌 `validation-panel`（統一 1–5 購買意願 rubric 的 AI 消費者驗證關卡）＋ 4 個 consumers-* 補「模擬非真實數據」聲明。skill 數 29 → 33。
- v0.11.0 — 品質治理（全 skill 審計後）：修復 10 處壞引用（已不存在的 ecommerce-operator / sourcing-expert，改指向 `channel-sales`／`seo-keyword-expander`／`operations-team`）；hub-router 新增「觸發衝突仲裁表」；plugin README 新增「格式選用指南(Pattern A/B/C)」；根 README 計數/目錄樹更新；新增 `scripts/check_skills.py` 與 `.github/workflows/check-skills.yml`（CI 自動檢查引用完整性、skill 計數與版本一致性）。
- v0.10.0 — 補強中優先角色缺口：新增 `security-engineer`（裝置/韌體/資料安全，防禦性技術面）與 `channel-sales`（marketplace 帳號健康/經銷批發/B2B/通路價格）；hub-router 動線於開發(安全需求)、上市/投放(通路鋪設)納入兩者；ROSTER 支援專家增至 8 位、新增資安中心與通路中心對照、總數更新為 29 個 skill。
- v0.9.0 — 補強角色缺口（以 agency-agents 16 部門盤點後）：新增支援專家 `product-manager`（產品決策/PRD/優先級）與 `data-analyst`（行為成效數據洞察/指標盤）；hub-router 動線於立項/開發/售後納入兩者；ROSTER 與「中心」對照同步更新（產品中心、數據中心落地）。
- v0.8.0 — 新增基礎建設 skill `quality-gate`（產出品質閘門 / 對抗式審查）：致命/重要/次要三級、HUB 專用審查維度、完成前驗證檢核表、收到審查意見的回應法；`hub-router` 每階段交棒前與結案前插入審查。改寫自 superpowers 的 code-review / verification 方法。
- v0.7.0 — 新增基礎建設 skill `planning-with-files`（Manus 風格檔案化規劃 / 持久記憶）：task_plan/findings/progress 三檔、完成閘門、多角色共享狀態；`hub-router` 動線加入「0. 建檔」前置步驟。
- v0.6.0 — 一致性與可發現性收尾：ROSTER 升級為完整索引（含「需求→召喚誰」路由表、「中心↔skill」對照、端到端實例）；統一寫死的版本 footer。
- v0.5.0 — 結構優化：新增 `hub-router`（總機路由）、`financial-analyst`、`legal-ip`；修正旗艦 vs 團隊的觸發詞重疊；8 個工具型 skill 各補 worked example。
- v0.4.0 — 再新增 4 個工具型 skill：pricing-calculator、email-sequence-builder、competitor-comparison、seo-keyword-expander（工具型共 8 個）。
- v0.3.0 — 新增 4 個原創工具型 skill：listing-optimizer、ad-hook-writer、copy-humanizer、review-miner，供團隊執行具體產出。
- v0.2.0 — 擴編為 100 位 AI 角色：新增 6 個專家團隊（30 人）＋ 4 個市場 AI 消費者小組（70 人）＋ ROSTER.md 編制表。
- v0.1.0 — 初版，收錄 electronics-engineer、animation-designer 兩個角色。
