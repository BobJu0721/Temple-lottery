---
name: implement
description: 程式碼實作技能指南定義 AI Agent 在生成程式碼時應遵守的規範、結構與品質標準。本專案採用 HTML/CSS/JavaScript 前端搭配 FastAPI 後端與 SQLite 資料庫，確保產出的程式碼符合 Python 慣例、可讀、可維護，並能直接整合進現有專案。

---

## 技術棧（Tech Stack）

| 層次     | 技術                        |
| -------- | --------------------------- |
| 前端     | HTML / CSS / JavaScript     |
| 後端框架 | Python + FastAPI            |
| 資料庫   | SQLite（透過 SQLAlchemy ORM）|
| 驗證     | Pydantic（FastAPI 內建）    |
| 環境管理 | `.venv` Python 虛擬環境     |

---

## 一、實作前置確認（Pre-Implementation Checklist）

在開始生成程式碼前，必須確認以下資訊已蒐集完整：

- [ ] 已閱讀相關 PRD，理解功能需求與驗收條件
- [ ] 已閱讀資料模型文件，了解資料結構與欄位定義
- [ ] 已了解目前 FastAPI 版本與 Python 版本
- [ ] 已了解現有專案的目錄結構與模組組織方式
- [ ] 已確認命名慣例（Python 慣例：snake_case）
- [ ] 已確認錯誤處理策略（HTTPException / 自訂 Exception）
- [ ] 已確認測試框架（pytest）

---

## 二、目錄結構規範（Project Structure）

```
project/
├── frontend/                  # 前端靜態檔案
│   ├── index.html
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
├── backend/                   # FastAPI 後端
│   ├── main.py                # FastAPI 進入點，掛載路由
│   ├── database.py            # SQLite 連線設定（SQLAlchemy）
│   ├── models/                # SQLAlchemy ORM 模型
│   │   └── user.py
│   ├── schemas/               # Pydantic 資料驗證 Schema
│   │   └── user.py
│   ├── routers/               # 路由（依業務功能分組）
│   │   └── user.py
│   ├── services/              # 業務邏輯層
│   │   └── user.py
│   └── crud/                  # 資料庫操作（CRUD）
│       └── user.py
├── .env                       # 環境變數（不提交 Git）
├── .venv/                     # Python 虛擬環境（不提交 Git）
├── requirements.txt           # 依賴套件清單
└── README.md
```

**原則**：
- 依業務功能分組（如 user、order、product），而非技術層
- `models/` 只定義資料庫表結構，`schemas/` 只做資料驗證
- `crud/` 只負責資料庫操作，業務邏輯放在 `services/`

---

## 三、命名規範（Naming Conventions）

| 對象              | 規範        | 範例                            |
| ----------------- | ----------- | ------------------------------- |
| 類別              | PascalCase  | `UserService`, `OrderModel`     |
| 函式 / 方法       | snake_case  | `get_user_by_id`, `create_order`|
| 變數 / 參數       | snake_case  | `user_id`, `order_list`         |
| 常數              | UPPER_SNAKE | `MAX_RETRY_COUNT`               |
| 資料庫欄位        | snake_case  | `created_at`, `user_id`         |
| 檔案名稱          | snake_case  | `user_service.py`               |
| 環境變數          | UPPER_SNAKE | `DATABASE_URL`                  |
| API 端點路徑      | kebab-case  | `/api/user-profiles`            |
| HTML class / id   | kebab-case  | `user-card`, `submit-btn`       |
| JS 變數 / 函式    | camelCase   | `userId`, `fetchUserData()`     |

---

## 四、FastAPI 後端規範（Backend）

### 4.1 路由結構（Router）

每個業務模組獨立一個 Router，在 `main.py` 統一掛載：

```python
# backend/routers/user.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend import schemas, crud

router = APIRouter(prefix="/api/users", tags=["users"])

@router.get("/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="找不到該用戶")
    return user
```

```python
# backend/main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from backend.routers import user

app = FastAPI()
app.include_router(user.router)

# 掛載前端靜態檔案
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
```

### 4.2 SQLite 資料庫設定

