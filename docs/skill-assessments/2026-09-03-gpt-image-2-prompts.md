# awesome-gpt-image-2-API-and-Prompts 安裝前評估報告

- **評估日期**：2026-09-03
- **評估標的**：`EvoLinkAI/awesome-gpt-image-2-API-and-Prompts`（GitHub，13.8k stars / 1.4k forks，CC0 1.0）
- **評估標準**：[`docs/SKILL_ADOPTION_RUBRIC.md`](../SKILL_ADOPTION_RUBRIC.md) v1.0
- **加權總分**：**情境甲（全量安裝為 skill）2.20** ／ **情境乙（最小 vendor 為參考資料）3.25**
- **決策**：**不安裝。情境甲否決，情境乙暫緩。** 兩者皆未達 4.50 自動安裝門檻

---

## 0. 先修正題目：它不是一個可安裝的 skill

實測全 repo 搜尋 `SKILL.md`、`.claude-plugin`、`plugin.json`、`marketplace.json`：**零命中**。

**上游自己劃了邊界**，這是本案最關鍵的單一事實：

> `README.md` 開頭 NOTE：「This repository owns the curated prompt library. API automation,
> **callable skills**, and image-to-video workflows are **separate surfaces**.」

`CONTRIBUTING.md` 的「Repository boundary」進一步規定：「A pull request that changes runnable API
or **skill-release** material requires a separately approved scope。」Related Repositories 段落
指向 `Evolink-AI/gpt-image-2-gen-skill`——**可呼叫的 skill 在那裡，不在這裡**。

因此「安裝這個 skill」這個提法本身不成立。本報告改評估兩個真實可執行的情境：

| 情境 | 內容 |
|------|------|
| **甲** | 全量 vendor 進 `plugins/frankaie-research-hub/skills/`，包裝成第 34 支 skill |
| **乙** | 最小 vendor：只取英文 `cases/*.md` 當 `animation-designer` 的 reference 資料，不含 `images/` |

---

## 1. 事實基準

### 1.1 內容組成（實測）

| 部分 | 體積 | 說明 |
|------|------|------|
| `.git`（shallow, depth=1） | 246 MB | |
| `images/` | 262 MB | 1,193 張 jpg |
| `cases/` | 19 MB | 7 個英文分類頁 × 11 語系 = 77 檔 |
| `README*.md` | 12 MB | 同一份內容的 11 個語系版本，1.1 MB × 11 |
| 其餘（`data/`／`docs/`／`script*/`） | ~0.9 MB | |
| **總計** | **539 MB** | |

案例分佈（966 個 heading）：poster 355（36.7%）、portrait 273（28.3%）、ui 134（13.9%）、
comparison 84（8.7%）、ad-creative 54（5.6%）、**ecommerce 34（3.5%）**、character 32（3.3%）。

`script/sync_multilingual_readmes.py` 與 `scripts/verify_prompt_repo.py` 是**上游自我維護腳本**
（同步 11 語系、驗證 case 編號連續），對我方零用途。`data/curation_report_*.json` 是上游策展流水帳。

### 1.2 名稱有「API」，但沒有 API

全 repo 掃描：

| 搜尋項目 | 命中次數 |
|---|---|
| `api.openai.com` | **0** |
| `OPENAI_API_KEY` / `import openai` / `requests.post` / curl 範例 | **0** |
| `base_url` / `Authorization: Bearer` | **0** |
| `evolink.ai` | **16,076** |

唯一與 API 相關的敘述是 `README.md:68` 一句「Works with OpenAI's standard API format
(`/v1/images/generations`)」——只有 path，沒有 host、沒有認證範例。**照這個 repo 無法呼叫任何東西。**

這是刻意設計。上游 CI 腳本 `scripts/verify_prompt_repo.py:67-72` 主動**禁止** API 內容出現：

```python
FORBIDDEN_API_FIRST_MARKERS = [
    'export EVOLINK_API_KEY=',
    "Authorization: Bearer",
    "npx evolink-gpt-image",
    "curl --request POST",
]
```

### 1.3 它實際是什麼：第三方中轉服務的導流漏斗

- **599 個**帶 UTM 追蹤參數的 `https://evolink.ai/gpt-image-2-prompts?utm_source=github&...` 連結，
  每一張範例圖都被包在裡面。
