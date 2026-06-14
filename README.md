# FrankAie-hub · LYCANDER AI RESEARCH HUB

> 專業 AI 角色技能庫（marketplace）。每個 skill 都是一位**資深領域專家 AI**，
> 依「**搜集市場資訊 → 驗證 → 開發 / 設計**」三階段 SOP，獨立發展該領域的專業技能。

由 **LYCANDER GROUP** 維護。本 repo 同時是一個 Claude 外掛 **marketplace**，
裡面收錄 `frankaie-research-hub` plugin，plugin 內含多個專家角色 skill。

---

## 目前收錄的專家 AI 角色

| 角色 skill | 定位（對標） | 三階段 SOP |
|------------|--------------|------------|
| `electronics-engineer` 資深電子工程師 | Anker 級 / 10 年+ 硬體研發 | 搜集市場資訊 → 驗證產品功能 → 開發對應產品 |
| `animation-designer` 資深動畫 / 視覺設計師 | Native Union 級 / 品牌動態視覺 | 搜集市場資訊 → 驗證視覺轉化率 → 設計對應圖像及影像 |

> 之後要再加新角色（例：供應鏈專家、品牌行銷長、UX 研究員…），只要在
> `plugins/frankaie-research-hub/skills/` 下新增一個資料夾 + `SKILL.md` 即可。

---

## 安裝方式（在 Claude 中）

1. 把本 repo push 上 GitHub（`Lycander168/FrankAie-hub`）。
2. 加入 marketplace：

   ```
   /plugin marketplace add Lycander168/FrankAie-hub
   ```

3. 安裝 plugin：

   ```
   /plugin install frankaie-research-hub@frankaie-hub
   ```

4. 重啟 session 後，兩個專家角色 skill 就會出現在 skill 清單，依描述關鍵字自動觸發。

> Repo 設為 **Public** 最省事；若設 Private，安裝時需設定 GitHub 認證。

---

## 目錄結構

```
FrankAie-hub/
├─ .claude-plugin/
│  └─ marketplace.json              ← marketplace 定義（指向 plugin）
├─ README.md                        ← 你正在看的這份
└─ plugins/
   └─ frankaie-research-hub/
      ├─ .claude-plugin/
      │  └─ plugin.json             ← plugin 基本資料
      ├─ README.md                  ← plugin 說明 + 新增角色教學
      └─ skills/
         ├─ electronics-engineer/
         │  └─ SKILL.md             ← 資深電子工程師 AI
         └─ animation-designer/
            └─ SKILL.md             ← 資深動畫 / 視覺設計師 AI
```

---

## 新增一位專家角色（快速版）

1. 在 `plugins/frankaie-research-hub/skills/` 新增資料夾，例如 `supply-chain-expert/`。
2. 裡面放 `SKILL.md`，frontmatter 至少要有 `name` 與 `description`（description 寫清楚觸發關鍵字）。
3. 內文建議沿用「Persona → 三階段 SOP → 輸出範本 → 協作介面 → 啟動方式」結構。
4. commit、push，重新 `/plugin marketplace update frankaie-hub` 即可。

詳見 `plugins/frankaie-research-hub/README.md`。
