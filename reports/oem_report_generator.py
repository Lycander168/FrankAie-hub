# -*- coding: utf-8 -*-
"""磁吸多功能 USB-C Hub OEM 立項評估報告 PDF 產生器（對標 TwoPan T11）"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
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

st_title   = S('title', fontSize=25, leading=35, alignment=TA_CENTER, textColor=PRIMARY)
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

def tbl(data, widths, header=True):
    rows = []
    for ri, row in enumerate(data):
        out = []
        for ci, cell in enumerate(row):
            if ri == 0 and header:
                out.append(Paragraph(str(cell), st_thead))
            else:
                out.append(Paragraph(str(cell), st_tcell if ci == 0 else st_tcellc))
        rows.append(out)
    t = Table(rows, colWidths=widths, repeatRows=1 if header else 0)
    style = [
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#b8c6d4')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('BACKGROUND', (0, 0), (-1, 0), ACCENT),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT]),
    ]
    t.setStyle(TableStyle(style))
    return t

story = []

# ---------- 封面 ----------
story.append(Spacer(1, 55 * mm))
story.append(Paragraph('OEM 立項評估報告', st_title))
story.append(Spacer(1, 6 * mm))
story.append(Paragraph('磁吸多功能 USB-C Hub 支架（自有品牌）', st_sub))
story.append(Paragraph('對標產品：TwoPan T11（Kickstarter）', st_sub))
story.append(Spacer(1, 4 * mm))
story.append(HRFlowable(width='60%', thickness=1, color=ACCENT, hAlign='CENTER'))
story.append(Spacer(1, 10 * mm))
story.append(Paragraph('銷售模式：眾籌（群眾募資）首發', st_sub))
story.append(Paragraph('預熱時間：2026 年 9 月　｜　出貨時間：2026 年 12 月', st_sub))
story.append(Spacer(1, 38 * mm))
story.append(Paragraph('報告日期：2026 年 7 月 23 日（OEM 立項版，取代代理引進版）', st_sub))
story.append(Paragraph('資料來源：Kickstarter 公開頁面、電商通路公開資訊、供應鏈通行報價區間', st_note))
story.append(PageBreak())

# ---------- 1. 執行摘要 ----------
story.append(Paragraph('一、執行摘要', st_h1))
story.append(Paragraph(
    '本報告以 OEM 立項角度評估：以 TwoPan T11（7-in-1 磁吸 USB-C Hub 支架，Kickstarter 達成率逾 1,076%）'
    '為對標規格，委託方案廠製造<b>自有品牌</b>產品，透過眾籌首發。與代理引進相比，OEM 模式單位成本可自'
    ' NT$600–750 降至 <b>NT$330–480</b>，毛利結構顯著改善，且品牌與通路資產累積在自己手上；'
    '代價是需承擔 NRE（開發性一次費用）、MOQ 庫存風險與全部品質／保固責任。', st_body))
story.append(Spacer(1, 2 * mm))
concl = tbl([
    ['評估面向', '結論'],
    ['可行路徑', '三條路徑中，<b>僅路徑 A「公模貼牌」可確保 12 月出貨</b>；路徑 B「半公模改殼」為極限排程；路徑 C「全私模自研」不可行（順延 2027 Q1–Q2）'],
    ['單位落地成本', '路徑 A 約 NT$330–480／台（EXW US$8–13 ＋運稅檢），取基準 NT$420'],
    ['NRE 一次費用', '路徑 A 約 NT$15–35 萬（樣品、絲印／雷雕、彩盒、BSMI）；路徑 B 另加模具 NT$15–30 萬'],
    ['MOQ', '公模 500–1,000 台起；量產階梯 1,000／2,000 台有明顯降價'],
    ['損益口徑', 'NRE（約 NT$25 萬）列為公司立項投資、由後續產品線攤提，<b>不計入本檔眾籌損益</b>'],
    ['損益兩平', '約 270 台（募資額約 NT$40 萬）'],
    ['基準情境損益', '900 台、營收 NT$135 萬，稅前淨利約 NT$38 萬（約 28%）；樂觀 2,000 台淨利約 NT$116 萬（38%）'],
    ['前期資金需求', '約 NT$41–80 萬（不含 NRE 及量產貨款尾款；NRE 約 14–29 萬另列立項投資預算）'],
    ['綜合建議', '<b>有條件 GO</b>：8 月底前完成選廠、樣品驗證與試產合約；差異化不足時以品牌、在地保固與加價購補強'],
], [38 * mm, 132 * mm])
story.append(concl)

# ---------- 2. 立項背景 ----------
story.append(Paragraph('二、立項背景與對標分析', st_h1))
story.append(Paragraph('2.1 對標產品：TwoPan T11', st_h2))
story.append(tbl([
    ['項目', '對標資訊（依公開資料整理）'],
    ['產品', 'Twopan T11：Portable Magnetic Multi-port USB-C Hub Stand（7-in-1）'],
    ['規格', 'USB-C PD 100W 直通、HDMI 4K@60Hz、USB 3.2（5Gbps）資料埠、SD／TF 讀卡、MagSafe 相容磁吸支架、鋁合金口袋型'],
    ['市場驗證', 'Kickstarter 目標 HK$10,000，快照達成率逾 1,076%（距結束約 4 週）；品牌另有 Amazon／BestBuy 通路與兩次成功眾籌紀錄'],
    ['啟示', '「磁吸支架 × Hub」的複合訴求可轉單，但募資量級為中小型；台灣市場合理期望值為數百至兩千台'],
], [30 * mm, 140 * mm]))
story.append(Paragraph('2.2 為何選擇 OEM 而非代理', st_h2))
story.append(tbl([
    ['比較項', '代理引進', 'OEM 自有品牌'],
    ['單位落地成本', 'NT$600–750', 'NT$330–480'],
    ['毛利率（均價 NT$1,500）', '約 50–60%', '約 68–78%'],
    ['一次性投入', '低（NT$5–29 萬）', '中（NT$15–65 萬，視路徑）'],
    ['品牌／通路資產', '歸原廠，續約有風險', '歸自己，可延伸產品線'],
    ['品質與保固責任', '原廠承擔為主', '<b>全數自負</b>（需驗廠與抽檢把關）'],
    ['庫存風險', '可小量下單', '受 MOQ 約束（500–1,000 起）'],
    ['12 月出貨可行性', '可行（依賴原廠產能）', '公模路徑可行；私模不可行'],
], [42 * mm, 62 * mm, 66 * mm]))
story.append(Paragraph(
    '結論：若定位為「做一檔生意」，代理較輕；若定位為「建立自有 3C 配件品牌並累積供應鏈能力」，'
    'OEM 是正確起點，且成本結構足以支撐後續零售與電商長尾銷售。本報告以 OEM 為基礎展開。', st_body))
story.append(PageBreak())

# ---------- 3. 路徑選擇 ----------
story.append(Paragraph('三、OEM 路徑選擇', st_h1))
story.append(tbl([
    ['項目', '路徑 A：公模貼牌', '路徑 B：半公模改殼', '路徑 C：全私模自研'],
    ['作法', '方案廠現成公模（磁吸 Hub 支架），客製 Logo、配色、彩盒', '沿用公板 PCBA，開私模外殼（CNC／壓鑄）', '外觀＋結構＋電子全自主設計'],
    ['NRE 費用', 'NT$15–35 萬（含 BSMI）', 'NT$35–65 萬（含模具 15–30 萬）', 'NT$60–120 萬以上'],
    ['單位成本（EXW）', 'US$8–13', 'US$10–15', 'US$11–17'],
    ['MOQ', '500–1,000', '1,000–2,000', '2,000–3,000'],
    ['開發＋量產週期', '45–75 天', '100–130 天', '120–180 天'],
    ['差異化程度', '低（同模多品牌）', '中（外觀獨佔）', '高（可申請專利）'],
    ['12 月出貨', '<b>可行</b>', '極限（8 月底前定案且零失誤）', '不可行'],
], [28 * mm, 47 * mm, 47 * mm, 48 * mm]))
story.append(Paragraph(
    '<b>建議：本檔眾籌採路徑 A</b>，以品牌、包裝、加價購與在地服務創造差異；同步啟動路徑 B 之外殼設計，'
    '作為 2027 年二代私模產品（眾籌驗證需求 → 私模放大毛利與差異化，為 3C 配件品牌的標準演進路線）。'
    '路徑 A 需注意：公模可能同時供給其他品牌（含陸廠低價品牌），上市後 3–6 個月內恐出現同模低價品，'
    '故眾籌檔期的「首發時間窗」價值極高。', st_body))

# ---------- 4. 規格定義 ----------
story.append(Paragraph('四、產品規格定義（立項目標規格）', st_h1))
story.append(tbl([
    ['模組', '目標規格', '選型備註'],
    ['上行埠', 'USB-C（PD 3.0 100W 充電直通）', 'E-Marker 線材、PD 誘騙／直通電路'],
    ['影像輸出', 'HDMI 2.0 4K@60Hz', 'DP Alt-Mode 轉 HDMI（PS176／ANX 等級 IC）'],
    ['資料埠', 'USB 3.2 Gen1 5Gbps ×2（A 或 C）＋ USB 2.0 ×1', 'VL817／GL3510 等級主控'],
    ['讀卡', 'SD ＋ TF（UHS-I）', 'GL823K 等級'],
    ['磁吸支架', 'MagSafe 相容 N52 磁陣（吸力 ≥ 800g）、直立／橫放雙向', '含軟膠防刮面'],
    ['外殼', '鋁合金＋陽極處理，口袋型（≤ 100g）', '公模既有規格內挑選'],
    ['相容性', 'macOS／iPadOS／iOS／Windows／Android 免驅動', '出貨前全平台相容性測試'],
    ['認證', 'BSMI（台灣必要）；CE／FCC（沿用方案廠報告）', '無 RF，免 NCC'],
], [28 * mm, 76 * mm, 66 * mm]))
story.append(Paragraph(
    '智財注意：不得複製 T11 之外觀設計（外觀專利／著作權風險）；公模之外觀權利屬方案廠，'
    '簽約時應取得「無侵權聲明與擔保條款」，並確認該公模未被對標品牌註冊外觀專利。', st_warnbox))
story.append(PageBreak())

# ---------- 5. 成本結構 ----------
story.append(Paragraph('五、成本結構預估（路徑 A 為主）', st_h1))
story.append(Paragraph('5.1 量產單位成本（階梯報價）', st_h2))
story.append(tbl([
    ['數量級', 'EXW 單價（US$)', '落地成本（NT$）', '說明'],
    ['500 台（試產／小量）', '11–13', '約 430–500', '含空運攤提 NT$25–40、營業稅 5%、抽檢貼標 NT$12'],
    ['1,000 台', '9.5–11.5', '約 380–450', '基準採用帶；本模型取 NT$420'],
    ['2,000 台', '8.5–10', '約 340–400', '樂觀情境取 NT$400'],
    ['3,000 台以上', '8–9', '約 320–370', '轉海運可再降 NT$15–25'],
], [38 * mm, 33 * mm, 36 * mm, 63 * mm]))
story.append(Paragraph('參考 BOM 拆解（1,000–2,000 台量級，供議價校驗用）：', st_body))
story.append(tbl([
    ['BOM 項目', '單價（US$）'],
    ['Hub 主控＋PD＋HDMI 轉換＋讀卡 IC 組', '3.6–5.2'],
    ['連接器組（USB-C×2、USB-A、HDMI、SD/TF 槽）', '1.2–1.8'],
    ['PCB＋SMT＋組裝測試（含治具攤提）', '1.8–2.6'],
    ['鋁合金外殼＋陽極（公模）', '1.6–2.6'],
    ['磁陣（N52）＋鐵片＋軟膠', '0.6–1.0'],
    ['彩盒＋說明書＋內襯', '0.7–1.1'],
    ['<b>合計（含廠商毛利前）</b>', '<b>約 9.5–14.3</b>'],
], [110 * mm, 60 * mm]))
story.append(Paragraph('註：方案廠 EXW 報價通常為 BOM ＋ 10–20% 廠利；上表用於判斷報價合理性，非直接採購價。', st_note))

story.append(Paragraph('5.2 NRE 一次性費用', st_h2))
story.append(tbl([
    ['項目', '金額（NT$）', '說明'],
    ['樣品（3–5 家 ×2 台）＋快遞', '15,000–30,000', '選廠比測：埠速、發熱、磁力、相容性'],
    ['Logo 雷雕／絲印製版＋配色打樣', '20,000–50,000', '陽極色板費另計'],
    ['彩盒＋包材結構設計與打樣', '30,000–60,000', '含繁中說明書設計'],
    ['BSMI 驗證登錄（自有品牌名義）', '60,000–120,000', '可沿用方案廠 CB／FCC 報告加速，仍需台灣測試'],
    ['第三方驗貨（試產＋量產各一次）', '16,000–30,000', 'AQL 2.5 抽檢'],
    ['<b>合計</b>', '<b>約 141,000–290,000</b>', '取 NT$25 萬；<b>列為立項投資、不計入本檔眾籌損益</b>'],
], [55 * mm, 40 * mm, 75 * mm]))
story.append(Paragraph(
    '付款條件通行慣例：試產訂金 30–50%、量產 30% 訂金＋出貨前 70% 尾款；'
    '基準情境（1,000 台 × EXW 約 US$10.5）貨款約 NT$34 萬，需自備訂金約 NT$10–17 萬作為過橋資金，'
    '尾款可於眾籌結案撥款後支付。', st_body))
story.append(PageBreak())

# ---------- 6. 財務模型 ----------
story.append(Paragraph('六、眾籌財務模型與情境分析', st_h1))
story.append(Paragraph('6.1 假設', st_h2))
story.append(tbl([
    ['參數', '假設值', '備註'],
    ['定價階梯', '超早鳥 NT$1,290（限 100）／早鳥 NT$1,490／眾籌價 NT$1,690', '未來零售 NT$2,290'],
    ['實收均價', 'NT$1,450–1,520', '含階梯混合與加價購（磁吸環貼片、收納袋）'],
    ['平台＋金流費', '募資額 10.5%', '台灣平台 8% ＋金流 2.5%'],
    ['行銷費', '預熱固定 NT$15–22 萬＋上線期募資額 12%', '合計約占募資額 22–28%'],
    ['出貨物流', 'NT$70／件', '台灣本島宅配含包材'],
    ['貨物落地成本', 'NT$420–430／台（依量級）', '樂觀情境 NT$400'],
    ['下單量', 'max（售出台數＋5% 備品, MOQ 500）', '超出部分轉為零售庫存（以成本計入本檔）'],
    ['NRE 處理', '<b>不計入本檔損益</b>', '約 NT$25 萬列為立項投資，由眾籌＋零售＋二代產品攤提'],
], [38 * mm, 72 * mm, 60 * mm]))

story.append(Paragraph('6.2 三情境損益試算', st_h2))

def scenario(units, avg_price, goods, order_qty, ship=70, plat_rate=0.105,
             mkt_rate=0.12, preheat=180000, onetime=0):
    rev = units * avg_price
    plat = rev * plat_rate
    mkt = rev * mkt_rate + preheat
    cogs = order_qty * goods
    logi = units * ship
    profit = rev - plat - mkt - cogs - logi - onetime
    return rev, plat, mkt, cogs, logi, onetime, profit

sc = {
    '保守': scenario(400, 1450, 430, 500, preheat=150000),
    '基準': scenario(900, 1500, 420, 1000, preheat=180000),
    '樂觀': scenario(2000, 1520, 400, 2100, preheat=220000),
}
def f(n):
    return f'{n/10000:,.1f} 萬'
rows = [['項目', '保守情境', '基準情境', '樂觀情境'],
        ['售出台數／均價', '400 台／NT$1,450', '900 台／NT$1,500', '2,000 台／NT$1,520'],
        ['下單量（含 MOQ／備品）', '500 台', '1,000 台', '2,100 台']]
labels = [(0, '募資總額'), (1, '平台＋金流費'), (2, '行銷費（含預熱）'),
          (3, '貨物成本（依下單量）'), (4, '出貨物流'), (6, '<b>稅前損益（不含 NRE）</b>')]
for i, lab in labels:
    r = [lab]
    for k in ['保守', '基準', '樂觀']:
        cell = f(sc[k][i])
        if i == 6:
            cell = f'<b>{cell}</b>'
        r.append(cell)
    rows.append(r)
margin_row = ['稅前淨利率']
for k in ['保守', '基準', '樂觀']:
    margin_row.append(f'{sc[k][6]/sc[k][0]*100:,.1f}%')
rows.append(margin_row)
stock_row = ['期末庫存（可轉零售）', '100 台（成本約 4.3 萬）', '100 台（成本約 4.2 萬）', '100 台（成本約 4.0 萬）']
rows.append(stock_row)
story.append(tbl(rows, [45 * mm, 41 * mm, 42 * mm, 42 * mm]))
story.append(Paragraph(
    '解讀（NRE 不計入本檔）：每台邊際貢獻約 NT$650–670（售價扣平台費、貨物含 5% 備品、物流與變動行銷），'
    '本檔固定支出僅剩預熱行銷約 NT$15–18 萬，<b>損益兩平約 270 台（募資額約 NT$40 萬）</b>——'
    '門檻低，三情境皆為正報酬：保守約 +5.6 萬（10%）、基準約 +38 萬（28%）、樂觀約 +116 萬（38%）。'
    '每台邊際貢獻較代理模式高出約 37%，量級放大後差距快速拉開，且期末庫存與品牌資產可延伸至電商零售。'
    '需注意：NRE 約 25 萬另列立項投資——以基準情境計，本檔檔期利潤已可全額回收 NRE 並有餘裕；'
    '保守情境則需靠後續零售銷售攤提（含全案口徑時保守情境實為虧損約 19 萬），'
    '故達標門檻與止損機制（見第九章）仍不可省略。', st_body))

story.append(Paragraph('6.3 前期資金需求（不含 NRE 與量產貨款尾款）', st_h2))
story.append(tbl([
    ['項目', '金額（NT$）'],
    ['素材製作（攝影、影片、募資頁）', '80,000–150,000'],
    ['預熱期廣告（9 月，名單蒐集）', '150,000–300,000'],
    ['KOL／公關種子合作', '50,000–120,000'],
    ['試產＋量產訂金（30%，基準 1,000 台）', '100,000–170,000'],
    ['雜支與備用金', '30,000–60,000'],
    ['<b>合計</b>', '<b>約 410,000–800,000</b>'],
], [100 * mm, 70 * mm]))
story.append(Paragraph(
    'NRE（約 NT$14–29 萬，見 5.2）另列公司立項投資預算，不佔本檔營運資金；'
    '量產尾款（約 NT$24 萬）由眾籌結案撥款支應。', st_body))
story.append(PageBreak())

# ---------- 7. 供應商 ----------
story.append(Paragraph('七、供應鏈與選廠策略', st_h1))
story.append(Paragraph(
    '磁吸 Hub 支架公模方案集中於深圳／東莞之 USB 週邊方案廠（多同時供貨歐美白牌與亞馬遜品牌）。'
    '建議 8 月第一週即發 RFQ 給 4–6 家，並以下列標準篩選：', st_body))
story.append(tbl([
    ['篩選構面', '合格標準'],
    ['方案能力', '支援 PD 3.0 100W 直通、DP Alt-Mode 4K@60Hz、UHS-I 讀卡；提供 IC 料號清單（防後續偷換料）'],
    ['認證基礎', '既有 CE／FCC／RoHS 報告可查驗；願配合 BSMI 送測提供技術文件'],
    ['品質體系', 'ISO 9001；接受第三方驗貨（AQL 2.5）與 3% 備品；不良率承諾與換貨條款'],
    ['商務條件', 'MOQ ≤ 1,000、樣品 7 天內、試產 15 天、量產 30–35 天；訂金 ≤ 30%'],
    ['智財與獨佔', '無侵權聲明擔保；爭取台灣市場 6–12 個月同模獨供（或以年採購量交換）'],
], [35 * mm, 135 * mm]))
story.append(Paragraph(
    '選廠流程：RFQ（第 1 週）→ 樣品比測（第 2–3 週：實測 4K60 輸出、SSD 讀寫 5Gbps、滿載發熱 ≤ 45°C、'
    '磁吸力、iPhone/iPad/Mac/Win 相容）→ 試產 500 台驗貨 → 簽量產框架合約。'
    '樣品比測務必做「滿載長時間」測試——公模 Hub 最常見翻車點是 PD 大功率＋4K 輸出同時運作的過熱降速。', st_body))

# ---------- 8. 時程 ----------
story.append(Paragraph('八、時程規劃（2026/7 → 2026/12，路徑 A）', st_h1))
story.append(tbl([
    ['期間', '工作項目', '關鍵節點'],
    ['7 月底–8 月中', 'RFQ 發出、樣品比測、規格與配色定案', '8/15 前完成選廠'],
    ['8 月中–8 月底', '簽約＋下試產單（500 台）、BSMI 送測、包裝定稿', '<b>8/31 立項死線：未完成即順延</b>'],
    ['9 月（預熱）', '素材拍攝、募資頁、前導頁廣告蒐集名單；試產完成＋驗貨', '名單 3,000–6,000 筆、CPA ≤ NT$50'],
    ['10 月上旬–11 月中', '正式上線 35–45 天；10 月底依曲線下量產追加單', '首週達成率 ≥ 60%；BSMI 取證'],
    ['11 月中–12 月初', '量產完成、驗貨、空運來台、清關貼標', '12/5 前貨到'],
    ['12 月中', '分裝出貨、客服追蹤、結案報告', '12/20 前完成出貨'],
], [32 * mm, 90 * mm, 48 * mm]))
story.append(Paragraph(
    '<b>時程風險提示：</b>路徑 A 的緩衝僅約 2 週，且集中在「BSMI 取證」與「量產追加單」兩點。'
    '（1）BSMI 若 10 月底前未取證，12 月出貨即違規——8 月送測不可拖延；'
    '（2）追加單超過試產量 3 倍時，方案廠備料（主控 IC、鋁料）可能斷鏈，簽約時應要求鎖定 2,000 台份物料；'
    '（3）Q4 空運旺季艙位需 11 月初預訂。任一節點失守，對外承諾應立即改口 12 月底／1 月初並主動溝通。', st_warnbox))
story.append(PageBreak())

# ---------- 9. 風險 ----------
story.append(Paragraph('九、風險評估與因應', st_h1))
story.append(tbl([
    ['風險', '等級', '因應措施'],
    ['公模同質品低價競爭（同模多品牌）', '高', '爭取台灣同模獨供條款；以品牌、保固、加價購與首發時間窗建立區隔'],
    ['品質責任自負（過熱、相容性、退貨潮）', '高', '樣品滿載實測＋試產 AQL 2.5 驗貨＋3% 備品；保固金提列營收 2%'],
    ['BSMI 取證延誤', '中高', '8 月送測；選有 CB／FCC 報告之方案廠加速；取證前不出貨'],
    ['MOQ 庫存風險（募資不如預期）', '中高', '試產 500 台起步、量產依募資曲線追加；期末庫存轉電商零售'],
    ['對標品牌（Twopan）進入台灣市場', '中', '搶 12 月首發；價格帶錯開（低其零售價 20% 以上）'],
    ['方案廠偷換料／量產品質漂移', '中', '合約鎖 IC 料號＋量產抽檢比對；尾款於驗貨合格後支付'],
    ['募資量偏低（<270 台未達檔期損平；<600 台難回收 NRE）', '中', '達標門檻設 NT$60 萬；量低僅出試產量、餘轉零售、停止追單'],
    ['匯率與運價波動', '低中', '報價鎖匯 30 天；空運報價預留 15% 緩衝'],
], [58 * mm, 18 * mm, 94 * mm]))

# ---------- 10. 結論 ----------
story.append(Paragraph('十、結論與建議', st_h1))
for x in [
    '<b>綜合評等：有條件 GO。</b>OEM 公模貼牌路徑可同時滿足「9 月預熱、12 月出貨」與自有品牌立項目標；死線為 8/31 前完成選廠、樣品驗證與試產合約。',
    '財務結構（NRE 另列立項投資）：單位落地成本 NT$420（代理約 NT$600–650），本檔損平僅約 270 台（募資額約 NT$40 萬），三情境皆正報酬——保守 +5.6 萬（10%）、基準 +38 萬（28%）、樂觀 +116 萬（38%）；基準情境檔期利潤即可全額回收另列之 NRE。本檔前期資金需求約 41–80 萬（不含 NRE）。',
    '本檔眾籌的戰略價值在「以低風險驗證需求＋建立品牌與供應鏈」：結案數據直接決定是否啟動二代私模（路徑 B）放大差異化與毛利。',
    '兩大自負風險需以制度對沖：品質（樣品滿載實測、試產驗貨、保固金 2%）與庫存（試產 500 起步、依曲線追單、達標門檻 NT$60 萬止損）。',
    '若 8/31 前無法完成選廠簽約，或樣品比測全數未過滿載測試，建議順延至 2027 農曆年前檔期，勿以未驗證公模硬衝 12 月。',
]:
    story.append(Paragraph(f'•  {x}', st_bullet))
story.append(Spacer(1, 6 * mm))
story.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#b8c6d4')))
story.append(Paragraph(
    '免責聲明：本報告之成本與財務數字係依 2026 年 7 月之公開資訊與供應鏈通行報價區間推估，僅供內部立項評估；'
    '實際成本以方案廠正式報價、檢測機構與物流商報價為準。對標產品之 Kickstarter 數據為搜尋快照，非即時數字。', st_note))

doc = SimpleDocTemplate('磁吸Hub_OEM立項評估報告.pdf', pagesize=A4,
                        leftMargin=18 * mm, rightMargin=18 * mm,
                        topMargin=18 * mm, bottomMargin=18 * mm,
                        title='磁吸多功能 USB-C Hub OEM 立項評估報告')

def footer(canvas, doc_):
    canvas.saveState()
    canvas.setFont('WQY', 8)
    canvas.setFillColor(colors.HexColor('#999999'))
    canvas.drawCentredString(A4[0] / 2, 10 * mm, f'- {doc_.page} -')
    canvas.restoreState()

doc.build(story, onFirstPage=footer, onLaterPages=footer)
print('OK')
