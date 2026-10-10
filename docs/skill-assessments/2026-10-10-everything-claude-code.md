# Everything Claude Code (ECC) 安裝前評估報告

- **評估日期**：2026-10-10
- **評估標的**：`affaan-m/everything-claude-code`（ECC v2.2.3，MIT，Copyright 2026 Affaan Mustafa）
- **來源**：使用者提供的 Instagram Reel 截圖（`iamlily.genai`，標題卡「Everything Claude Code」＋「Affaan Mustafa」）
- **評估標準**：[`docs/SKILL_ADOPTION_RUBRIC.md`](../SKILL_ADOPTION_RUBRIC.md) v1.1
- **決策**：**不自動安裝。全裝否決；兩個限縮範圍達「條件式」**

| 採用範圍 | 加權總分 | 決策 |
|---|---|---|
| **A. 全裝 plugin**（hooks 預設開） | **2.35** | **否決** |
| **B1. 只取供應鏈 7 支**，vendor 成內容 | **3.85** | **條件式安裝** |
| **B2. 只取 `business-content` 14 支** | **2.85** | 暫緩 |
| **C. 純參考資料**（抄設計養分，不裝 skill） | **3.93** | **條件式安裝（上緣）** |

> 四次評估以來第一次有範圍進入「條件式」區間。但沒有任何範圍達到 4.50 自動安裝門檻。

---

## 0. 標的識別

截圖本身沒有 repo 名稱或網址，只有 Reel 標題卡、作者名與貼文文案「有在用 Claude Code 的人，這包先存起來」。依這三個線索定位到 `affaan-m/everything-claude-code`，並以 shallow clone 查證。

**查證結果**：105 MB，MIT，HEAD `4eb71d9`（2026-10-09，merge PR #3484），含 `.claude-plugin/`（`marketplace.json` ＋ `plugin.json`）。確認是 Claude Code plugin + marketplace，**安裝成立**（不同於 2026-09-03 評估的 GPT-Image-2 提示詞集）。

### 第 0 步：界定採用範圍（Rubric v1.1 必做）

- **它是什麼**：有 302 份 `SKILL.md`、有 `.claude-plugin/` → 安裝成立，不是純參考資料。
- **我們要用的是執行能力還是內容**：ECC 的 skill 幾乎全是「方法論＋模板」的**內容型**；但它的 **hooks／scripts 是真執行能力**（Node.js，會 deny 工具呼叫、會改寫檔案）。**兩者必須分開評**。
- **結論**：存在四個合理採用範圍，依 Rubric 規定分別計分、不合併平均。

---

## 1. 事實基準（全部實測，不引用二手數字）

### 1.1 規模

> **先更正一個流傳數字。** 網路文章普遍引用「119 skills / 14 MCP servers」。實測不是這樣：

| 項目 | 實測 | 備註 |
|---|---|---|
| `skills/` | **302** | `find skills -name SKILL.md` = 302，與 `plugin.json` 宣稱一致 |
| `agents/` | **71** | |
| `commands/` | **95** | |
| `rules/` | **122 檔** | `common/` 10 檔 ＋ 22 個語言／框架目錄 |
| `hooks/hooks.json` | **27 個 hook 註冊** | 橫跨 8 個事件 |
| `mcp-configs/` | **34 個 MCP server** | |

**全裝後你的 skill 清單會從 33 支變成 335 支（10.2 倍）**，另加 71 個 agent 與 95 個 slash command 進入命名空間。

### 1.2 ECC 的 302 支在做什麼（用它自己的模組分類，100% 覆蓋）

| 類別 | 支數 | 占比 |
|---|---|---|
| **軟體開發流程／語言**（framework-language 71、workflow-quality 48、agentic-patterns 36、security 21、devops-infra 17…） | **223** | **73.8%** |
| 商務／行銷／內容／研究（business-content 14、media-generation 11、research-apis 10、social 3） | 38 | 12.6% |
| **營運／後勤／供應鏈**（operator-workflows 20、**supply-chain-domain 8**、operator-desk 4、document 2） | 34 | 11.3% |
| 利基（預測市場／自家算力） | 7 | 2.3% |

