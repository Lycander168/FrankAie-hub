#!/usr/bin/env python3
# Build pqi GaN65W Combo bilingual leaflet (front=Chinese, back=English)
# Mirrors LYCANDER VoltiX GaN45W combo manual (band3/band4) layout.
import fitz, re, os

HERE = os.path.dirname(os.path.abspath(__file__))
# CJK font (WenQuanYi Zen Hei). Override with env FONT if installed elsewhere.
FONT = os.environ.get("FONT", "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc")
F = fitz.Font(fontfile=FONT)
CHARGER = os.path.join(HERE, "assets", "charger.png")
CABLE   = os.path.join(HERE, "assets", "cable.png")
OUT     = os.path.join(HERE, "pqi_GaN65W_Combo_Manual.pdf")

PW, PH = 936.0, 268.0          # page size (pt)  ~ reference face proportions
DARK  = (0.16,0.16,0.16)
GRAY  = (0.85,0.85,0.85)
BLUE  = (0.55,0.78,0.90)
BLACK = (0,0,0)
LINE  = (0.45,0.45,0.45)

# ---- text engine -----------------------------------------------------------
def wrap(text, size, w):
    out=[]
    for para in text.split("\n"):
        if para=="":
            out.append(""); continue
        atoms=re.findall(r'[A-Za-z0-9][A-Za-z0-9.\-+]*|\s+|.', para)
        cur=""
        for a in atoms:
            test=cur+a
            if F.text_length(test.rstrip(), size) > w and cur.strip():
                out.append(cur.rstrip())
                cur="" if a.isspace() else a
            else:
                cur=test
        out.append(cur.rstrip())
    return out

def text(page, x, y, s, size, w, lh=1.32, bold=False, color=DARK, align="l"):
    """Draw wrapped text starting with baseline near y(top). Returns y after block."""
    lines=wrap(s, size, w)
    leading=size*lh
    yy=y+size
    for ln in lines:
        lx=x
        if align=="c":
            lx=x+(w-F.text_length(ln,size))/2
        elif align=="r":
            lx=x+(w-F.text_length(ln,size))
        page.insert_text((lx,yy), ln, fontname="wqy", fontsize=size, color=color)
        if bold:
            page.insert_text((lx+0.3,yy), ln, fontname="wqy", fontsize=size, color=color)
        yy+=leading
    return yy-size+ (leading-size)

def header(page, x, y, w, s, size=6.4):
    page.draw_rect(fitz.Rect(x, y, x+w, y+size+4.5), color=None, fill=GRAY)
    page.insert_text((x+3, y+size+0.5), s, fontname="wqy", fontsize=size, color=(0.25,0.25,0.25))
    return y+size+4.5+3

def img(page, path, rect):
    page.insert_image(rect, filename=path, keep_proportion=True)

# ---- column geometry -------------------------------------------------------
M=16
FX0,FY0,FX1,FY1 = M, M, PW-M, PH-M           # outer frame
# 5 columns
C1=(22,184); C2=(190,356); C3=(362,556); C4=(562,702); C5=(708,PW-22)
ROHS_X0, ROHS_X1 = C3[0], C4[1]              # rohs spans C3+C4
TOP=26
ROHS_Y=150

def frame(page):
    page.draw_rect(fitz.Rect(FX0,FY0,FX1,FY1), color=BLACK, width=1.3)
    page.draw_rect(fitz.Rect(FX0+5,FY0+5,FX1-5,FY1-5), color=BLUE, width=0.5)

def vdiv(page, x):
    page.draw_line(fitz.Point(x, FY0+8), fitz.Point(x, FY1-8), color=BLUE, width=0.4)

