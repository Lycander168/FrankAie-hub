/*
 * LUNA OS — 語音紀錄模組（v8.2 · LUNA Voice Notes）
 * -------------------------------------------------
 * 自包含 React 模組，供併入主檔 lycander-os-nu-v5.jsx 使用。
 * 錄音（MediaRecorder）＋ 即時逐字稿（Web Speech API zh-TW），
 * 停止後進入可編輯草稿（標題/內容皆可修改），儲存經 Supabase
 * Edge Function `luna-voice-note` 寫入 voice_notes 表與
 * Notion「🎙 LUNA 語音紀錄」資料庫。
 *
 * 依主檔管線約定：React 以全域存在（React.useState 直接取用，
 * 不用 import；tsc target ES2018 / jsx react 可直接編譯本檔）。
 *
 * 掛載方式（見 INTEGRATION.md；建議掛「總覽」快速工具區，全帳號可見）：
 *   <VoiceNotes user={currentUser} center={activeCenter}
 *     supabaseUrl={SB_URL} supabaseKey={SB_KEY} />
 *
 * 隱私揭露：即時轉錄音訊會送 Google 語音服務處理；音檔本體不保存
 * （停止即棄）；現行 anon 過渡模式下 7 個帳號可互見全部紀錄。
 */

const VN_COLORS = {
  bg: "#F7F4EF",
  card: "#FFFFFF",
  theme: "#5C6E7A",
  themeDark: "#43525C",
  danger: "#C0392B",
  warn: "#B9770E",
  ok: "#2E7D32",
  line: "#E3DED6",
  text: "#2B2B2B",
  sub: "#8A8578",
};

// 逐字稿長度上限（與 Edge Function 驗證一致）
const VN_MAX_TRANSCRIPT = 60000;
const VN_MAX_TITLE = 200;

function vnFmtDur(sec) {
  const m = Math.floor(sec / 60);
  const s = sec % 60;
  return (m < 10 ? "0" + m : "" + m) + ":" + (s < 10 ? "0" + s : "" + s);
}

function vnDefaultTitle(transcript) {
  const d = new Date();
  const pad = (n) => (n < 10 ? "0" + n : "" + n);
  const stamp =
    d.getFullYear() + "-" + pad(d.getMonth() + 1) + "-" + pad(d.getDate()) +
    " " + pad(d.getHours()) + ":" + pad(d.getMinutes());
  const head = (transcript || "").trim().slice(0, 12);
  return head ? stamp + "・" + head : stamp + "・語音紀錄";
}

// 僅渲染可信任的 Notion 連結（防 anon 表被灌入 javascript: URL 之儲存型 XSS）
function vnSafeNotionUrl(url) {
  if (typeof url !== "string") return null;
  if (url.indexOf("https://www.notion.so/") === 0 || url.indexOf("https://notion.so/") === 0) {
    return url;
  }
  return null;
}