- Quick Start 第 3 步直接叫使用者到 EvoLink playground 貼 prompt 並**上傳輸入圖**。
- 官方 API 文件連結指向 `docs.evolink.ai`，**不是** platform.openai.com。
- 上述 CI 黑名單洩漏的 `EVOLINK_API_KEY` 證明中轉服務用自家 key，不是 OpenAI key。

這解釋了為什麼 poster + portrait 佔 65%（那些會在推特上瘋傳），而 ecommerce 只佔 3.5%：
**這不是為電商品牌策展的資產，是為 API 銷售漏斗策展的資產。**

### 1.4 本環境連通性（實測，未送出任何憑證）

| 網域 | 結果 |
|---|---|
| `api.openai.com` | **403 CONNECT 拒絕** |
| `evolink.ai` / `docs.evolink.ai` / `api.evolink.ai` | **403 CONNECT 拒絕** |
| `github.com`（對照組） | HTTP 400，可連通 |
| `raw.githubusercontent.com`（對照組） | HTTP 301，可連通 |

環境變數檢查（只查名稱不讀值）：`OPENAI_API_KEY`、`OPENAI_BASE_URL`、`EVOLINK_API_KEY`
**皆為 NOT SET**。

> **端到端產圖在本環境為零可能。** 使用者須自備付費帳號與 key。

### 1.5 成本（查得日 2026-09-03，指示性）

GPT-Image-2 為 token 計價：文字輸入 $5/1M、影像輸入 $8/1M、**影像輸出 $30/1M**。
換算每張約：低品質 $0.005–0.006、中品質 $0.041–0.053、高品質 $0.165–0.211。Batch API 打 5 折。

> `developers.openai.com` 在本環境亦被封鎖，上述數字來自第三方彙整，正式採購前需以官方頁面複核。

### 1.6 上游已停更

最後 commit **2026-07-18**、News 最後一則 2026-06-30（距評估日約 2 個月），
但 README 仍宣稱有「daily image-prompt update loop」。另有資料品質問題：README 自稱 462 個案例，
`cases/` 實際有 966 個 heading，且存在重複 ID（`ad-creative.md` 有三個不同標題的「Case 17」）。

---

## 2. 專家交叉驗證 — 獨立分數

### 專家 A｜架構稽核

**功能重疊**：HUB **已具備「產出圖像 prompt」的能力**。`animation-designer/SKILL.md:179` 明文
「本技能負責 brief、分鏡與 prompt」，範本 C 內建 `- 圖像 prompt：` 欄位。
本 repo 加的不是 capability，是**填充該空欄的範例語料**。

**觸發詞衝突**：grep 全 33 skill，「主視覺」命中 `animation-designer`(desc L7) 與
`visual-team`(desc L4/L19/L45–48)——**兩者 description 本身就含這些詞**，會形成三方競爭。
`hub-router:81` 的仲裁規則只寫了 animation-designer vs visual-team 二選一，**無第三方容身規則**。
緩解事實：誤觸副作用僅為多產一段文字，無執行指令／寫檔／起 server。

**CI 實測**：

| 情境 | 結果 |
|---|---|
| Baseline | `✓✓✓✓ Checked 33 skills` exit=0；`.git` 476 K |
| **甲：全量 vendor** | **exit=1** — `docs/update-log.md:7` 的 `gpt-image-2-gen-skill` 被判為未知 skill |
| **乙：只放 7 個英文 `cases/*.md` 到 `animation-designer/reference/`** | **1.8 MB，CI exit=0 全綠，skill 數仍為 33** |

**體積實測（非估算）**：262 MB `images/` 實際 `git add` + commit 後 `.git` = **250 MB**；
zlib 壓縮率 **0.997**（JPEG 不可壓，git 1:1 永久存放且刪不掉）。HUB 的 `.git` 會從 476 K
膨脹到約 250 MB（**約 550 倍**），marketplace 使用者每次安裝都要拉這 250 MB。
`git gc --aggressive` 在此資料集上逾時 2 分鐘未完成。

> **修正一個常見誤判**：GitHub 100 MB 單檔上限**不會**被觸發（最大檔 `images/logo.png` 僅 5.5 MB）。
> 真正的殺傷力是 repo 總量膨脹與 clone 時間。
>
> **且這 262 MB 幾乎全是死重**：README 中 461 個圖片引用是 `raw.githubusercontent.com`
> 絕對網址，只有 149 個是相對路徑。vendor 圖片對閱讀 prompt 毫無幫助。

