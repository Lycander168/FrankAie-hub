---
name: drive-md-to-gdoc
description: >
  LYCANDER AI RESEARCH HUB — Google 雲端硬碟 Markdown 轉 Google Doc（工具型 skill · 手機可讀解法）。
  當使用者提到「手機看不到 md」、「手機打不開報告」、「Drive 預覽不了」、「手機在雲端硬碟看不到內容」、
  「md 轉 Google 文件」、「把報告轉成 Google Doc」、「轉檔給手機看」、「手機可讀報告」、
  「report 在手機打不開」、「行動版 Drive 看不到 markdown」時觸發。
  把 Drive 上的 .md 報告轉成「手機原生可讀」的 Google Doc，回傳可在手機開啟的連結。
---

# Google 雲端硬碟 Markdown 轉 Google Doc（Drive MD → Google Doc）

這是一個**工具型 skill**，專門解一個痛點：**Google Drive 行動版 App 不渲染 `text/markdown`**——
在手機點開 `.md` 只會看到通用檔案圖示、完全沒有內容預覽（桌面瀏覽器對 `.md` 也一樣）。HUB 每天
產出的 `.md` 報告因此在手機上「看得到檔名、看不到內容」。

**解法**：把 `.md` 轉成 **Google Doc**（`application/vnd.google-apps.document`）。Google Doc 在
Drive 手機 App 可**原生開啟並渲染**標題 / 表格 / 粗體 / 清單，且可編輯、可搜尋、可留言——這正是
使用者要的「直接在手機上的 Drive 看報告內容」。

> 原則：只轉格式、不改內容。每筆轉換都附「來源 .md 檔名＋連結」與「新 Google Doc 連結」，
> 取不到或空檔（size 0）明確標註，不腦補。

---

## 何時用

- 在手機 / 平板上想看雲端硬碟的每日報告，但 `.md` 打不開、沒預覽
- 要把某類型（客服 / 營運 / 競品…）或某段日期的報告整批轉成手機可讀
- 要把一份報告轉給同事在手機上快速讀 / 留言

> 想「在對話裡瀏覽 / 彙整」報告 → 用 `drive-md-browser`；想「在手機 Drive 直接看」→ 用本 skill。

## 需要的輸入（缺哪項就問或用預設）

1. **範圍**：哪一份 / 某類型 / 某日期 / 某資料夾？預設「使用者指名那份」或「某類型最新一份」。
2. **放哪裡**：預設集中到專屬資料夾「📱 手機可讀報告（Google Doc）」；或指定放回原資料夾。
3. **批次量**：預設只轉「最新版次」，避免同日多版（v1…v11）灌爆。

## 運作流程（用 Google Drive 工具）

1. **定位**：用 `search_files` 找目標 `.md`（沿用 `drive-md-browser` 查詢語法）。例：
   `title contains '客服監控報告' and mimeType = 'text/markdown'`，依 `modifiedTime` 取最新。
2. **備妥目標資料夾**：先 `search_files` 找「📱 手機可讀報告（Google Doc）」資料夾；不存在則用
   `create_file`（`contentMimeType = application/vnd.google-apps.folder`）建立一次，記下其 `id`。
3. **取原始 markdown**：用 `download_file_content(fileId)` 取回 `content`（base64）。
   （不要用 `read_file_content`——它會重排 / 跳脫 markdown 符號；base64 最忠實。）
4. **建立 Google Doc**：用 `create_file`：
   - `base64Content = <步驟 3 取回的 base64>`（原樣傳入，勿手動解碼以免截斷）
   - `contentMimeType = "text/markdown"`，保留 `disableConversionToGoogleType` 預設 false
     → 轉成 `application/vnd.google-apps.document`（**已實測**：回傳 mimeType 為 Google Doc，
     Google Docs 會把 markdown 渲染成真正的標題 / 表格 / 粗體 / 清單）。
   - `title = <原檔名去掉 .md>`（例：`客服監控報告_2026-06-19_v3`）。
   - `parentId = <目標資料夾 id>`。
