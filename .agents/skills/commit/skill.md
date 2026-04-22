---
name: commit
description: 提交推送技能指南定義 AI Agent 在執行 Git 提交與推送時應遵守的訊息格式、分支策略與 Pull Request 規範，確保版本歷史清晰可追溯，並讓團隊協作順暢。

---

## 零、Git 使用者設定（Git User Config）

執行 Git 提交前，必須確認已設定使用者資訊。
若無特別指定，一律使用以下預設值：

```bash
# 設定本地專案的 Git 使用者（建議使用 local，避免影響全域設定）
git config user.name "Antigravity"
git config user.email "antigravity@example.com"

# 確認目前設定
git config user.name
git config user.email
```

> **注意**：若使用者有指定自己的 name / email，以使用者提供的為準，不要覆蓋。

---

## 一、Commit 訊息格式規範

採用 **Conventional Commits** 標準，格式如下：

```
<type>(<scope>): <subject>

[body]

[footer]
```

### 各欄位說明

| 欄位      | 必填 | 說明                                       |
| --------- | ---- | ------------------------------------------ |
| `type`    | ✅   | 提交類型（見下表）                         |
| `scope`   | ❌   | 影響範圍，如模組名稱（`user`, `auth`）     |
| `subject` | ✅   | 簡短描述，不超過 72 字元，動詞開頭        |
| `body`    | ❌   | 詳細說明「為什麼」做這個變更               |
| `footer`  | ❌   | 關聯 Issue、Breaking Change 標記           |

---

## 二、Commit Type 類型定義

| Type       | 說明                                       | 範例                                      |
| ---------- | ------------------------------------------ | ----------------------------------------- |
| `feat`     | 新增功能                                   | `feat(auth): add OAuth2 login`            |
| `fix`      | 修復 Bug                                   | `fix(user): correct null check on email`  |
| `docs`     | 文件變更（README、註解等）                 | `docs(api): update endpoint description`  |
| `style`    | 格式調整，不影響邏輯（空白、縮排、分號）   | `style: format code with prettier`        |
| `refactor` | 重構，不新增功能也不修 Bug                 | `refactor(order): extract payment logic`  |
| `test`     | 新增或修改測試                             | `test(user): add unit test for getUserById` |
| `chore`    | 維護性工作（依賴更新、設定檔調整）         | `chore: upgrade typescript to 5.4`        |
| `perf`     | 效能改善                                   | `perf(query): add index on created_at`    |
| `ci`       | CI/CD 設定變更                             | `ci: add coverage report to pipeline`     |
| `revert`   | 還原先前的 Commit                          | `revert: feat(auth): add OAuth2 login`    |
| `build`    | 建置系統或外部依賴變更                     | `build: migrate from webpack to vite`     |

---

## 三、Commit 訊息撰寫原則

### ✅ 好的 Commit 訊息

```
feat(order): add discount calculation for premium users

Premium users now receive a 10% discount automatically applied
at checkout. Discount is calculated before tax and stored in
the order.discount_amount field.

Closes #142
```

### ❌ 不好的 Commit 訊息

```
fix bug          ← 太模糊
update           ← 沒有描述做了什麼
WIP              ← 不應出現在主分支歷史中
asdfgh           ← 完全沒有意義
fixed everything ← 一次改太多事
```

### 撰寫規則

1. **主旨行（subject）**：用祈使語氣動詞開頭，首字小寫，句尾不加句號
   - ✅ `add user authentication`
   - ❌ `Added user authentication.`
2. **主旨行不超過 72 字元**，確保在各工具中完整顯示
3. **body 說明「為什麼」**，而不只是「做了什麼」（程式碼已說明做了什麼）
4. **一個 Commit 只做一件事**，不要把多個不相關的變更混在一起

---

## 四、分支命名規範（Branch Naming）

```
<type>/<issue-id>-<short-description>
```

