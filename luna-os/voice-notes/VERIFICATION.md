# VERIFICATION.md — 語音紀錄功能專家驗證報告（v8.2 · LUNA Voice Notes）

驗證日期：2026-07-26 ｜ 驗證方式：召集 LYCANDER AI RESEARCH HUB skill 專家平行審查（比照 `hub-router` 派工、`quality-gate` 對抗性關卡、`validation-panel` 評分模式）＋ 實機自動化測試。

## 一、專家小組結論總覽

| 專家 | 角色 | 初審結論 | 條件處理後 |
|---|---|---|---|
| web-engineer | 前端/管線相容 | 有條件通過（1 高 2 中 4 低） | ✅ 條件已修 |
| security-engineer | 資安 | 有條件通過（3 條件 + 8 風險項） | ✅ 條件已修/已揭露 |
| product-manager | 產品/UX | 有條件通過（3 P0 + 6 P1 + 5 P2） | ✅ P0 全修，P1 大部分修，餘列未來增補 |
| quality-gate | 對抗性審查 | 對最新版覆核中（背景執行） | 見文末補記 |

## 二、發現 → 處置對照表

### 已修正（程式碼變更）

| 編號 | 發現 | 修法 |
|---|---|---|
| 前端 H1 | startRecording 重入競態：getUserMedia await 空窗連按 → 孤兒麥克風串流不釋放 | `startingRef` 守衛，錄音中/啟動中再按無效；實測同步連按 3 次 getUserMedia 僅呼叫 1 次 |
| 前端 M1 | SpeechRecognition onend 自動重啟無煞車 → 離線時無限重啟迴圈 | 致命錯誤旗標（network/not-allowed/service-not-allowed/audio-capture/language-not-supported）+ 500ms backoff + 實例比對 |
| 前端 M2 + PM P0-1 | 逐字稿存檔前不可編輯；手動輸入會被辨識結果覆蓋丟棄 | 停止後一律進入可編輯草稿（標題+內文 textarea），儲存以草稿為準 |
| PM P0-3 | Notion 同步失敗時前端誤報「未設定」 | 判讀 `notion_error`，三分流：已存入 Notion／同步失敗／尚未設定 |
| PM P1-1 | 未儲存草稿被「開始錄音」一鍵清空 | 有草稿時先 window.confirm |
| PM P1-3 | 標題不可改（固定時間戳） | 草稿標題欄可編輯，預填時間戳+前12字 |
| 資安 B | notion_url 未驗證即渲染 → anon 表可灌 `javascript:` URL 形成儲存型 XSS | `vnSafeNotionUrl()` 僅 `https://www.notion.so/`、`https://notion.so/` 開頭才渲染連結；E2E 實測惡意 URL 不渲染 |
| 資安 A | setup 模式常駐可被任何持 publishable key 者濫用建庫 | `SETUP_SECRET` 環境變數比對，不符回 403；文件補「設定完成即關通道」驗收項 |
| 資安 F | recorder/center 自由字串 → Notion select 選項污染/冒名亂值 | Edge Function 白名單驗證，非法值落 unknown/other |
| 資安 E | title 無伺服器端上限 | DB 寫入前 `slice(0, 200)`，與 Notion 端一致 |
| 資安 H | 錯誤訊息透傳洩漏內部資訊 | 對外泛化（"db error"/"setup failed"），詳細留 function logs |
| 資安 C（部分） | voice_notes 加入 realtime 擴大匿名訂閱洩漏面 | 移除 realtime publication（前端本就只用輪詢） |
| 前端 L1/L3 | 音檔 chunks 儲存後不釋放；停止瞬間 interim 文字丟失 | 停止即清 `chunksRef`；stop 時 interim 併入 final |
| 前端 L2 | loadNotes 失敗全靜默 | 補 console.warn |
| PM P0-2 | 整合指南建議掛 AI 中心（僅 L5 可見）→ 第一線帳號用不到 | 指南改為「總覽快速工具區（全帳號可見）」為主，明文警告勿只掛 AI 中心 |
| PM P1-2 | 退化模式讓使用者誤以為音檔有保存 | UI 常駐揭露「音檔本體不保存」；文件隱私節明列 |
| 資安 I / PM P1-5 | 轉錄經 Google 語音服務、7 帳號互見未揭露 | UI 底部常駐揭露 + INTEGRATION.md「隱私揭露」節 + SQL 註解標高敏感 |