```python
# backend/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./database.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### 4.3 ORM 模型（SQLAlchemy Model）

```python
# backend/models/user.py
from sqlalchemy import Column, Integer, String, DateTime, func
from backend.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=func.now())
```

### 4.4 Pydantic Schema（請求與回應驗證）

```python
# backend/schemas/user.py
from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: EmailStr

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True  # 允許從 ORM 物件轉換
```

---

## 五、前端規範（Frontend）

### 5.1 HTML 結構原則

- 使用語意化標籤（`<header>`, `<main>`, `<section>`, `<article>`）
- 每個頁面只有一個 `<h1>`
- 表單元素必須有對應的 `<label>`
- 互動元素（按鈕、輸入框）必須有唯一的 `id`

### 5.2 與後端 API 互動

使用 `fetch` API 與 FastAPI 後端溝通：

```javascript
// frontend/js/main.js

async function fetchUsers() {
  try {
    const response = await fetch('/api/users');
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail);
    }
    const users = await response.json();
    renderUserList(users);
  } catch (error) {
    showErrorMessage(error.message);
  }
}

async function createUser(userData) {
  const response = await fetch('/api/users', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(userData),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail);
  }
  return response.json();
}
```

---

## 六、錯誤處理規範（Error Handling）

### 後端（FastAPI）

```python
from fastapi import HTTPException

# 資源不存在
raise HTTPException(status_code=404, detail="找不到該用戶")

# 輸入不合法
raise HTTPException(status_code=422, detail="Email 格式不正確")

# 伺服器錯誤
raise HTTPException(status_code=500, detail="伺服器發生錯誤，請稍後再試")
```

### 前端（JavaScript）

- 所有 `fetch` 呼叫必須有 `try/catch`
- 顯示用戶友善的錯誤訊息，不顯示技術細節
- 區分網路錯誤與 API 業務錯誤

---

## 七、安全性規範（Security）

- **永不**在程式碼中硬寫 API Key、密碼（使用 `.env` + `python-dotenv`）
- 所有輸入透過 Pydantic Schema 驗證，不接受未宣告的欄位
- SQLAlchemy ORM 查詢可防止 SQL Injection，避免使用 raw SQL
- 密碼必須使用 `passlib[bcrypt]` 雜湊後儲存，絕不明文存入資料庫
- 啟用 CORS 設定，限制允許的來源（`CORSMiddleware`）

---

## 八、生成程式碼的輸出順序（Output Order）

1. **資料庫模型**（`models/`）
2. **Pydantic Schema**（`schemas/`）
3. **CRUD 操作**（`crud/`）
4. **業務邏輯**（`services/`，若有）
5. **路由**（`routers/`）
6. **前端 HTML**（`frontend/`）
7. **前端 JavaScript**（`frontend/js/`）
8. **測試檔案**（`pytest`）

---

## 九、程式碼審查自我檢查清單（Self-Review Checklist）

生成程式碼後，在交付前自我確認：

- [ ] 函式與變數命名符合 Python snake_case 慣例
- [ ] 沒有硬寫的憑證或敏感資訊（使用 `.env`）
- [ ] 所有 API 輸入都透過 Pydantic Schema 驗證
- [ ] FastAPI 路由有正確的 `response_model`
- [ ] SQLAlchemy 查詢使用 ORM，不使用 raw SQL
- [ ] 資料庫 Session 有正確使用 `Depends(get_db)` 管理
- [ ] 前端 fetch 呼叫有 `try/catch` 與錯誤顯示
- [ ] 錯誤情境都有適當的 `HTTPException` 處理
- [ ] 有對應的 pytest 測試覆蓋關鍵邏輯

---

## 撰寫實作指南的核心原則

1. **可讀性優先**：程式碼寫給人看，其次才是機器執行
2. **顯式優於隱式**：讓意圖清楚，避免過度簡寫或魔術行為
3. **一致性**：遵守現有專案的風格，而非引入新慣例
4. **最小驚訝原則**：程式碼的行為應符合讀者的直覺預期
5. **先讓它正確，再讓它快**：不要過早優化，先確保正確性
