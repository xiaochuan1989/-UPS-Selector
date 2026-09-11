# UPS选型助手技术架构

（已更新：2026-09-11，版本 v1.8.38）

## 正式入口

- 唯一产品文件：`index.html`
- 单文件架构是产品约束，便于复制、双击和离线使用。
- GitHub Pages 与 Netlify 公开制品只包含 `index.html`。

## 内嵌数据

- `PRODUCTS`：105 款 UPS。
- `BATTERY_POWER_DATA`：91 款当前电池恒功率数据。
- `MONITOR_PRODUCTS`：15 款监控产品。

## 第三方库容灾（v1.8.38）

- 头部 `LIB_SOURCES` 声明每个库的主源和实测可用备用源：`XLSX`→jsdelivr/unpkg、`mammoth`→jsdelivr/cdnjs、`pdfjsLib`→cdnjs/jsdelivr。
- `libLoadState` 记录 `ready` / `loading` / `failed`；主源未定义全局对象时自动注入备用源。
- `setPdfWorkerSrc` 包裹 `pdfjsLib.GlobalWorkerOptions.workerSrc` 赋值，并在走备用源时切到同源 worker。
- `ensureLib(全局名)` 是所有依赖三方库入口的统一守卫：`importExcel`、`exportProjectSummary`、`exportQuickQuote`、`exportHistory`、`handleDocUpload` 的 DOCX/PDF 分支。
- 新增依赖三方库的入口时必须先调 `ensureLib`，否则库缺失会抛未捕获异常且界面无反馈。

## 功能模块

1. AI选型：`callAI`、`analyze`、`validateModels`、`renderResult`。
2. 产品数据：`importExcel`、IndexedDB 数据持久化、双栏数据库查看、型号全景详情和 localStorage 收藏筛选。
3. 数据中心校核：N、N+1、2N、分布式冗余。
4. 电池统一配置：`calcAllBatteryConfig`。
5. 核心纯函数：
   - `calculateBatteryElectricals`
   - `getNextBreakerSize`
   - `selectCurrentSensor`
   - `getVoltLevel`
6. 后备时间反算：`calcBatteryRuntime`。
7. 项目输出：`renderProjectSummary`、`collectProjectSummaryRows`、`getOrderedSummaryRows`、`exportProjectSummary`、`exportQuickQuote`、`exportTechnicalBrief`。

## 状态

- `localStorage["ups_config"]`：AI接口配置。
- `localStorage["ups_custom_prompt"]`：自定义提示词。
- `localStorage["ups_selection_history"]`：选型历史。
- `localStorage["ups_db_favorites_v1"]`：产品数据库收藏型号。
- `IndexedDB["ups_data_db"]`：用户导入产品。
- `window.projectSummary`：当前项目汇总。
- `window.projectSummary.rowOrder`：汇总清单当前排序。
- `window.projectSummary.hiddenRowKeys`：本次隐藏的标准汇总行；重新计算后恢复。

## 质量门禁

- `test.py --quick`：环境、HTML、版本、结构、业务规则。
- `audit_html.py` 含「零引用函数」检查：全文仅出现定义处一次即判定死代码；确需保留的预留入口写入 `UNREFERENCED_ALLOWLIST` 并说明原因。
- `test.py --all`：增加提示词、Excel、产品JSON和数据库视图检查。
- `audit_html.py`：检查HTML层级、隐藏祖先、DOM ID、函数和DOM引用。
- `test_business_rules.js`：直接提取正式纯函数验证工程公式。
- Playwright：登录、主面板、设置/历史弹窗和计算流程浏览器回归。

## 重要结构规则

- `data-table-panel`、`dc-check-panel`、`runtime-calc-panel`、`battery-calc-v1-panel`、`battery-calc-panel` 必须是 `.container` 的直接子元素。
- 客户需求主卡片不能嵌套在任何 `display:none` 容器中。
- 不保留无UI入口的旧业务函数。
- 文档用函数名定位，不维护易漂移的绝对行号。
- 汇总清单新增列或字段时，必须同步页面渲染、`collectProjectSummaryRows()`、项目汇总Excel、快速报价单和技术说明HTML。
