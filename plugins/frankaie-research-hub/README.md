# frankaie-research-hub

LYCANDER AI RESEARCH HUB 的核心 plugin —— 收錄各領域**資深專家 AI 角色**。
設計理念：讓每個 AI 角色像一位真正的資深從業者，依固定 SOP 把工作做完、做扎實。

## 設計原則（所有角色共用）

1. **Persona 先行** — 明確的資歷、專長、思考風格與邊界（不臆造、缺資料要標註）。
2. **三階段 SOP** — 一律是「搜集市場資訊 → 驗證 → 開發 / 設計」三段，逐階段推進、逐階段確認。
3. **每階段有產出範本** — 用表格化範本確保輸出可被檢驗、可被交接。
4. **可被驗證** — 任何主張要能回溯來源或測試 / 指標；沒依據的不算數。
5. **與 LYCANDER 中心串接** — 上游取數據、下游交營運 / 行銷 / 財務 / 視覺中心。

## 現有角色

- `electronics-engineer` — 資深電子工程師（Anker 級）。產品想法 → 市場情報卡 → 功能驗證報告 → 產品開發包（Spec + BOM + 里程碑）。
- `animation-designer` — 資深動畫 / 視覺設計師（Native Union 級）。視覺需求 → 視覺情報卡 → 轉化率驗證報告 → 創意製作包（Brief + 分鏡 + 規格 + prompt）。

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

- v0.1.0 — 初版，收錄 electronics-engineer、animation-designer 兩個角色。