# ---- cover panel -----------------------------------------------------------
def cover(page, t1, t2, t3, manual_label):
    x0,x1=C1; w=x1-x0; cx=x0+w/2
    # logo wordmark "pqi" + dot
    lw=F.text_length("pqi",16)
    page.insert_text((cx-lw/2, TOP+11), "pqi", fontname="wqy", fontsize=16, color=(0.1,0.1,0.1))
    page.insert_text((cx-lw/2+0.3, TOP+11), "pqi", fontname="wqy", fontsize=16, color=(0.1,0.1,0.1))
    page.draw_circle(fitz.Point(cx+lw/2+3, TOP+2.5), 1.7, color=None, fill=(0.1,0.1,0.1))
    # title block
    page.insert_text((cx-F.text_length(t1,10.5)/2, TOP+27), t1, fontname="wqy", fontsize=10.5, color=DARK)
    page.insert_text((cx-F.text_length(t1,10.5)/2+0.3, TOP+27), t1, fontname="wqy", fontsize=10.5, color=DARK)
    page.insert_text((cx-F.text_length(t2,7.2)/2, TOP+39), t2, fontname="wqy", fontsize=7.2, color=DARK)
    page.insert_text((cx-F.text_length(t3,7.0)/2, TOP+50), t3, fontname="wqy", fontsize=7.0, color=DARK)
    # hero images (non-overlapping): charger upper, coiled cable lower
    img(page, CHARGER, fitz.Rect(x0+44, TOP+56, x1-18, TOP+120))
    img(page, CABLE,   fitz.Rect(x0+6,  TOP+118, x0+w*0.80, TOP+170))
    # manual label bottom centre
    page.insert_text((cx-F.text_length(manual_label,8.5)/2, FY1-12), manual_label,
                     fontname="wqy", fontsize=8.5, color=DARK)

# ---- RoHS table ------------------------------------------------------------
def rohs(page, caption, head_cols, rows, note):
    x0,x1=ROHS_X0,ROHS_X1; w=x1-x0
    y=ROHS_Y
    text(page, x0, y, caption, 4.6, w); y+=11
    # title spanning
    title="限用物質及其化學符號  Restricted substances and its chemical symbols"
    # column widths
    cw=[w*0.17]+[w*0.83/6]*6
    xs=[x0]
    for c in cw: xs.append(xs[-1]+c)
    th=y
    # outer + title row
    title_h=9
    page.draw_rect(fitz.Rect(x0, th, x1, th+title_h), color=LINE, width=0.4)
    page.insert_text((x0+ (w-F.text_length(title,4.3))/2, th+6.3), title, fontname="wqy", fontsize=4.3, color=DARK)
    hy=th+title_h
    head_h=15
    for i,hc in enumerate(head_cols):
        r=fitz.Rect(xs[i],hy,xs[i+1],hy+head_h)
        page.draw_rect(r, color=LINE, width=0.4)
        lines=hc.split("\n")
        ty=hy+ (head_h-len(lines)*4.4)/2 +3.6
        for ln in lines:
            page.insert_text((xs[i]+(cw[i]-F.text_length(ln,3.9))/2, ty), ln, fontname="wqy", fontsize=3.9, color=DARK)
            ty+=4.4
    ry=hy+head_h
    row_h=8.2
    for row in rows:
        for i,val in enumerate(row):
            r=fitz.Rect(xs[i],ry,xs[i+1],ry+row_h)
            page.draw_rect(r, color=LINE, width=0.4)
            fs=4.4 if i==0 else 5.2
            page.insert_text((xs[i]+(cw[i]-F.text_length(val,fs))/2, ry+row_h-2.6), val, fontname="wqy", fontsize=fs, color=DARK)
        ry+=row_h
    text(page, x0, ry+1, note, 3.7, w)

def icons(page, x, y):
    # WEEE crossed bin
    s=fitz.utils
    bx,by=x,y
    page.draw_rect(fitz.Rect(bx,by,bx+9,by+10), color=(0.1,0.1,0.1), width=0.7)
    page.draw_line(fitz.Point(bx,by+2.5),fitz.Point(bx+9,by+2.5),color=(0.1,0.1,0.1),width=0.7)
    page.draw_line(fitz.Point(bx,by),fitz.Point(bx+9,by+10),color=(0.1,0.1,0.1),width=0.8)
    page.draw_line(fitz.Point(bx,by+13),fitz.Point(bx+9,by+13),color=(0.1,0.1,0.1),width=1.2)
    # CE
    page.insert_text((bx+15,by+9),"CE",fontname="wqy",fontsize=10,color=(0.1,0.1,0.1))
    # RoHS badge
    page.draw_circle(fitz.Point(bx+40,by+5),7,color=(0.1,0.45,0.2),width=0.8)
    page.insert_text((bx+34.5,by+6.6),"RoHS",fontname="wqy",fontsize=3.6,color=(0.1,0.45,0.2))

