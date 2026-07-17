# 如何讓 Claude Code 連結 GitHub（設定操作指南）

> 這份文件教你**把 Claude Code 連上 GitHub**：授權、選 repo、建環境、送出第一個任務，以及常見問題排除。
> 適合直接轉給團隊或任何要開始用 Claude Code 的人。
> 內容依 [Claude Code 官方文件](https://code.claude.com/docs/en/web-quickstart) 整理。

---

## 0. 先搞懂：有兩種連法

Claude Code 的雲端 session 需要存取你的 GitHub repo（clone 程式碼、push 分支）。連接 GitHub 有**兩種**方式，擇一即可：

| 方法 | 怎麼運作 | 適合誰 |
|---|---|---|
| **A. GitHub App（瀏覽器）** | 在網頁 onboarding 時授權 Claude GitHub App | 用瀏覽器上手、想要「自動修 PR」的團隊 |
| **B. `/web-setup`（終端機）** | 在 Claude Code CLI 跑 `/web-setup`，把本機 `gh` 的 token 同步到 Claude 帳號 | 已經在用 `gh` CLI 的個人開發者 |

> **重點**：不論用哪種，雲端 session 都能存取「連接的 GitHub 帳號看得到的所有 repo」，不限於安裝了 App 的那些。安裝 App 的作用是**開啟 PR webhook（自動修 PR 需要它）**，它不是 repo 層級的存取控制。要限制能碰哪些 repo，請直接在 GitHub 上限制帳號的 team／repo 權限。

---

## 方法 A：用瀏覽器連（GitHub App）

一次性設定，跟著四步走：

### 步驟 1 — 登入
前往 **[claude.ai/code](https://claude.ai/code)**，用你的 Anthropic 帳號登入。

### 步驟 2 — 安裝 Claude GitHub App
登入後頁面會提示你連接 GitHub。依提示**安裝 Claude GitHub App** 並授權它存取你的 repo。
> 雲端 session 只能用「既有的」GitHub repo。要開新專案，請先到 [github.com/new](https://github.com/new) 建一個空 repo。

### 步驟 3 — 建立雲端環境（Environment）
連上 GitHub 後會要你建一個雲端環境。環境決定 session 有多少網路權限、以及開 session 前要跑什麼。表單欄位：

- **Name**：顯示名稱（多專案時好辨識）。
- **Network access**：session 能連的網路。預設 `Trusted`＝允許 npm／PyPI／RubyGems 等常見套件源，但擋一般網路。
- **Environment variables**：`.env` 格式的變數，每行一個 `KEY=value`（**值不要加引號**，引號會被當成值的一部分）。凡能編輯此環境的人都看得到，**別放機密**。
- **Setup script**：session 啟動前跑的 Bash 腳本，用來裝 VM 沒內建的工具（例如 `apt install -y gh`）。結果會被快取，不會每次重跑。

第一次用**保留預設**即可，按 **Create environment**。之後隨時能改或多開幾個環境。

### 步驟 4 — 完成
連接完成，可以送任務了（見下方[「送出第一個任務」](#送出第一個任務)）。

---

## 方法 B：用終端機連（`/web-setup`）

已經在用 GitHub CLI（`gh`）的人，不用開瀏覽器。需要先裝好 [Claude Code CLI](https://code.claude.com/docs/en/quickstart)。

```text
# 1. 先讓 gh 登入（若還沒登入）
gh auth login

# 2. 啟動 Claude Code CLI，登入 claude.ai 帳號（若還沒登入）
claude
/login

# 3. 在 Claude Code CLI 內執行
/web-setup
```

`/web-setup` 會把 `gh` 的 token 同步到你的 Claude 帳號；若你還沒有雲端環境，它會自動建一個（Trusted 網路、無 setup script）。完成後就能用 `--cloud` 從終端機開雲端 session，或用 `/schedule` 排程任務。

> **注意**
> - `/web-setup` 是在 **Claude Code CLI 裡**打，不是在 shell 裡。先跑 `claude` 再輸入。
> - 若指令顯示「No commands match」或「Unknown command」，通常是你用 API key／第三方 provider 登入而非 claude.ai 訂閱 —— 跑 `/login` 用 claude.ai 帳號登入即可。
> - 開了 **Zero Data Retention** 的組織無法使用 `/web-setup` 與雲端功能。

---

## 送出第一個任務

GitHub 連好、環境建好後：

1. **選 repo 與分支** — 在 [claude.ai/code](https://claude.ai/code)（或手機 App 的 Code 分頁）點輸入框下方的 repo 選擇器，選要動的 repo。每個 repo 旁有分支選擇器，可從 feature 分支開始。可加多個 repo 一起工作。
2. **選權限模式** — 輸入框旁的下拉預設 **Accept edits**（Claude 直接改並 push 分支）。想先看方案再動手就切 **Plan**。雲端不提供 Manual／Bypass。
3. **描述任務並送出** — 講清楚要什麼再按 Enter。越具體越好：
   - 指名檔案／函式：「在 `tests/test_auth.py` 修好失敗的 auth 測試」勝過「修測試」。
   - 有錯誤訊息就貼上。
   - 描述期望行為，而非只講症狀。

Claude 會 clone repo、跑 setup script、開始工作。每個任務有獨立 session 和分支，不用等前一個做完。

---

## 審查、開 PR、持續迭代

1. **看 diff** — 畫面上有 `+42 -18` 這種增減指標，點開就是 diff 檢視（左邊檔案清單、右邊變更）。
2. **行內留言** — 在 diff 上選某一行、輸入意見按 Enter，留言會跟你下一則訊息一起送給 Claude，它會知道「在 `src/auth.ts:47` 別 catch 這個錯」。
3. **開 PR** — diff 檢視上方按 **Create PR**，可開正式 PR、草稿，或跳到 GitHub compose 頁（帶自動產生的標題與說明）。
4. **PR 後繼續** — session 不會關。把 CI 失敗訊息或 reviewer 留言貼進聊天請 Claude 處理；或用下方的自動修 PR。

---

## 自動修 PR（Auto-fix，需 GitHub App）

裝了 Claude GitHub App 後，可讓 Claude **自動盯 PR**：CI 失敗或有 review 留言時，事件會透過 webhook 進來，Claude 自動診斷、修好、push。

- **啟用前提**：GitHub App 必須裝在該 repo 上（webhook 靠它）。用 `/web-setup` 連的人若想要 Auto-fix，要另外把 App 裝到那些 repo。
- **怎麼用**：直接請 Claude「watch / 監看 PR #N，CI 失敗就自動修」。它會訂閱後等事件，不會空轉輪詢。
- **終止**：PR 被 merge／close，或你說「停」即結束。

---

## 管理 repo 存取權（GitHub 端）

要調整 Claude GitHub App 能碰哪些 repo：

1. 到 **github.com** → 個人或組織 **Settings** → **Applications** → 找到 **Claude** → **Configure**。
2. 在 **Repository access** 選「所有 repo」或「指定 repo」。
3. 私有 repo 需要跟公開 repo 一樣的授權。

> 組織若由管理員控管：Team／Enterprise 的 Owner 可在 [claude.ai/admin-settings/claude-code](https://claude.ai/admin-settings/claude-code) 開關「Quick web setup」等設定。

---

## 常見問題排除

| 症狀 | 原因 / 解法 |
|---|---|
| **連了 GitHub 卻看不到 repo** | 雲端 session 用的是「連接帳號看得到的 repo」。先確認該 GitHub 帳號在 GitHub 上真的有權限。想要 Auto-fix 就到 **Settings → Applications → Claude → Configure** 確認 repo 有列在 Repository access。 |
| **頁面只顯示一顆 GitHub 登入鈕** | 雲端 session 需要已連接的 GitHub 帳號。走瀏覽器流程或跑 `/web-setup`。完全不想連 GitHub，可改用 Remote Control 在自己機器跑。 |
| **「Not available for the selected organization」** | Enterprise 組織可能需要 Owner 先啟用 Claude Code on the web，聯絡你們的 Anthropic 窗口。 |
| **`/web-setup` 顯示 No commands / Unknown command** | 要在 `claude` CLI 內打，不是 shell。且需用 claude.ai 帳號登入（`/login`），API key 登入會隱藏此指令。 |
| **「Could not create a cloud environment」** | 自動建環境失敗。手動跑 `/web-setup` 建一個，或到 claude.ai/code 走「Create your environment」。 |
| **Setup script 失敗擋住 session** | 常見於套件源不在網路權限內（`Trusted` 涵蓋多數套件源，`None` 全擋）、腳本引用了不存在的路徑、或指令在 Ubuntu 上寫法不同。腳本開頭加 `set -x` 看哪行掛掉；非關鍵指令加 `|| true`。 |
| **關掉分頁 session 還在跑** | 這是設計如此。session 會在背景跑到任務完成再閒置。可在側欄 archive 或 delete。 |

---

## 名詞速查

- **雲端 session**：跑在 Anthropic 管理的 VM，每次啟動都重新 clone 你的 repo。
- **Environment（環境）**：控制網路權限、環境變數、setup script 的設定組合，可個人或組織共用。
- **GitHub App**：授權 Claude 存取 GitHub 的官方 App；同時提供 PR webhook 給 Auto-fix。
- **`/web-setup`**：把本機 `gh` token 同步到 Claude 帳號的終端機指令。
- **Trusted 網路**：預設網路等級，放行常見套件源、擋一般網路。

---

## 延伸閱讀（官方文件）

- 快速上手：<https://code.claude.com/docs/en/web-quickstart>
- 完整參考（環境／網路／setup script／teleport）：<https://code.claude.com/docs/en/claude-code-on-the-web>
- 排程與 GitHub 事件觸發（Routines）：<https://code.claude.com/docs/en/routines>
- 終端機 CLI 快速上手：<https://code.claude.com/docs/en/quickstart>

---

_整理：LYCANDER GROUP · 依 Claude Code 官方文件（2026 研究預覽版）撰寫，實際介面以官方最新為準。_
