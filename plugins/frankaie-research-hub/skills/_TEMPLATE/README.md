# 新增 skill 範本（_TEMPLATE）

新增一個 skill 時，複製對應 Pattern 的範本，放到
`plugins/frankaie-research-hub/skills/<skill-id>/SKILL.md`，再填空。

| Pattern | 適用 | 範本檔 |
|---------|------|--------|
| A 專家型 | 單一資深專家（深度諮詢） | `pattern-a-expert.md` |
| B 工具型 | 執行具體產出的工具 | `pattern-b-tool.md` |
| C 團隊型 | 5 人具名團隊 | `pattern-c-team.md` |

## 共同必備（CI `scripts/check_skills.py` 會檢查）

1. frontmatter 的 `name` 必須**等於資料夾名**。
2. frontmatter 要有 `description`（含明確觸發關鍵字，並用 `⚠️` 標出與相近 skill 的分界）。
3. 內文至少一份**輸出範本**（code fence 或表格）。
4. 內文要有**防臆造守則**（如 `【需查證】`／`【需數據】`／`【假設】`／「不臆造」「不杜撰」「模擬非真實數據」等）。
5. 引用其他 skill 時，名稱必須是**真實存在**的 skill。

> 此資料夾沒有 `SKILL.md`，因此不會被當成一個 skill 計數，也不受結構檢查。
