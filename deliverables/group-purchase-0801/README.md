# 三檔齊發團購提報簡報（8/1 on 檔）

向團購業者 **ama shop** 提報的團購檔期簡報，涵蓋三檔嘖嘖募資商品：
**Wokyis M5、LYCANDER LUNA Mag 小露娜、Sharge Disk Pro**，8/1 同步上檔。

## 檔案
| 檔案 | 說明 |
|------|------|
| `三檔齊發團購提報_0801.pptx` | **交付物**：12 頁 16:9 簡報（繁體中文） |
| `build_deck.py` | 生成腳本（python-pptx），可重複執行 |
| `content.md` | 文案來源備份 |

## 重新生成
```bash
pip install python-pptx          # 首次需安裝
python3 build_deck.py            # 於本資料夾執行，輸出同名 .pptx
```

## ⚠️ 交付前待補（業務／品牌方填寫）
1. **商業條件（全部標示「待填 TBD」）**：每檔的 建議售價／募資價／團購價／拆帳%／MOQ／出貨日；
   合作條件總表的 結帳請款／物流／售後保固；機制頁的 滿額/加購門檻、結團日。
   → 改 `build_deck.py` 的 `OFFER_FIELDS`／`slide_summary_table`／`slide_mechanics`，或開 PPT 直接填。
2. **產品圖／KV**：P2、P4、P6、P8 留有虛線「產品圖 / KV 置入處」佔位框，請於 PowerPoint/Keynote 內置入實際圖檔
   （嘖嘖頁面無法程式抓圖，故未內嵌）。
3. **規格校對**：產品規格依公開募資資訊整理，正式數字以 LYCANDER 與品牌方最終確認為準。

## 頁面結構（12 頁）
1. 封面　2. 三檔齊發總覽　3. 提案概要
4–5. Wokyis M5（介紹／規格＋團購方案）
6–7. LUNA Mag 小露娜（介紹／規格＋團購方案）
8–9. Sharge Disk Pro（介紹／規格＋團購方案）
10. 團購機制與檔期時程　11. 合作條件總表（TBD）　12. 結尾／聯絡

> 註：本環境 LibreOffice 無法轉檔預覽，簡報已通過 python-pptx 結構驗證（12 頁、OOXML 合法）。
> 請於 PowerPoint / Keynote / Google Slides 開啟確認中文字型與版面。
