# -*- coding: utf-8 -*-
"""磁吸 Hub OEM 立項案：專家評審意見書 PDF"""
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

st_title  = S('title', fontSize=24, leading=34, alignment=TA_CENTER, textColor=PRIMARY)
st_sub    = S('sub', fontSize=13, leading=21, alignment=TA_CENTER, textColor=colors.HexColor('#555555'))
st_h1     = S('h1', fontSize=15.5, leading=23, textColor=PRIMARY, spaceBefore=14, spaceAfter=8)
st_h2     = S('h2', fontSize=12.5, leading=19, textColor=ACCENT, spaceBefore=10, spaceAfter=5)
st_body   = S('body', fontSize=10.5, leading=17, alignment=TA_JUSTIFY, spaceAfter=5)
st_bullet = S('bullet', fontSize=10.5, leading=16.5, leftIndent=14, spaceAfter=3)
st_note   = S('note', fontSize=9, leading=13.5, textColor=colors.HexColor('#777777'), spaceAfter=4)
st_tcell  = S('tcell', fontSize=9.5, leading=13.5, spaceAfter=0)
st_tcellc = S('tcellc', fontSize=9.5, leading=13.5, spaceAfter=0, alignment=TA_CENTER)
st_thead  = S('thead', fontSize=9.5, leading=13.5, spaceAfter=0, textColor=colors.white, alignment=TA_CENTER)
st_warn   = S('warn', fontSize=10.5, leading=17, textColor=WARN)
st_expert = S('expert', fontSize=10, leading=16, alignment=TA_JUSTIFY, spaceAfter=4,
              leftIndent=6, textColor=colors.HexColor('#333333'))

def tbl(data, widths, center_cols=None):
    center_cols = center_cols or set()
    rows = []
    for ri, row in enumerate(data):
        out = []
        for ci, cell in enumerate(row):
            if ri == 0:
                out.append(Paragraph(str(cell), st_thead))
            else:
                out.append(Paragraph(str(cell), st_tcellc if ci in center_cols else st_tcell))
        rows.append(out)
    t = Table(rows, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#b8c6d4')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('BACKGROUND', (0, 0), (-1, 0), ACCENT),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT]),
    ]))
    return t

story = []

# ---------- 封面 ----------
story.append(Spacer(1, 52 * mm))
story.append(Paragraph('產品立項專家評審意見書', st_title))
story.append(Spacer(1, 5 * mm))
story.append(Paragraph('磁吸多功能 USB-C Hub 支架 OEM 立項案', st_sub))
story.append(Paragraph('（對標 TwoPan T11・公模貼牌・台灣眾籌首發）', st_sub))
story.append(Spacer(1, 4 * mm))
story.append(HRFlowable(width='60%', thickness=1, color=ACCENT, hAlign='CENTER'))
story.append(Spacer(1, 10 * mm))
story.append(Paragraph('評審形式：五領域專家獨立平行評審 → 彙整共識與放行條件', st_sub))
story.append(Spacer(1, 42 * mm))
story.append(Paragraph('評審日期：2026 年 7 月 23 日', st_sub))
story.append(Paragraph('評審基礎文件：《磁吸 Hub OEM 立項評估報告》（NRE 另列口徑版）', st_note))
story.append(PageBreak())

# ---------- 1. 總覽 ----------
story.append(Paragraph('一、評審總覽', st_h1))
story.append(Paragraph(
    '本次評審由五個領域的專家視角獨立進行，各自僅依據立項評估報告內容出具意見，互不影響。'
    '結果高度一致：<b>五位專家全數給出「有條件 GO」</b>，平均評分 6.0／10——'
    '方向與驗證邏輯獲得肯定，但「時程樂觀、公模護城河薄弱、現金流錯位」三大問題被多位專家獨立點名，'
    '須在簽約前完成對應修正。', st_body))
story.append(tbl([
    ['評審視角', '評分', '一句話總評', '結論'],
    ['供應鏈製造', '6.5', '方向正確、數字有做功課，但時程與獨供條款過度樂觀', '有條件 GO'],
    ['眾籌行銷', '5.5', '財務結構尚可，但品類疲勞加比價劣勢，成敗全繫於預熱名單品質', '有條件 GO'],
    ['財務（CFO）', '6.0', '模型結構清楚、損平點低，但現金流時序過度樂觀', '有條件 GO'],
    ['法規與品質', '6.0', '規劃有基本骨架，但時程過度樂觀且 IP 與品質關卡偏鬆', '有條件 GO'],
    ['產品策略', '5.5', '驗證邏輯成立，但產品無護城河，成敗取決於速度與行銷執行', '有條件 GO'],
], [30 * mm, 14 * mm, 100 * mm, 26 * mm], center_cols={1, 3}))

