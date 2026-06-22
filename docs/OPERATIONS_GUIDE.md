# 作業指南 · FrankAie-hub（HUB 操作手冊）

> 這份是 **實際使用** LYCANDER AI RESEARCH HUB 的標準作業流程（SOP）。
> 教你怎麼把這 100 位 AI 角色＋工具，從「一個想法」一路跑到「上市與售後」。
> 想學 Git / 推送程式碼，請看另一份 `docs/GITHUB_GUIDE.md`。
> 由 **LYCANDER GROUP** 維護。

---

## 0. 三句話搞懂這個 HUB

1. **專家**負責把產品做出來、賣出去、服務好（30 位 · 6 團隊）。
2. **AI 消費者**負責「投錢前先告訴你會不會買」（70 位 · 4 市場）。
3. **總機（hub-router）**負責分流排序、**工具型 skill** 負責把具體產出做出來。

核心心法（所有角色共用）：**搜集市場資訊 → 驗證 → 開發 / 設計** 三階段 SOP，逐段推進、逐段確認、不臆造。

---

## 1. 我該怎麼開始？（決策樹）

```
你的需求是……
│
├─ 一個完整專案 / 跨多領域 / 不知道該找誰
│     → 先找「hub-router」，它會產出「專案作戰計畫」與分工表
│
├─ 只要一位專家快速判斷（單兵）
│     → 直接找旗艦專家：
│        電子→ electronics-engineer｜視覺→ animation-designer
│        財務→ financial-analyst｜法務→ legal-ip
│
├─ 要一個領域「完整分工協作」
│     → 找對應團隊：electronics / mechanical / visual /
│        marketing / operations / cx -team
│
├─ 要驗證「會不會買」
│     → 找 consumers-taiwan / usa / japan / europe
│
└─ 要做出一個具體產出物（listing / hook / 定價表…）
      → 直接找對應「工具型 skill」（見第 5 節）
```

> 口訣：**大需求先過總機；單一任務直接點對的人。**

---

## 2. 標準作業流程：新品從 0 到上市

這是 HUB 的主動線（與 `hub-router` 一致），共 7 站：

| 站 | 階段 | 召集 | 主要產出 |
|----|------|------|----------|
| 1 | **立項** | `financial-analyst`＋`consumers-*`＋`competitor-comparison` | 算帳 + 需求驗證 + 競品差異 |
| 2 | **開發** | `electronics-team`＋`mechanical-team`（並行）→ `legal-ip` | Spec / BOM / 機構 + 專利迴避 |
| 3 | **認證量產** | `electronics-team`(認證)＋`operations-team` | 認證計畫 + 採購/量產 |
| 4 | **上市素材** | `visual-team`＋`marketing-team`＋工具群 | KV/包裝 + 行銷 + hook/listing/seo |
| 5 | **上市前驗證** | `consumers-*` | 素材/定價購買意願評分（1–5） |
| 6 | **上架投放** | `marketing-team`＋`operations-team` | 投放 + 出貨 |
| 7 | **售後迭代** | `cx-team`＋`review-miner` | 客訴/口碑 → 回饋到第 1 站 |

> 這是一個**循環**：第 7 站的回饋會餵回第 1 站，啟動下一輪迭代。

---

## 3. 每一站怎麼跑：三階段 SOP

不論召集誰，都會走同一套三階段。每段都要先確認再往下：

| 階段 | 做什麼 | 結束條件（Gate） |
|------|--------|------------------|
| ① 搜集市場資訊 | 蒐集現況、競品、數據、限制條件 | 資料夠不夠下判斷？缺的有沒有標註？ |
| ② 驗證 | 用 consumers-* / 測試 / 指標檢驗假設 | 假設站得住腳嗎？購買意願 / 數據過關嗎？ |
| ③ 開發 / 設計 | 產出實際成果（spec / 文案 / 視覺 / 計畫） | 產出可被檢驗、可被交接嗎？ |

**防臆造守則（最重要）**：任何主張都要能回溯來源或測試指標；沒有依據的，標註「待補」而不是編一個。缺資料時，角色會主動列出「需要你先補的資訊」。

---

## 4. 實戰範例：開發並上架一顆 65W GaN 充電器