| 構面 | 分數 | 理由 |
|---|---|---|
| D1 必要性 | **2** | 視覺流程未被卡住；61% 內容是 poster/portrait，對 3C 電商對口的 ecommerce 僅 34 例 |
| D2 非重複性 | **2** | 上游自陳為 prompt library 而非 skill；提供的是範例語料而非新能力 |
| D4 衝突風險 | **2** | 「主視覺／圖像 prompt」與兩支既有 skill 的 description 大量重疊，`hub-router` 無第三方仲裁規則（若改為無 SKILL.md 的被動 reference，此項為 **5**） |
| D5 整合成本 | **2** | 全量 vendor 使 CI 由綠轉紅、`.git` 476 K→250 MB（最小 vendor 路徑實測為 **4**） |

### 專家 B｜技術可行性（實測）

**裁切方案實測**：

| 方案 | 體積 | 縮減 |
|---|---|---|
| 原始 clone | 539 MB | — |
| A. 只留 md + json，去 `images/` 與 `.git` | 31 MB | −94% |
| B. 只留英文 | 2.9 MB | −99.5% |
| **C. 只抽純 prompt 文字 → 單一 JSON** | **746 KB** | **−99.86%** |

方案 C 已實作驗證，成功抽出 **461 / 462 個 case（99.8%）**，並順帶剝除全部 599 個 EvoLink
UTM 導流連結與所有外部 hotlink——一次解決體積與資安兩個問題。

| 構面 | 分數 | 理由 |
|---|---|---|
| D3 技術可行性 | **2**（全量）<br>**4**（僅離線參考） | 文字資產本身 100% 可用且已實測；但這個 repo 存在的目的是餵給 GPT-Image-2，而該環節三重受阻——網域全封鎖、無 key、付費外部服務。端到端產出實測為零 |
| D6 授權與合規 | **4** | CC0 1.0 是最寬鬆授權、商用無條件免費，單看授權應為 5；扣 1 分因 (a) 599 個 UTM 導流連結指向非 OpenAI 官方網域，(b) prompt 蒐集自 X 貼文由 EvoLink 單方面套上 CC0，repo 自承「cannot guarantee that every case is attributed to the original creator」 |

> **未觸發 D6 ≤ 2 否決條款的關鍵**：資安風險是**導流式而非執行式**——repo 內零 API 程式碼、
> 零網路呼叫，兩支 Python 腳本純離線。採方案 C 抽純文字後殘餘外洩風險趨近於零。

### 專家 C｜商業價值

**Prompt 性質**：77% 消費者玩票取向。具體證據——`comparison.md` Case 432「Sam Altman Bear Selfie」、
Case 36「Among Us Realistic Screenshot」；`character.md` Case 30「LEGO Football Collectible Figure」、
Case 12「GTA 6 Shinjuku Bar Scene」；`poster.md` Case 199「Naruto Propaganda Poster」。

**商用案例確實存在且品質不差**（須誠實記錄）：`ecommerce.md` Case 155「Earbuds E-commerce Infographic」
是標準 Amazon／Shopee 主圖套路（前景充電盒特寫／中景模特配戴／背景灰色漸層棚拍／右中「30 hours of
battery life」）；`ui.md` Case 44/45 把 FOREGROUND／CENTRAL SUBJECT／BACKGROUND／LIGHTING／TYPOGRAPHY
分段寫成結構化 brief；`ecommerce.md` Case 116「Industrial Design Presentation Sheet」。

**但對 3C 品牌有三個硬傷**：

1. 與 3C 品類直接相關的案例僅約 12 個（**1.2%**），集中在耳機／手機／主機板。
   **充電器、行動電源、線材、GaN——LYCANDER 的實際品類——零案例。**
2. **1,194 張圖全是 `output.jpg`，`input*` 檔案數為 0**。整個 repo 沒有任何
   image-to-image／參考圖工作流，全部是純文生圖虛構產品。LYCANDER 有真實的 GaN 充電器實體，
   需要的是「把我這顆充電器放進情境」，一個案例都不提供。
3. **`ecommerce.md` 裡「white background」出現次數為 0**。Amazon 主圖強制純白底
   （RGB 255,255,255）——最高頻、最剛性的需求，這份「電商案例集」完全沒覆蓋。

**能力缺口的真相**：HUB 缺的是**執行能力**，不是 prompt 靈感。三支 skill 的斷點都在同一處——
寫完 prompt 之後沒有東西可以按下去生成。**它是一本菜譜，而廚房缺的是爐子。**

**替代方案（實際載入工具 schema 查證，推翻既有假設）**：

