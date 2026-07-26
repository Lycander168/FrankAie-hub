# LUNA OS 語音紀錄整合指南（v8.2 · LUNA Voice Notes）

給工程師：把本資料夾的語音紀錄功能併入主檔 `lycander-os-nu-v5.jsx` 並部署後端。
全程比照《🛠 LUNA OS 工程師維護文件 v8.1》既有流程。
本套件已通過四位 skill 專家（web-engineer / security-engineer / product-manager / quality-gate）驗證，詳見 `VERIFICATION.md`。

## 架構

```
[使用者按 🎙 錄音]（OS 前端）
   │ MediaRecorder（getUserMedia，音檔僅錄音期間暫存，停止即棄）
   │ Web Speech API（webkitSpeechRecognition，zh-TW 即時逐字稿）
   ▼
[停止] → 可編輯草稿（標題 + 逐字稿皆可修改）
   │ 按「存入 Notion」 fetch POST（帶 publishable key）
   ▼
Supabase Edge Function: luna-voice-note
   ├─ 寫入 voice_notes 表（主要儲存，Notion 失敗不掉資料）
   └─ Notion API → 「🎙 LUNA 語音紀錄」資料庫建頁（逐字稿入內文）
   ▼
回傳 Notion 頁面 URL → 前端顯示「已存入 Notion ✅」
```

設計要點：
- 逐字稿用 Web Speech API：免金鑰免費，Chrome/Edge 支援 zh-TW；需連網（音訊經 Google 語音服務處理）。不支援時自動退化為「錄音 + 手動輸入重點」，UI 會明確揭露。
- 停止錄音後一律進入**可編輯草稿**：辨識錯字（人名/品名/金額）可在儲存前修正，標題可改。
- Notion 金鑰只存在 Edge Function 環境變數，前端永不可見。
- Notion 未設定或同步失敗時不擋流程：紀錄仍存 Supabase，前端訊息會區分「未設定」與「同步失敗」。

## 部署步驟（每步標註執行者）

### 步驟 1：建 voice_notes 表 ｜ 執行者：本人或 AI session
Supabase SQL Editor 執行 `sql/voice_notes.sql`（可重複執行）。

### 步驟 2：部署 Edge Function ｜ 執行者：工程師（本機終端機）
把 `supabase/functions/luna-voice-note/` 複製到 `~/luna-os-backend/supabase/functions/` 後：

```bash
supabase functions deploy luna-voice-note --use-api   # 一律加 --use-api 免 Docker
```

### 步驟 3：Notion 一次性設定 ｜ 執行者：本人（token 申請 AI 無法代辦）
1. 【本人】到 https://www.notion.so/profile/integrations 建立 internal integration（名稱例：`LUNA-OS`），取得 token（`ntn_` 開頭）。權限最小化：capabilities 只勾「Insert content」即可，不需勾 Read/Update user 資訊。
2. 【本人】到《LYCANDER GROUP — 系統總部》頁右上「…」→「Connect to」→ 選擇該 integration（比照 Lycander OS Sync 做法）。
3. 【本人或工程師】設定 Supabase secrets（SETUP_SECRET 自訂一組隨機字串，僅設定期間使用）：

```bash
supabase secrets set NOTION_TOKEN=ntn_xxxx SETUP_SECRET=<自訂隨機字串>
supabase functions deploy luna-voice-note --use-api   # secrets 變更後重佈生效
```

4. 【工程師】用 Function 內建 setup 模式一鍵建立「🎙 LUNA 語音紀錄」資料庫（parent 為系統總部頁 ID；需帶 setup_secret）：

```bash
curl -s -X POST "https://<project-ref>.supabase.co/functions/v1/luna-voice-note" \
  -H "Authorization: Bearer <publishable key>" -H "Content-Type: application/json" \
  -d '{"action":"setup","parent_page_id":"<系統總部頁ID>","setup_secret":"<步驟3自訂的字串>"}'
# 回傳 {"ok":true,"database_id":"...","url":"..."} → 記下 database_id
```

5. 【工程師】把回傳的 database_id 設進 secrets 並重新部署生效：

```bash
supabase secrets set NOTION_VOICE_DB_ID=<database_id>
supabase functions deploy luna-voice-note --use-api
```

6. 【工程師·資安建議】設定完成後，把 index.ts 內 setup 分支整段刪除再部署一次，或將 SETUP_SECRET 從 secrets 移除——一次性通道用完即關。

