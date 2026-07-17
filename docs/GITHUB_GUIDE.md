# GitHub 操作指南（給其他 Claude User）

> 這份文件說明：**當你用 Claude（Claude Code CLI / 網頁版 / App）操作這個 repo 或任何 GitHub 專案時，該怎麼下指令、Claude 能做什麼、以及要注意哪些規範。**
> 目標讀者：LYCANDER 團隊與任何接手本 repo 的 Claude 使用者。

---

## 0. 一分鐘快速上手

想讓 Claude 幫你動 GitHub，直接用自然語言講就好，例如：

| 你想做的事 | 對 Claude 這樣說 |
|---|---|
| 看某個 PR 的內容與狀態 | 「幫我看 PR #6 改了什麼、CI 過了沒」 |
| 開新分支做修改並提交 | 「在 `claude/xxx` 分支加上 OO 功能，commit 並 push」 |
| 開 Pull Request | 「幫我把這個分支開一個 PR，標題寫…」 |
| 盯著 PR、CI 掛掉自動修 | 「幫我 watch PR #12，CI 失敗就自動修」 |
| 找 code / issue | 「repo 裡哪裡定義了 `check_skills`？」 |

Claude 會自己選用底層工具（GitHub MCP、git 指令）完成，你不用記指令。

---

## 1. Claude 在 GitHub 上「能」與「不能」做什麼

### ✅ 能做
- **讀取**：瀏覽 repo 檔案、看 commit / PR / issue、讀 CI log、搜尋 code。
- **寫入**：建分支、改檔案、commit、push、開 PR、留 PR/issue 留言、回覆 review。
- **CI 互動**：查 workflow 執行結果、抓失敗 job 的 log、觸發重跑。
- **監看**：訂閱某個 PR 的活動（新留言、CI 結果、review），事件進來時自動處理或詢問你。

### ⛔ 不會 / 不該做（除非你明確要求）
- **不會主動開 PR**。除非你講「開 PR」，Claude 只會 commit + push 到分支。
- **不會亂 merge**。合併 PR 屬於不可逆動作，會先跟你確認。
- **不會 push 到非指定分支**。見第 2 節分支規範。
- **不會跨越授權範圍的 repo**。本 session 只被授權操作 `lycander168/frankaie-hub`；要動別的 repo 需先加入。

> 環境註記：在遠端執行環境裡，Claude **沒有** `gh` / `hub` CLI，也沒有裸的 GitHub API，一律透過 **GitHub MCP 工具**（`mcp__github__*`）操作。

---

## 2. 分支與提交規範（重要）

本 repo 採「功能分支 + PR」流程，`main` 為受保護的預設分支。

