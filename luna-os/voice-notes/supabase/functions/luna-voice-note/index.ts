// LUNA OS — luna-voice-note Edge Function（v8.2 · 語音紀錄）
// ----------------------------------------------------------
// 職責：
//   POST {title, transcript, duration_sec, recorder, center, recorded_at}
//     1) 寫入 Supabase voice_notes 表
//     2) 呼叫 Notion API 在「🎙 LUNA 語音紀錄」資料庫建頁（逐字稿寫入內文）
//     3) 回傳 {ok, id, notion_url}
//   POST {action:"setup", parent_page_id, setup_secret}
//     一次性：在指定 Notion 頁下建立「🎙 LUNA 語音紀錄」資料庫，
//     回傳 database_id（供設定 NOTION_VOICE_DB_ID）。
//     需 setup_secret 與 SETUP_SECRET 環境變數相符（防持 publishable key
//     者濫用）；設定完成後建議刪除本分支重新部署。
//
// 環境變數（Supabase Secrets，不進版控）：
//   NOTION_TOKEN         Notion internal integration token（選配；未設則僅存 Supabase）
//   NOTION_VOICE_DB_ID   「🎙 LUNA 語音紀錄」database ID
//   SETUP_SECRET         setup 模式通行碼（僅一次性設定期間需要）
//   SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY  平台自動注入
//
// 部署（比照維護文件第三節既有管線，一律加 --use-api 免 Docker）：
//   supabase functions deploy luna-voice-note --use-api

import { createClient } from "jsr:@supabase/supabase-js@2";

const sb = createClient(
  Deno.env.get("SUPABASE_URL")!,
  Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!,
);

const NOTION_TOKEN = Deno.env.get("NOTION_TOKEN") || "";
const NOTION_DB_ID = Deno.env.get("NOTION_VOICE_DB_ID") || "";
const SETUP_SECRET = Deno.env.get("SETUP_SECRET") || "";
const NOTION_VERSION = "2022-06-28";

const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};

const MAX_TRANSCRIPT = 60000; // 與前端一致
const MAX_TITLE = 200;

// recorder / center 白名單（與 OS USERS/中心一致；防冒名亂值污染 Notion select 選項）
const RECORDERS: [string, string][] = [
  ["service", "blue"], ["frankie", "green"], ["aaron", "red"],
  ["maggie", "orange"], ["sales", "yellow"], ["tina", "purple"], ["ec", "pink"],
  ["unknown", "default"],
];
const CENTERS: [string, string][] = [
  ["ops", "blue"], ["mkt", "yellow"], ["vis", "purple"], ["proc", "orange"],
  ["wh", "brown"], ["ec", "green"], ["ai", "gray"], ["other", "default"],
];
const RECORDER_SET = new Set(RECORDERS.map(([n]) => n));
const CENTER_SET = new Set(CENTERS.map(([n]) => n));

function json(body: unknown, status = 200): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json", ...CORS },
  });
}