它自陳是「a production-ready **AI coding plugin**」（`SOUL.md:4`）、「**for engineering teams**」（`marketplace.json`）。95 支 slash command 裡對 LYCANDER 有直接意義的是 **1 支**（`/marketing-campaign`），間接 3 支。

### 1.3 工程品質：證據推翻了預期

原本預期會看到典型社群安裝腳本的亂象，**實測相反**：

- **348 個 `*.test.js` ＋ 22 個 `test_*.py`**，對照 311 個 `scripts/*.js`。其中 68 個 hook 測試、32 個 installer 測試——覆蓋面集中在最高風險處。
- **12 個 CI workflow**，OS × Node × 套件管理器矩陣；**所有 GitHub Action pin 到 commit SHA**（非 tag）；有 `packed-install-lifecycle` job 實測「打包→安裝→卸載」全流程。
- **SLSA Level 3 provenance**、`supply-chain-watch.yml`、dependabot、CODEOWNERS、commitlint。
- `SECURITY.md`（7 KB）內容紮實，甚至有一節處理 prompt injection。
- 程式碼內的安全註解**帶 issue 編號與 CVE**（如 `auto-update.js:135` 引 `GHSA-hfpv-w6mp-5g95`）。
- `.gitleaksignore` 全檔只有 2 行，只忽略一個西班牙文文件裡的範例 key——**不是用來蓋掉真實洩漏**。

**保留訊號**：3484+ PR 但單一 maintainer（bus factor = 1）；體積失控（README 112 KB）；`.env.example` 推銷兩個第三方推論平台，含中國端點 `api.modelverse.cn` 與帶 `utm_campaign=ECC` 聯盟追蹤的 Atlas Cloud。

### 1.4 install.sh 比體積暗示的安全得多

| 問題 | 實測結果 | 證據 |
|---|---|---|
| 覆蓋既有 `settings.json`？ | **不會盲目覆蓋**。以 hook id 為鍵 merge；偵測到 drift 直接 throw 拒裝 | `claude-settings.js:477, 528` |
| 覆蓋既有 `CLAUDE.md`？ | **完全不碰**，不在任何模組的 paths 裡 | `install-modules.json:38` |
| 覆蓋任何使用者檔案？ | **不會**。ownership guard：目的檔已存在且不在帳本中 → 跳過並警告，且不記入帳本 | `ownership-guard.js:87, 150` |
| `curl \| bash`？ | **沒有**，全 repo 零命中 | |
| sudo？ | **不需要** | |
| 改 shell profile／PATH？ | **不會** | |
| 自動 `npm install`？ | 會，但帶 `--ignore-scripts`（明文註解為阻擋 pre/postinstall RCE） | `install.sh:30` |
| 能乾淨移除？ | **可以**。`uninstall.js` 依 SHA-256 帳本刪除，使用者改過的檔案標為 `drifted` 不刪，支援 `--dry-run` | `install-lifecycle.js:235, 674` |

**真正的侵入點不是破壞性，是體積**：302 個 skill **扁平倒進** `~/.claude/skills/`，**無 namespace 隔離**（`claude-home.js:31-41`）——`rules/` 有隔離，`skills/` 沒有。

### 1.5 hooks：本案最硬的風險

`plugin.json` 的 `hooks_enabled` 預設 **true**、`hook_profile` 預設 **standard**。**走 plugin 路徑安裝，27 個 hook 預設全部生效，不需使用者額外動作。**

四項實質風險（檔名＋行號）：

**🔴 GateGuard 會「拒絕」寫檔**（`gateguard-fact-force.js:1929-1956`，2033 行）
對每個 session 內**首次觸碰的檔案**回傳 `permissionDecision: 'deny'`，要求先交出 importers／受影響 API／data schema 才放行。預設**沒有 `.md` 豁免**。
→ **直接後果：`planning-with-files` 第一次建立 `task_plan.md` / `findings.md` / `progress.md` 會被 deny，每檔一次。**

**🔴 Stop hook 自動改寫檔案**（`stop-format-typecheck.js:94-100`）
每次 Claude 停下來，對本 session 編輯過的檔案跑 `biome check --write` 或 `prettier --write`。
我方 repo 無 `.prettierrc`／`biome.json`／`package.json`，但容器內 `prettier` 在 PATH → **會用預設設定改寫**。

