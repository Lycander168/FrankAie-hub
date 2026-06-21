---
name: planning-with-files
description: >
  LYCANDER AI RESEARCH HUB — 檔案化規劃 / 持久記憶（Manus 風格）。
  當任務是「多步驟 / 跨多角色 / 長時間研究」、需要 5 次以上工具或搜尋、
  或使用者說「規劃整個案子」、「拆解步驟」、「追蹤進度」、「組織工作」、「先做計畫」、
  「會做很久」、「分階段進行」，以及任何擔心「context 被清空 / session 中斷後接不上」的情境時觸發。
  把工作記憶寫進磁碟上的 markdown 檔（task_plan.md / findings.md / progress.md），
  讓任務即使 /clear、context 壓縮或中斷後仍能無縫恢復，並支援多角色共享狀態。
  ⚠️ 本 skill 是「記憶與流程基礎建設」，與內容型角色互補：角色負責產出，本 skill 負責記住與追蹤。
---

# 檔案化規劃 / 持久記憶（Planning with Files）

把 Claude 的「工作記憶」從脆弱的對話 context 搬到磁碟上的 markdown 檔。
核心心法一句話：

> **Context Window = RAM（易失、有限）；檔案系統 = Disk（持久、無限）。**
> 凡是「之後還要用到、或不能忘」的東西，立刻寫進檔案，不要只放在腦袋（context）裡。

> 本 skill 改寫自開源社群的 Manus 風格 file-based planning 模式
> （參考 `OthmanAdi/planning-with-files`），並在地化整合進 LYCANDER HUB 的三階段 SOP 與多角色協作。

---

## 何時啟動

- **長任務**：一個專案要跑很久、要召集多個團隊（最典型：`hub-router` 的「新品從 0 到上市」動線）。
- **多步驟 / 多搜尋**：需要 5 次以上工具呼叫、多輪市場資訊搜集與驗證。
- **怕失憶**：session 可能中斷、context 會被壓縮、使用者可能 `/clear`，但任務不能從頭再來。
- **多角色協作**：多個 skill 接力或並行，需要一份大家都看得到的共享狀態。

若只是單一、短任務（問一個 hook、算一次定價），**不必啟動**——直接做完即可，不要為小事建一堆檔案。

---

## 三個核心檔案（你的「磁碟記憶」）

預設建立在專案根目錄的 `.planning/<日期>-<專案代號>/` 下（多專案隔離）；
單一專案也可直接放專案根目錄。

| 檔案 | 角色 | 內容 |
|------|------|------|
| `task_plan.md` | **計畫** | 階段拆解、每階段狀態（`todo / in_progress / done`）、召集名單、策略決策 |
| `findings.md` | **發現** | 搜集到的市場資訊、競品數據、驗證結果、外部來源（含日期與來源連結） |
| `progress.md` | **日誌** | 每一步做了什麼、產出在哪、遇到什麼錯、下一步是什麼 |

> 對應 HUB 既有產出：`findings.md` 是各角色《市場情報卡 / 驗證報告》的彙整索引；
> `task_plan.md` 則是 `hub-router`《專案作戰計畫》的可執行、可勾選版本。

---

## 運作守則（讓記憶不流失）

1. **開場先讀**：任務恢復或新一輪開始，**第一件事**是讀這三個檔，重建現況，再動手。
2. **2-Action Rule**：每做 2 次「查看 / 搜尋」，就把發現 flush 進 `findings.md`，趁還沒被新 context 擠掉。
3. **做完就記**：每完成一個動作 / 子任務，立刻在 `progress.md` 補一行，並更新 `task_plan.md` 對應階段狀態。
4. **壓縮前快存**：感覺 context 快滿 / 要被壓縮前，先把進行中的工作寫回磁碟，再繼續。
5. **完成閘門（Completion Gate）**：只要 `task_plan.md` 還有 `in_progress` 或 `todo` 階段，就**不算完成**——
   不要提早收尾。全部 `done` 且通過驗證，才宣告結案。