```
Step 0  使用者：「我想開發並上架一顆 65W GaN 充電器」
        → 觸發 hub-router，產出「專案作戰計畫」

Step 1  立項
        financial-analyst   → 成本/毛利/回本試算
        consumers-usa/taiwan→ 對「65W GaN」概念打購買意願分
        competitor-comparison→ vs Anker/UGREEN 差異化定位

Step 2  開發（並行）
        electronics-team → 電源架構/快充協議/安全
        mechanical-team  → 外觀/散熱/模具
        legal-ip         → 專利迴避 FTO、認證紅線提醒

Step 3  認證量產
        electronics-team(認證) → UL/CE/BSMI 計畫
        operations-team        → 採購/打樣/量產排程

Step 4  上市素材
        visual-team   → KV / 包裝
        marketing-team→ 賣點訊息 / 通路策略
        工具群        → ad-hook-writer / listing-optimizer /
                        seo-keyword-expander / copy-humanizer

Step 5  上市前驗證
        consumers-*   → 對 listing / 定價 / 主視覺打分，回修

Step 6  上架投放 + 出貨
        marketing-team + operations-team

Step 7  售後
        cx-team + review-miner → 痛點回饋 → 回到 Step 1 做 v2
```

---

## 5. 工具型 skill 速查（要具體產出時直接點）

| 想要的產出 | 用這個 skill |
|------------|--------------|
| 轉換導向 Listing（標題/五點/A+/後台關鍵字） | `listing-optimizer` |
| 廣告前三秒 hook + 短影音開場分鏡 | `ad-hook-writer` |
| 把生硬文案改自然、去 AI 味 | `copy-humanizer` |
| 從雜亂評論萃取痛點/賣點 | `review-miner` |
| 定價/毛利/break-even 試算 | `pricing-calculator` |
| EDM 自動化序列 | `email-sequence-builder` |
| 競品加權比較 + 差異化定位 | `competitor-comparison` |
| 分群分意圖的 SEO 關鍵字地圖 | `seo-keyword-expander` |

---

## 6. 作業守則（黃金 6 條）

1. **大需求先過總機** —— 不確定找誰就先 `hub-router`，避免重工漏接。
2. **逐階段確認** —— 三階段 SOP 每段有 Gate，沒過不硬推下一段。
3. **凡主張必有據** —— 防臆造優先；缺資料標「待補」並列出要補什麼。
4. **投錢前先驗證** —— 重要決策（概念/定價/素材）一律過 `consumers-*` 打分。
5. **單一任務不繞路** —— 只要一個 hook / 一張定價表，直接點工具型 skill。
6. **產出要可交接** —— 用各角色的表格化輸出範本，方便下一棒接手。

---

## 7. 召集語句範例（直接照抄）

- 整案規劃：「幫我規劃**開發並上架一顆 65W GaN 充電器**的完整流程，召集需要的團隊。」
- 單兵諮詢：「以**資深電子工程師**角度，幫我快速判斷這顆充電器的快充架構可行性。」
- 市場驗證：「召集**美國消費者小組**，對這個定價 $39.99 與主視覺打購買意願分。」
- 具體產出：「用 **listing-optimizer** 幫這顆充電器寫 Amazon Listing。」

---

## 8. 連接 GitHub：把變更同步上去

HUB 的角色與 skill 都存在 `Lycander168/FrankAie-hub` 這個 GitHub repo。
**用 HUB 做事**（前面 7 節）跟**同步到 GitHub**是同一條動線的兩端：

```
改 / 新增角色或文件（本機）
   → commit → push（GitHub）
   → /plugin marketplace update（Claude 端生效）
```

### A. 第一次連接（安裝 marketplace）

在 Claude 中執行，連到本 repo：

```
/plugin marketplace add Lycander168/FrankAie-hub
/plugin install frankaie-research-hub@frankaie-hub
```

> Repo 設為 **Public** 最省事；若為 Private，安裝時需設定 GitHub 認證。

### B. 改完角色 / 文件後，同步回 GitHub

完整 Git 指令（clone、開分支、commit、push、開 PR）見
**`docs/GITHUB_GUIDE.md`**。最短路徑：

```bash
git checkout -b feat/你的變更
git add .
git commit -m "新增 XX 角色（vX.Y.0）"
git push -u origin feat/你的變更
# 在 GitHub 開 PR → 審查 → 合併進 main
```

### C. 讓變更在 Claude 端生效

合併進 `main` 後，使用者端更新即可看到新角色 / 文件：

```
/plugin marketplace update frankaie-hub
```

> 一句話：**HUB 產出 → Git 同步 → marketplace update**，三步走完才算真正上線。
> 詳細 Git 操作一律以 `docs/GITHUB_GUIDE.md` 為準。

---

由 **LYCANDER GROUP** 維護 · 有問題請開 issue 或聯絡 service@lycander.tw