> **實測（scratchpad 複本）**：
> ```
> prettier --write "plugins/.../skills/*/SKILL.md" README.md   → exit 0
> git diff --stat → 28 files changed, 444 insertions(+), 229 deletions(-)
> python3 scripts/check_skills.py → exit 0（4 項全綠）
> ```
> **好消息：CI 不會由綠轉紅，一票否決第 3 條未觸發。**
> **壞消息**：prettier 以半角寬計算 CJK，產生視覺上**更歪**的表格；每個 session 結束都可能產出 20+ 檔的無意義 diff，污染 git history 與 PR review。

**🔴 自動改寫 Bash 指令**（`auto-tmux-dev.js:81`）
攔截 `npm run dev` 類指令整條換掉，並先 `tmux kill-session`（殺掉同名既有 session）。用字串插值組 shell command。**無 `profiles` 欄位 → 預設 profile 下即 active。**

**🟠 硬性攔截工具呼叫**：`config-protection.js:238` `process.exit(2)` 封鎖對 linter／formatter 設定檔的修改；`block-no-verify.js:250` 封鎖 `git commit --no-verify`。

**🟠 對話內容重送**：`llm-summary.js:153` 透過 `spawnSync('claude', ['-p'])` 把整份 conversation 送出。
→ **緩解：送往的是使用者自己的 `claude` CLI，資料落在 Anthropic，與 Claude Code 同一信任邊界，不是第三方外流。**代價是額外計費。

**已查證為低風險（避免誤判）**：`doc-file-warning` 的 denylist 只比對**大寫**檔名且永遠 exit 0，不會碰 `task_plan.md`；`hookify-runtime` 只讀 project-local `.claude/hookify/`，我方無該目錄 → no-op；`delivery-gate` 與 `ck` 的 SessionStart hook **未註冊在 hooks.json，屬 opt-in**。

### 1.6 MCP 型錄是惰性的

**34 個 server 不會被自動註冊。** 它屬於 `platform-configs` 模組，但只是被**原樣複製**到 `~/.claude/mcp-configs/`。安裝器的 operation kind 裡**沒有任何 MCP 註冊動作**；grep `claude.json`／`mcpServers` 在安裝相關目錄**全部零命中** → **從不改動 `~/.claude.json`**。

連線測試（未送任何憑證）：安裝必需網域全部可達（`registry.npmjs.org` 200、`pypi.org` 200、`github.com` 已穿透、`api.anthropic.com` 已達）；**第三方 MCP 端點全部 403 CONNECT 拒絕**（Vercel／Cloudflare／ClickHouse／parallel.ai／browser-use／memxus／modelverse／atlascloud）。

對台灣 3C 品牌的商務用途，**34 個中需要的是 0 個**——全是部署、資料庫、瀏覽器自動化、工程專案管理。

---

## 2. 專家交叉驗證

### 專家 A｜架構稽核

**檔名層面：302 ∩ 33 = 0**（實測 set intersection 為空），且 plugin 路徑下 skill 會被加 `ecc:` 前綴。但**語意層面有 5 組真重複**：

| 我方 skill | ECC 對應 | 判斷依據 |
|---|---|---|
| **`planning-with-files`** | **`ck`**（Context Keeper） | ck 的 description 逐字就是我方定位：「context must survive across sessions… resuming where a previous session left off」。**同一架構槽位、同一問題、兩套不相容的落盤格式**，會出現「哪份記憶才是權威」的歧義 |
| `product-manager` | `product-lens` | go/no-go ＋ PMF 訊號 ＋ ICE 優先級 ＋ PRODUCT-BRIEF.md，同一件事的英文版 |
| `marketing-team` ＋ 3 支工具 | `marketing-campaign` | 自稱 orchestration layer，涵蓋 LP／EDM／社群／廣告／短影音五項，**一支吃掉我方四支** |
| `seo-keyword-expander` | `seo` | keyword mapping 直接對上 |
| `competitor-comparison` | `competitive-platform-analysis` → `benchmark-methodology` → `competitive-report-structure` | **ECC 是三段式 pipeline，比我方單檔比較表完整——這組是升級版** |