6. **3-Strike 錯誤協定**：同一個動作連續失敗：① 診斷 → ② 換方法重試 → ③ 重新想；三次仍不行，
   寫進 `progress.md` 並回報使用者，不要無限空轉。

---

## 多角色 / 多 agent 共享狀態

當 `hub-router` 召集多個團隊（如 `electronics-team` 與 `mechanical-team` 並行）：

- **總機持有主計畫**：`hub-router` 擁有 `task_plan.md`，負責排程與勾選階段狀態。
- **各角色寫自己的段落**：每個被召集的 skill 把自己的產出寫進 `findings.md` 對應小節（標明角色名），
  避免互相覆蓋。
- **進度集中記**：所有角色的完成事件都追加到同一份 `progress.md`，形成單一事實來源（single source of truth）。
- **交棒看檔案**：下一棒角色開工前先讀 `task_plan.md` + `findings.md`，承接前一棒的結論，不重問、不重工。

---

## 輸出範本

### 範本 A — `task_plan.md`（計畫）

```
# 專案計畫 | <專案名>｜代號 <slug>｜<日期>

## 目標 / 範圍 / 限制
-

## 階段清單（勾選 = done）
- [ ] S1 立項：financial-analyst + consumers-* + competitor-comparison   <status: todo>
- [ ] S2 開發：electronics-team ∥ mechanical-team → legal-ip            <status: todo>
- [ ] S3 認證量產：electronics-team(認證) + operations-team             <status: todo>
- [ ] S4 上市素材：visual-team + marketing-team + 工具                  <status: todo>
- [ ] S5 上市前驗證：consumers-*                                        <status: todo>

## 策略決策紀錄（為什麼這樣排）
- <日期> 決定：…（理由 / 依據）

## 目前焦點
- 進行中階段：
- 阻塞 / 待使用者補的資訊：
```

### 範本 B — `findings.md`（發現）

```
# 市場發現彙整 | <專案名>

## [角色: electronics-engineer] 市場情報
- 競品 A 65W：售價 $39，效率 ~92%，主要負評=發熱（來源:平台評論 2026-06）
- …（每筆標來源 + 日期；無一手資料標【需查證】）

## [角色: consumers-usa] 驗證結果
- 概念購買意願：3.8/5；主要顧慮=體積

## 未解問題 / 待查證
- [ ] …
```

### 範本 C — `progress.md`（日誌）

```
# 進度日誌 | <專案名>

## 2026-06-21
- ✅ 完成 S1 立項：財務試算回本 8 個月，consumers 平均 3.8/5 → 決定進開發
- ⏳ 啟動 S2：electronics-team 出規格假設中
- ❗ 阻塞：缺目標市場（US/EU?），已請使用者確認
- ▶️ 下一步：使用者回覆市場後，啟動 mechanical-team 並行
```

---

## 與 LYCANDER GROUP 的協作介面

- **上游（hub-router）**：總機產出《專案作戰計畫》時，同步落地成 `task_plan.md`，把口頭計畫變成可勾選、可恢復的狀態。
- **平行（各團隊/工具）**：每個角色的《情報卡 / 驗證報告 / 產出》摘要寫進 `findings.md`，正式檔案另存、在此留索引。
- **下游（營運/財務）**：結案時 `progress.md` + `task_plan.md` 即為完整交接紀錄與決策軌跡。

## 啟動方式

接到「大需求 / 長專案 / 多角色」任務時：
1. 先建立 `.planning/<日期>-<slug>/` 與三個檔（或沿用既有的）。
2. 把計畫寫進 `task_plan.md`，邊做邊更新 `findings.md` / `progress.md`。
3. 每次恢復先讀這三檔重建現況，依「完成閘門」確認全部階段 done 才結案。

> 提醒：本 skill 只負責「記住與追蹤」，不替專業角色下技術結論；
> 寫進 `findings.md` 的每筆主張仍沿用各角色的防臆造守則（無一手資料標 `【需查證】`）。
