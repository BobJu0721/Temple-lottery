---
name: test
description: 測試驗證技能指南定義 AI Agent 在撰寫與執行測試時應遵守的規範、測試策略與品質標準，確保產出的測試程式碼能有效驗證業務邏輯、捕捉回歸問題，並作為程式碼的活文件。

---

## 一、測試策略概覽（Testing Strategy）

採用測試金字塔（Testing Pyramid）作為測試比例的基本原則：

```
        /\
       /  \
      / E2E \        ← 少量，驗證關鍵使用者流程
     /--------\
    /Integration\    ← 適量，驗證模組間協作
   /--------------\
  /   Unit Tests   \ ← 大量，快速、獨立、精準
 /------------------\
```

| 測試類型         | 目的                         | 執行速度 | 比例建議 |
| ---------------- | ---------------------------- | -------- | -------- |
| 單元測試（Unit） | 驗證單一函式 / 類別的行為    | 毫秒     | ~70%     |
| 整合測試（Integration） | 驗證模組間、資料庫互動 | 秒       | ~20%     |
| 端對端測試（E2E） | 驗證完整用戶操作流程        | 分鐘     | ~10%     |

---

## 二、測試檔案規範（File Conventions）

- 測試檔案與被測程式碼放在相同目錄（Co-location），或統一放在 `__tests__/` 目錄
- 命名格式：`[被測檔案名稱].test.ts` 或 `[被測檔案名稱].spec.ts`
- 測試輔助工具（Fixture、Factory、Mock）放在 `tests/helpers/` 或 `tests/fixtures/`

```
src/
└── modules/
    └── user/
        ├── user.service.ts
        ├── user.service.test.ts    ← 單元測試（同目錄）
        └── user.repository.ts
tests/
├── integration/
│   └── user.integration.test.ts   ← 整合測試
├── e2e/
│   └── user-flow.e2e.test.ts      ← 端對端測試
└── helpers/
    ├── user.factory.ts             ← 測試資料工廠
    └── mock-database.ts            ← Mock 輔助
```

---

## 三、單元測試規範（Unit Testing）

### 3.1 測試結構：AAA 模式

每個測試案例遵循 **Arrange → Act → Assert** 三段式結構：

```typescript
it('should return user when id is valid', async () => {
  // Arrange（準備測試資料與環境）
  const userId = 'user-123';
  const expectedUser = { id: userId, name: 'Alice' };
  mockUserRepository.findById.mockResolvedValue(expectedUser);

  // Act（執行被測目標）
  const result = await userService.getUserById(userId);

  // Assert（驗證結果）
  expect(result).toEqual(expectedUser);
  expect(mockUserRepository.findById).toHaveBeenCalledWith(userId);
});
```

### 3.2 測試命名規範

使用描述性語句，讓測試失敗時能立即理解問題：

```
// 格式：should [預期行為] when [條件]
✅ should return null when user does not exist
✅ should throw UnauthorizedException when token is expired
✅ should send welcome email when user registers successfully

❌ test1
❌ userService test
❌ works correctly
```

### 3.3 需測試的邊界情境

每個功能至少覆蓋以下情境：

- **Happy Path**：正常流程，輸入合法，預期成功
- **Error Path**：輸入不合法或資源不存在時的錯誤處理
- **Edge Case**：空值、空陣列、最大值、最小值、重複呼叫

### 3.4 Mock 使用原則

- 只 Mock 外部依賴（資料庫、第三方 API、時間、隨機數）
- 不要 Mock 被測目標本身的方法
- Mock 應盡可能接近真實行為，避免過度 Stub

---

## 四、整合測試規範（Integration Testing）

- 使用真實資料庫（建議使用 Docker 啟動測試用的獨立資料庫）
- 每個測試案例執行前清空相關資料表，確保測試隔離
- 測試應涵蓋：API 端點 → Service → Repository → 資料庫的完整鏈路

```typescript
describe('POST /users', () => {
  beforeEach(async () => {
    await db.table('users').truncate();
  });

  it('should create user and return 201', async () => {
    const response = await request(app)
      .post('/users')
      .send({ name: 'Alice', email: 'alice@example.com' });

    expect(response.status).toBe(201);
    expect(response.body.data.email).toBe('alice@example.com');

    const savedUser = await db('users').where({ email: 'alice@example.com' }).first();
    expect(savedUser).toBeDefined();
  });
});
```