**4 組半重複**：`quality-gate`↔`verification-loop`／`council`（同槽位但對象不同：ECC 審程式碼，我方審內容產出物）、`hub-router`↔`team-builder`／`dev-team`、`visual-team`↔motion 系列、`web-engineer`↔frontend 系列。

**24 支不重複**，其中：

> **我方護城河：`consumers-*` ×4 ＋ `validation-panel`。ECC 302 支中無任何虛擬消費者小組／購買意願 rubric／跨市場焦點驗證，零對應。**
> 另外 `electronics-*`（USB-PD／GaN／BMS／EMI）、`mechanical-team`（模具 DFM／CMF）、`listing-optimizer`（Amazon FBA 費率反算／A+ EBC）、`legal-ip`（FTO 迴避設計）也全無對應。

**規模暴增的具體傷害**：
1. **選擇集稀釋**——我方 skill 從「33 選 1」變成「335 選 1」，base rate 從 3.0% 掉到 **0.3%**。
2. **`hub-router` 失效**——它的價值在那張 7 列觸發衝突仲裁表，對 302 支 `ecc:*` **沒有任何規則**。正中 Rubric D4=2 的錨點原文。
3. **三階段 SOP 斷鏈**——一旦中途被 ECC skill 接手，交棒鏈在那個節點斷掉，`quality-gate` 不會被叫、`progress.md` 不會被更新。
4. **context 成本**——335 支 description 全進 system prompt，粗估增加 15–25k token 常駐開銷。

> **上游自己承認全裝不是建議做法。** ECC 專門做了一支 `agent-sort`：「sorting skills into DAILY vs LIBRARY buckets… **when ECC should be trimmed to what a project actually needs instead of loading the full bundle**」。它還提供 `strategic-compact`、`context-budget`、`token-budget-advisor` 三支 skill 專門處理自己造成的 context 問題。

**共存性**：marketplace 與 plugin 命名空間都不衝突；`CLAUDE.md`／`SOUL.md` **不會**被裝到全域（任何模組都不含它們），`AGENTS.md` 只對 Codex／Antigravity 生效，**對 Claude Code 無效**。

> **真正的全域指令污染來自 `rules/`。** README 明寫「Claude Code plugins cannot distribute rules」，所以 122 個 rules 檔要使用者手動 `cp -R rules/common ~/.claude/rules/ecc/`。一旦照做，`rules/common/development-workflow.md` 的「**mandatory** Research & Reuse」「必用 planner agent」「必走 TDD，80%+ coverage」與 `rules/common/agents.md` 的「**No user prompt needed**」就成為全域 always-follow 指令，**直接與我方三階段 SOP 搶「該怎麼做事」的指令權**。

⚠️ 另有一個形式不一致：我方 `.claude/settings.json` 用 **array** 形式 `"enabledPlugins": [...]`，ECC 文件給的是 **object** 形式 `{"ecc@ecc": true}`，兩者不能直接拼接。

### 專家 B｜技術與資安稽核

見 §1.3–1.6（install.sh 稽核、hooks 稽核、MCP 型錄、連線測試、品質訊號）。

**B 的決定性結論**：

> ECC 以「開發者機器上**長期存在**的 `~/.claude`」為設計前提，而我方是**雲端 session，`~/.claude` 每次重置**。install-state／digest／uninstall 的整套機制失去前提，每個 session 要重裝一次，**攤提期為零**。
>
> 而這也意味著 §1.5 的兩大風險（hooks、全域污染）在我方情境下**完全不必承擔**——因為正確的採用路徑本來就是只取內容。

**B 另發現一條更乾淨的來源**：CHANGELOG 2.2.2 的 **`pi/core` profile**——「123 portable engineering skills… **no extensions, no hooks, no runtime downloads, and no network or SaaS dependencies**」，build 時對 non-allowlisted URL、pipe-to-shell、secrets、絕對家目錄路徑、symlink 做硬性檢查。這是上游自己維護的安全子集。

### 專家 C｜商業價值與使用者適配

