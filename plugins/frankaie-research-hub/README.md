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

> 角色覆蓋「一個產品想法 → 開發 → 認證 → 採購量產 → 上架投放」的完整價值鏈。

**開發端**
- `electronics-engineer` — 資深電子工程師（Anker 級）。產品想法 → 市場情報卡 → 功能驗證報告 → 產品開發包（Spec + BOM + 里程碑）。
- `structural-id-designer` — 資深結構 / 工業設計師（Anker / Native Union 級）。把板子包進好看好握好生產的外殼。產品想法 → 設計情報卡 → 機構驗證報告 → 結構設計包（ID Spec + ME Spec + CMF + DFM + 里程碑）。
- `certification-expert` — 資深認證 / 法規合規專家。確保產品合法能賣、賣得安全。產品 + 市場 → 認證地圖卡 → 合規驗證報告 → 合規執行包（Master Cert List + 送測文件 + 標示規範 + 排程）。

**中游（BOM → 量產）**
- `sourcing-expert` — 資深供應鏈 / 採購專家。接 BOM → 供應鏈情報卡 → 供應商與成本驗證報告 → 採購量產方案包（採購版 BOM + 議價 + QC + 風控 + 里程碑）。

**上市 / 變現端**
- `animation-designer` — 資深動畫 / 視覺設計師（Native Union 級）。視覺需求 → 視覺情報卡 → 轉化率驗證報告 → 創意製作包（Brief + 分鏡 + 規格 + prompt）。
- `ecommerce-operator` — 資深跨境電商營運（Amazon / Shopee 級）。把產品真正賣出去。產品 → 電商情報卡 → 選品與 Listing 驗證報告 → 上架投放作戰包（Listing + PPC + 排名打法 + 補貨 + 儀表板）。

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

- v0.2.0 — 新增 4 位角色：structural-id-designer、certification-expert、sourcing-expert、ecommerce-operator，補滿「開發 → 認證 → 採購量產 → 上架投放」價值鏈。
- v0.1.0 — 初版，收錄 electronics-engineer、animation-designer 兩個角色。
