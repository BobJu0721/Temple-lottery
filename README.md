# 作業：設計 Skill + 打造 宮廟抽籤系統

> **繳交方式**：將你的 GitHub repo 網址貼到作業繳交區
> **作業性質**：個人作業

---

## 作業目標

使用 Antigravity Skill 引導 AI，完成一個具備前後端的宮廟抽籤系統。
重點不只是「讓程式跑起來」，而是透過設計 Skill，學會用結構化的方式與 AI 協作開發。

---

## 繳交項目

你的 GitHub repo 需要包含以下內容：

### 1. Skill 設計（`.agents/skills/`）

為以下五個開發階段＋提交方式各設計一個 SKILL.md：

| 資料夾名稱        | 對應指令          | 說明                                                                           |
| ----------------- | ----------------- | ------------------------------------------------------------------------------ |
| `prd/`          | `/prd`          | 產出 `docs/PRD.md`                                                           |
| `architecture/` | `/architecture` | 產出 `docs/ARCHITECTURE.md`                                                  |
| `models/`       | `/models`       | 產出 `docs/MODELS.md`                                                        |
| `implement/`    | `/implement`    | 產出程式碼（**需指定**：HTML 前端 + FastAPI + SQLite 後端）              |
| `test/`         | `/test`         | 產出手動測試清單                                                               |
| `commit/`       | `/commit`       | 自動 commit + push（**需指定**：使用者與 email 使用 Antigravity 預設值） |

### 2. 開發文件（`docs/`）

用你設計的 Skill 產出的文件，需包含：

- `docs/PRD.md`
- `docs/ARCHITECTURE.md`
- `docs/MODELS.md`

### 3. 程式碼

一個可執行的宮廟抽籤系統，需支援以下功能：

| 功能           | 說明                                       | 是否完成 |
| -------------- | ------------------------------------------ | -------- |
| 抽籤核心功能   | 虛擬搖籤、顯示籤號與籤詩、籤詩解釋         | O        |
| 抽籤歷史紀錄   | 個人抽籤紀錄查詢（依 session 識別）        | O        |
| 香油錢捐贈     | 填寫捐款表單、選擇金額、送出紀錄           | O        |
| 捐款歷史紀錄   | 個人捐款查詢                               | O        |
| 管理後台       | 廟方查看抽籤統計、捐款紀錄、匯出功能       | O        |

### 4. 系統截圖（`screenshots/`）

在 `screenshots/` 資料夾放入以下截圖：

- `fortune.png`：抽籤主畫面
- `history.png`：對話歷史或多 session 切換的畫面

### 5. 心得報告（本 README.md 下方）

在本 README 的**心得報告**區填寫。

---

## 專案結構範例

```
your-repo/
├── .agents/
│   └── skills/
│       ├── prd/SKILL.md
│       ├── architecture/SKILL.md
│       ├── models/SKILL.md
│       ├── implement/SKILL.md
│       ├── test/SKILL.md
│       └── commit/SKILL.md
├── docs/
│   ├── PRD.md
│   ├── ARCHITECTURE.md
│   └── MODELS.md
├── frontend/
│   ├── index.html
│   ├── fortune.html
│   ├── donation.html
│   ├── history.html
│   ├── css/
│   └── js/
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── models/
│   ├── schemas/
│   ├── routers/
│   ├── crud/
│   └── seed_data.py
├── screenshots/
│   ├── fortune.png
│   ├── history.png
│   └── skill.png
├── requirements.txt
├── .env
└── README.md          ← 本檔案（含心得報告）
```

---

## 啟動方式

```bash
# 1. 建立虛擬環境
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 2. 安裝套件
pip install -r requirements.txt

# 3. 建立預設資料庫與種子資料
python -m backend.seed_data

# 4. 啟動伺服器
uvicorn backend.main:app --reload
# 開啟瀏覽器：http://localhost:8000
```

---

## 心得報告

**姓名**：朱覺祥
**學號**：D1257081

### 問題與反思

**Q1. 你設計的哪一個 Skill 效果最好？為什麼？哪一個效果最差？你認為原因是什麼？**

> 我覺得架構設計這裡最好，我是資工系的本身是有上過軟工的東西也是寫過報告的，這裡很簡單的都把東西給寫好甚至各種uml圖都已經畫好了，但凡以前坐電商平台的專題知道這東西也不用大費周章的畫圖寫報告，至於最沒用的我覺得應該是commit，這東西自己手操就行

---

**Q2. 在用 AI 產生程式碼的過程中，你遇到什麼問題是 AI 沒辦法自己解決、需要你介入處理的？**

> AI再登入這裡我還是要自己登入