**C 找到了整份評估的唯一高價值區**：`supply-chain-domain` 8 支是**密度極高的 codified domain knowledge**，不是 persona 包裝。

| ECC skill | 大小 | 實際內容證據 |
|---|---|---|
| `customs-trade-compliance` | 29 KB | GRI 1–6 **逐條優先順序規則**、US 10-digit HTS／EU TARIC／UK Global Tariff 區別、「多功能裝置依主要功能而非最貴元件分類（GRI 3(b)）」、「零件 vs 配件看 Section XVI Note 2」、USMCA／RCEP／FTZ／duty drawback、Incoterms 2020 |
| `quality-nonconformance` | 30 KB | ANSI/ASQ Z1.4 檢驗水準、「連續 5 批中 2 批退→加嚴；連續 10 批允收→減量」、critical=AQL 0／major 1.0–2.5／minor 2.5–6.5、Western Electric 四條判讀規則、**Cp vs Cpk（Cp=2.0 但 Cpk=0.8 要修平均不是修變異）**、8D D0–D8、SCAR 10 天回覆/30 天改善 |
| `returns-reverse-logistics` | 25 KB | A–D 條件分級、restock/refurbish/liquidate/scrap/RTV 回收經濟比較、serial returner 判定 |
| `logistics-exception-management` | 17 KB | 「吃掉成本 vs 打索賠」判斷框架、**Carmack 9 個月索賠時效** |
| `inventory-demand-planning` | 24 KB | ABC/XYZ 分群選預測法、安全庫存同時納入需求變異與前置變異、促銷 lift 與**促後 dip**、新品用 analog SKU |
| `production-scheduling` | 29 KB | TOC drum-buffer-rope、SMED、OEE、換線矩陣 nearest-neighbor + 2-opt、24–48h 凍結窗 |
| `carrier-relationship-management` | 24 KB | 物流商議價與服務水準 |
| `energy-procurement` | 30 KB | **用不到**（工業電力／天然氣採購，與我方規模不符） |

**對照我方**：`operations-team/SKILL.md` 是 9.3 KB 涵蓋 5 個角色，報關那段只有「HS Code 準確性零容忍」與一張空白表格模板；`supply-chain-expert/SKILL.md` 是 5.4 KB 的策略層 TCO 框架。

> **兩者都有流程與角色，但沒有方法本體；ECC 這 8 支正好反過來：沒有角色、全是方法。這是互補，不是重工。**

**C 的關鍵發現——中英文觸發的雙面效應**：

實測 302 支中**只有 5 支 frontmatter 含中文**。我方 33 支全部是中文 description ＋ 中文觸發詞。

- **好處（推高 D4）**：中文 prompt 下，ECC 的英文 skill 幾乎不會搶走 FrankAie 的觸發。
- **壞處（打掉 D1）**：**反過來也成立**。你問「這顆 65W GaN 充電器報關 HS Code 要用哪個」，命中的是 `operations-team`（中文觸發詞「報關」），`customs-trade-compliance` 不會出現。

> **全裝 ECC 的淨效果是：清單暴增 10 倍，而真正有用的那 8 支還是不會自己跳出來。**
> 要拿到價值，必須手動指名英文 skill 名，或**重寫 description 成中文**。

**C 對五項日常的誠實盤點**：

| Frankie 的日常 | ECC 有沒有幫助 |
|---|---|
| 讀工作日誌回信 | `email-ops` 存在但依賴信箱介面，加的是流程紀律不是能力。**無實質改善** |
| 評估要不要裝 skill | ECC **沒有**任何採用評估 rubric。`docs/SKILL_ADOPTION_RUBRIC.md` 比 ECC 任何東西都嚴謹。**這塊 ECC 不如我方** |
| 寫電商文案 | `business-content` 14 支都是 3–5 KB 薄框架且**全部 X/LinkedIn/newsletter 導向**；我方是 Amazon/Shopee/momo/Rakuten listing 導向，更貼。**12 支重工，2 支有加值**（`brand-voice` 的可重用風格 profile、`brand-discovery` 的 8 模組品牌訪談） |
| 規劃包裝打樣排程 | **沒有**。`production-scheduling` 是 SAP PP + MES 的工廠內部排程，不是品牌方的打樣里程碑管理 |
| 跟 Tina 和工廠協作 | 工廠端 `quality-nonconformance` 的 AQL／8D／SCAR **真的有用**；Tina 端只有 `brand-discovery` 的 brandbook |