async function notionRequest(method: string, path: string, payload: unknown): Promise<any> {
  const r = await fetch("https://api.notion.com/v1" + path, {
    method,
    headers: {
      Authorization: `Bearer ${NOTION_TOKEN}`,
      "Notion-Version": NOTION_VERSION,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });
  const data = await r.json();
  if (!r.ok) {
    // 詳細錯誤只進 function logs，不透傳給呼叫端
    console.error("Notion API error", r.status, data?.message);
    throw new Error(`notion ${r.status}`);
  }
  return data;
}

// 逐字稿 → Notion paragraph blocks（單一 rich_text 上限 2000 字；每次 append 上限 100 blocks）
function transcriptToBlocks(transcript: string): any[] {
  const blocks: any[] = [];
  for (let i = 0; i < transcript.length; i += 1800) {
    blocks.push({
      object: "block",
      type: "paragraph",
      paragraph: {
        rich_text: [{ type: "text", text: { content: transcript.slice(i, i + 1800) } }],
      },
    });
  }
  return blocks;
}

async function createNotionPage(note: {
  title: string;
  transcript: string;
  duration_sec: number;
  recorder: string;
  center: string;
  recorded_at: string;
}): Promise<{ page_id: string; url: string }> {
  const blocks = transcriptToBlocks(note.transcript);
  const page = await notionRequest("POST", "/pages", {
    parent: { database_id: NOTION_DB_ID },
    icon: { type: "emoji", emoji: "🎙" },
    properties: {
      "標題": { title: [{ text: { content: note.title } }] },
      "日期": { date: { start: note.recorded_at } },
      "錄音者": { select: { name: note.recorder } },
      "中心": { select: { name: note.center } },
      "時長秒數": { number: note.duration_sec },
      "狀態": { select: { name: "新增" } },
    },
    children: blocks.slice(0, 90),
  });
  // 超過 90 blocks 的長逐字稿分批 append（60000 字上限下最多 34 blocks，此為防禦性保留）
  for (let i = 90; i < blocks.length; i += 90) {
    await notionRequest("PATCH", `/blocks/${page.id}/children`, { children: blocks.slice(i, i + 90) });
  }
  return { page_id: page.id, url: page.url };
}

// 一次性 setup：在指定頁下建立語音紀錄資料庫
async function setupDatabase(parentPageId: string): Promise<any> {
  const sel = (opts: [string, string][]) => ({
    select: { options: opts.map(([name, color]) => ({ name, color })) },
  });
  const db = await notionRequest("POST", "/databases", {
    parent: { type: "page_id", page_id: parentPageId },
    icon: { type: "emoji", emoji: "🎙" },
    title: [{ type: "text", text: { content: "🎙 LUNA 語音紀錄" } }],
    properties: {
      "標題": { title: {} },
      "日期": { date: {} },
      "錄音者": sel(RECORDERS),
      "中心": sel(CENTERS),
      "時長秒數": { number: { format: "number" } },
      "狀態": sel([["新增", "blue"], ["已整理", "green"], ["待跟進", "red"]]),
    },
  });
  return { database_id: db.id, url: db.url };
}

Deno.serve(async (req: Request) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: CORS });
  if (req.method !== "POST") return json({ ok: false, error: "POST only" }, 405);

  let body: any;
  try {
    body = await req.json();
  } catch {
    return json({ ok: false, error: "invalid JSON" }, 400);
  }

  // ---- 一次性 setup 模式（需 SETUP_SECRET 相符）----
  if (body?.action === "setup") {
    if (!SETUP_SECRET || body.setup_secret !== SETUP_SECRET) {
      return json({ ok: false, error: "forbidden" }, 403);
    }
    if (!NOTION_TOKEN) return json({ ok: false, error: "NOTION_TOKEN not set" }, 500);
    if (typeof body.parent_page_id !== "string" || !body.parent_page_id) {
      return json({ ok: false, error: "parent_page_id required" }, 400);
    }
    try {
      const result = await setupDatabase(body.parent_page_id.replace(/-/g, ""));
      return json({ ok: true, ...result });
    } catch (e) {
      console.error("setup failed", e);
      return json({ ok: false, error: "setup failed (see function logs)" }, 500);
    }
  }

  // ---- 一般語音紀錄寫入 ----
  const title = typeof body?.title === "string" ? body.title.trim().slice(0, MAX_TITLE) : "";
  const transcript = typeof body?.transcript === "string" ? body.transcript.trim() : "";
  const duration = Number.isFinite(body?.duration_sec) ? Math.max(0, Math.floor(body.duration_sec)) : 0;
  const rawRecorder = typeof body?.recorder === "string" ? body.recorder.trim().toLowerCase() : "";
  const rawCenter = typeof body?.center === "string" ? body.center.trim().toLowerCase() : "";
  const recorder = RECORDER_SET.has(rawRecorder) ? rawRecorder : "unknown";
  const center = CENTER_SET.has(rawCenter) ? rawCenter : "other";
  const recordedAt =
    typeof body?.recorded_at === "string" && !isNaN(Date.parse(body.recorded_at))
      ? body.recorded_at
      : new Date().toISOString();

  if (!transcript) return json({ ok: false, error: "transcript required" }, 400);
  if (transcript.length > MAX_TRANSCRIPT) return json({ ok: false, error: "transcript too long" }, 400);

  const note = {
    title: title || recordedAt.slice(0, 16).replace("T", " ") + "・語音紀錄",
    transcript,
    duration_sec: duration,
    recorder,
    center,
    recorded_at: recordedAt,
  };

  // 1) 寫入 Supabase（主要儲存，Notion 失敗也不掉資料）
  const { data: row, error: dbErr } = await sb
    .from("voice_notes")
    .insert({
      title: note.title,
      transcript: note.transcript,
      duration_sec: note.duration_sec,
      recorder: note.recorder,
      center: note.center,
      recorded_at: note.recorded_at,
    })
    .select("id")
    .single();
  if (dbErr) {
    console.error("db insert failed", dbErr.message);
    return json({ ok: false, error: "db error (see function logs)" }, 500);
  }

  // 2) 寫入 Notion（未設定 token/DB 則略過，僅存 Supabase）
  let notionUrl: string | null = null;
  let notionErr: string | null = null;
  if (NOTION_TOKEN && NOTION_DB_ID) {
    try {
      const page = await createNotionPage(note);
      notionUrl = page.url;
      await sb
        .from("voice_notes")
        .update({ notion_page_id: page.page_id, notion_url: page.url })
        .eq("id", row.id);
    } catch (e) {
      console.error("notion sync failed", e);
      notionErr = "notion sync failed";
    }
  }

  return json({ ok: true, id: row.id, notion_url: notionUrl, notion_error: notionErr });
});