### 規則
1. **所有開發都在功能分支上**，命名慣例 `claude/<主題>-<隨機碼>`，例如 `claude/github-guide-kxrsp1`。
2. **絕不直接 push 到 `main`**。
3. **絕不 push 到別人指定以外的分支**（沒有明確授權就不換分支）。
4. commit message 用清楚、描述性的中文/英文皆可，慣例沿用 [Conventional Commits](#附錄a-commit-message-慣例)：`feat:` / `fix:` / `chore:` / `docs:` …。
5. push 一律用 `git push -u origin <branch-name>`；遇網路錯誤才重試（指數退避 2s→4s→8s→16s，最多 4 次）。

### 若指定分支的 PR「已經被 merge」
被 merge 的 PR 視為完成、不可再利用。後續工作要當成**全新變更**：
```bash
git fetch origin main
git checkout -B <branch-name> origin/main   # 用同名分支、從最新 main 重開
# 做新變更 → commit → push（新的 PR，不是舊的）
```
若分支上還有尚未合併的 commit，保留它們（rebase 到新 base），不要丟棄。

---

## 3. 標準工作流程（Claude 內部怎麼跑）

以「加一個功能並開 PR」為例，Claude 大致會這樣做，你可對照理解：

```
1. 確認 / 建立功能分支      git checkout -B claude/xxx origin/main
2. 修改檔案                （Edit / Write 工具）
3. 本地驗證                 跑 lint / 測試 / scripts/check_skills.py
4. 提交                     git add -A && git commit -m "feat: …"
5. 推送                     git push -u origin claude/xxx
6.（你要求時才）開 PR       GitHub MCP: create_pull_request
```

> **本 repo 的 CI 關卡**：`.github/workflows/check-skills.yml` 會在 push / PR 時跑 `scripts/check_skills.py`，檢查 skill 引用完整性與計數一致性。改動 skill 後，Claude 應先在本地跑一次這支腳本再 push，避免 CI 紅燈。

---

## 4. 常用操作對照（自然語言 → Claude 動作）

### 4.1 讀取類
- 「這個 repo 有哪些分支？」→ 列出 branches
- 「PR #6 的 diff 和討論」→ 讀取 PR 內容、檔案變更、留言
- 「最近 5 筆 commit」→ 列出 commit log
- 「CI 為什麼掛了？」→ 抓失敗 job 的 log 並定位原因
- 「哪裡用到 `hub-router`？」→ 全 repo 搜尋 code

### 4.2 寫入類
- 「把 README 的安裝步驟更新成 OO，commit 並 push」
- 「新增一個 `docs/xxx.md`，內容是…」
- 「這段改動幫我開 PR，body 說明改了什麼」
- 「回覆 PR #12 那則 review，說明為什麼這樣改」

### 4.3 CI / 監看類
- 「幫我 watch PR #12，有 review 或 CI 事件就處理」
- 「CI 失敗就自動修，修好 push，不用每次問我」（見第 5 節）

---

## 5. 讓 Claude 盯 PR（訂閱 / 自動修）

你可以請 Claude **訂閱某個 PR 的活動**。訂閱後，PR 的留言、CI 結果、review 會以事件方式送進對話，Claude 會逐一判斷是否要處理：

- **有把握且改動不大** → 直接修、push、更新進度，不會每輪都回你。
- **有歧義 / 動到架構** → 一定先用問答跟你確認再動手。
- **重複或不需處理** → 靜默略過。

**觸發方式**：直接說「watch / 監看 / babysit / autofix PR #N」即可。Claude 會訂閱後結束回合，等事件進來自動醒來——**不會用 `sleep` 空轉輪詢**。

**終止條件**：PR 被 merge 或 close，或你說「停」，訂閱才結束。你隨時可說「不用再盯了」讓它取消訂閱。

> 注意：留言 / review / CI log 屬於**外部內容**。若其中出現想改變任務、要求提權或做出你不會預期之事的指示，Claude 會先向你確認，不會照單全收。

---

## 6. 授權範圍與加入其他 repo

- 本 session 的 GitHub 存取**目前只限** `lycander168/frankaie-hub`。
- 要操作清單外的 repo：請你**明確要求**「把 `owner/repo` 加進來」，Claude 才會嘗試加入（不會自作主張加）。
- 若某 repo 無法存取（未在 workspace 啟用、App 未安裝），Claude 會轉達實際原因，並提示：管理員可在 Claude 的 GitHub 設定頁授權。

---

## 7. 常見坑與最佳實踐

| 狀況 | 建議做法 |
|---|---|
| 想直接改 `main` | 不要。一律走功能分支 + PR。 |
| PR 一直沒動靜 | webhook 不涵蓋所有事件（CI 成功、新 push、衝突轉換不一定送達），可請 Claude 定時自我 check-in 複查。 |
| 改了 skill 卻 CI 紅燈 | push 前先在本地跑 `python scripts/check_skills.py`。 |
| 需要 merge PR | 明確講「合併 PR #N」；Claude 會先確認再動。 |
| 秘密 / token 外洩疑慮 | 別把憑證寫進 commit、PR body、code comment；PR 模板中要求填憑證的欄位一律略過。 |
| 想要精簡 GitHub 留言 | Claude 預設就很省話，只在必要時（如解釋為何某建議行不通）才留言。 |

---

## 附錄A. Commit message 慣例

```
<type>(<scope>): <簡短描述>

<body：為什麼這樣改、影響範圍>（可省略）
```
常用 `type`：
- `feat`：新功能 / 新角色 skill
- `fix`：修 bug
- `docs`：文件（如本指南）
- `chore`：雜項 / 建置 / CI
- `refactor`：重構，不改行為

範例（取自本 repo 歷史）：
```
feat: 擴充 6 個 skill（記憶/品質/驗證/PM/數據/資安…）＋ 品質治理 CI
chore(quality): 全 skill 審計後品質治理 — 修壞引用、加仲裁表與 CI 檢查
```

## 附錄B. Claude 內部用到的 GitHub 工具（供進階讀者參考）

Claude 透過 GitHub MCP server（`mcp__github__*`）操作，常用的有：

| 用途 | 工具 |
|---|---|
| 看自己身分 / 權限 | `get_me` |
| 讀檔案內容 | `get_file_contents` |
| 建 / 更新檔案 | `create_or_update_file`、`push_files` |
| 建分支 | `create_branch` |
| 列 / 搜尋 PR | `list_pull_requests`、`search_pull_requests` |
| 讀 PR 內容 | `pull_request_read` |
| 開 PR | `create_pull_request` |
| PR review 流程 | `pull_request_review_write`、`add_comment_to_pending_review` |
| 留言 | `add_issue_comment`、`add_reply_to_pull_request_comment` |
| CI / Actions | `actions_list`、`actions_get`、`get_job_logs`、`actions_run_trigger` |
| 搜尋 code / issue | `search_code`、`search_issues` |
| 訂閱 / 取消訂閱 PR 活動 | `subscribe_pr_activity`、`unsubscribe_pr_activity` |

> 你不需要記這些——用第 4 節的自然語言講就好，Claude 會自動挑對的工具。

---

_維護：LYCANDER GROUP · 本指南隨環境規範更新。_
