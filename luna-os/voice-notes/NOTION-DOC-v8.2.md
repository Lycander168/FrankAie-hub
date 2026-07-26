# 貼入 Notion 用 — 維護文件 v8.2 新章節

> 本檔為《🛠 LUNA OS 工程師維護文件》的更新內容。
> 若 AI session 具 Notion 寫入權限會自動追加；否則請把下方內容貼到該文件「第二部分 未來功能更新」章節後，並把標題版本改為 v8.2。

---

## 二八、v8.2 語音紀錄功能（LUNA Voice Notes）

**功能**：OS 內錄音 → 即時逐字稿（zh-TW）→ 停止後可編輯草稿（標題/內容可修）→ 自動存入 Supabase + Notion「🎙 LUNA 語音紀錄」資料庫。

**架構**

```
OS 前端 VoiceNotes 模組
  MediaRecorder（錄音）+ Web Speech API（即時逐字稿 zh-TW）
        ↓ 停止 → 可編輯草稿 → fetch POST（publishable key）
Edge Function: luna-voice-note
  ├─ 寫 voice_notes 表（主要儲存，Notion 失敗不掉資料）
  └─ Notion API 建頁（逐字稿入內文，長稿自動分批 append）
        ↓
回傳 Notion 頁 URL → 前端顯示「已存入 Notion ✅」
```

**程式碼位置**：GitHub `Lycander168/FrankAie-hub` → `luna-os/voice-notes/`
（`VoiceNotesModule.jsx` 前端模組、`supabase/functions/luna-voice-note/index.ts`、`sql/voice_notes.sql`、`INTEGRATION.md` 完整部署指南、`VERIFICATION.md` 四位 skill 專家驗證報告）

**資料表**：`voice_notes`（title/transcript/duration_sec/recorder/center/recorded_at/notion_page_id/notion_url）＋ anon policy（過渡，與 os_state 一致）。不加入 realtime（前端輪詢即可，降低匿名訂閱洩漏面）。⚠️ 逐字稿屬高敏感資料，補 Auth 時本表第一批收緊。

**環境變數（Supabase Secrets）**
| 變數 | 說明 |
|---|---|
| NOTION_TOKEN | Notion internal integration token（本人於 notion.so/profile/integrations 建立；capabilities 只勾 Insert content；integration 需 Connect 系統總部頁） |
| NOTION_VOICE_DB_ID | 「🎙 LUNA 語音紀錄」database ID（用 Function 的 setup 模式一鍵建庫取得） |
| SETUP_SECRET | setup 模式通行碼（自訂隨機字串；一次性設定完成後建議移除並刪 setup 分支） |

**部署四步**：① SQL Editor 跑 `voice_notes.sql` ② `supabase functions deploy luna-voice-note --use-api` ③ 設 secrets → setup 模式建庫（POST `{"action":"setup","parent_page_id":"<系統總部頁ID>","setup_secret":"..."}`）→ 設 NOTION_VOICE_DB_ID 重佈 ④ 前端模組貼入主檔 `lycander-os-nu-v5.jsx`，掛「總覽」快速工具區（全帳號可見，勿只掛 L5-only 的 AI 中心），照第三節流程重編譯打包。

**安全設計**：Notion token 只在 Secrets；setup 需通行碼；recorder/center 白名單防污染；notion_url 前端驗證來源才渲染；錯誤訊息對外泛化；麥克風按錄才取用、停止即釋放、連按有重入守衛。

**隱私揭露（全員須知，UI 有註記）**：① 即時轉錄音訊經 Google 語音服務處理 ② 現行 anon 模式 7 帳號互見全部紀錄 ③ 音檔本體不保存（只留文字）。

**已知限制**
- 即時轉錄需 Chrome/Edge + 連網；不支援時退化為錄音＋手動輸入（UI 有提示）。
- 麥克風需 secure context（https 或 localhost，本機安裝包 127.0.0.1 可用）。
- 【需查證】Claude Artifact iframe 的麥克風權限與 Supabase fetch 放行需實機驗證；被擋則僅走本機安裝包路徑。
- NOTION_TOKEN 未設或同步失敗時紀錄僅存 Supabase，不擋流程；前端訊息會區分兩種情況。

**未來增補**：類型欄位（會議/任務/客訴）、音檔上傳 Storage、只看我的、暫停鍵、Auth 後 RLS 收緊。