### 已揭露（既有系統性風險，非本功能引入，文件明文標註）

- anon RLS 全開過渡方案（與 os_state/tasks 一致）：`voice_notes.sql` 註解 + INTEGRATION.md 標明「逐字稿高敏感，補 Auth 時第一批收緊（建議 recorder = auth.uid()）」。
- publishable key 內嵌前端（設計即如此，維護文件已載）。
- 無 Auth → recorder 可自報冒名：白名單擋亂值，歸責問題待 Auth。
- 主寫入路徑無速率限制（資安 D）：內部 7 人過渡期接受，文件建議開 Supabase 用量告警。
- deploy 時 verify_jwt 與新制 sb_publishable key 相容性：INTEGRATION.md 部署步驟提醒核對。

### 列入未來增補（PM P1-4／P2 系列，不擋上線）

「類型」欄位（會議/任務/客訴；資料庫 schema 已預留「待跟進」狀態）、音檔上傳 Storage、只看我的篩選、暫停鍵、Notion 顯示中文姓名、時長 mm:ss 顯示。

## 三、實測證據（本 session 實際執行）

| 測試 | 結果 |
|---|---|
| tsc 編譯（target ES2018 / jsx react，比照主檔管線） | ✅ 0 錯誤；產物無 `(0, React.useXXX)` 陷阱模式 |
| Edge Function TS 語法（transpileModule + parse diagnostics） | ✅ 0 錯誤 |
| Edge Function 邏輯單元測試（Node 模擬 Deno + Supabase/Notion 替身） | ✅ **14/14**：CORS preflight、405、壞 JSON、缺/超長 transcript、無 token 僅存 Supabase、有 token 建頁+回填 URL、長稿分批、setup 無/錯 secret 403、白名單 fallback、title 截斷、setup 建庫 payload、缺 parent 400 |
| headless Chromium E2E（fake mic + mock SpeechRecognition/fetch） | ✅ **12/12**：渲染、REST 清單、XSS 連結過濾（javascript: 不渲染/合法 notion.so 渲染）、同步連按重入守衛（getUserMedia=1 次）、即時逐字稿、可編輯草稿預填、標題/內文編輯後 payload 正確、成功訊息+連結、notion_error 警告分支、草稿保護 confirm、全程 0 JS error |
| repo CI `python3 scripts/check_skills.py` | ✅ exit 0（33 skills 全一致，本套件不影響 plugin 檢查範圍） |

## 四、【需查證】— 需實機/真實使用者驗證（本環境無法代測）

1. **Claude Artifact iframe**：麥克風 Permissions-Policy 與對 `*.supabase.co` 的 fetch 是否放行 — 需在實際 Artifact 頁各測一次 getUserMedia／webkitSpeechRecognition／fetch。被擋則此功能僅走本機安裝包路徑（127.0.0.1 為 secure context，可用）。
2. **真實 zh-TW 辨識率**：多人會議、口音、中英夾雜、品名術語的可用性 — 建議 2 個帳號試錄一週。
3. **公司網路可達 Google 語音服務**：防火牆/代理環境下 Web Speech 會 network error 退化 — 需在辦公室網路實測。
4. **長會議（30–60 分）** continuous 模式重啟漏字程度。
5. **資料政策**：客訴語音含客戶個資經 Google 轉錄 + 全帳號互見，是否符合公司內規。

## 五、部署狀態

- 程式碼/文件五檔已入庫（本資料夾）。
- 自動部署（Supabase MCP／Notion MCP 寫入）在本 session 被權限核准機制擋下 → 改交付手動路徑：`INTEGRATION.md` 四步驟（含既有已驗證管線指令 `supabase functions deploy luna-voice-note --use-api`）＋ `NOTION-DOC-v8.2.md` 可直接貼入維護文件。
- 待使用者一次性設定：`NOTION_TOKEN`（本人申請）、`SETUP_SECRET`、setup 建庫取得 `NOTION_VOICE_DB_ID`、前端模組併入主檔重編譯。

---
> 提醒：第四節所列項目屬環境限制無法在本 session 驗證，一律標【需查證】，絕不臆造實測結果。

## 六、quality-gate 補記

（對最新版程式碼的對抗性覆核完成後補上結論。）