# ---- column content drawers ------------------------------------------------
def col_features(page, thanks, feat_hdr, feats):
    x0,x1=C2; w=x1-x0; y=TOP
    y=text(page, x0, y, thanks, 5.0, w, lh=1.3); y+=4
    y=header(page, x0, y, w, feat_hdr)
    for t,b in feats:
        y=text(page, x0, y, t, 5.2, w, bold=True); y+=1.5
        y=text(page, x0, y, b, 4.8, w, lh=1.28); y+=3

def col_spec(page, hdr, lines, col):
    x0,x1=col; w=x1-x0; y=TOP
    y=header(page, x0, y, w, hdr)
    body="\n".join(lines)
    text(page, x0, y, body, 5.0, w, lh=1.35)

def col_cable(page, title, lines):
    x0,x1=C4; w=x1-x0; y=TOP+3
    y=text(page, x0, y, title, 5.0, w, bold=True); y+=2
    text(page, x0, y, "\n".join(lines), 4.9, w, lh=1.34)

def col_c5(page, blocks):
    x0,x1=C5; w=x1-x0; y=TOP
    for kind,val in blocks:
        if kind=="h":
            y=header(page, x0, y, w, val)
        elif kind=="t":
            y=text(page, x0, y, val, 4.9, w, lh=1.3)+2
        elif kind=="b":
            y=text(page, x0, y, val, 4.8, w, lh=1.28)+1.5
        elif kind=="bold":
            y=text(page, x0, y, val, 5.0, w, bold=True, lh=1.3)+1.5
        elif kind=="gap":
            y+=val
        elif kind=="icons":
            icons(page, x0, y+2)

# ===========================================================================
doc=fitz.open()

# ---------- PAGE 1 : CHINESE FRONT ----------
p=doc.new_page(width=PW,height=PH); p.insert_font(fontname="wqy",fontfile=FONT)
frame(p)
for x in (C1[1]+3, C2[1]+3, C3[1]+3, C4[1]+3): vdiv(p,x)
cover(p, "pqi GaN65W", "雙孔USB-C 氮化鎵快速充電器", "Combo快充組", "使用說明書")
col_features(p,
  "感謝您購買「pqi GaN65W 雙孔USB-C 氮化鎵快速充電器」(以下簡稱為本產品)。此說明書內容記載著本產品的使用方法以及安全注意事項，使用前請詳細閱讀本說明書。",
  "產品特色",
  [("雙孔高效充電","pqi 65W氮化鎵充電器提供雙USB-C孔，每孔最大支援65W，使您可以同時為多個設備提供高效能量。"),
   ("智能電流分配","憑藉智能電流分配技術，確保您的設備獲得最適合的充電速度，延長電池壽命。"),
   ("輕巧便攜","小巧輕便，方便攜帶，是您外出旅行的理想配置，讓您保持充電不中斷。"),
   ("具有多重保護功能","包括過熱、過充、短路保護，確保您的設備在安全的狀態下充電。"),
   ("廣泛兼容性","兼容各種USB-C設備，包括智能手機、平板電腦、筆記型電腦等，無論您使用什麼設備，都可以信賴它。")])
