# pqi GaN65W Combo — 雙語說明書 (Bilingual User Manual)

印刷用組合說明書：**pqi GaN65W 雙孔 USB-C 氮化鎵充電器 + USB-C 100W 傳輸線 Combo**。
版面比照 LYCANDER VoltiX GaN45W Combo 說明書（正面中文 / 背面英文，5 欄式對折單張）。

## 檔案
| 檔案 | 說明 |
|------|------|
| `pqi_GaN65W_Combo_Manual.pdf` | 成品，2 頁（第1頁正面中文、第2頁背面英文），936×268pt |
| `make_manual.py` | PyMuPDF 重建腳本，內含全部已驗證文案與版面 |
| `assets/charger.png` | 去背裁切後的充電器渲染主圖 |
| `assets/cable.png` | 去背裁切後的編織線盤圈渲染主圖 |

## 重建方式
```bash
pip install pymupdf pillow
python3 make_manual.py        # 產出同目錄下的 PDF
```
需要繁中字型 **WenQuanYi Zen Hei**（`/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc`），
或以環境變數覆寫：`FONT=/path/to/font.ttc python3 make_manual.py`。

## 規格來源與交叉驗證
- 充電器規格：炫輝/Shinetech `pqi_65w` 規格書（型號 RWD065X / 結構款 RWD065H）。
- 線材規格：志澤 ZEZK `USB3.1 GEN1 Type-C 1.0M 100W` 規格書。
- 主圖：pqi 65W 白色充電器渲染 + pqi 編織線渲染。

關鍵規格（已採用 65W 實際值，非沿用 45W）：單孔 65W（…20V/3.25A）、雙孔同時 45W+20W、
PPS 5V-11V/5A、輸入 100-240Vac 1.5A、工作 0~35℃／儲存 -40~70℃；線材 100W（20V/5A）、100CM、
TPE+尼龍編織+鋁殼、傳輸速率 **10Gbps**。

## ⚠️ 待補件 / 已知事項
1. **充電器重量** — 規格書未列；稿中為佔位 `________ g`，請填入後重建。
2. **尺寸標註方向** — 機構圖數值 55×30×55mm，L/W/H 對應方向待確認。
3. **線材工作/儲存溫度** — 線材規格書未列，暫沿用 0~40℃ / -20~80℃。
4. **10Gbps**（依客戶裁決）與線材規格書名稱「USB3.1 Gen1 / 5G」不一致，建議請供應商更新規格書名稱。
5. **認證圖示**（CE / RoHS / WEEE）目前為示意向量圖；正式印刷請替換為官方標準 logo 檔。
