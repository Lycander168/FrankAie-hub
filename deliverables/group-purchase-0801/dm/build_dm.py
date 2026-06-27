# -*- coding: utf-8 -*-
"""
8/1 三檔齊發團購 DM 宣傳圖生成器
產出 4 張社群直式 DM（1080×1350，2x 輸出 = 2160×2700 PNG）：
  - DM_主視覺_三檔齊發.png
  - DM_Wokyis-M5.png
  - DM_LUNA-Mag.png
  - DM_Sharge-Disk-Pro.png

作法：以 HTML/CSS 設計 → 內建 Chromium headless 截圖成 PNG（無外部素材相依）。
團購價／拆帳等商業條件一律標「即將公布（待填）」，產品圖以佔位框呈現。

重新生成：python3 build_dm.py
"""

import os
import glob
import subprocess
import html as _html

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

# 各產品對應的圖檔關鍵字（檔名含其一即視為該產品商品圖）
IMG_KEYS = {
    "Wokyis M5": ["wokyis", "m5"],
    "LUNA Mag 小露娜": ["luna", "mag", "lycander"],
    "Sharge Disk Pro": ["sharge", "disk", "pro"],
}
IMG_EXT = (".jpg", ".jpeg", ".png", ".webp", ".gif")


def find_img(name):
    """在 assets/ 內依關鍵字找出該產品商品圖；找不到回傳 None。"""
    if not os.path.isdir(ASSETS):
        return None
    keys = IMG_KEYS.get(name, [])
    files = [f for f in sorted(glob.glob(os.path.join(ASSETS, "*")))
             if f.lower().endswith(IMG_EXT)]
    for f in files:
        base = os.path.basename(f).lower()
        if any(k in base for k in keys):
            return f
    return None


def img_box(name, cls, label):
    """有商品圖→以 cover 背景填滿；否則維持虛線佔位框。"""
    path = find_img(name)
    if path:
        return ("<div class='%s' style=\"background-image:url('file://%s');"
                "background-size:cover;background-position:center;border:none\"></div>"
                % (cls, path))
    return "<div class='%s ph'>%s</div>" % (cls, esc(label))

W, H = 1080, 1350
FONT = "'WenQuanYi Zen Hei','Noto Sans CJK TC',sans-serif"

C_WOKYIS = "#E8743B"
C_LUNA   = "#7C5CFF"
C_SHARGE = "#1FA2FF"
ACCENT   = "#00C2C2"
INK      = "#0E2A47"

PRODUCTS = [
    {
        "brand": "Wokyis", "name": "Wokyis M5", "accent": C_WOKYIS,
        "tag": "13 合 1 迷你螢幕擴充座 · 復古外觀，現代武裝",
        "bullets": ["13 合 1 多埠擴充", "復古造型 × 現代效能",
                    "標準 10G / 專業 80G TB5", "內建螢幕顯示狀態"],
        "specs": "for Mac mini · MacBook · Windows",
        "url": "zeczec.com/projects/wokyis",
    },
    {
        "brand": "LYCANDER", "name": "LUNA Mag 小露娜", "accent": C_LUNA,
        "tag": "口袋型無線充電站 · 一秒展開電就到",
        "bullets": ["3-in-1 手機 / 耳機 / 手錶", "Qi2.2 速度提升約 70%",
                    "MagSafe 磁吸精準對位", "口袋型 · 一秒展開"],
        "specs": "Qi2.2 · MagSafe 相容 · 隨身攜帶",
        "url": "zeczec.com/projects/luna-mag",
    },
    {
        "brand": "Sharge", "name": "Sharge Disk Pro", "accent": C_SHARGE,
        "tag": "全球首款主動散熱 PSSD × 多埠 Hub",
        "bullets": ["主動散熱 PSSD + Hub", "5-in-1：4埠 + HDMI2.1 + 內建線",
                    "最高 4TB · 10Gbps", "MagSafe · 僅約 150g"],
        "specs": "Ice-storm 散熱 · 口袋尺寸",
        "url": "zeczec.com/projects/disk-pro",
    },
]

