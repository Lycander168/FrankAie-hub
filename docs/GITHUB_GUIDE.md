# GitHub 操作指南 · FrankAie-hub

> 本指南帶你從零開始，學會維護 `Lycander168/FrankAie-hub` 這個 repo 所需要的所有
> GitHub 操作：取得程式碼、修改、提交、推送、開 PR，以及更新 Claude marketplace。
> 由 **LYCANDER GROUP** 維護。

適用對象：第一次接觸 Git / GitHub，或只想要一份可照抄的指令清單的維護者。

---

## 0. 名詞快速理解

| 名詞 | 白話解釋 |
|------|----------|
| **repo（儲存庫）** | 專案的資料夾，含所有檔案與歷史紀錄。本專案是 `Lycander168/FrankAie-hub`。 |
| **clone（複製）** | 把 GitHub 上的 repo 下載到自己電腦。 |
| **branch（分支）** | 一條獨立的開發線。在分支上改東西不會影響 `main`。 |
| **commit（提交）** | 一次存檔，附帶一句說明這次改了什麼。 |
| **push（推送）** | 把本機的 commit 上傳到 GitHub。 |
| **pull（拉取）** | 把 GitHub 上別人的最新變更下載到本機。 |
| **PR（Pull Request）** | 提議把某分支的變更合併進 `main`，可供他人審查。 |

---

## 1. 一次性設定（每台電腦只需做一次）

```bash
# 設定你的身分（會顯示在每個 commit 上）
git config --global user.name  "你的名字"
git config --global user.email "service@lycander.tw"

# 建議：讓 git 用 main 當預設分支名
git config --global init.defaultBranch main
```

### 安裝與登入

1. 安裝 [Git](https://git-scm.com/downloads)。
2. 建議安裝 [GitHub CLI](https://cli.github.com/)（`gh`），登入最方便：
   ```bash
   gh auth login
   ```
   依指示選 `GitHub.com` → `HTTPS` → 用瀏覽器登入即可。

> 沒有 `gh` 也可以，改用 HTTPS + [Personal Access Token](https://github.com/settings/tokens)
> 或 SSH 金鑰當密碼。

---

## 2. 取得專案

```bash
# 用 gh（推薦）
gh repo clone Lycander168/FrankAie-hub

# 或用一般 git
git clone https://github.com/Lycander168/FrankAie-hub.git

cd FrankAie-hub
```

---

## 3. 標準工作流程（每次改東西都照這套）

### 步驟 1：先同步最新的 main

```bash
git checkout main
git pull origin main
```

### 步驟 2：開一條新分支

分支命名建議：`類型/簡短描述`，例如 `feat/supply-chain-expert`、`docs/github-guide`、`fix/roster-typo`。

```bash
git checkout -b feat/你的功能名稱
```

### 步驟 3：修改檔案

依需求新增或編輯檔案（例如新增一位專家角色 skill，見第 6 節）。

### 步驟 4：檢視變更

```bash
git status          # 看哪些檔案被改了
git diff            # 看具體改了哪幾行
```

### 步驟 5：提交（commit）

```bash
git add .                              # 把所有變更加入這次提交
git commit -m "新增供應鏈專家 skill（v0.7.0）"
```

**好的 commit 訊息**：用一句話講清楚「做了什麼」，沿用本 repo 既有風格（中文、必要時附版號），例如：
- `新增 4 個原創工具型 skill（v0.3.0）`
- `團隊結構優化（v0.5.0）`
- `docs：新增 GitHub 操作指南`

### 步驟 6：推送到 GitHub

```bash
git push -u origin feat/你的功能名稱
```

> `-u` 只有第一次推送該分支需要；之後同分支直接 `git push` 即可。

### 步驟 7：開 Pull Request

```bash
# 用 gh（會在終端機互動式建立）
gh pr create --base main --title "新增供應鏈專家 skill" --body "說明這次變更內容"
```

或到 GitHub 網站，repo 頁面上會出現 **Compare & pull request** 按鈕，點下去填標題與說明即可。

### 步驟 8：合併

審查通過後，在 PR 頁面按 **Merge pull request**（或 `gh pr merge --squash`）。
合併後記得把本機切回 main 並更新：

```bash
git checkout main
git pull origin main
```

---

## 4. 常用指令速查表

| 想做的事 | 指令 |
|----------|------|
| 看目前狀態 | `git status` |
| 看改了哪幾行 | `git diff` |
| 看分支清單 | `git branch -a` |
| 切換分支 | `git checkout 分支名` |
| 開新分支並切過去 | `git checkout -b 分支名` |
| 加入暫存 | `git add 檔名`（或 `git add .` 全加） |
| 提交 | `git commit -m "訊息"` |
| 推送 | `git push`（首次加 `-u origin 分支名`） |
| 拉取最新 | `git pull origin main` |
| 看提交歷史 | `git log --oneline -10` |
| 丟棄某檔尚未提交的修改 | `git checkout -- 檔名` |
| 把剛加入暫存的取消 | `git restore --staged 檔名` |

---

## 5. 常見狀況排解

### 推送被拒絕（rejected / non-fast-forward）
遠端有你本機還沒有的提交。先拉取再推：
```bash
git pull origin 你的分支名 --rebase
git push
```

### 推送遇到網路錯誤
重試即可；若反覆失敗，間隔 2s → 4s → 8s → 16s 多試幾次。

### 合併衝突（merge conflict）
Git 會在衝突檔案中標記 `<<<<<<<`、`=======`、`>>>>>>>`。手動編輯保留正確內容、刪掉標記，然後：
```bash
git add 衝突檔名
git commit          # 或 git rebase --continue
```

### 不小心改錯、想回到乾淨狀態（尚未 commit）
```bash
git checkout -- .   # 丟棄所有未提交的變更（無法復原，請確認）
```

### 提交訊息打錯（尚未推送）
```bash
git commit --amend -m "正確的訊息"
```

---

## 6. 本專案專屬：更新 marketplace / 新增角色後

本 repo 是一個 Claude 外掛 marketplace。改完並合併進 `main` 後，使用者端要更新才看得到變更：

```
/plugin marketplace update frankaie-hub
```

新增一位專家角色的完整步驟：

1. 在 `plugins/frankaie-research-hub/skills/` 下新增資料夾，如 `supply-chain-expert/`。
2. 放入 `SKILL.md`，frontmatter 至少要有 `name` 與 `description`。
3. 依第 3 節流程 commit、push、開 PR、合併。
4. 提醒使用者執行上面的 `/plugin marketplace update`。

詳見 `plugins/frankaie-research-hub/README.md`。

---

## 7. 黃金守則

1. **永遠不要直接在 `main` 上開發** —— 一律開分支再 PR。
2. **每個 commit 訊息都要看得懂** —— 之後是你自己在查歷史。
3. **推送前先 `git status` 確認** —— 別把不該進版控的檔案（如 `.DS_Store`）加進去。
4. **小步快跑** —— 一個 PR 只做一件事，比較好審查也好回溯。

---

由 **LYCANDER GROUP** 維護 · 有問題請開 issue 或聯絡 service@lycander.tw
