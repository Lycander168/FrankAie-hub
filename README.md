# FrankAie-hub · LYCANDER AI RESEARCH HUB

> 專業 AI 角色技能庫（marketplace）。每個 skill 都是一位**資深領域專家 AI**，
> 依「**搜集市場資訊 → 驗證 → 開發 / 設計**」三階段 SOP，獨立發展該領域的專業技能。

由 **LYCANDER GROUP** 維護。本 repo 同時是一個 Claude 外掛 **marketplace**，
裡面收錄 `frankaie-research-hub` plugin，plugin 內含多個專家角色 skill。

---

## 編制：100 位 AI 角色

**30 位專家（6 團隊）＋ 70 位 AI 消費者（4 市場）**。完整名冊見
`plugins/frankaie-research-hub/ROSTER.md`。

### 旗艦單一專家
| 角色 skill | 定位（對標） | 三階段 SOP |
|------------|--------------|------------|
| `electronics-engineer` 資深電子工程師 | Anker 級 | 搜集市場資訊 → 驗證產品功能 → 開發對應產品 |
| `animation-designer` 資深動畫 / 視覺設計師 | Native Union 級 | 搜集市場資訊 → 驗證視覺轉化率 → 設計對應圖像及影像 |

### 6 個專家團隊（每個 = 5 位具名專家，共 30 人）
`electronics-team`（電子工程）、`mechanical-team`（機構設計）、`visual-team`（視覺設計）、
`marketing-team`（行銷企劃）、`operations-team`（營運執行）、`cx-team`（售後客服）。

### 4 個 AI 消費者市場小組（共 70 人）
`consumers-taiwan`（22）、`consumers-usa`（18）、`consumers-japan`（15）、`consumers-europe`（15）。
用來在「驗證」階段召集虛擬焦點小組，對產品/定價/文案/視覺給購買意願評分與改善建議。

> 要再擴編，只要在 `plugins/frankaie-research-hub/skills/` 下新增資料夾 + `SKILL.md` 即可。

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

---

## 維護者文件

- **作業指南（HUB 操作手冊）**：`docs/OPERATIONS_GUIDE.md` —— 怎麼用這 100 位角色＋工具，
  把一個專案從「想法」跑到「上市與售後」的標準作業流程（含決策樹、7 站動線、實戰範例）。
- **GitHub 操作指南**：`docs/GITHUB_GUIDE.md` —— 從 clone、開分支、commit、push 到開 PR
  與更新 marketplace 的完整照抄指令，適合第一次接觸 Git 的維護者。
