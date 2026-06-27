# 8/1 三檔齊發團購 DM 宣傳圖

社群直式 DM（**1080×1350** 設計，輸出 **2160×2700** PNG，2x 高解析），給團購業者 **ama shop** 開團使用。

## 檔案
| 檔案 | 用途 |
|------|------|
| `DM_主視覺_三檔齊發.png` | 三合一主視覺／開團首圖（8/1 三檔齊發） |
| `DM_Wokyis-M5.png` | Wokyis M5 單品 DM |
| `DM_LUNA-Mag.png` | LUNA Mag 小露娜 單品 DM |
| `DM_Sharge-Disk-Pro.png` | Sharge Disk Pro 單品 DM |
| `build_dm.py` | 生成腳本（HTML → Chromium headless 截圖） |
| `*.html` | 各 DM 的 HTML 原稿（可微調後重生成） |

## 重新生成
```bash
python3 build_dm.py     # 於本資料夾執行；用內建 Chromium 渲染 PNG
```

## 從 Dropbox API 抓商品圖（自動套圖）
`fetch_dropbox.py` 以 Dropbox 官方 API 下載商品圖到 `assets/`，`build_dm.py` 會依檔名關鍵字
（wokyis / luna·mag·lycander / sharge·disk·pro）自動把圖套進對應 DM 的佔位框。

```bash
# token 由環境變數提供，不寫入檔案、不進 repo
DROPBOX_TOKEN=sl.xxxxx python3 fetch_dropbox.py --path "/團購/8月商品圖"     # 資料夾路徑
DROPBOX_TOKEN=sl.xxxxx python3 fetch_dropbox.py --link "https://www.dropbox.com/scl/fo/...?rlkey=..."  # 共享連結
python3 build_dm.py     # 套圖並重出 4 張 DM
```

- **取得 token**：Dropbox App Console 建立 app → 產生 access token，scope 需含
  `files.metadata.read`、`files.content.read`（用共享連結另加 `sharing.read`）。
- `assets/`（原始圖）已列入 `.gitignore`，不進 repo；最終 DM 已內嵌圖片即為交付物。

## ⚠️ 交付前待補
1. **團購價／拆帳**：DM 上標「即將公布」，數字確認後改 `build_dm.py` 內 `PRODUCTS` 或 HTML 再重生成。
2. **產品圖／KV**：每張留有虛線「產品圖置入處」佔位框，請以實際商品圖替換（改 HTML 的 `.ph`/`.thumb` 區塊，
   或在影像軟體上後製置入）。
3. **字型**：本環境用開源「文泉驛正黑」渲染；若要品牌指定字型，請在 HTML 換上對應 `font-family` 後重生成。

## 規格
- 尺寸：1080×1350（4:5 社群直式），輸出 2x = 2160×2700。
- 風格：深色科技感漸層 + 各產品識別色（Wokyis 橘／LUNA 紫／Sharge 藍）。
- 商業條件一律「即將公布（待填）」，不臆測數字。
