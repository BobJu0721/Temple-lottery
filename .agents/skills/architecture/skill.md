---
name: architecture
description: 架構設計文件（Architecture Design Document，ADD）是技術團隊在動手實作前，針對系統結構做出關鍵決策的核心文件。它回答「系統如何被建構」，確保工程師、架構師、維運人員之間對技術方向有共同理解。

---

## 一、文件基本資訊

| 欄位     | 說明                             |
| -------- | -------------------------------- |
| 文件標題 | 系統 / 功能名稱                  |
| 版本號   | v1.0、v1.1…                      |
| 作者     | 主要架構師或技術負責人           |
| 審閱者   | 技術主管、資安、DevOps 等相關人員 |
| 建立日期 | 文件創建時間                     |
| 最後更新 | 最近修改時間                     |
| 狀態     | 草稿 / 審閱中 / 已核准 / 封存    |
| 關聯文件 | 對應 PRD、RFC、Ticket 連結       |

---

## 二、背景與動機（Context & Motivation）

說明「為什麼要設計這套架構」。

- **現況描述**：現有系統或技術棧的狀況
- **問題與挑戰**：當前架構的瓶頸、痛點或限制
- **設計目標**：這份架構設計要解決什麼問題？達成什麼目標？
- **不在此次範圍內**：明確說明本次設計不涵蓋哪些面向

---

## 三、架構目標與非目標（Goals & Non-Goals）

| 類型   | 說明                                       |
| ------ | ------------------------------------------ |
| 目標   | 明確列出此架構要滿足的技術與業務目標       |
| 非目標 | 明確排除，避免設計過度複雜或範圍擴散       |

**常見目標範例：**
- 支援每秒 10,000 筆請求（TPS）
- 系統可用性達 99.95%（SLA）
- 部署時間從 30 分鐘縮短至 5 分鐘

---

## 四、架構概覽（Architecture Overview）

用一張高階圖（High-Level Diagram）說明整體架構，讓讀者快速掌握全局。

- **系統邊界圖（Context Diagram）**：系統與外部實體（用戶、第三方服務）的關係
- **主要組件**：列出核心模組或服務及其職責
- **資料流向**：請求如何從入口流經各組件到輸出

> 建議使用 C4 Model（Context → Container → Component → Code）層次化描述架構。

---

## 五、技術選型（Technology Stack）

說明每個關鍵技術決策，並說明選擇理由。

| 層次         | 技術選擇       | 選擇理由                   | 被淘汰的替代方案 |
| ------------ | -------------- | -------------------------- | ---------------- |
| 前端框架     | React          | 生態成熟、團隊熟悉度高     | Vue、Angular     |
| 後端語言     | Go             | 高併發效能、低記憶體消耗   | Node.js、Python  |
| 資料庫       | PostgreSQL     | ACID 事務支援、查詢靈活度  | MySQL、MongoDB   |
| 快取         | Redis          | 低延遲、支援多種資料結構   | Memcached        |
| 訊息佇列     | Kafka          | 高吞吐量、持久化支援       | RabbitMQ、SQS    |
| 容器化       | Docker + K8s   | 標準化部署、自動擴縮容     | ECS、Nomad       |

---

## 六、詳細架構設計（Detailed Design）

### 6.1 組件設計（Component Design）

針對每個核心組件說明：
- **職責（Responsibility）**：這個組件做什麼事
- **介面（Interface）**：對外暴露哪些 API 或事件
- **內部邏輯**：重要的業務規則或演算法
- **依賴關係**：依賴哪些其他組件或服務

### 6.2 API 設計（API Design）

- RESTful / GraphQL / gRPC 規格
- 端點列表（Endpoint）、請求 / 回應格式
- 認證與授權機制（JWT、OAuth2 等）
- 版本控制策略（URL Versioning、Header Versioning）

### 6.3 資料模型（Data Model）

- 核心實體（Entity）與其屬性
- 實體關聯圖（ER Diagram）
- 資料庫 Schema 或 Collection 結構
- 索引策略（Index Strategy）

### 6.4 資料流程（Data Flow）

- 關鍵操作的請求生命週期（Request Lifecycle）
- 非同步處理流程（Event / Message Flow）
- 批次處理邏輯（Batch Processing）

