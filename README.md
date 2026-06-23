# FrankAie-hub · LYCANDER AI RESEARCH HUB

> 專業 AI 角色技能庫（marketplace）。每個 skill 都是一位**資深領域專家 AI**，
> 依「**搜集市場資訊 → 驗證 → 開發 / 設計**」三階段 SOP，獨立發展該領域的專業技能。

由 **LYCANDER GROUP** 維護。本 repo 同時是一個 Claude 外掛 **marketplace**，
裡面收錄 `frankaie-research-hub` plugin，plugin 內含多個專家角色 skill。

---

## 編制：100 位 AI 角色 ＋ 支援陣容（共 33 個 skill）

**核心 100 人 = 30 位團隊專家（6 團隊）＋ 70 位 AI 消費者（4 市場）**，
另有總機、支援專家、工具與基礎建設。完整名冊見
`plugins/frankaie-research-hub/ROSTER.md`。

### 6 個專家團隊（每個 = 5 位具名專家，共 30 人）
`electronics-team`（電子工程）、`mechanical-team`（機構設計）、`visual-team`（視覺設計）、
`marketing-team`（行銷企劃）、`operations-team`（營運執行）、`cx-team`（售後客服）。

### 4 個 AI 消費者市場小組（共 70 人）
`consumers-taiwan`（22）、`consumers-usa`（18）、`consumers-japan`（15）、`consumers-europe`（15）。
用來在「驗證」階段召集虛擬焦點小組，對產品/定價/文案/視覺給購買意願評分與改善建議。

### 1 總機 ＋ 11 位支援專家（單兵深度諮詢）
`hub-router`（總機路由）；`electronics-engineer`、`animation-designer`、`product-manager`、
`data-analyst`、`security-engineer`、`channel-sales`、`supply-chain-expert`、`growth-retention`、
`web-engineer`、`financial-analyst`、`legal-ip`。

### 8 個工具型 skill（執行具體產出）
`listing-optimizer`、`ad-hook-writer`、`copy-humanizer`、`review-miner`、
`pricing-calculator`、`email-sequence-builder`、`competitor-comparison`、`seo-keyword-expander`。

### 3 個基礎建設 skill（記憶 / 品質 / 驗證）
`planning-with-files`（長專案持久記憶）、`quality-gate`（產出對抗式審查 + 完成前驗證）、
`validation-panel`（AI 消費者驗證關卡，統一 1–5 購買意願 rubric）。

> 要再擴編，只要在 `plugins/frankaie-research-hub/skills/` 下新增資料夾 + `SKILL.md` 即可
> （新增後 `scripts/check_skills.py` 會在 CI 自動檢查引用與計數一致性）。

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

4. 重啟 session 後，33 個 skill 就會出現在清單，依各自 description 的觸發關鍵字自動觸發；
   不確定該找誰時先呼叫 `hub-router` 由總機分流。

> Repo 設為 **Public** 最省事；若設 Private，安裝時需設定 GitHub 認證。

---

## 目錄結構

```
FrankAie-hub/
├─ .claude-plugin/
│  └─ marketplace.json              ← marketplace 定義（指向 plugin）
├─ README.md                        ← 你正在看的這份
├─ scripts/
│  └─ check_skills.py               ← 引用完整性 + 計數一致性檢查（CI 用）
├─ .github/workflows/
│  └─ check-skills.yml              ← PR / push 時自動跑上面的檢查
└─ plugins/
   └─ frankaie-research-hub/
      ├─ .claude-plugin/
      │  └─ plugin.json             ← plugin 基本資料
      ├─ README.md                  ← plugin 說明 + 新增角色教學 + 格式選用指南
      ├─ ROSTER.md                  ← 完整編制名冊 & 路由表（33 個 skill）
      └─ skills/                    ← 33 個 skill，每個一個資料夾 + SKILL.md
         ├─ _TEMPLATE/              ← 新增 skill 範本（Pattern A/B/C）
         ├─ hub-router/             ← 總機路由
         ├─ electronics-team/ … cx-team/        ← 6 專家團隊
         ├─ consumers-taiwan/ … consumers-europe/ ← 4 AI 消費者小組
         ├─ product-manager/ data-analyst/ …    ← 支援專家
         ├─ listing-optimizer/ …                ← 工具型
         └─ planning-with-files/ quality-gate/  ← 基礎建設
```

---

## 新增一位專家角色（快速版）

1. 在 `plugins/frankaie-research-hub/skills/` 新增資料夾，例如 `supply-chain-expert/`。
2. 裡面放 `SKILL.md`，frontmatter 至少要有 `name` 與 `description`（description 寫清楚觸發關鍵字）。
3. 內文建議沿用「Persona → 三階段 SOP → 輸出範本 → 協作介面 → 啟動方式」結構。
4. commit、push，重新 `/plugin marketplace update frankaie-hub` 即可。

詳見 `plugins/frankaie-research-hub/README.md`。