# ---------- 2. 共識問題 ----------
story.append(Paragraph('二、跨專家共識問題（被兩位以上專家獨立點名）', st_h1))
story.append(Paragraph('2.1 時程過度樂觀（供應鏈、法規、行銷一致點名）', st_h2))
for x in [
    '原時程未計中國十一長假（實損 8–10 個工作天）與 Q4 空運艙位漲價，「9 月試產 → 12/5 到港」幾乎零緩衝。',
    'BSMI「8 月送測、10 月底取證」是一次過測的最佳情境；台灣認可實驗室須重測（CB/CE/FCC 僅供參考），一旦整改複測，整案斷鏈。',
    '眾籌頁面屬販售行為——<b>取證前上線眾籌有違規踩線風險</b>，10 月上線與取證時點高度重疊。',
    '共識修正：對外交付承諾改為 12 月底–2027 年 1 月中；8 月中前送測並預留一次整改週期；上線時點壓在取證後，或頁面明確標示預購性質。',
]:
    story.append(Paragraph(f'•  {x}', st_bullet))
story.append(Paragraph('2.2 公模護城河薄弱（供應鏈、行銷、產品策略一致點名）', st_h2))
for x in [
    '「同模獨供 6–12 個月」對公模廠幾無執行力（換殼再賣防不了），不可作為立項前提，僅能當談判籌碼。',
    '同模低價品 3–6 個月內必現；贊助者一搜蝦皮即見千元內同規格品，早鳥優惠正當性瓦解——比價是本案最致命的行銷風險。',
    '零售價 NT$2,290 已貼近 Satechi 下緣，公模質感撐不起，實際成交價恐回落 1,690–1,890。',
    '共識修正：爭取「改色改刻／外觀件小改模」的最低限度獨佔（成本略增）；零售價下修至 NT$1,990；行銷敘事避開規格戰，聚焦單一強場景與在地保固。',
]:
    story.append(Paragraph(f'•  {x}', st_bullet))
story.append(Paragraph('2.3 現金流錯位與模型漏項（財務點名，供應鏈呼應）', st_h2))
for x in [
    '最大資金缺口在 <b>11 月中下旬</b>：前期投入已全數投出，量產 70% 尾款（約 24 萬）須「出貨前」付清，但平台結案後 7–14 個工作天才撥款——「尾款由撥款支應」的原假設不成立。',
    '含 NRE 的最壞情境資金缺口約 <b>NT$133 萬</b>（80＋29＋24），遠高於報告所列 41–80 萬。',
    '模型漏項：營業稅與發票成本、退款率 2–5%、美元匯損 1–2%、保固準備（5% 備品同時吃保固與零售恐不足）、保守情境庫存跌價。',
    '共識修正：與廠商重談尾款為出貨後 T/T 15–30 天（或降至 50%）；備妥約 130 萬自有資金或過橋額度；模型補入稅務、退款 3%、匯損 2% 重算。',
]:
    story.append(Paragraph(f'•  {x}', st_bullet))
story.append(PageBreak())

# ---------- 3. 各專家意見 ----------
story.append(Paragraph('三、專家個別意見（全文）', st_h1))