col_spec(p,"產品規格",
  ["材質：聚碳酸酯 + ABS",
   "尺寸：約 55 × 30 × 55 mm",
   "重量：________ g",
   "輸入：100-240Vac 50/60Hz 1.5A max",
   "USB-C1輸出：5V/3A、9V/3A、12V/3A、15V/3A、20V/3.25A（最大65W）",
   "USB-C2輸出：5V/3A、9V/3A、12V/3A、15V/3A、20V/3.25A（最大65W）",
   "USB-C1 & USB-C2 同時輸出：",
   "USB-C1：5V/3A、9V/3A、12V/3A、15V/3A、20V/2.25A（最大45W）",
   "USB-C2：5V/3A、9V/2.22A、12V/1.67A（最大20W）",
   "PPS：5V-11V/5A",
   "工作溫度：0℃~35℃　儲存溫度：-40℃~70℃",
   "相對濕度：5%~95%（無冷凝）"], C3)
col_cable(p,"＊USB Type-C to Type-C 100W 充電傳輸線＿100CM＊",
  ["材質：TPE + 尼龍編織 + 鋁合金外殼",
   "功能：充電、數據傳輸",
   "端子：USB Type-C to USB Type-C",
   "輸入/輸出：20V/5A（100W）",
   "傳輸速率：10Gbps",
   "支援協議：PD / QC / BC1.2",
   "彎折試驗：1000次",
   "長度：1.0公尺（100CM）",
   "工作溫度：0℃~40℃",
   "儲存溫度：-20℃~80℃"])
rohs(p,
  "設備名稱：電源供應器，型號（型式）：pqi GaN65W 雙孔USB-C 氮化鎵快速充電器",
  ["單元\nUnit","鉛\nLead\n(Pb)","汞\nMercury\n(Hg)","鎘\nCadmium\n(Cd)","六價鉻\nCr(VI)","多溴聯苯\n(PBB)","多溴二苯醚\n(PBDE)"],
  [["塑膠外殼","○","○","○","○","○","○"],
   ["電路板","○","○","○","○","○","○"],
   ["輸出端子","○","○","○","○","○","○"],
   ["輸入金屬組件","○","○","○","○","○","○"]],
  "備考：「○」係指該項限用物質之百分比含量未超出百分比含量基準值。")
col_c5(p,[
  ("h","包裝內含物"),
  ("t","PD 65W 氮化鎵電源供應器 x1\nUSB-C to USB-C 100W 充電傳輸線（1.0M）x1\n說明書 x1"),
  ("gap",2),
  ("h","注意事項"),
  ("b","◆請勿強烈撞擊或私自拆解更換產品零件等動作。"),
  ("b","◆請遠離高溫、潮濕、腐蝕性產品、火源之環境。"),
  ("b","◆提醒您不使用時請將充電器拔離電源。"),
  ("b","◆使用本產品時請注意符合欲充電產品之限定電壓及電流，以免造成產品損壞。"),
  ("b","◆在正常操作情況下(非人為)，若產品需於猶豫期間七天內更換時，請保存您的購買証明，而商品必須是完整包裝及配件。"),
  ("gap",1),
  ("t","說明書涉及圖片均為示意圖，最終產品實物為準。"),
  ("gap",2),
  ("bold","進口商/委製商：炫輝國際有限公司"),
  ("t","地址：新北市板橋區和平路15號B1"),
  ("t","客服專線：(02) 2274-8555"),
  ("gap",3),
  ("icons",0),
])

# ---------- PAGE 2 : ENGLISH BACK ----------
p=doc.new_page(width=PW,height=PH); p.insert_font(fontname="wqy",fontfile=FONT)
frame(p)
for x in (C1[1]+3, C2[1]+3, C3[1]+3, C4[1]+3): vdiv(p,x)
cover(p, "pqi GaN65W", "Dual USB-C Fast Charger", "Combo", "User Manual")
col_features(p,
  "Thank you for purchasing \"pqi GaN65W Dual USB-C Fast Charger\" (below this product). This instruction booklet content is recording this product application method as well as the safety matters needing attention; before use, please read this instruction booklet in detail.",
  "Products Features",
  [("Dual-Port Efficiency.","pqi Gallium Nitride 65W charger boasts two USB-C ports, each delivering up to 65W, allowing you to power multiple devices simultaneously with high efficiency."),
   ("Intelligent Current Allocation.","With intelligent current allocation technology, it ensures your devices receive the optimal charging speed, extending battery life."),
   ("Compact & Portable.","Small and lightweight, it's your ideal travel companion, ensuring uninterrupted charging on the go."),
   ("Worry-Free Safety.","Equipped with multiple protection features, including overheat, overcharge, and short-circuit protection, ensuring your devices charge safely."),
   ("Broad Compatibility.","Compatible with a wide range of USB-C devices, including smartphones, tablets, laptops, and more. Trust it, no matter what device you use.")])
