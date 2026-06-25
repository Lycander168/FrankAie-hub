# 德誼 Roadshow 活動簡報 · Wokyis × LYCANDER

交付對象：**行銷協作公司**　|　版本：**v1**　|　產出日期：2026.06.25

## 檔案
- `德誼Roadshow活動簡報_WokyisxLYCANDER_v1.pptx` — 主交付物，**可編輯** PowerPoint（16:9，12 頁）
- `build_deck.py` — 簡報產生器原始碼（python-pptx），調整文案／配色後可重新產出

## 簡報結構（12 頁）
1. 封面
2. 活動總覽・一頁看懂
3. 活動目的與策略目標
4. 活動檔期與場地（7/5 新竹巨城、7/12 台北三創）
5. 主題品牌與商品線（Wokyis × LYCANDER）
6. 核心優惠：快閃 9 折
7. 加碼贈品：買 Wokyis M5 雙重送
8. 滿額好禮：單筆滿千即送
9. 優惠機制總表（一頁掌握）
10. 現場執行重點（建議）
11. 行銷協作分工與時程（建議）
12. KPI 與後續 / 聯絡窗口

## 活動重點摘要
| 項目 | 內容 |
| --- | --- |
| 檔期 | 7/5（日）新竹巨城、7/12（日）台北三創 |
| 主題品牌 | Wokyis、LYCANDER |
| 核心優惠 | 快閃 **9 折** |
| 加碼贈品 | 買 **Wokyis M5** 雙重送：①【LYCANDER】Mac Mini M4 & M4 Pro 鋁合金支架 ②【LYCANDER】HDMI 2.1 8K 影音傳輸線（1.5M） |
| 滿額贈 | 單筆結帳滿 **$1,000** 送【YOYOISLES】Air Stars AirTag 保護套（市值 $190） |

## 給行銷公司的編輯提醒
- **字型**：採用「微軟正黑體（Microsoft JhengHei）」，Windows PowerPoint 原生支援；如於 Mac 開啟可改用「蘋方-繁」。
- **商品圖占位**：第 7、8 頁有「商品圖」方框，請替換為實際商品去背圖。
- **標示為「建議」之頁面**（現場執行、分工時程、KPI）為提案草案，數值與分工待三方確認後填入。
- 所有折扣／贈品之最終適用條件、品項範圍與庫存，以德誼及品牌方正式公告為準。

## 重新產出方式
```bash
pip install python-pptx
python3 build_deck.py 德誼Roadshow活動簡報_WokyisxLYCANDER_v1.pptx
```