---

## 五、端對端測試規範（E2E Testing）

- 針對最關鍵的用戶流程（Critical User Journeys）撰寫
- 測試應從用戶角度描述行為，而非技術實作
- 常見關鍵流程：
  - 用戶註冊 → 登入 → 執行核心操作 → 登出
  - 購物車 → 結帳 → 付款 → 訂單確認
  - 資料建立 → 修改 → 查詢 → 刪除（CRUD 完整流程）

---

## 六、測試資料管理（Test Data Management）

### 6.1 使用 Factory 模式產生測試資料

避免在測試中硬寫大量物件，改用 Factory 集中管理：

```typescript
// tests/helpers/user.factory.ts
export const createUser = (overrides = {}) => ({
  id: 'user-' + Math.random().toString(36).slice(2),
  name: 'Test User',
  email: 'test@example.com',
  status: 'active',
  createdAt: new Date(),
  ...overrides,   // 允許覆寫特定欄位
});

// 使用方式
const inactiveUser = createUser({ status: 'inactive' });
const adminUser = createUser({ role: 'admin', email: 'admin@example.com' });
```

### 6.2 測試資料原則

- 不使用真實的個人資料（姓名、Email、電話）
- 使用語意明確的假資料（`test@example.com` 而非隨機字串）
- 避免測試之間共用狀態，每個測試自帶所需資料

---

## 七、測試覆蓋率規範（Coverage Requirements）

| 覆蓋率類型       | 最低門檻 | 建議目標 |
| ---------------- | -------- | -------- |
| 行覆蓋率（Line） | 70%      | 85%      |
| 分支覆蓋率（Branch） | 60%  | 80%      |
| 函式覆蓋率（Function） | 80% | 90%    |

**注意**：覆蓋率是手段而非目的，100% 覆蓋率不代表沒有 Bug。
重點是覆蓋**關鍵業務邏輯**與**錯誤處理路徑**。

---

## 八、測試案例文件格式（Test Case Documentation）

當需要正式記錄測試案例時（如 QA 驗收），使用以下格式：

| 欄位       | 說明                                 |
| ---------- | ------------------------------------ |
| 測試 ID    | TC-001                               |
| 功能模組   | 用戶管理                             |
| 測試目標   | 驗證用戶登入成功流程                 |
| 前置條件   | 用戶已存在於資料庫，帳號狀態為 active |
| 測試步驟   | 1. 呼叫 POST /auth/login，帶入正確帳密 |
| 預期結果   | HTTP 200，回傳 access_token 與 refresh_token |
| 實際結果   | （執行後填入）                       |
| 通過 / 失敗 | Pass / Fail                         |

---

## 九、CI/CD 整合規範（Continuous Testing）

- 所有測試必須在 CI Pipeline 中自動執行
- Pull Request 合併前必須通過所有測試
- 測試失敗時 Pipeline 應阻斷合併，不允許帶著失敗的測試上線
- 建議分層執行以加快回饋速度：
  1. 單元測試（每次 Push）
  2. 整合測試（每次 PR）
  3. E2E 測試（合併至主分支後 / 部署前）

---

## 十、測試自我檢查清單（Self-Review Checklist）

撰寫測試後，在提交前確認：

- [ ] 每個測試只驗證一個行為（單一斷言原則）
- [ ] 測試命名清楚描述「條件」與「預期行為」
- [ ] 涵蓋 Happy Path、Error Path 與關鍵 Edge Case
- [ ] 沒有測試之間的共用狀態或執行順序依賴
- [ ] Mock 只用於外部依賴，非被測邏輯本身
- [ ] 測試資料使用 Factory 或 Fixture 管理
- [ ] 測試可獨立執行，不依賴執行環境或特定資料
- [ ] 整合測試有正確清理測試資料

---

## 撰寫測試的核心原則

1. **測試即文件**：好的測試案例就是功能規格書，讓人一眼看懂系統行為
2. **測試先於信心**：不是為了覆蓋率而寫測試，而是為了對程式碼有信心
3. **獨立且可重複**：測試執行順序不應影響結果，任何時候都能重跑
4. **快速回饋**：單元測試要夠快（毫秒級），讓開發者樂於頻繁執行
5. **失敗要有意義**：測試失敗時的錯誤訊息要清楚指出問題所在