experts = [
    ('專家 A｜供應鏈製造（15 年深圳／東莞 3C 週邊經驗）', '6.5／10・有條件 GO', [
        '成本檢驗：IC 組 US$3.6–5.2 高估——VL817＋PS176 等級 HDMI 橋接＋GL823K＋PD 協議 IC 實際約 US$2.8–3.8；報告 BOM 上緣 14.3 與 EXW 報價 8.5–13 自相矛盾，公模廠真實 BOM 約 US$7.5–9.5。1,000 台 EXW 可談到 US$8.5–10；500 台試產單多數廠加價 10–15%。落地 NT$420 在 Q4 空運旺季偏緊，建議抓 NT$450。',
        '盲點一：時程未計十一長假（實損 8–10 工作天）與 Q4 艙位漲價，9 月試產到 12/5 到港幾乎零緩衝；BSMI 約 4–6 週且與量產平行跑，一旦複測整案斷鏈。',
        '盲點二：「同模獨供 6–12 個月」對公模廠幾無執行力，換殼再賣防不了，勿當護城河。',
        '盲點三：公模廠慣性換料——IC 改國產替代、N52 磁鐵降 N45；鎖料號若無封樣加拆機 IQC 比對，形同虛設。',
        '建議：(1) 眾籌交付承諾改 2027 年 1 月中，換取 PP 驗證通過後才下量產單的緩衝；(2) 合約附 BOM 鎖定清單與雙方封存金樣，驗貨納入拆機抽驗、磁吸力實測（≥800g）與 100W 負載熱測（殼溫 ≤45°C）；(3) 試產樣提前送 BSMI，並索取同方案既有 CE/FCC 報告預篩 EMC 風險。',
    ]),
    ('專家 B｜眾籌行銷（30+ 檔台灣募資操盤經驗）', '5.5／10・有條件 GO', [
        '轉換假設檢驗：CPA ≤ NT$50 收表單名單可行，但純名單轉贊助率經驗值僅 3–8%——4,500 筆約產出 150–350 單，離基準 900 台甚遠（名單通常只貢獻首週四至五成訂單）。均價 1,450–1,520 合理，惟眾籌價 1,690 已高於 UGREEN 零售上限。真正該管理的指標是「每贊助者成本」，經驗值 NT$600–900。',
        '盲點一：比價風險致命——贊助者一搜蝦皮即見千元內同規格公模品，早鳥優惠正當性瓦解。',
        '盲點二：Hub 品類在嘖嘖已明顯疲勞，近兩年同類案多停在數十萬規模，難複製 T11 小額目標的高達成率光環。',
        '盲點三：12 月出貨撞 Q4 產能物流高峰，延遲將重創品牌首役信任。',
        '建議：(1) 預熱改「付訂金 100 元抵 300 元」鎖單——訂金名單轉換率可達 30–50%，以訂金數重估三情境；(2) 敘事別打規格，主打台灣品牌、在地一年保固到府換新與磁吸支架情境，上線前安排 10–15 位 3C／辦公 KOL 實測開箱；(3) 天期縮至 30 天、超早鳥擴至 300 名、配 LINE 社群倒數，確保首 48 小時破 60 萬門檻觸發平台流量飛輪。',
        '止損線：訂金未達 800–1,000 筆不上線；低於 500 筆轉電商預購。',
    ]),
    ('專家 C｜財務（消費電子新創 CFO）', '6.0／10・有條件 GO', [
        '漏項檢查：(1) 5% 營業稅與發票成本未列；(2) 退款率（眾籌常見 2–5%）；(3) EXW 美元計價匯損約 1–2% 未提列；(4) 保固與 DOA 換貨準備——5% 備品同時吃保固與零售恐不足；(5) 保守情境 400 台仍須下單 MOQ 500，庫存跌價風險；(6) NRE 不入本檔損益是口徑選擇，但 14–29 萬仍是真實現金流出，資金規劃不得排除。',
        '現金流時序：最大缺口在 11 月中下旬——前期 41–80 萬已全數投出，量產 70% 尾款約 24 萬須「出貨前」付清，而平台結案後 7–14 個工作天才撥款；「尾款由結案撥款支應」的假設不成立。含 NRE 最壞情境缺口約 80＋29＋24 ≈ 133 萬。',
        '建議：(1) 與代工廠重談尾款為出貨後 T/T 15–30 天或降至 50%，消除撥款錯位；(2) 啟動前備妥至少 130 萬自有資金或過橋額度；(3) 模型補入營業稅、退款 3%、匯損 2% 重算三情境，保守情境改以含 NRE 口徑呈現，並設預熱名單門檻作為止損點。',
    ]),
    ('專家 D｜法規與品質（BSMI／IP／QA）', '6.0／10・有條件 GO', [
        '法規檢驗：USB Hub 屬 BSMI 應施檢驗資訊類產品（EMC 依 CNS 13438，無內建電源通常免安規），驗證登錄可行；但 CB/CE/FCC 報告僅供參考，須由台灣認可實驗室重測，「8 月送測、10 月底取證」屬一次過測的最佳情境。免 NCC 判斷成立（無 RF）。',
        '遺漏三項：商品標示法之中文標示與進口商資訊；N52 強磁應加兒童誤食與心律調節器警語；<b>眾籌頁面屬販售行為，取證前不得販售</b>——10 月上線與取證時點高度重疊，踩線風險大。',
        'IP 評估：公模「無侵權聲明」實務效力薄弱——跨境求償困難、方案廠賠償能力有限，且公模一模多賣，可能已有他人在台搶註設計專利；TwoPan 若在台申請設計專利，「不複製外觀」不足以免責，近似即可能侵權。應自行在 TIPO 做設計專利 FTO 檢索，並要求方案廠提供模具權屬與專利證明。',
        '品質漏洞：(a) PD 誘騙與協議相容未列——100W 直通扣自耗後的實際可用瓦數、E-marker 線材相容、與各廠充電器握手異常；(b) 4K60 僅測輸出瞬間，未測滿載長時間熱衰減下的 HDMI 訊號劣化；(c) 磁陣對信用卡／悠遊卡消磁及對 SD 卡影響未驗證；主功能缺陷 AQL 2.5 偏鬆，應收緊至 1.0。',
        '建議：(1) 8 月中前送測並預留一次整改週期，上線壓在取證後或明確標示預購；(2) 簽約前完成台灣設計專利 FTO 檢索，合約提高侵權賠償上限並加列貨款保留條款；(3) 增加 PD 相容矩陣、48 小時滿載老化與磁害驗證，功能缺陷 AQL 收緊至 1.0。',
    ]),
    ('專家 E｜產品策略（USB-C／MagSafe 配件市場）', '5.5／10・有條件 GO', [
        '需求檢驗：MacBook＋iPhone 雙持族在行動辦公、手機當 webcam／副屏、桌面理線等場景確有痛點，「磁吸×Hub」是情境交集的真需求，非偽組合；惟台灣可觸及核心客群估僅數千至低萬人——足以撐起一檔眾籌，難撐長期零售動能。',
        '差異化可持續性：公模＋品牌包裝的窗口期僅約 3–6 個月；同模品殺到千元內後，NT$2,290 已貼近 Satechi 下緣、公模質感撐不起此價，實際成交價恐被迫回到 1,690–1,890。',
        '戰略評價：「先公模驗證、後私模二代」方向正確，但眾籌成績驗證的是行銷力與價格帶，對真實需求規模的推論有限。替代方案：爭取台灣區域獨家窗口＋改色改刻的半私模，成本略增即可取得最低限度獨佔，比純公模更有驗證價值。',
        '建議：(1) 合約鎖定供應商 6 個月內不供台灣同業，並做外觀件小改模；(2) 零售價下修至 NT$1,990，以編織線、收納包等加價購拉高客單與毛利；(3) 行銷聚焦「iPhone 接續互通攝影／視訊會議」單一強場景，結案時回收使用情境問卷，作為二代私模規格依據。',
        '底線：若區域獨家窗口與價格防禦方案皆不可得，NO-GO。',
    ]),
]
for title, score, paras in experts:
    story.append(Paragraph(title, st_h2))
    story.append(Paragraph(f'評分與結論：{score}', st_body))
    for p in paras:
        story.append(Paragraph(f'－ {p}', st_expert))
    story.append(Spacer(1, 2 * mm))

