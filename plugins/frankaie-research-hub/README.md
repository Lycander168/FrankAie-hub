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

### 旗艦單一專家（深度 SOP）
- `electronics-engineer` — 資深電子工程師（Anker 級）。產品想法 → 市場情報卡 → 功能驗證報告 → 產品開發包（Spec + BOM + 里程碑）。
- `animation-designer` — 資深動畫 / 視覺設計師（Native Union 級）。視覺需求 → 視覺情報卡 → 轉化率驗證報告 → 創意製作包（Brief + 分鏡 + 規格 + prompt）。

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

- v0.3.0 — 新增 4 個原創工具型 skill：listing-optimizer、ad-hook-writer、copy-humanizer、review-miner，供團隊執行具體產出。
- v0.2.0 — 擴編為 100 位 AI 角色：新增 6 個專家團隊（30 人）＋ 4 個市場 AI 消費者小組（70 人）＋ ROSTER.md 編制表。
- v0.1.0 — 初版，收錄 electronics-engineer、animation-designer 兩個角色。
