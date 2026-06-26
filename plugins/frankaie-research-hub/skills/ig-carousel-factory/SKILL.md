---
name: ig-carousel-factory
description: >
  LYCANDER AI RESEARCH HUB — IG 輪播工廠（工具型 skill）。
  當使用者要「IG 輪播」、「carousel」、「多圖貼文」、「一次做一整組貼文」、「批量生成貼文」、
  「程式化生圖」、「content.py」、「BASE 風格一鍵切換」、「貼文排程 / 發文行事曆」、
  「雜誌編輯風圖文」時觸發。把「一個產品賣點」展開成一整組品牌一致的 IG 輪播（逐頁 prompt ＋ caption ＋ 發文時段）。
  ⚠️ 這是工具不是角色：負責把整組輪播「企劃 + 文案 + 批量生圖樣板」做出來；
  ⚠️ 與 `ad-hook-writer`（只寫前三秒 hook）、`copy-humanizer`（只潤稿去 AI 味）、
  `visual-team`/`animation-designer`（定創意方向/分鏡）分工——本工具把它們串成「一整組可批量產出的輪播」。
---

# IG 輪播工廠（IG Carousel Factory）

這是一個**工具型 skill**。功能：把**一個產品 + 一個賣點**，展開成一整組**品牌調性一致**的 IG 輪播貼文——逐頁 prompt、逐頁文字、整篇 caption 與建議發文時段，並附「程式化批量生成」樣板。
和 `ad-hook-writer`、`copy-humanizer`、`visual-team`、`animation-designer`、`validation-panel` 搭配——它們各管一段，本工具把它們**串成一整組可重複、可交接、可批量的輪播**。

> 核心理念（改寫自社群「程式化輪播生成」工作流）：
> **一個檔案 = 一整組輪播企劃**。設一個共享的 `BASE` 風格區塊，讓每頁都繼承同一套比例 / 色調 / 排版 / 浮水印，**絕不前後頁風格跳躍**；每頁只負責加上「當頁要講的事」。
> 想換風格時只改 `BASE` 一行，整組圖一鍵換皮——徹底避開「一眼就看穿是 AI」的廉價塑膠感。

---

## 何時用

- 要一次產出**一整組** IG 輪播（封面 + 內頁 + CTA），而不是單張圖。
- 同一個產品要**爆量產出多組**輪播測哪組互動高，且每組都要維持品牌一致。
- 要把「文案企劃」與「視覺 prompt」**綁在同一份 brief** 裡，交給生圖工具批量跑、自動配 caption。
- 要排一個月的 IG 內容，且每篇都要對應**發文日期 / 時段**。

## 需要的輸入（缺的會主動問）

1. **產品** + 這組輪播要主打的**單一**賣點 / 痛點（聚焦，不要一篇講十個賣點）。
2. **品牌風格錨點**：色調、字體調性、是否要產品實拍感 vs 插畫感、浮水印 / 帳號（預設 `@lycander.tw`）。
3. **頁數**（預設 6 頁）與**輪播結構**（預設：封面 → 痛點 → 解法/規格 → 使用情境 → 社會證明 → CTA）。
4. **平台與受眾**（IG 為主；受眾是誰、什麼情境滑到）。
5.（可選）**發文日期 / 時段**——若未提供真實 IG Insights，本工具會以大盤基準排程並標 `【需數據】`，待回填真實數據校準。

## 運作流程

1. **定 BASE**：把比例（IG 輪播建議 `4:5 portrait`）、視覺調性、品牌色、字體感、浮水印寫成一段共享字串。
2. **拆頁**：依輪播結構，每頁寫一句「這頁要讓人 get 到什麼」，再轉成 `BASE + 當頁具體畫面/字卡` 的 prompt。
   - 封面那頁的主標，**直接引用 `ad-hook-writer` 的前三秒 hook**（滑不走的開頭）。
3. **寫 caption**：首句 = hook、中段 = 價值 / 規格（未證實規格標 `【需查證】`）、結尾 = CTA + hashtag。
   - caption 草稿過一輪 `copy-humanizer` 去 AI 味、貼品牌語氣。
4. **批量樣板**：把所有頁整理成 `slides` 陣列（檔名, prompt），交給生圖工具並行批量產出 + 自動生成 `caption.txt`（樣板見下）。
5. **驗證**：整組丟 `validation-panel` / `consumers-taiwan` 等虛擬焦點小組打 1–5 購買意願，低分頁回到步驟 2 換 hook / 換畫面。
6. **排程**：把每篇掛上發文日期 / 時段（接 `marketing-team` 月度社群日曆）。

---

## 輸出範本

### 1) `content.py` 風格 brief（一個檔案 = 一整組輪播）