**C 的 CI 實測（決定 D5）**：這 8 支**每支都是單一 SKILL.md、零附屬檔、零 script**，合計 202 KB。但 **8/8 支都不含** `check_skills.py` 的 `GUARDRAIL_RE`（中文反幻覺標記）→ **直接放進 `plugins/frankaie-research-hub/skills/` 會讓 CI 由綠轉紅**（一票否決第 3 條）。表格檢查 8/8 通過，只缺這一項。

> ⚠️ **授權細節**：這 8 支的 frontmatter 標的是 **Apache-2.0**，而非 repo 整體的 MIT。vendor 時需保留 `metadata.origin: ECC` 與對應的 license 欄位。

---

## 3. 加權計分（四個範圍）

### 範圍 A：全裝 plugin（`/plugin install ecc@ecc`，hooks 預設開）

| 構面 | 權重 | 來源 | 平均 | 加權 |
|---|---|---|---|---|
| D1 需求必要性與使用頻率 | 25% | A 2、C 2 | **2.00** | 0.500 |
| D2 非重複性／能力加值 | 20% | A 3、C 2 | **2.50** | 0.500 |
| D3 技術可行性 | 15% | B 2（實測受阻） | **2.00** | 0.300 |
| D4 衝突與誤觸風險 | 15% | A 2 | **2.00** | 0.300 |
| D5 整合與維運成本 | 15% | A 2、C 2 | **2.00** | 0.300 |
| D6 授權與合規 | 10% | A 5、B 4 | **4.50** | 0.450 |
| **加權總分** | | **< 2.50 → 否決** | | **2.35** |

> **D3 的計分說明**：Rubric v1.1 規定「無實測者一律以 3 分計」。但本案不是「沒有證據」，而是**有證據且為負**——第三方端點實測 403 全封鎖、`~/.claude` 經確認每 session 重置。若機械套用 3 分，總分為 2.50（暫緩下緣）；兩種算法都遠低於 4.50，不影響決策。此問題已回饋為 **Rubric v1.2** 的新增條款。

### 範圍 B1：只取供應鏈 7 支（剔除 `energy-procurement`），vendor 成內容

| 構面 | 權重 | 來源 | 平均 | 加權 |
|---|---|---|---|---|
| D1 需求必要性與使用頻率 | 25% | A 3、C 4 | **3.50** | 0.875 |
| D2 非重複性／能力加值 | 20% | A 4、C 4 | **4.00** | 0.800 |
| D3 技術可行性 | 15% | B 4（純檔案複製，零外部依賴） | **4.00** | 0.600 |
| D4 衝突與誤觸風險 | 15% | A 4（不帶 hook，誤觸無副作用） | **4.00** | 0.600 |
| D5 整合與維運成本 | 15% | A 4、C 3 | **3.50** | 0.525 |
| D6 授權與合規 | 10% | A 5、B 4 | **4.50** | 0.450 |
| **加權總分** | | **3.50–4.49 → 條件式安裝** | | **3.85** |

### 範圍 B2：只取 `business-content` 14 支

D1 2.00／D2 2.00／D3 4.00／D4 3.00／D5 3.00／D6 4.50 → **2.85，暫緩**。
建議改法：只抽 `competitive-platform-analysis`、`competitive-report-structure`、`brand-discovery` **3 支當參考資料**升級我方 `competitor-comparison`，不整組安裝。

### 範圍 C：純參考資料（不裝任何 skill）

| 構面 | 權重 | 來源 | 平均 | 加權 |
|---|---|---|---|---|
| D1 | 25% | A 3、C 3 | **3.00** | 0.750 |
| D2 | 20% | A 4、C 3 | **3.50** | 0.700 |
| D3 | 15% | B 4 | **4.00** | 0.600 |
| D4 | 15% | A 5（不安裝 → 觸發詞零重疊） | **5.00** | 0.750 |
| D5 | 15% | A 4、C 5 | **4.50** | 0.675 |
| D6 | 10% | A 5、B 4 | **4.50** | 0.450 |
| **加權總分** | | **3.50–4.49 → 條件式（上緣）** | | **3.93** |