> **Adobe MCP 沒有 text-to-image 生成工具。** `image_select_by_prompt` 說明明寫：「DO NOT USE
> for generative requests... inform them that generative editing is not currently available.」
> Canva `generate-design` 產的是版面設計而非照片級產品攝影；Figma 只有 shader / diagram。

這造成對稱結論，兩邊都不利於採納：現有 MCP 取代不了文生圖——**但這份 repo 也提供不了**，
它只有文字。裝它不會讓 HUB 多出任何生圖能力。而在 3C 電商真正要做的事情上，現有 MCP 覆蓋度反而更高：

| 實際需求 | 這份 prompt 集 | 現有 MCP |
|---|---|---|
| Amazon 合規純白底主圖 | 0 個案例 | `image_remove_background` 帶 `backgroundColor:"#ffffff"`，用**真實產品照** |
| 電商資訊圖 | Case 155/44/45（燒死成點陣圖，文字不可改） | Canva `generate-design` + brand_kit_id，**文字是可編輯圖層、可多語版本** |
| 多通路尺寸適配 | 無 | `image_crop_and_resize`（主體感知）+ `image_generative_expand` |
| 修圖／調色／去背 | 無 | `image_apply_adjustments` 等 20+ 工具 |
| 情境圖／模特配戴 | 有（但生的是虛構產品） | 無 |

**跨模型可移植性：低。** 價值密度集中在兩個 GPT-Image-2 專屬強項——圖內精確文字渲染
（`poster.md` 有 230 處指定圖內確切字串與位置）與 `keep the details, typography and structure
locked 100%` 這類多輪編輯語法。**在 Canva 上這整段 prompt 是廢話，你直接打字就好。**
可移植的部分（灰色漸層棚拍、三點打光、淺景深）是通用攝影術語，任何 LLM 都寫得出來。
**可移植的部分沒價值，有價值的部分不可移植。**

**使用頻率**：估一年真正打開來查 **3–6 次**，集中在新品上市（一年 2–4 支新品）。
更關鍵的是——這是**參考素材**不是**工具**，第一次讀完 Case 155 的結構就記住了，
**使用頻率是遞減的，不是穩定的**。

| 構面 | 分數 | 理由 |
|---|---|---|
| D1 必要性 | **2** | 966 個案例僅約 12 個與 3C 相關、0 個充電器品類、0 個白底合規主圖；年使用 3–6 次且遞減 |
| D2 非重複性 | **2** | `animation-designer` 已內建「圖像 prompt」欄位，寫 prompt 本就不是瓶頸；真正的電商圖需求已被現有 MCP 更好覆蓋，且產出可編輯圖層優於燒死的點陣圖 |
| D5 整合成本 | **2** | 無 SKILL.md／plugin.json，要進 HUB 必須從零封裝；且上游已停更，維護成本全落我方卻沒有活的上游可同步 |

---

## 3. 加權計分（兩情境）

### 情境甲：全量安裝為 skill

| 構面 | 權重 | 來源 | 平均 | 加權 |
|---|---|---|---|---|
| D1 需求必要性與使用頻率 | 25% | A 2、C 2 | **2.00** | 0.500 |
| D2 非重複性／能力加值 | 20% | A 2、C 2 | **2.00** | 0.400 |
| D3 技術可行性 | 15% | B 2（端到端產圖不可行） | **2.00** | 0.300 |
| D4 衝突與誤觸風險 | 15% | A 2 | **2.00** | 0.300 |
| D5 整合與維運成本 | 15% | A 2、C 2 | **2.00** | 0.300 |
| D6 授權與合規 | 10% | B 4 | **4.00** | 0.400 |
| **加權總分** | | | | **2.20** |

**→ < 2.50，判定「否決」。** 另觸發一票否決條款 3（CI 由綠轉紅，實測 exit=1）。

### 情境乙：最小 vendor 為參考資料

| 構面 | 權重 | 來源 | 平均 | 加權 |
|---|---|---|---|---|
| D1 需求必要性與使用頻率 | 25% | 需求不因形式改變 | **2.00** | 0.500 |
| D2 非重複性／能力加值 | 20% | 加值不因形式改變 | **2.00** | 0.400 |
| D3 技術可行性 | 15% | B 4（純離線參考，已實測） | **4.00** | 0.600 |
| D4 衝突與誤觸風險 | 15% | A 5（被動 reference 無 SKILL.md，不參與觸發） | **5.00** | 0.750 |
| D5 整合與維運成本 | 15% | A 4（1.8 MB、CI 全綠、僅動 1 個資料夾） | **4.00** | 0.600 |
| D6 授權與合規 | 10% | B 4 | **4.00** | 0.400 |
| **加權總分** | | | | **3.25** |