# ----------------------------------------------------------------------------
# 共用樣式
# ----------------------------------------------------------------------------
BASE_CSS = """
* { margin:0; padding:0; box-sizing:border-box; }
html,body { width:%(W)dpx; height:%(H)dpx; }
body { font-family:%(FONT)s; overflow:hidden; -webkit-font-smoothing:antialiased;
       color:#fff; position:relative; }
.ph { /* 圖片佔位 */
   border:3px dashed rgba(255,255,255,.45); border-radius:24px;
   display:flex; align-items:center; justify-content:center;
   color:rgba(255,255,255,.6); font-size:30px; letter-spacing:2px;
   background:rgba(255,255,255,.05); }
.pill { display:inline-flex; align-items:center; border-radius:999px;
   font-weight:700; letter-spacing:1px; }
""" % {"W": W, "H": H, "FONT": FONT}


def esc(s):
    return _html.escape(s)


def page(body, extra_css=""):
    return ("<!doctype html><html><head><meta charset='utf-8'>"
            "<style>%s%s</style></head><body>%s</body></html>"
            % (BASE_CSS, extra_css, body))


# ----------------------------------------------------------------------------
# 主視覺 DM（三檔齊發）
# ----------------------------------------------------------------------------
def hero_html():
    css = """
    body { background:
        radial-gradient(1200px 700px at 80% -10%, #16456f 0%, rgba(22,69,111,0) 60%),
        linear-gradient(160deg, #0E2A47 0%, #081A2E 100%); }
    .wrap { padding:70px 64px 56px; height:100%; display:flex; flex-direction:column; }
    .kick { color:#7FE3E3; font-size:26px; font-weight:700; letter-spacing:6px; }
    .title { font-size:118px; font-weight:800; line-height:1.02; margin-top:14px;
             letter-spacing:4px; }
    .title .g { background:linear-gradient(90deg,#E8743B,#7C5CFF 50%,#1FA2FF);
                -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
    .sub { margin-top:20px; font-size:38px; font-weight:700; }
    .sub b { color:#7FE3E3; }
    .cards { margin-top:40px; display:flex; flex-direction:column; gap:22px; flex:1; }
    .card { background:rgba(255,255,255,.06); border:1px solid rgba(255,255,255,.10);
            border-radius:24px; padding:22px 26px; display:flex; align-items:center; gap:26px; }
    .bar { width:10px; align-self:stretch; border-radius:6px; }
    .thumb { width:150px; height:150px; flex:none; }
    .ci { flex:1; }
    .ci .bd { font-size:24px; font-weight:700; letter-spacing:2px; opacity:.85; }
    .ci .nm { font-size:46px; font-weight:800; margin-top:2px; }
    .ci .tg { font-size:27px; margin-top:8px; color:#C8D6E5; line-height:1.3; }
    .foot { margin-top:34px; display:flex; align-items:center; justify-content:space-between; }
    .offer { background:linear-gradient(90deg,#00C2C2,#0EA5A5); color:#06262a;
             padding:20px 34px; border-radius:18px; }
    .offer .s { font-size:24px; font-weight:700; letter-spacing:1px; }
    .offer .b { font-size:40px; font-weight:800; margin-top:2px; }
    .meta { text-align:right; font-size:24px; line-height:1.5; color:#C8D6E5; }
    .meta b { color:#fff; }
    """
    cards = ""
    for p in PRODUCTS:
        cards += (
            "<div class='card'>"
            "<div class='bar' style='background:%s'></div>"
            "" + img_box(p["name"], "thumb", "產品圖") +
            "<div class='ci'><div class='bd' style='color:%s'>%s</div>"
            "<div class='nm'>%s</div><div class='tg'>%s</div></div>"
            "</div>"
        ) % (p["accent"], p["accent"], esc(p["brand"]), esc(p["name"]), esc(p["tag"]))

    body = (
        "<div class='wrap'>"
        "<div class='kick'>嘖嘖人氣募資 ‧ 團購限定</div>"
        "<div class='title'>三<span class='g'>檔齊發</span></div>"
        "<div class='sub'><b>8/1</b> 三檔同步開團　Wokyis × LYCANDER × Sharge</div>"
        "<div class='cards'>" + cards + "</div>"
        "<div class='foot'>"
        "<div class='offer'><div class='s'>團購優惠價</div><div class='b'>即將公布</div></div>"
        "<div class='meta'>團購主　<b>ama shop</b><br>LYCANDER ｜ service@lycander.tw</div>"
        "</div></div>"
    )
    return page(body, css)


