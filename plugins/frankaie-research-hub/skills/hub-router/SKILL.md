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
| `animation-designer` | 只需一位資深視覺/動畫師快速出 brief / 影片分鏡 |
| `3d-motion-designer` | 要 Apple/Native Union 級網頁 3D / scroll 動態 / 微互動（可即時算繪）|
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
| `motion-spec-builder` | 網頁動態規格 + GSAP/Three.js 可貼程式碼 + 即時算繪 |

## 標準調度動線（新品從 0 到上市）

```
1. 立項     → financial-analyst（算帳）＋ consumers-*（需求驗證）＋ competitor-comparison
2. 開發     → electronics-team ＋ mechanical-team（並行）→ legal-ip（專利迴避）
3. 認證量產 → electronics-team(認證) ＋ operations-team（採購/量產）
4. 上市素材 → visual-team ＋ marketing-team ＋ 工具（hook/listing/seo/humanizer）
              └ 官網/landing 互動：3d-motion-designer → motion-spec-builder（網頁 3D/scroll 動態）
5. 上市前驗證→ consumers-*（素材/定價打分）
6. 上架投放 → marketing-team ＋ operations-team（出貨）
7. 售後迭代 → cx-team ＋ review-miner →（回饋 1.）
```

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