function VoiceNotes(props) {
  const user = props.user || { id: "unknown", name: "未登入" };
  const center = props.center || "other";
  const sbUrl = props.supabaseUrl;
  const sbKey = props.supabaseKey;
  const fnUrl =
    props.functionUrl || (sbUrl ? sbUrl + "/functions/v1/luna-voice-note" : "");

  const [recording, setRecording] = React.useState(false);
  const [elapsed, setElapsed] = React.useState(0);
  const [finalText, setFinalText] = React.useState("");
  const [interimText, setInterimText] = React.useState("");
  const [draft, setDraft] = React.useState(null); // {title, text, duration} | null
  const [speechOk, setSpeechOk] = React.useState(true);
  const [saving, setSaving] = React.useState(false);
  const [msg, setMsg] = React.useState(null); // {kind:"ok"|"warn"|"err", text, url}
  const [notes, setNotes] = React.useState([]);

  const mediaRef = React.useRef(null);     // MediaRecorder
  const streamRef = React.useRef(null);    // MediaStream
  const recogRef = React.useRef(null);     // SpeechRecognition
  const timerRef = React.useRef(null);
  const restartRef = React.useRef(null);   // recognition 重啟 backoff timer
  const finalRef = React.useRef("");       // 避免 closure 拿到舊 state
  const interimRef = React.useRef("");     // 停止時搶救未定案文字
  const recordingRef = React.useRef(false);
  const startingRef = React.useRef(false); // getUserMedia await 空窗防重入
  const fatalSpeechRef = React.useRef(false); // 致命辨識錯誤 → 停止自動重啟
  const elapsedRef = React.useRef(0);
  const chunksRef = React.useRef([]);      // 音檔（僅錄音期間暫存，停止即棄）

  // 近期清單（voice_notes 表，anon 讀取，比照 stor 層 REST 模式）
  const loadNotes = React.useCallback(() => {
    if (!sbUrl || !sbKey) return;
    fetch(
      sbUrl +
        "/rest/v1/voice_notes?select=id,title,duration_sec,recorder,center,notion_url,created_at&order=created_at.desc&limit=10",
      { headers: { apikey: sbKey, Authorization: "Bearer " + sbKey } }
    )
      .then((r) => (r.ok ? r.json() : []))
      .then((rows) => setNotes(Array.isArray(rows) ? rows : []))
      .catch((e) => { if (window.console) console.warn("voice_notes list load failed", e); });
  }, [sbUrl, sbKey]);

  React.useEffect(() => {
    loadNotes();
  }, [loadNotes]);

  const releaseResources = () => {
    if (timerRef.current) { clearInterval(timerRef.current); timerRef.current = null; }
    if (restartRef.current) { clearTimeout(restartRef.current); restartRef.current = null; }
    if (recogRef.current) {
      try { recogRef.current.onend = null; recogRef.current.stop(); } catch (e) {}
      recogRef.current = null;
    }
    if (mediaRef.current && mediaRef.current.state !== "inactive") {
      try { mediaRef.current.stop(); } catch (e) {}
    }
    mediaRef.current = null;
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((t) => t.stop());
      streamRef.current = null;
    }
    chunksRef.current = []; // 音檔不保存，立即釋放記憶體
  };

  // 卸載時釋放資源
  React.useEffect(() => {
    return () => { recordingRef.current = false; releaseResources(); };
  }, []);

  const startRecording = async () => {
    // 防重入：錄音中或 getUserMedia await 空窗期間再點無效
    if (recordingRef.current || startingRef.current) return;
    // 草稿保護：未儲存內容需確認才覆蓋
    if (draft && draft.text && draft.text.trim()) {
      const okToDiscard = window.confirm("尚有未儲存的語音草稿，重新錄音將清除。確定繼續？");
      if (!okToDiscard) return;
    }
    startingRef.current = true;
    setMsg(null);
    setDraft(null);
    setFinalText("");
    setInterimText("");
    finalRef.current = "";
    interimRef.current = "";
    fatalSpeechRef.current = false;
    chunksRef.current = [];
    elapsedRef.current = 0;
    setElapsed(0);

    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      startingRef.current = false;
      setMsg({ kind: "err", text: "此環境不支援麥克風（需 https 或 localhost + Chrome/Edge）" });
      return;
    }
    let stream;
    try {
      stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    } catch (e) {
      startingRef.current = false;
      setMsg({ kind: "err", text: "無法取得麥克風權限：" + (e && e.message ? e.message : e) });
      return;
    }
    streamRef.current = stream;

    // 音檔錄製（僅錄音期間暫存記憶體，不上傳不保存）
    try {
      const mr = new MediaRecorder(stream);
      mr.ondataavailable = (ev) => { if (ev.data && ev.data.size > 0) chunksRef.current.push(ev.data); };
      mr.start();
      mediaRef.current = mr;
    } catch (e) {
      // MediaRecorder 不支援不阻斷流程：逐字稿仍可用
      mediaRef.current = null;
    }

    // 即時逐字稿（Web Speech API；音訊經 Google 語音服務處理）
    const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SR) {
      setSpeechOk(true);
      const recog = new SR();
      recog.lang = "zh-TW";
      recog.continuous = true;
      recog.interimResults = true;
      recog.onresult = (ev) => {
        let interim = "";
        for (let i = ev.resultIndex; i < ev.results.length; i++) {
          const res = ev.results[i];
          if (res.isFinal) {
            finalRef.current += res[0].transcript;
          } else {
            interim += res[0].transcript;
          }
        }
        interimRef.current = interim;
        setFinalText(finalRef.current);
        setInterimText(interim);
      };
      recog.onerror = (ev) => {
        // no-speech / aborted 屬正常；以下錯誤碼代表辨識已不可用，停止自動重啟
        if (
          ev.error === "network" || ev.error === "not-allowed" ||
          ev.error === "service-not-allowed" || ev.error === "audio-capture" ||
          ev.error === "language-not-supported"
        ) {
          fatalSpeechRef.current = true;
          setSpeechOk(false);
        }
      };
      recog.onend = () => {
        // continuous 模式常被瀏覽器自動切斷 → 加 backoff 重啟；致命錯誤或已停止則不重啟
        if (recordingRef.current && !fatalSpeechRef.current) {
          restartRef.current = setTimeout(() => {
            if (recordingRef.current && !fatalSpeechRef.current && recogRef.current === recog) {
              try { recog.start(); } catch (e) {}
            }
          }, 500);
        }
      };
      try { recog.start(); recogRef.current = recog; } catch (e) { setSpeechOk(false); }
    } else {
      setSpeechOk(false);
    }

    recordingRef.current = true;
    startingRef.current = false;
    setRecording(true);
    timerRef.current = setInterval(() => {
      elapsedRef.current += 1;
      setElapsed(elapsedRef.current);
    }, 1000);
  };

  const stopRecording = () => {
    if (!recordingRef.current) return;
    recordingRef.current = false;
    setRecording(false);
    releaseResources();
    // 搶救停止瞬間未定案的 interim 文字（小機率重複，屬取捨）
    const text = (finalRef.current + (interimRef.current || "")).trim().slice(0, VN_MAX_TRANSCRIPT);
    interimRef.current = "";
    setInterimText("");
    setFinalText("");
    // 進入可編輯草稿：辨識結果預填，儲存前可修錯字/改標題
    setDraft({
      title: vnDefaultTitle(text),
      text: text,
      duration: elapsedRef.current,
    });
  };

  const saveNote = async () => {
    if (!draft) return;
    const transcript = (draft.text || "").trim().slice(0, VN_MAX_TRANSCRIPT);
    if (!transcript) {
      setMsg({ kind: "err", text: "草稿是空的 — 請輸入內容後再儲存" });
      return;
    }
    if (!fnUrl) {
      setMsg({ kind: "err", text: "尚未設定 Edge Function URL（functionUrl / supabaseUrl）" });
      return;
    }
    setSaving(true);
    setMsg(null);
    const payload = {
      title: (draft.title || "").trim().slice(0, VN_MAX_TITLE) || vnDefaultTitle(transcript),
      transcript: transcript,
      duration_sec: draft.duration || 0,
      recorder: user.id,
      center: center,
      recorded_at: new Date().toISOString(),
    };
    try {
      const r = await fetch(fnUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          apikey: sbKey || "",
          Authorization: "Bearer " + (sbKey || ""),
        },
        body: JSON.stringify(payload),
      });
      const data = await r.json().catch(() => ({}));
      if (r.ok && data && data.ok) {
        if (data.notion_url) {
          setMsg({ kind: "ok", text: "已存入 Notion ✅", url: vnSafeNotionUrl(data.notion_url) });
        } else if (data.notion_error) {
          setMsg({ kind: "warn", text: "已存 Supabase ✅，但 Notion 同步失敗（可請 IT 至後台查看 logs 重試）" });
        } else {
          setMsg({ kind: "warn", text: "已存 Supabase ✅（Notion 尚未設定，設定後新紀錄將自動同步）" });
        }
        setDraft(null);
        elapsedRef.current = 0;
        setElapsed(0);
        loadNotes();
      } else {
        setMsg({ kind: "err", text: "儲存失敗：" + ((data && data.error) || "HTTP " + r.status) });
      }
    } catch (e) {
      setMsg({ kind: "err", text: "連線失敗：" + (e && e.message ? e.message : e) });
    }
    setSaving(false);
  };

  const discardDraft = () => {
    if (draft && draft.text && draft.text.trim()) {
      if (!window.confirm("確定捨棄這份未儲存的語音草稿？")) return;
    }
    setDraft(null);
    elapsedRef.current = 0;
    setElapsed(0);
  };

  return (
    <div style={{ background: VN_COLORS.bg, borderRadius: 14, padding: 18, border: "1px solid " + VN_COLORS.line, fontFamily: "inherit", color: VN_COLORS.text }}>
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 12 }}>
        <div style={{ fontWeight: 700, fontSize: 15 }}>🎙 語音紀錄</div>
        <div style={{ fontSize: 12, color: VN_COLORS.sub }}>
          {user.name || user.id}・{center}
        </div>
      </div>

      {/* 錄音控制 */}
      <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 12 }}>
        {!recording ? (
          <button
            onClick={startRecording}
            style={{ background: VN_COLORS.theme, color: "#fff", border: "none", borderRadius: 10, padding: "10px 18px", fontSize: 14, cursor: "pointer", fontWeight: 600 }}
          >
            ● 開始錄音
          </button>
        ) : (
          <button
            onClick={stopRecording}
            style={{ background: VN_COLORS.danger, color: "#fff", border: "none", borderRadius: 10, padding: "10px 18px", fontSize: 14, cursor: "pointer", fontWeight: 600 }}
          >
            ■ 停止（{vnFmtDur(elapsed)}）
          </button>
        )}
        {recording ? (
          <span style={{ fontSize: 12, color: VN_COLORS.danger }}>
            ● 錄音中{speechOk ? "・即時轉錄" : "・轉錄不可用（停止後可手動輸入）"}
          </span>
        ) : null}
      </div>

      {/* 錄音中：即時逐字稿（唯讀顯示；含已擷取文字，即使轉錄中途失效仍可見） */}
      {recording && (finalText || interimText || speechOk) ? (
        <div style={{ background: VN_COLORS.card, borderRadius: 10, border: "1px solid " + VN_COLORS.line, padding: 12, fontSize: 13, lineHeight: 1.7, minHeight: 48, marginBottom: 10, whiteSpace: "pre-wrap" }}>
          {finalText}
          <span style={{ color: VN_COLORS.sub }}>{interimText}</span>
          {!finalText && !interimText ? (
            <span style={{ color: VN_COLORS.sub }}>{speechOk ? "（開始說話…）" : ""}</span>
          ) : null}
        </div>
      ) : null}

      {/* 停止後：可編輯草稿（標題 + 內容），儲存以此為準 */}
      {draft ? (
        <div style={{ marginBottom: 10 }}>
          <input
            value={draft.title}
            onChange={(e) => setDraft({ title: e.target.value, text: draft.text, duration: draft.duration })}
            placeholder="標題"
            maxLength={VN_MAX_TITLE}
            style={{ width: "100%", boxSizing: "border-box", background: VN_COLORS.card, borderRadius: 10, border: "1px solid " + VN_COLORS.line, padding: "10px 12px", fontSize: 13, fontWeight: 600, marginBottom: 8, fontFamily: "inherit" }}
          />
          <textarea
            value={draft.text}
            onChange={(e) => setDraft({ title: draft.title, text: e.target.value, duration: draft.duration })}
            placeholder={speechOk ? "逐字稿（可修正錯字）…" : "此環境不支援即時轉錄，請手動輸入語音重點…"}
            style={{ width: "100%", boxSizing: "border-box", background: VN_COLORS.card, borderRadius: 10, border: "1px solid " + VN_COLORS.line, padding: 12, fontSize: 13, lineHeight: 1.7, minHeight: 96, marginBottom: 8, fontFamily: "inherit" }}
          />
          <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
            <button
              onClick={saveNote}
              disabled={saving}
              style={{ background: saving ? VN_COLORS.sub : VN_COLORS.ok, color: "#fff", border: "none", borderRadius: 10, padding: "10px 18px", fontSize: 14, cursor: saving ? "default" : "pointer", fontWeight: 600 }}
            >
              {saving ? "儲存中…" : "存入 Notion"}
            </button>
            <button
              onClick={discardDraft}
              disabled={saving}
              style={{ background: "transparent", color: VN_COLORS.sub, border: "1px solid " + VN_COLORS.line, borderRadius: 10, padding: "10px 14px", fontSize: 13, cursor: "pointer" }}
            >
              捨棄
            </button>
            <span style={{ fontSize: 12, color: VN_COLORS.sub }}>時長 {vnFmtDur(draft.duration || 0)}</span>
          </div>
        </div>
      ) : null}

      {/* 結果訊息 */}
      {msg ? (
        <div style={{ fontSize: 13, marginBottom: 10, color: msg.kind === "ok" ? VN_COLORS.ok : msg.kind === "warn" ? VN_COLORS.warn : VN_COLORS.danger }}>
          {msg.text}
          {msg.url ? (
            <a href={msg.url} target="_blank" rel="noreferrer" style={{ marginLeft: 8, color: VN_COLORS.theme }}>
              開啟 Notion 頁面 ↗
            </a>
          ) : null}
        </div>
      ) : null}

      {/* 近期紀錄 */}
      {notes.length > 0 ? (
        <div>
          <div style={{ fontSize: 12, color: VN_COLORS.sub, margin: "10px 0 6px" }}>近期紀錄</div>
          {notes.map((n) => {
            const safeUrl = vnSafeNotionUrl(n.notion_url);
            return (
              <div key={n.id} style={{ display: "flex", alignItems: "center", justifyContent: "space-between", background: VN_COLORS.card, border: "1px solid " + VN_COLORS.line, borderRadius: 10, padding: "8px 12px", marginBottom: 6, fontSize: 13 }}>
                <div style={{ overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap", marginRight: 8 }}>
                  {n.title}
                  <span style={{ color: VN_COLORS.sub, fontSize: 11, marginLeft: 8 }}>
                    {n.recorder}・{vnFmtDur(n.duration_sec || 0)}
                  </span>
                </div>
                {safeUrl ? (
                  <a href={safeUrl} target="_blank" rel="noreferrer" style={{ color: VN_COLORS.theme, fontSize: 12, flexShrink: 0 }}>
                    Notion ↗
                  </a>
                ) : null}
              </div>
            );
          })}
        </div>
      ) : null}

      {/* 隱私揭露 */}
      <div style={{ fontSize: 11, color: VN_COLORS.sub, marginTop: 10, lineHeight: 1.6 }}>
        即時轉錄音訊經 Google 語音服務處理・音檔本體不保存（僅存文字）・紀錄目前全帳號可見，敏感內容請留意
      </div>
    </div>
  );
}