story.append(PageBreak())

# ---------- 4. 修正後關鍵參數 ----------
story.append(Paragraph('四、評審後修正的關鍵參數', st_h1))
story.append(tbl([
    ['參數', '原立項報告', '專家修正後'],
    ['落地成本（1,000 台級）', 'NT$420／台', 'NT$450／台（Q4 空運旺季）'],
    ['EXW 議價目標（1,000 台）', 'US$9.5–11.5', 'US$8.5–10（真實 BOM 約 US$7.5–9.5）'],
    ['對外交付承諾', '2026 年 12 月中', '12 月底–2027 年 1 月中（保留緩衝）'],
    ['上線時點', '10 月上旬', 'BSMI 取證後（或明確標示預購性質）'],
    ['未來零售價', 'NT$2,290', 'NT$1,990（防同模低價品比價）'],
    ['預熱機制', '免費名單（CPA ≤50）', '訂金制（100 抵 300），轉換率 30–50%'],
    ['上線門檻', '名單 3,000 筆', '訂金 800–1,000 筆（<500 筆轉電商預購）'],
    ['前期資金準備', 'NT$41–80 萬', '約 NT$130 萬（含 NRE 與尾款錯位緩衝）'],
    ['功能缺陷驗貨標準', 'AQL 2.5', 'AQL 1.0（外觀維持 2.5）'],
    ['天期', '35–45 天', '30 天（集中火力）'],
], [42 * mm, 58 * mm, 70 * mm]))