5. **回傳**：新 Doc 的 `viewUrl`，請使用者在手機 Drive App / Google 文件 App 開啟確認。

## 冪等 / 避免重複

轉檔前先在目標資料夾 `search_files` 查是否已有同名 Google Doc：
- 已存在 → 預設**略過並回報**（附既有 Doc 連結），除非使用者要求覆蓋。
- 覆蓋 → 刪舊建新（或建新版並在標題標註）；刪除前先確認，不誤刪非本流程產物。

## 批次模式

- 「某類型最新一份」：找該類型 → 取 `modifiedTime` 最新一份 → 轉。
- 「某日期區間全部」：`modifiedTime` 區間過濾 → 預設每日只取最新版次 → 逐檔轉。
- 大量轉換時，逐檔回報來源→產出，最後給彙總對照表。

---

## 輸出範本

### A. 單檔轉換結果

```
# 轉檔完成（手機可讀）| <日期>

| 來源 .md | 新 Google Doc（手機可開）| 狀態 |
|----------|--------------------------|------|
| 客服監控報告_2026-06-19_v3.md <來源連結> | <Doc viewUrl> | ✅ 已轉換 |

📱 在手機開啟上面 Google Doc 連結即可看到完整內容（標題/表格/粗體皆渲染）。
提示：把「📱 手機可讀報告（Google Doc）」資料夾加星號，手機一站瀏覽。
```

### B. 批次轉換對照表

```
# 批次轉檔 | <類型/日期區間>｜共 N 份｜<日期>

| # | 來源 .md | 新 Google Doc | 狀態 |
|---|----------|----------------|------|
| 1 | <檔名> <連結> | <Doc 連結> | ✅ 已轉換 / ⏭️ 已存在略過 / ⚠️ 空檔 |

集中位置：📱 手機可讀報告（Google Doc）資料夾 <資料夾連結>
```

---

## 實例演練（Worked Example）

**輸入**：「我手機打不開那份產品開發進度追蹤報告，幫我弄成手機看得到的。」

**步驟**：
1. `search_files`：`title contains '產品開發進度追蹤報告' and mimeType = 'text/markdown'` → 取最新一份。
2. 確認 / 建立「📱 手機可讀報告（Google Doc）」資料夾。
3. `download_file_content(fileId)` → 取 base64。
4. `create_file`（`base64Content` + `contentMimeType='text/markdown'` + `parentId=資料夾`）
   → 回傳 `mimeType: application/vnd.google-apps.document` ＋ `viewUrl`。
5. 用範本 A 回覆，附 Doc 連結，請使用者在手機開啟確認標題 / 表格渲染。

> 實測佐證：以 markdown（含 H1/H2、表格、清單）建立 Doc，`create_file` 回傳
> `application/vnd.google-apps.document` —— 確認可轉成手機原生可讀的 Google Doc。

## 與團隊串接

- **互補**：`drive-md-browser`（在對話瀏覽 / 彙整）↔ 本 skill（在手機 Drive 原生閱讀）。
- **報告類型 → 團隊**：沿用 `drive-md-browser` 的對照表（客服→`cx-team`、營運→`operations-team`…）。
- **下游**：轉好的 Doc 可直接在手機分享 / 留言給對應團隊。

## 限制與備援

- Google Docs 的 markdown 匯入對**極複雜巢狀表格**渲染可能不完美；若遇到，退用
  `text/plain`→Doc（可讀但保留 `#`/`|` 原始符號），或改輸出 PDF 為備選。
- 本 skill 只做「轉格式供手機閱讀」，不改寫內容、不產生新報告。

> 附註（不在本 skill 範圍）：若要從源頭免轉檔，建議產報告的排程任務日後直接「同時輸出一份
> Google Doc」；本 skill 仍可處理既有 / 歷史 `.md`。