---

## 七、跨切面關注點（Cross-Cutting Concerns）

### 7.1 安全性（Security）
- 身份驗證（Authentication）與授權（Authorization）
- 資料加密（傳輸中 TLS、靜態加密 AES）
- 敏感資料處理（PII、Secrets 管理）
- 常見威脅防禦（SQL Injection、XSS、CSRF）

### 7.2 效能與擴展性（Performance & Scalability）
- 水平擴展（Horizontal Scaling）策略
- 快取策略（Cache-Aside、Write-Through）
- 資料庫讀寫分離、分片（Sharding）
- CDN 靜態資源加速

### 7.3 可用性與容錯（Availability & Fault Tolerance）
- 冗餘設計（Redundancy）
- 熔斷器模式（Circuit Breaker）
- 重試機制（Retry with Exponential Backoff）
- 優雅降級（Graceful Degradation）

### 7.4 可觀測性（Observability）
- **日誌（Logging）**：結構化日誌格式、集中式收集（ELK、Loki）
- **指標（Metrics）**：系統健康指標、Prometheus + Grafana
- **追蹤（Tracing）**：分散式追蹤（OpenTelemetry、Jaeger）
- **告警（Alerting）**：告警規則、On-call 流程

### 7.5 部署與維運（Deployment & Operations）
- CI/CD 流程設計
- 部署策略（Blue-Green、Canary、Rolling Update）
- 環境規劃（Dev / Staging / Production）
- 備份與災難復原（Backup & DR）策略

---

## 八、架構決策記錄（Architecture Decision Records，ADR）

記錄重要的架構決策，讓未來的人理解「為什麼」當初這樣設計。

每條 ADR 包含：

```
## ADR-001：[決策標題]

**日期**：YYYY-MM-DD  
**狀態**：已接受 / 已棄用 / 已取代

### 背景
為什麼需要做這個決策？

### 決策
我們決定採用什麼方案？

### 理由
為什麼選這個方案而不是其他方案？

### 後果
這個決策帶來哪些影響（正面與負面）？
```

---

## 九、相依關係與整合（Dependencies & Integrations）

- 依賴的內部服務或系統
- 依賴的第三方 API / SaaS（附上 SLA、限流規格）
- 整合方式（同步 / 非同步、Webhook、Polling）
- 服務版本相容性要求

---

## 十、遷移計畫（Migration Plan）

若為改造現有系統，需說明：

- **遷移策略**：大爆炸式（Big Bang）vs. 漸進式（Strangler Fig）
- **相容性處理**：新舊系統並行期間的資料同步方式
- **回滾計畫（Rollback Plan）**：發現問題時如何安全退回
- **遷移里程碑**：各階段時程

---

## 十一、風險與未解問題（Risks & Open Questions）

| # | 風險 / 問題描述           | 嚴重度 | 因應策略         | 負責人 | 狀態   |
|---|---------------------------|--------|------------------|--------|--------|
| 1 | 第三方 API 穩定性未知     | 高     | 加入熔斷與快取   |        | 待確認 |
| 2 | 資料量成長超出預估        | 中     | 提前規劃分片策略 |        | 進行中 |

---

## 十二、詞彙表（Glossary）

定義文件中使用的技術術語或縮寫，避免讀者理解歧義。

| 術語 | 定義 |
|------|------|
| SLA  | Service Level Agreement，服務等級協議 |
| TPS  | Transactions Per Second，每秒交易數  |
| ADR  | Architecture Decision Record，架構決策記錄 |
| CDN  | Content Delivery Network，內容傳遞網路 |

---

## 撰寫架構設計文件的原則

1. **先問為什麼，再說怎麼做**：架構決策需有明確動機，不要只描述實作
2. **圖文並茂**：善用架構圖、時序圖、ER Diagram 幫助讀者理解
3. **記錄被否決的方案**：說明為什麼不選其他方案，避免未來重複討論
4. **設計文件不是程式碼**：描述意圖與邊界，細節留給程式碼與 API 文件
5. **持續更新**：架構演進時同步更新文件，標記版本與變更原因
6. **考慮讀者**：兼顧不同背景的讀者（開發者、維運、管理層）的理解需求