### 評估者一致性檢查

最大分差為 1 分（D2 範圍 A：A 3 / C 2；D1 範圍 B1：A 3 / C 4；D3 範圍 A：A 3 / B 2），**無任一構面分差 ≥ 3**，未觸發重評條款。三方對「工程品質高、但規模與情境錯配、唯一高價值是供應鏈那 8 支」高度一致。

### 一票否決條款檢核

| 條款 | 狀態 |
|---|---|
| 1. 任一構面得 1 分 | **未觸發**（最低 2 分） |
| 2. D6 ≤ 2 | **未觸發**（D6 = 4.50，MIT，無須授權或預算簽核） |
| 3. CI 由綠轉紅 | **範圍 A 未觸發**（實測 prettier 改寫後 `check_skills.py` 仍 exit 0）；**範圍 B1 會觸發**——8/8 支缺中文反幻覺標記，**必須逐支補一行才能 vendor**，這是 B1 的硬性前置條件 |
| 4. 評估者分差 ≥ 3 | **未觸發** |

---

## 4. 決策

**不自動安裝。** 沒有任何範圍達到 4.50 門檻。

**否決全裝（範圍 A，2.35）**——不是因為 ECC 品質差。它品質很高：348 個測試、SLSA3 provenance、Action pin 到 SHA、ownership guard、真 uninstaller、MIT。否決的理由是三件具體的事：

1. **規模比 302:33**——我方最獨特的資產（`consumers-*` ×4 ＋ `validation-panel`，ECC 零對應）會被稀釋到 0.3% 的選中率。
2. **`hub-router` 對 `ecc:*` 零仲裁規則**——正中 Rubric D4=2 的錨點原文。
3. **27 個預設啟用的 hook 中有兩個會阻擋寫檔／自動改寫檔案**——GateGuard 會 deny `planning-with-files` 建立 `task_plan.md`；Stop hook 的 `prettier --write` 實測產生 28 檔、+444/−229 的無意義 diff。

而最根本的一點是 B 指出的：**雲端 session 的 `~/.claude` 每次重置，整套安裝的價值前提本來就不存在。**

---

## 5. 建議處置（依投報比排序）

### ① 範圍 C — 今天就能做，零成本零風險（總分 3.93，最高）

把 ECC 的設計養分抄進既有檔案，**一支 skill 都不裝**：

- **抄進 `CLAUDE.md`**：
  - 「MCP 可以配 20–30 個但**同時只開 ≤10 個、active tool ≤80 個**，否則 200k context 實際只剩 70k」（`the-shortform-guide.md:137-146`）——**這條對你立刻有用**，你現在掛著 Adobe、Canva、Figma、Gmail、Drive、Dropbox、Slack、Supabase、GitHub 一大串 MCP。
  - 「context window 最後 20% 不做大型工作」（`rules/common/performance.md`）。
  - session 結束前寫「什麼有效（附證據）／什麼試過沒用／什麼還沒做」三問交接（`the-longform-guide.md:38-50`）。
- **強化 `planning-with-files`**：吸收 `ck` 的 `/ck save|resume` 格式與上面的三問。
- **強化 `quality-gate`**：吸收 `delivery-gate` 的「決定論檢查（mtime/disk/regex）vs 推理檢查（內容品質）」分工——這與我方「看內容」正交。
- **強化 `hub-router`**：吸收 `agent-sort` 的 DAILY/LIBRARY 分桶概念。
- **改善工作日誌品質**：`growth-log` 教「寫 root cause + 可移轉規則 + 可辨識信號，不要寫『修好了 X』」——直接改善你讀日誌回信的輸入品質。

CI 的 `ALLOWLIST` 已有引用上游 skill 的先例（`verification-before-completion`），加 attribution 即可。

### ② 範圍 B1 — 條件式，約半天（總分 3.85）

vendor 供應鏈 **7 支**（剔除 `energy-procurement`）。三個**硬性**前置條件：

