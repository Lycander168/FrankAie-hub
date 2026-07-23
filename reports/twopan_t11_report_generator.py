# -*- coding: utf-8 -*-
"""TwoPan T11 眾籌項目評估報告 PDF 產生器"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, PageBreak, HRFlowable)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('WQY', '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc', subfontIndex=0))

PRIMARY = colors.HexColor('#1a3a5c')
ACCENT = colors.HexColor('#2e6da4')
LIGHT = colors.HexColor('#eef3f8')
WARN = colors.HexColor('#b03a2e')

def S(name, **kw):
    base = dict(fontName='WQY', leading=16, spaceAfter=6)
    base.update(kw)
    return ParagraphStyle(name, **base)

st_title   = S('title', fontSize=26, leading=36, alignment=TA_CENTER, textColor=PRIMARY)
st_sub     = S('sub', fontSize=14, leading=22, alignment=TA_CENTER, textColor=colors.HexColor('#555555'))
st_h1      = S('h1', fontSize=16, leading=24, textColor=PRIMARY, spaceBefore=14, spaceAfter=8)
st_h2      = S('h2', fontSize=12.5, leading=19, textColor=ACCENT, spaceBefore=10, spaceAfter=5)
st_body    = S('body', fontSize=10.5, leading=17, alignment=TA_JUSTIFY, spaceAfter=5)
st_bullet  = S('bullet', fontSize=10.5, leading=16.5, leftIndent=14, spaceAfter=3)
st_note    = S('note', fontSize=9, leading=13.5, textColor=colors.HexColor('#777777'), spaceAfter=4)
st_tcell   = S('tcell', fontSize=9.5, leading=13.5, spaceAfter=0)
st_tcellc  = S('tcellc', fontSize=9.5, leading=13.5, spaceAfter=0, alignment=TA_CENTER)
st_thead   = S('thead', fontSize=9.5, leading=13.5, spaceAfter=0, textColor=colors.white, alignment=TA_CENTER)
st_warnbox = S('warnbox', fontSize=10.5, leading=17, textColor=WARN)

def tbl(data, widths, header=True, align_first_left=True):
    rows = []
    for ri, row in enumerate(data):
        out = []
        for ci, cell in enumerate(row):
            if ri == 0 and header:
                out.append(Paragraph(str(cell), st_thead))
            else:
                sty = st_tcell if (ci == 0 and align_first_left) else st_tcellc
                out.append(Paragraph(str(cell), sty))
        rows.append(out)
    t = Table(rows, colWidths=widths, repeatRows=1 if header else 0)
    style = [
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#b8c6d4')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]
    if header:
        style.append(('BACKGROUND', (0, 0), (-1, 0), ACCENT))
        style.append(('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT]))
    else:
        style.append(('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, LIGHT]))
    t.setStyle(TableStyle(style))
    return t

def bullets(items):
    return [Paragraph(f'•  {x}', st_bullet) for x in items]

story = []

# ---------- 封面 ----------
story.append(Spacer(1, 60 * mm))
story.append(Paragraph('眾籌商品項目評估報告', st_title))
story.append(Spacer(1, 6 * mm))
story.append(Paragraph('TwoPan T11 口袋型磁吸多功能 USB-C Hub 支架', st_sub))
story.append(Spacer(1, 4 * mm))
story.append(HRFlowable(width='60%', thickness=1, color=ACCENT, hAlign='CENTER'))
story.append(Spacer(1, 10 * mm))
story.append(Paragraph('標的模式：眾籌（群眾募資）', st_sub))
story.append(Paragraph('預熱時間：2026 年 9 月　｜　出貨時間：2026 年 12 月', st_sub))
story.append(Spacer(1, 40 * mm))
story.append(Paragraph('報告日期：2026 年 7 月 23 日', st_sub))
story.append(Paragraph('資料來源：Kickstarter 公開頁面、品牌官網與電商通路公開資訊', st_note))
story.append(PageBreak())

# ---------- 1. 執行摘要 ----------
story.append(Paragraph('一、執行摘要', st_h1))
story.append(Paragraph(
    'TwoPan T11 為香港品牌 Twopan 於 Kickstarter 推出的「口袋型磁吸多功能 USB-C Hub 支架」，'
    '整合 7-in-1 擴充埠（100W PD、4K@60Hz HDMI、5Gbps USB 資料埠、SD/TF 讀卡）與 MagSafe 相容磁吸手機支架功能。'
    '原始活動以低目標（HK$10,000）操作，公開資訊顯示達成率已逾 1,076%，屬於「小額目標、快速達標」的典型 3C 配件眾籌打法，'
    '市場需求獲得初步驗證，但整體募資規模屬中小型。', st_body))
story.append(Paragraph(
    '本報告以「2026 年 9 月預熱、12 月出貨」為前提，評估在台灣（或華語市場）平台再眾籌／代理引進此類產品的可行成本與損益。'
    '核心結論如下：', st_body))
story.append(Spacer(1, 2 * mm))
concl = tbl([
    ['評估面向', '結論'],
    ['商品力', '規格完整、磁吸支架差異化明確；但同類 Hub 競爭激烈，屬「改良型」而非「開創型」商品'],
    ['時程可行性', '12 月出貨<b>僅「代理現貨／半現貨」模式可行</b>；ODM 自製開模＋認證需 4–6 個月，來不及'],
    ['單位成本', '代理採購落地成本約 NT$600–750／台；ODM 量產 BOM 約 US$11–17（NT$360–550）'],
    ['建議眾籌定價', '超早鳥 NT$1,290、早鳥 NT$1,490、眾籌價 NT$1,690（未來零售 NT$2,290）'],
    ['基準情境損益', '約 900 台、營收約 NT$135 萬，稅前淨利約 NT$13 萬（淨利率約 10%）；損益兩平約 630 台'],
    ['總前期投入', '約 NT$45–75 萬（樣品、預熱廣告、素材、認證、平台與雜支；不含貨款）'],
    ['綜合建議', '<b>有條件 GO</b>：確認原廠授權與 11 月中前交貨能力後執行；否則改期或改品'],
], [38 * mm, 132 * mm])
story.append(concl)

# ---------- 2. 產品概述 ----------
story.append(Paragraph('二、產品概述與規格', st_h1))
story.append(Paragraph('2.1 產品定位', st_h2))
story.append(Paragraph(
    'T11 主打「一件裝備解決行動工作者的擴充與手機支架需求」：口袋大小的鋁合金 Hub，'
    '正面為 MagSafe 相容磁吸區，可吸附 iPhone 作為直立／橫放支架，側邊提供完整 I/O。'
    '目標客群為 MacBook／iPad／iPhone 生態的行動工作者、Vlogger 與商務差旅族。', st_body))
story.append(Paragraph('2.2 公開規格整理', st_h2))
story.append(tbl([
    ['項目', '規格（依公開資訊整理）'],
    ['型號／名稱', 'Twopan T11：Portable Magnetic Multi-port USB-C Hub Stand'],
    ['埠位', '7-in-1：USB-C PD 100W 充電直通、HDMI 4K@60Hz、USB 資料埠（USB 3.2、5Gbps）×2、USB-C 資料埠、SD／TF 讀卡槽'],
    ['特色功能', 'MagSafe 相容磁吸手機支架、即插即用（免驅動）、全系統相容（macOS／iPadOS／iOS／Windows／Android）'],
    ['材質', '鋁合金外殼（陽極處理）＋強磁陣列'],
    ['形態', '口袋型（Pocket-size），兼具支架與 Hub 雙功能'],
    ['品牌背景', 'Twopan（香港）：Amazon／BestBuy 有售的 3C 配件品牌，曾成功眾籌 Nano SSD（1,774 位贊助者）、Pro SSD 等產品'],
], [32 * mm, 138 * mm]))
story.append(Paragraph('註：部分埠位細節（如 USB-A／USB-C 配置數量）為依產品線與公開描述之合理推估，正式合作前應向原廠索取完整規格書。', st_note))

story.append(Paragraph('2.3 原始 Kickstarter 活動數據', st_h2))
story.append(tbl([
    ['項目', '數據'],
    ['募資目標', 'HK$10,000（約 NT$4.2 萬）— 低門檻目標，用於確保達標'],
    ['達成率', '公開快照顯示逾 1,076%（約 HK$10.8 萬起，約 NT$45 萬），當時距結束尚有約 4 週'],
    ['類別', 'Technology › Gadgets'],
    ['推估最終規模', '以同類項目曲線推估最終約 HK$20–40 萬（NT$83–166 萬）、贊助者數百人，屬中小型成功案'],
], [32 * mm, 138 * mm]))
story.append(Paragraph(
    '解讀：原始活動證明「磁吸 Hub 支架」訴求可轉單，但並非爆款量級。對台灣再眾籌而言，'
    '合理期望值應設定在數百台至兩千台之間，不宜以萬人級專案規劃庫存與行銷預算。', st_body))
story.append(PageBreak())

# ---------- 3. 市場與競品 ----------
story.append(Paragraph('三、市場與競品定價分析', st_h1))
story.append(tbl([
    ['競品／參照', '規格重點', '參考售價'],
    ['Twopan 自家 7-in-1 Hub（Amazon／BestBuy）', '4K HDMI、USB 3.2、SD/TF', '約 US$30–60（NT$980–1,950）'],
    ['UGREEN／Baseus 7-in-1 Hub', '4K HDMI、PD100W、SD/TF', '約 NT$900–1,600'],
    ['Anker 7-in-1／8-in-1 Hub', '4K HDMI、PD、雙 USB-A', '約 NT$1,400–2,500'],
    ['Satechi 磁吸／支架類配件', '鋁合金、質感定位', '約 NT$2,000–3,500'],
    ['同類磁吸 Hub 眾籌案（MEMDock、TobenONE 等）', '磁吸＋模組化訴求', '早鳥約 US$39–69'],
], [55 * mm, 55 * mm, 60 * mm]))
story.append(Paragraph(
    '定價結論：台灣市場對 7-in-1 Hub 的「無故事零售價」帶約在 NT$1,000–1,600；'
    '磁吸支架差異化與眾籌限定優惠可支撐 NT$1,290–1,690 的眾籌價位帶，'
    '未來零售價 NT$2,290 則需靠品牌與通路溢價支撐。價位帶上限受 UGREEN 等大陸品牌低價競爭壓制，'
    '不建議眾籌均價超過 NT$1,800。', st_body))

# ---------- 4. 成本結構 ----------
story.append(Paragraph('四、成本結構預估', st_h1))
story.append(Paragraph(
    '依取得貨源方式分兩種模式估算。因 12 月出貨的時程限制（詳第六章），本案實際可行者為模式 A；'
    '模式 B 列出供中長期自有產品線參考。', st_body))

story.append(Paragraph('4.1 模式 A：代理／授權引進（本案建議）', st_h2))
story.append(tbl([
    ['成本項目', '單位成本（NT$）', '說明'],
    ['原廠採購價（FOB／EXW）', '520–650', '以 MSRP 40–45% 推估（US$16–20），視數量與授權條件'],
    ['國際運費（空運）', '20–40', 'Q4 旺季空運；海運可降至 NT$8–15 但時程風險高'],
    ['關稅＋營業稅', '30–35', 'USB Hub 屬 ITA 資訊產品稅率 0%，進口營業稅 5%'],
    ['本地質檢／重工／貼標', '10–15', '抽檢、繁中說明書、BSMI 標籤'],
    ['<b>落地成本小計</b>', '<b>約 600–750</b>', '對眾籌均價 NT$1,500 之貨物成本率約 40–50%'],
], [45 * mm, 35 * mm, 90 * mm]))
story.append(Paragraph('一次性費用（模式 A）：', st_body))
story.append(tbl([
    ['項目', '預估金額（NT$）', '說明'],
    ['BSMI 商品驗證登錄', '40,000–120,000', '原廠若有既有測試報告可轉用則取低值；無 RF 功能免 NCC'],
    ['樣品／打樣與運費', '10,000–20,000', '拍攝與測試用 5–10 台'],
    ['授權金／區域獨家（如有）', '0–150,000', '視談判；亦可能以 MOQ 承諾替代'],
], [45 * mm, 40 * mm, 85 * mm]))

story.append(Paragraph('4.2 模式 B：ODM 自製（參考，本案時程不可行）', st_h2))
story.append(tbl([
    ['BOM 項目', '單價（US$）', '說明'],
    ['USB Hub 主控 IC', '1.2–1.8', 'VIA VL817／Genesys GL3510 等級'],
    ['PD 100W 控制 IC＋電路', '0.8–1.2', 'PD 3.0 直通'],
    ['HDMI 4K60 轉換 IC', '1.5–2.2', 'DP Alt-Mode 轉 HDMI 2.0（如 PS176 等級）'],
    ['SD/TF 讀卡 IC', '0.5–0.8', 'GL823K 等級'],
    ['連接器（USB-C×2、USB-A、HDMI、卡槽）', '1.2–1.8', ''],
    ['PCB＋SMT＋組裝測試', '1.8–2.8', '含治具攤提'],
    ['鋁合金外殼（CNC＋陽極）', '2.5–4.0', '磁吸支架結構件'],
    ['磁鐵陣列（N52）＋鐵片', '0.6–1.0', 'MagSafe 相容磁力圈'],
    ['線材／轉軸／輔料', '0.6–1.0', ''],
    ['彩盒包裝＋說明書', '0.8–1.2', ''],
    ['<b>BOM 合計</b>', '<b>約 11–17</b>', '<b>約 NT$360–550／台（MOQ 2,000–3,000）</b>'],
], [55 * mm, 30 * mm, 85 * mm]))
story.append(Paragraph(
    '模式 B 另需：模具與治具 NT$25–50 萬、CE／FCC／BSMI 認證 NT$15–30 萬、'
    '開發至量產週期約 4–6 個月。故 9 月預熱、12 月出貨的排程下不可採用。', st_body))
story.append(PageBreak())

# ---------- 5. 財務模型 ----------
story.append(Paragraph('五、眾籌財務模型與情境分析', st_h1))
story.append(Paragraph('5.1 定價與費用假設', st_h2))
story.append(tbl([
    ['參數', '假設值', '備註'],
    ['定價階梯', '超早鳥 NT$1,290（限 100）／早鳥 NT$1,490／眾籌價 NT$1,690', '加價購：磁吸環貼片、收納袋'],
    ['實收均價', '約 NT$1,450–1,520', '含階梯混合與少量加價購'],
    ['平台＋金流費', '募資額 10.5%', '台灣平台約 8%＋金流 2.5%；若走 Kickstarter 約 8–10%'],
    ['行銷費', '預熱期固定 NT$15–22 萬＋上線期約募資額 12%', '合計約占募資額 22–28%'],
    ['出貨物流', 'NT$70／件', '台灣本島宅配含包材'],
    ['貨物落地成本', 'NT$600／台（FOB US$16＋運稅檢）', '2,000 台以上議價至 NT$580'],
], [38 * mm, 72 * mm, 60 * mm]))

story.append(Paragraph('5.2 三情境損益試算', st_h2))

def scenario(units, avg_price, goods, ship=70, plat_rate=0.105, mkt_rate=0.12,
             preheat=180000, onetime=130000):
    rev = units * avg_price
    plat = rev * plat_rate
    mkt = rev * mkt_rate + preheat
    cogs = units * goods
    logi = units * ship
    total = plat + mkt + cogs + logi + onetime
    profit = rev - total
    return rev, plat, mkt, cogs, logi, onetime, profit

rows = [['項目', '保守情境', '基準情境', '樂觀情境']]
sc = {
    '保守': scenario(400, 1450, 600, preheat=150000),
    '基準': scenario(900, 1500, 600, preheat=180000),
    '樂觀': scenario(2000, 1520, 580, preheat=220000),
}
def f(n):
    return f'{n/10000:,.1f} 萬'
labels = ['募資總額', '平台＋金流費', '行銷費（含預熱）', '貨物成本', '出貨物流', '一次性費用（認證等）', '<b>稅前損益</b>']
units_row = ['出貨台數／均價', '400 台／NT$1,450', '900 台／NT$1,500', '2,000 台／NT$1,520']
rows.append(units_row)
for i, lab in enumerate(labels):
    r = [lab]
    for k in ['保守', '基準', '樂觀']:
        v = sc[k][i] if i < 6 else sc[k][6]
        cell = f(v)
        if i == 6:
            cell = f'<b>{cell}</b>'
        r.append(cell)
    rows.append(r)
margin_row = ['稅前淨利率']
for k in ['保守', '基準', '樂觀']:
    rev = sc[k][0]; p = sc[k][6]
    margin_row.append(f'{p/rev*100:,.1f}%')
rows.append(margin_row)
story.append(tbl(rows, [45 * mm, 41 * mm, 42 * mm, 42 * mm]))
story.append(Paragraph(
    '解讀：以每台邊際貢獻約 NT$490（售價扣平台費、貨物、物流與變動行銷）對固定支出約 NT$31 萬計算，'
    '<b>損益兩平約 630 台（募資額約 NT$95 萬）</b>。保守情境（400 台）虧損約 10 萬元，'
    '顯示「預熱名單品質」與「首 48 小時轉換」是本案成敗關鍵；基準情境淨利率約 10%，屬本模式偏薄但可接受的水準，'
    '放大獲利的槓桿依序為：壓低採購單價（每降 NT$50，基準情境增利 4.5 萬）、提高加價購客單、控制廣告占比。', st_body))

story.append(Paragraph('5.3 前期資金需求（不含貨款）', st_h2))
story.append(tbl([
    ['項目', '金額（NT$）'],
    ['樣品與素材製作（攝影、影片、頁面）', '80,000–150,000'],
    ['預熱期廣告（9 月起，名單蒐集）', '150,000–300,000'],
    ['BSMI 認證與檢測', '40,000–120,000'],
    ['公關／KOL 種子合作', '50,000–120,000'],
    ['雜支與備用金', '30,000–60,000'],
    ['<b>合計</b>', '<b>約 350,000–750,000</b>'],
], [100 * mm, 70 * mm]))
story.append(Paragraph(
    '貨款（基準情境 900 台 × NT$600 ≈ NT$54 萬）可於結案撥款後支付訂金，'
    '一般需自備 30–50% 訂金（約 NT$18–30 萬）作為過橋資金。', st_body))
story.append(PageBreak())

# ---------- 6. 時程 ----------
story.append(Paragraph('六、時程規劃（2026/7 → 2026/12）', st_h1))
story.append(tbl([
    ['期間', '工作項目', '關鍵節點'],
    ['7 月底–8 月', '原廠接洽、授權／採購條件談判、樣品到手、規格驗證、定價定案', '8/31 前簽約與樣品確認'],
    ['8 月–9 月初', '素材拍攝（產品照、情境影片）、募資頁製作、BSMI 送測', '9/10 前頁面完成'],
    ['9 月（預熱）', '前導頁上線、FB/IG 廣告蒐集名單、社群與 KOL 種子鋪陳', '目標名單 3,000–6,000 筆、CPA ≤ NT$50'],
    ['10 月上旬–11 月中', '正式上線（35–45 天）、首 48 小時衝量、媒體與聯盟推廣', '首週達成率 ≥ 60%'],
    ['10 月底', '依募資曲線向原廠下正式訂單（預測量 ±20%）', '鎖定產能與艙位'],
    ['11 月中–12 月初', '量產／備貨完成、空運或快船來台、清關、貼標質檢', '12/5 前貨到台灣'],
    ['12 月中', '分裝出貨、客服與物流追蹤、結案報告', '12/20 前完成出貨'],
], [32 * mm, 90 * mm, 48 * mm]))
story.append(Paragraph(
    '<b>時程風險提示：</b>原始 Kickstarter 活動本身仍在進行中，原廠對其國際贊助者的交付亦排在年底前後，'
    '12 月為其產能與物流高峰；且 Q4 為空運旺季。務必在合約中鎖定「11 月中前完成本案訂單生產」之條款，'
    '否則 12 月出貨承諾將有跳票風險（建議對贊助者揭露為 12 月底前，保留緩衝）。', st_warnbox))

# ---------- 7. 風險 ----------
story.append(Paragraph('七、風險評估與因應', st_h1))
story.append(tbl([
    ['風險', '等級', '因應措施'],
    ['原廠產能排擠（自家 KS 訂單優先）', '高', '合約鎖定交期與違約條款；提早下單、接受分批出貨'],
    ['價格對比爭議（KS 國際價低於台灣眾籌價）', '中高', '以在地保固、快速到貨、繁中包裝與贈品區隔；定價勿高於 KS 早鳥價 +15%'],
    ['同質競品低價競爭（UGREEN 等）', '中高', '主打磁吸支架整合與鋁合金質感，避開純規格戰'],
    ['BSMI 時程延誤', '中', '8 月即送測；要求原廠提供既有報告加速'],
    ['募資未達損益平衡（<630 台）', '中', '設定達標門檻 NT$60 萬；未達損平即重談單價或退款止損'],
    ['匯率波動（USD/TWD）', '低中', '報價鎖匯或於合約約定匯率區間'],
    ['Q4 物流延誤', '中', '優先空運、預留 2 週緩衝、對外承諾 12 月底'],
], [58 * mm, 18 * mm, 94 * mm]))

# ---------- 8. 結論 ----------
story.append(Paragraph('八、結論與建議', st_h1))
for x in [
    '<b>綜合評等：有條件 GO。</b>商品力與市場驗證俱在，時程緊但可行，前提是採「代理／授權引進」模式並於 8 月底前完成簽約。',
    '損益兩平約 630 台（募資額約 NT$95 萬）。建議達標門檻設 NT$60 萬；若結案僅 400–600 台，啟動 B 方案：與原廠重談單價、縮減上線期廣告、以零售預售補量，或依止損條款退款不出貨。',
    '預熱（9 月）是本案最大槓桿：名單 CPA 控制在 NT$50 以內、蒐集 3,000 筆以上，首 48 小時轉換率 3–5% 即可奠定基準情境。',
    '與原廠談判重點：台灣區域授權、既有認證報告轉用、11 月中前交貨保證、分批出貨彈性與 30% 以下訂金。',
    '若原廠無法保證交期或授權，建議順延至 2027 年 Q1（農曆年前檔期）或改評估同類替代品，勿硬衝 12 月出貨。',
]:
    story.append(Paragraph(f'•  {x}', st_bullet))
story.append(Spacer(1, 6 * mm))
story.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#b8c6d4')))
story.append(Paragraph(
    '免責聲明：本報告之成本與財務數字係依 2026 年 7 月之公開資訊與產業通則推估，僅供內部評估參考；'
    '實際成本以原廠正式報價、檢測機構與物流商報價為準。原始 Kickstarter 活動數據為搜尋快照，非即時數字。', st_note))

doc = SimpleDocTemplate('TwoPan_T11_眾籌評估報告.pdf', pagesize=A4,
                        leftMargin=18 * mm, rightMargin=18 * mm,
                        topMargin=18 * mm, bottomMargin=18 * mm,
                        title='TwoPan T11 眾籌商品評估報告')

def footer(canvas, doc_):
    canvas.saveState()
    canvas.setFont('WQY', 8)
    canvas.setFillColor(colors.HexColor('#999999'))
    canvas.drawCentredString(A4[0] / 2, 10 * mm, f'- {doc_.page} -')
    canvas.restoreState()

doc.build(story, onFirstPage=footer, onLaterPages=footer)
print('OK')