col_spec(p,"Products Specification",
  ["Material: PC + ABS",
   "Dimensions: approx. 55 × 30 × 55 mm",
   "Weight: ________ g",
   "Input: AC 100-240V 50/60Hz 1.5A max",
   "USB-C1 Output: 5V/3A, 9V/3A, 12V/3A, 15V/3A, 20V/3.25A (Max 65W)",
   "USB-C2 Output: 5V/3A, 9V/3A, 12V/3A, 15V/3A, 20V/3.25A (Max 65W)",
   "USB-C1 & USB-C2 simultaneous output:",
   "USB-C1: 5V/3A, 9V/3A, 12V/3A, 15V/3A, 20V/2.25A (Max 45W)",
   "USB-C2: 5V/3A, 9V/2.22A, 12V/1.67A (Max 20W)",
   "PPS: 5V-11V/5A",
   "Operating temperature: 0℃~35℃",
   "Storage temperature: -40℃~70℃",
   "Relative humidity: 5%~95% (non-condensing)"], C3)
col_cable(p,"＊USB Type-C to Type-C 100W Cable ＿ 100CM＊",
  ["Material: TPE + nylon braid + aluminum housing",
   "Function: charging, data transmission",
   "Terminal: USB Type-C to USB Type-C",
   "Input/Output: 20V/5A (100W)",
   "Transfer rate: 10Gbps",
   "Protocols: PD / QC / BC1.2",
   "Bending test: 1000 times",
   "Length: 1.0 m (100CM)",
   "Operating temp.: 0℃~40℃",
   "Storage temp.: -20℃~80℃"])
rohs(p,
  "Equipment name: Power supply   Type designation (Type): pqi GaN65W Dual USB-C Fast Charger",
  ["Unit","Lead\n(Pb)","Mercury\n(Hg)","Cadmium\n(Cd)","Cr(VI)","PBB","PBDE"],
  [["Plastic housing","○","○","○","○","○","○"],
   ["PCB","○","○","○","○","○","○"],
   ["Output terminal","○","○","○","○","○","○"],
   ["Input metal parts","○","○","○","○","○","○"]],
  "Note: \"○\" indicates that the content of the restricted substance does not exceed the percentage reference value.")
col_c5(p,[
  ("h","Package inclusions"),
  ("t","PD 65W GaN Charger x1\nUSB-C to USB-C 100W Cable (1.0M) x1\nUser manual x1"),
  ("gap",2),
  ("h","Cautions"),
  ("b","● Don't impact or disassemble the product."),
  ("b","● Keep away from hazardous environment (Ex. high temperature, moisture, corrosive products, or fire)."),
  ("b","● Unplug the charger when not in use."),
  ("b","● To avoid product damage, please be aware of limited voltage and electricity."),
  ("b","● In normal operation, product could be exchanged with purchase receipt, complete package and fitting in 7 days grace period."),
  ("gap",2),
  ("bold","Lycander Company Information"),
  ("t","LEV ONE LIMITED — Intershore Chambers, PB 4342, Road Town Tortola, VG1110 British Virgin Islands"),
  ("t","UK Rep: ARCHES LIMITED — 75-71 Shelton Street, London, WC2H 9JQ, United Kingdom"),
  ("t","EU Rep: AISLING UPTREND LIMITED — Ground Floor, 71 Baggot Street Lower, Dublin, D02 P593, Ireland"),
  ("t","www.lycander.tw"),
  ("gap",2),
  ("icons",0),
])

doc.save(OUT, deflate=True)
print("saved", OUT)