### 步驟 4：前端併入主檔 ｜ 執行者：工程師
1. 把 `VoiceNotesModule.jsx` 全部內容貼進 `lycander-os-nu-v5.jsx`（建議放在其他模組元件定義區，USERS 陣列之後、主 App 元件之前）。模組不 import，直接用全域 `React.useState` 等，與主檔管線相容。
2. 掛載位置：**建議掛「總覽」快速工具區（全帳號可見）**。⚠️ 不要只掛 AI 中心——AI 中心僅 L5 可見，sales/tina/ec 等第一線帳號（客訴記錄主要使用者）會完全用不到。

```jsx
<VoiceNotes
  user={currentUser}
  center={activeCenter || "other"}
  supabaseUrl={SB_URL}     /* 主檔既有 Supabase URL 常數（第 4347 行附近） */
  supabaseKey={SB_KEY}     /* 主檔既有 publishable key 常數 */
/>
```

3. 依維護文件第三節既有流程重新編譯：tsc → 清 CJS boilerplate → 嵌入 HTML shell → 重打包安裝包 → 記 Notion Changelog。
   - 注意 `(0, React.useXXX)` → `React.useXXX` 置換對本模組同樣適用。
   - tsc 會把中文 escape 成 uXXXX 屬正常，以編譯成功為準。

## 權限與安全

| 項目 | 做法 |
|---|---|
| Notion token | 僅存 Supabase Secrets，前端/版控不可見；capabilities 最小化（只 Insert content） |
| Notion 權限範圍 | integration 只 Connect 系統總部頁（含語音紀錄資料庫），不給整個 workspace |
| setup 模式 | 需 SETUP_SECRET 相符（403 否則拒絕）；設定完成後建議刪除分支或移除 secret |
| recorder/center | Edge Function 白名單驗證，非法值落 unknown/other（防 Notion select 選項污染與冒名亂值） |
| voice_notes RLS | 過渡方案 anon 全開（與現有 os_state/tasks 一致）；逐字稿屬高敏感，補 Auth 時第一批收緊；不加入 realtime publication |
| notion_url 渲染 | 前端驗證 https://www.notion.so/ 開頭才顯示連結（防儲存型 XSS） |
| payload 驗證 | 型別驗證、逐字稿上限 60,000 字、標題上限 200 字、錯誤訊息對外泛化 |
| 麥克風 | 按「開始錄音」才取用，停止即釋放；連按有重入守衛，不會產生孤兒麥克風佔用 |

## 隱私揭露（請讓全員知悉，UI 亦有註記）

1. 即時轉錄的音訊會送 **Google 語音服務**處理（Web Speech API 機制）——含客戶個資或機密的內容請斟酌使用。
2. 現行 anon 過渡模式下，**7 個帳號可互見全部語音紀錄**（含逐字稿）。
3. **音檔本體不保存**：只留文字。若有「客訴需原始錄音佐證」需求，屬未來增補項。

## 已知限制

- 即時轉錄需 Chrome/Edge + 連網；Safari/Firefox、離線、或企業防火牆擋 Google 語音服務時，自動退化為手動輸入模式（UI 有提示）。
- 桌面版本機 server（http://127.0.0.1）與 https 環境皆為 secure context，麥克風可用；直接開 file:// 不行。
- 【需查證】Claude Artifact iframe 環境的麥克風權限（Permissions-Policy）與對 *.supabase.co 的 fetch 是否放行——需實機各測一次；若被擋，此功能僅走本機安裝包路徑。
- Notion API 單次建頁最多 100 blocks；長逐字稿由 Function 自動分批 append。

## 未來增補（不擋本次上線）

- 「類型」欄位（會議/任務/客訴）＋ 狀態動線（資料庫 schema 已含「待跟進」選項）
- 音檔上傳 Supabase Storage + Notion 附連結（客訴佐證需求）
- 「只看我的」篩選、錄音暫停鍵、Notion 端顯示中文姓名
- Supabase Auth 上線後：voice_notes RLS 收緊為本人可寫、依等級可讀

## 驗收清單

- [ ] `sql/voice_notes.sql` 執行成功，voice_notes 表存在
- [ ] `luna-voice-note` 部署成功（`supabase functions list` 可見）
- [ ] setup 模式（帶 setup_secret）建立「🎙 LUNA 語音紀錄」資料庫成功，NOTION_VOICE_DB_ID 已設
- [ ] curl 測試 POST 一筆假資料 → 回傳 ok:true 且 notion_url 非空
- [ ] Notion 資料庫出現該筆紀錄（屬性 + 逐字稿內文）
- [ ] OS 前端錄音 → 停止 → 草稿可編輯 → 存入 Notion → 顯示「已存入 Notion ✅」
- [ ] 近期紀錄列表出現新紀錄，Notion ↗ 連結可開
- [ ] setup 通道已關閉（刪分支重佈或移除 SETUP_SECRET）
