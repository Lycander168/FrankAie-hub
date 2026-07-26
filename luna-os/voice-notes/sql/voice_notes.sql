-- LUNA OS — voice_notes 建表 SQL（v8.2 · 語音紀錄）
-- 於 Supabase SQL Editor 執行；含 if not exists，可重複執行。
-- 比照現有 os_state / tasks 過渡模式：anon 讀寫。
-- ⚠️ anon 全開為「內部桌面版」過渡方案（同維護文件 RLS 現況）。
-- ⚠️ 語音逐字稿屬高敏感資料：日後補 Auth 時本表應第一批收緊
--    （建議 policy 收為 recorder = auth.uid() 對應帳號）。
-- 註：本表「不」加入 realtime publication —— 前端僅用輪詢讀取，
--    加入只會擴大匿名即時訂閱的洩漏面（資安審查建議）。

create table if not exists voice_notes (
  id uuid primary key default gen_random_uuid(),
  title text not null,
  transcript text not null,
  duration_sec int default 0,
  recorder text not null default 'unknown',   -- service/frankie/aaron/maggie/sales/tina/ec
  center text default 'other',                -- ops/mkt/vis/proc/wh/ec/ai/other
  recorded_at timestamptz default now(),
  notion_page_id text,                        -- 寫入 Notion 成功後回填
  notion_url text,
  created_at timestamptz default now()
);

create index if not exists idx_voice_notes_created on voice_notes (created_at desc);
create index if not exists idx_voice_notes_recorder on voice_notes (recorder, created_at desc);

alter table voice_notes enable row level security;

do $$
begin
  if not exists (
    select 1 from pg_policies
    where tablename = 'voice_notes' and policyname = 'voice_notes_anon_all'
  ) then
    create policy voice_notes_anon_all on voice_notes
      for all to anon using (true) with check (true);
  end if;
  if not exists (
    select 1 from pg_policies
    where tablename = 'voice_notes' and policyname = 'voice_notes_auth_all'
  ) then
    create policy voice_notes_auth_all on voice_notes
      for all to authenticated using (true) with check (true);
  end if;
end $$;