# ----------------------------------------------------------------------------
# 單品 DM
# ----------------------------------------------------------------------------
def product_html(p):
    accent = p["accent"]
    css = """
    body { background:linear-gradient(165deg,#0E2A47 0%, #081A2E 100%); }
    .wrap { padding:64px; height:100%; display:flex; flex-direction:column; }
    .top { display:flex; align-items:center; justify-content:space-between; }
    .brand { font-size:34px; font-weight:800; letter-spacing:3px;
             padding:12px 26px; border-radius:999px; color:#06121f; }
    .open { font-size:30px; font-weight:800; letter-spacing:2px; color:#06262a;
            background:#7FE3E3; padding:12px 26px; border-radius:999px; }
    .name { font-size:78px; font-weight:800; margin-top:34px; line-height:1.05; }
    .tag  { font-size:34px; margin-top:14px; color:#C8D6E5; line-height:1.35; }
    .hero { flex:1; margin:30px 0; min-height:0; }
    .hero.ph { font-size:34px; }
    .chips { display:grid; grid-template-columns:1fr 1fr; gap:16px; }
    .chip { background:rgba(255,255,255,.07); border:1px solid rgba(255,255,255,.12);
            border-radius:16px; padding:20px 22px; font-size:28px; font-weight:700;
            display:flex; align-items:center; gap:14px; }
    .dot { width:14px; height:14px; border-radius:50%; flex:none; }
    .spec { margin-top:20px; font-size:26px; color:#9FB4C9; letter-spacing:1px; }
    .foot { margin-top:26px; display:flex; align-items:center; justify-content:space-between;
            border-top:1px solid rgba(255,255,255,.12); padding-top:24px; }
    .price .s { font-size:26px; font-weight:700; color:#9FB4C9; }
    .price .b { font-size:48px; font-weight:800; }
    .price .b span { color:__ACCENT__; }
    .right { text-align:right; font-size:25px; color:#C8D6E5; line-height:1.5; }
    .right .u { color:#fff; font-weight:700; }
    """.replace("__ACCENT__", accent)

    chips = ""
    for b in p["bullets"]:
        chips += ("<div class='chip'><span class='dot' style='background:%s'></span>%s</div>"
                  % (accent, esc(b)))

    body = (
        "<div class='wrap'>"
        "<div class='top'>"
        "<div class='brand' style='background:%s'>%s</div>"
        "<div class='open'>8/1 開團</div>"
        "</div>"
        "<div class='name'>%s</div>"
        "<div class='tag'>%s</div>"
        "" + img_box(p["name"], "hero", "產品圖 / KV 置入處") +
        "<div class='chips'>%s</div>"
        "<div class='spec'>%s</div>"
        "<div class='foot'>"
        "<div class='price'><div class='s'>團購價</div><div class='b'><span>即將公布</span></div></div>"
        "<div class='right'><span class='u'>嘖嘖募資</span> %s<br>團購主 ama shop ｜ LYCANDER</div>"
        "</div></div>"
    ) % (accent, esc(p["brand"]), esc(p["name"]), esc(p["tag"]), chips,
         esc(p["specs"]), esc(p["url"]))
    return page(body, css)


# ----------------------------------------------------------------------------
# 渲染
# ----------------------------------------------------------------------------
def render(name, html_str):
    html_path = os.path.join(HERE, name + ".html")
    png_path = os.path.join(HERE, name + ".png")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_str)
    cmd = [
        CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
        "--force-device-scale-factor=2", "--window-size=%d,%d" % (W, H),
        "--default-background-color=00000000",
        "--screenshot=" + png_path, "file://" + html_path,
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    ok = os.path.exists(png_path) and os.path.getsize(png_path) > 0
    print(("✓" if ok else "✗"), os.path.basename(png_path),
          "" if ok else (r.stderr.strip()[-300:]))
    return ok


def main():
    render("DM_主視覺_三檔齊發", hero_html())
    slug = {"Wokyis M5": "Wokyis-M5", "LUNA Mag 小露娜": "LUNA-Mag",
            "Sharge Disk Pro": "Sharge-Disk-Pro"}
    for p in PRODUCTS:
        render("DM_" + slug[p["name"]], product_html(p))


if __name__ == "__main__":
    main()