# ---------- 5. 放行條件 ----------
story.append(Paragraph('五、立項放行條件（Gate Checklist）', st_h1))
story.append(Paragraph('五位專家一致結論為「有條件 GO」。彙整各專家前置條件如下，<b>全數達成方可簽約放行</b>：', st_body))
story.append(tbl([
    ['#', '放行條件', '負責節點', '期限'],
    ['G1', 'TIPO 設計專利 FTO 檢索完成、無阻卻性近似案；方案廠提供模具權屬與無侵權擔保文件', 'IP／法務', '簽約前'],
    ['G2', '樣品比測通過：PD 相容矩陣、4K60 長時間熱衰減、磁害（信用卡／悠遊卡／SD）、磁吸力 ≥800g、殼溫 ≤45°C', '品質', '8/25'],
    ['G3', '合約條款落地：BOM 鎖料＋雙方封存金樣＋拆機抽驗、尾款改出貨後 T/T 15–30 天（或降 50%）、6 個月不供台灣同業＋外觀件小改模', '採購／法務', '8/31'],
    ['G4', 'BSMI 8 月中前送測，時程含一次整改緩衝；上線時點壓在取證後或標示預購', '法規', '8/15'],
    ['G5', '自有資金或過橋額度 ≥ NT$130 萬到位', '財務', '8/31'],
    ['G6', '財務模型補入營業稅、退款 3%、匯損 2%、落地成本 450 重算，三情境仍為可接受報酬', '財務', '8/31'],
    ['G7', '預熱採訂金制；上線前訂金 ≥800 筆（<500 筆轉電商預購止損）', '行銷', '9/30'],
], [12 * mm, 92 * mm, 32 * mm, 24 * mm], center_cols={0, 3}))
story.append(Paragraph(
    '任一條件未達成：G1–G4 未過 → 順延至 2027 農曆年前檔期或更換方案廠；'
    'G5–G6 未過 → 縮小規模（僅試產 500 台、目標下修）；G7 未過 → 轉電商預購，不上眾籌。', st_warn))

# ---------- 6. 總結論 ----------
story.append(Paragraph('六、評審總結論', st_h1))
for x in [
    '<b>一致結論：有條件 GO（5／5 位專家）</b>，平均評分 6.0／10。立項方向與「低風險驗證＋建品牌」邏輯獲得肯定，但執行假設多處樂觀。',
    '三大核心修正：時程後移（交付改 12 月底–1 月中、上線壓在 BSMI 取證後）、護城河補強（小改模＋區域獨供＋零售價下修 1,990）、資金備足（130 萬，解決 11 月尾款與撥款錯位）。',
    '成敗關鍵指標從「名單數」改為「訂金數」：訂金 800 筆以上才上線，是本案最有效的風險開關。',
    '對原「9 月預熱、12 月出貨」目標的最終判定：預熱 9 月不變；<b>12 月出貨改列「挑戰目標」</b>，對外承諾以 12 月底–1 月中為準——寧可少賣、不可跳票。',
]:
    story.append(Paragraph(f'•  {x}', st_bullet))
story.append(Spacer(1, 6 * mm))
story.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#b8c6d4')))
story.append(Paragraph(
    '說明：本意見書之「專家」為五個獨立領域視角的 AI 評審代理，基於立項評估報告與產業通則出具意見，'
    '非具名人類顧問；引用數字屬經驗區間，執行前應以實際報價與檢測結果驗證。', st_note))

doc = SimpleDocTemplate('磁吸Hub_OEM立項_專家評審意見書.pdf', pagesize=A4,
                        leftMargin=18 * mm, rightMargin=18 * mm,
                        topMargin=18 * mm, bottomMargin=18 * mm,
                        title='磁吸 Hub OEM 立項專家評審意見書')

def footer(canvas, doc_):
    canvas.saveState()
    canvas.setFont('WQY', 8)
    canvas.setFillColor(colors.HexColor('#999999'))
    canvas.drawCentredString(A4[0] / 2, 10 * mm, f'- {doc_.page} -')
    canvas.restoreState()

doc.build(story, onFirstPage=footer, onLaterPages=footer)
print('OK')