1. **每支補一行中文反幻覺標記**——8/8 支都不含 `GUARDRAIL_RE`，不補 **CI 必定由綠轉紅**（一票否決第 3 條）。
2. **description 改寫成中文觸發詞**——例如 `customs-trade-compliance` 要加「報關、HS Code、關稅、原產地、進出口文件、Incoterms」，否則中文 prompt 下**永遠觸發不到**，等於白裝。
3. **同步 `ROSTER.md` 的「共 N 個 skill」、`README.md` 編制數字、`hub-router` 路由表（補報關／庫存／排程／品質異常 4 列）、marketplace 與 plugin 版號**——`check_skills.py` 的 `check_count` 與 `check_versions` 會抓。

授權：保留 MIT 著作權聲明；注意這 8 支 frontmatter 標的是 **Apache-2.0**，保留 `metadata.origin: ECC` 與 license 欄位。

**不走 plugin install，不帶任何 hook，不 `cp` rules。**

### ③ 範圍 B2 — 只抽 3 支當參考

`competitive-platform-analysis`、`competitive-report-structure`、`brand-discovery`，用來升級 `competitor-comparison`。其餘 11 支是重工。

### ④ 明確不要做

- 全裝 plugin
- 開 hooks（若未來真要裝：`hook_profile=minimal` 或 `hooks_enabled=false`、設 `GATEGUARD_EXEMPT_GLOBS` 涵蓋 `**/*.md`）
- **`cp -R rules/common ~/.claude/rules/ecc/`**——這是全域指令層污染的唯一來源
- 裝 `business-content` 整組、`unified-memory`（需另外 `npm install -g ecc-universal`）
- 使用 `.env.example` 推銷的 `api.modelverse.cn`（中國端點）——建議列入政策明確禁用

---

## 6. 累積觀察（四次評估後）

| 日期 | 標的 | 結果 |
|---|---|---|
| 2026-09-03 | Remotion 官方 Agent Skills | 3.24，暫緩 |
| 2026-09-03 | GPT-Image-2 提示詞集 | 2.20 否決 / 3.25 暫緩 |
| 2026-10-10 | **Everything Claude Code** | **2.35 否決 / 3.85 條件式 / 3.93 條件式** |

**三個模式浮現：**

1. **缺口一直在執行端，不在創意端。** Remotion 與 GPT-Image-2 的結論都是「HUB 缺的是產出檔案的能力」；ECC 則是第一個證明「HUB 的方法論層其實不缺，缺的是特定領域的方法本體」（供應鏈那 8 支）。
2. **「安裝整包」幾乎從不是對的答案。** 三個標的、四個全量範圍，全部落在否決或暫緩；而每次的最佳解都是「只取其中 3–8 支，或只抄設計養分」。ECC 連上游自己都做了 `agent-sort` 來勸退全裝。
3. **中文 persona 是護城河也是牆。** 它擋住外來 skill 搶觸發，但也擋住外來 skill 被觸發。任何 vendor 進來的英文 skill，**description 中文化是必做工序，不是可選項**。

---

## 7. 附註與來源

- 全程靜態閱讀，**未執行 ECC 的 `install.sh`／`install.ps1`／任何 script／hook**，未安裝任何相依套件。
- `/home/user/FrankAie-hub` 全程未被修改（三位專家皆確認 `git status --porcelain` 為空）；CI 模擬在 scratchpad 複本上進行。
- 連線測試僅發 TCP CONNECT，未送出任何憑證；環境變數檢查只讀名稱不讀值。

**來源**：
[affaan-m/everything-claude-code](https://github.com/affaan-m/everything-claude-code) ·
[Everything Claude Code 解説（weel.co.jp）](https://weel.co.jp/media/tech/everything-claude-code/) ·
[Inside the 82K-Star Agent Harness（Medium）](https://medium.com/@tentenco/everything-claude-code-inside-the-82k-star-agent-harness-thats-dividing-the-developer-community-4fe54feccbc1) ·
[ECC Explained（emelia.io）](https://emelia.io/pt/hub/everything-claude-code-explained)

> 二手文章的 skill 數字（119／150+）與本報告實測（302）不符，一律以實測為準。