```python
# content.py — <產品>｜主打：<單一賣點>｜<日期>

# 1) 共享風格區塊（改這一段＝整組一鍵換皮）
BASE = "4:5 portrait. <視覺調性，如 Cream editorial 奶油色雜誌編輯風>. " \
       "<品牌色/字體感>. watermark @lycander.tw"

# 2) 逐頁 prompt（BASE + 當頁內容）
COVER  = BASE + "封面：<hook 主標（取自 ad-hook-writer）> + 產品主視覺"
PAGE_2 = BASE + "痛點：<受眾正在受的苦的畫面>"
PAGE_3 = BASE + "解法/規格：<產品如何解，關鍵規格【需查證】>"
PAGE_4 = BASE + "使用情境：<受眾日常使用畫面>"
PAGE_5 = BASE + "社會證明：<評價/數據/UGC 風格，數字【需查證】>"
CTA    = BASE + "行動呼籲：<留言關鍵字/點主頁連結>"

# 3) 輪播陣列（檔名, prompt）→ 交批量生圖
slides = [
    ("01_cover.png", COVER),
    ("02_pain.png",  PAGE_2),
    ("03_solution.png", PAGE_3),
    ("04_scene.png", PAGE_4),
    ("05_proof.png", PAGE_5),
    ("06_cta.png",   CTA),
]
```

> 創作者筆記：把 `BASE` 的 `"Cream editorial"` 換成 `"Cinematic real product photography"`，整組圖就從雜誌風一鍵切成真實系商業攝影——同一份文案、兩種風格 A/B。

### 2) caption 範本（每篇一份，對應 caption.txt）

```
# <貼文標題>｜<發文日期 時段>
[首句 hook]  ← 滑到就停的那句
[價值/規格]  ← 2–3 句，未證實規格標【需查證】
[CTA]        ← 留言 / 點主頁連結 / 導購
[hashtag]    ← 5–10 個（品牌 + 品類 + 情境），避免無關熱門 tag
```

### 3) 發文行事曆表（一個月一張）

| 日期 | 星期 | 時段 | 主題 | 商品 | 形式 | 對應 brief | 預期觸及【需數據】 |
|------|------|------|------|------|------|------------|--------------------|
| 7/1 | 二 | 12:30【需數據】 | … | … | 輪播 | content_0701.py | … |

---

## 批量生成樣板（generate.py 概念，純參考）

> 與來源工作流一致：用執行緒池並行呼叫生圖 API、跳過已存在檔案（斷點續傳）、順手生 caption。實際生圖可改接本環境可用的設計 / 生圖工具。

```python
import concurrent.futures, os
from content import slides   # 引入上面那份 brief

def generate_image(filename, prompt):
    if os.path.exists(filename):
        return f"SKIP {filename}"          # 斷點續傳
    # image = call_image_api(prompt); save(filename, image)
    return f"OK {filename}"

with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
    futs = [ex.submit(generate_image, f, p) for f, p in slides]
    for fut in concurrent.futures.as_completed(futs):
        print(fut.result())
# 另把每頁 caption 寫進同資料夾 caption.txt，發布直接複製貼上
```

---

## 實例演練（Worked Example）

**輸入**：65W GaN 充電器｜主打單一賣點「快充不發燙」｜受眾：通勤上班族｜風格：奶油色雜誌編輯風。

**BASE**：`"4:5 portrait. Cream editorial. warm beige, clean sans-serif. watermark @lycander.tw"`

**逐頁（節錄）**：
| 頁 | 角色 | prompt 重點 | 文字 |
|----|------|-------------|------|
| 01 封面 | hook | 手摸充電器縮手的瞬間 | 「充電器不該燙到不敢摸」 |
| 03 解法 | 規格 | 產品 + 熱顯示低溫 | 「同樣 65W，低 12°C【需查證】」 |
| 06 CTA | 導購 | 留言關鍵字 | 「留言『不燙』拿連結」 |

**caption（節錄）**：`充電器充一充就燙到不敢摸？/ 65W GaN，實測比舊款低 12°C【需查證】，塞包包也安心 / 留言「不燙」我私訊連結 #LYCANDER #GaN充電器 #快充 #通勤神器`

> 一鍵換皮：把 BASE 改成 `"Cinematic real product photography"`，同一份文案立刻產出真實系版本做 A/B。

## 與團隊串接

- **上游 / 平行**：封面 hook 取自 `ad-hook-writer`；風格錨點 / 分鏡方向接 `visual-team`、`animation-designer`；痛點 / 賣點素材可由 `review-miner`、`consumers-taiwan`（虛擬焦點小組）提供。
- **文案**：caption 草稿交 `copy-humanizer` 去 AI 味、貼品牌語氣。
- **驗證**：整組輪播丟 `validation-panel` 調度 `consumers-taiwan`/`consumers-usa`/`consumers-japan`/`consumers-europe` 打 1–5 購買意願，低分頁迭代。
- **下游**：發文時段接 `marketing-team` 月度社群日曆；上線後觸及 / 互動 / 轉換回 `data-analyst`、`marketing-team` 迭代；導購成效接 `web-engineer`（埋點）。

> 提醒：輪播可以有張力，但任何規格 / 數據 / 認證主張無一手依據一律標 `【需查證】`；發文時段未接真實 IG Insights 一律標 `【需數據】`，不誇大、不杜撰、不臆造效能。