| Type        | 用途                           | 範例                              |
| ----------- | ------------------------------ | --------------------------------- |
| `feature/`  | 新功能開發                     | `feature/142-premium-discount`    |
| `fix/`      | Bug 修復                       | `fix/156-null-email-crash`        |
| `hotfix/`   | 緊急生產環境修復               | `hotfix/163-payment-timeout`      |
| `release/`  | 版本發布準備                   | `release/v2.3.0`                  |
| `chore/`    | 維護性工作                     | `chore/upgrade-dependencies`      |
| `docs/`     | 文件更新                       | `docs/update-api-reference`       |
| `refactor/` | 重構                           | `refactor/order-service-cleanup`  |
| `test/`     | 補充測試                       | `test/user-service-coverage`      |

**規則**：
- 全小寫，使用 `-` 連接單字
- 附上 Issue ID，方便追溯需求來源
- 描述部分保持簡短（3〜5 個單字）

---

## 五、Git 工作流程（Branching Strategy）

採用 **GitHub Flow** 或 **Git Flow**，依專案規模選擇：

### GitHub Flow（適合持續部署的小型團隊）

```
main
 ├── feature/xxx  → PR → main（合併後立即部署）
 ├── fix/xxx      → PR → main
 └── hotfix/xxx   → PR → main
```

### Git Flow（適合有明確版本週期的團隊）

```
main（生產）
 └── develop（整合）
      ├── feature/xxx  → develop
      ├── release/x.x  → main + develop
      └── hotfix/xxx   → main + develop
```

---

## 六、Pull Request 規範（PR Guidelines）

### 6.1 PR 標題格式

與 Commit 訊息格式一致：

```
feat(auth): add Google OAuth2 login
```

### 6.2 PR 描述範本

```markdown
## 變更摘要（Summary）
簡述這個 PR 做了什麼，以及為什麼要做。

## 變更類型（Change Type）
- [ ] 新功能（feat）
- [ ] Bug 修復（fix）
- [ ] 重構（refactor）
- [ ] 文件更新（docs）
- [ ] 其他：___

## 測試方式（How to Test）
1. 步驟一
2. 步驟二
3. 預期結果

## 截圖（Screenshots）
（如有 UI 變更請附上截圖）

## 關聯 Issue
Closes #<issue-number>

## 審查重點（Review Focus）
請審閱者特別注意以下部分：
- [ ] 業務邏輯是否正確
- [ ] 錯誤處理是否完整
- [ ] 效能是否有潛在問題
```

### 6.3 PR 規模控制

- **理想大小**：一個 PR 只處理一件事，變更行數建議在 400 行以內
- **拆分原則**：若 PR 過大，按功能或層次拆成多個小 PR
- **避免**：把重構、功能開發、Bug 修復混在同一個 PR

---

## 七、提交前自我檢查（Pre-Commit Checklist）

在執行 `git push` 前確認：

- [ ] Commit 訊息符合 Conventional Commits 格式
- [ ] 每個 Commit 只包含相關的變更（不混入不相關的修改）
- [ ] 沒有提交偵錯用程式碼（`console.log`、`debugger`、`TODO: remove`）
- [ ] 沒有提交敏感資訊（API Key、密碼、個人資料）
- [ ] 沒有提交暫存檔、編輯器設定（確認 `.gitignore` 設定正確）
- [ ] 所有測試通過（`pytest`）
- [ ] 程式碼通過格式檢查（`ruff check .` 或 `flake8`）

---

## 八、常用 Git 指令參考

```bash
# 建立並切換到新分支
git checkout -b feature/142-premium-discount

# 分段暫存（只提交部分變更）
git add -p

# 修改最後一次 Commit 訊息（尚未 Push）
git commit --amend

# 整理 Commit 歷史（互動式 Rebase）
git rebase -i HEAD~3

# 同步主分支的最新變更到當前分支
git fetch origin
git rebase origin/main

# 推送並建立遠端分支
git push -u origin feature/142-premium-discount
```

---

## 撰寫提交推送規範的核心原則

1. **每次提交代表一個邏輯單元**：讓 `git log` 成為清晰的變更日誌
2. **提交訊息寫給未來的自己**：六個月後看到這條記錄能理解當時的決策
3. **小步提交，頻繁推送**：避免龐大難 Review 的 Commit
4. **不要重寫已推送的歷史**：`git push --force` 應謹慎使用，使用 `--force-with-lease` 替代
5. **主分支永遠保持可部署狀態**：不合格的程式碼不應進入 `main`