**→ 2.50–3.49，判定「暫緩」。**

**評估者一致性檢查**：D3 出現 A 4 / B 2 的分歧（差 2 分，未達重評門檻 3 分）。分歧根源是
**採用範圍未先界定**——B 依 repo 的原始用途（餵 GPT-Image-2 產圖）評分，A 依離線文字參考評分。
本報告以兩情境分別計分解決。此問題已回饋為 Rubric v1.1 的新增條款。

---

## 4. 決策

**不安裝。** 兩個情境皆未達 4.50 自動安裝門檻，且情境甲落入否決區。

三位專家在三件事上完全一致，沒有任何分歧：

1. **它不是 skill**——上游自己明說 callable skills 在別的 repo。
2. **HUB 缺的是生圖執行能力，不是 prompt 靈感**——`animation-designer` 早已承接 prompt 產出。
3. **對 3C 充電器品類的實際覆蓋接近零**——12/966 相關、0 個充電器案例、0 個白底主圖、0 個參考圖工作流。

---

## 5. 建議處置

### 立即動作（半天，不需安裝任何東西）

一次性人工萃取 **6 個案例的結構骨架**，補進 `animation-designer` 範本 C 的「圖像 prompt」欄位
當填空模板，然後刪除 clone：

- `ecommerce.md` Case 155（電商主圖資訊圖）、Case 116（工業設計提案版面）、Case 153（棚拍）
- `ui.md` Case 44 / 45（耳機資訊圖模板）
- `ad-creative.md` Case 33（lifestyle 廣告）

要萃取的是那個**分區式 brief 寫法**：FOREGROUND ／ CENTRAL SUBJECT ／ BACKGROUND ／
LIGHTING ／ TYPOGRAPHY。這是整份 repo 對 LYCANDER 唯一有遷移價值的東西。

> 替代路徑（若希望把完整案例庫留在手邊）：把 7 個英文 `cases/*.md` 放進
> `plugins/frankaie-research-hub/skills/animation-designer/reference/`（實測 1.8 MB、CI 全綠、
> skill 數不變）。**不要** vendor `images/`（250 MB 死重，圖本來就從上游 CDN 抓）、
> **不要** vendor `docs/update-log.md`（唯一 CI 破口）、10 個非英文語系、
> `data/curation_report_*`（上游內部流水帳）、兩支上游自維護 `.py`。

### 真正該評估的下一個標的

HUB 的實際缺口是**生圖執行端**。應另跑一次 Rubric 的標的是：

1. **`Evolink-AI/gpt-image-2-gen-skill`**——上游宣告的可呼叫 skill 介面，才是真正的 skill。
   評估前需先確認 egress 政策是否放行 `api.openai.com`，否則同樣卡在連通性。
2. 或任何能在本環境實際產出圖檔的方案。

> 注意這與 REMOTION 評估（2026-09-03，總分 3.24）指向同一個結構性問題：
> **HUB 在「視覺／影像產出」這條線上，缺的一律是執行端，不是創意端。**
> 未來的視覺類 skill 評估應優先問「它能不能產出檔案」，而不是「它的內容好不好」。

---

## 6. 附註與來源

- 本次未安裝任何套件到 repo，全部模擬在暫存區複本進行；`/home/user/FrankAie-hub`
  全程未被修改（`git status --porcelain` 為空）。
- `api.openai.com`、`evolink.ai`、`docs.evolink.ai`、`developers.openai.com`
  在本環境被 egress proxy 封鎖，連通性測試僅發 TCP CONNECT，未送出任何憑證。

**來源**：
[EvoLinkAI/awesome-gpt-image-2-API-and-Prompts](https://github.com/EvoLinkAI/awesome-gpt-image-2-API-and-Prompts) ·
[Evolink-AI/gpt-image-2-gen-skill](https://github.com/Evolink-AI/gpt-image-2-gen-skill) ·
[OpenAI API Pricing](https://developers.openai.com/api/docs/pricing) ·
[CostGoat OpenAI Images Calculator](https://costgoat.com/pricing/openai-images) ·
[apimodels.app GPT-Image-2 pricing](https://apimodels.app/access/gpt-image-2-api-pricing)
