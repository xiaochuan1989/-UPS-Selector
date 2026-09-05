# UPS 智能选型助手——工程开发手册

> 版本：v1.8.13
> 更新日期：2026-09-05
> 文档职责：说明如何搭建环境、修改代码、运行测试、回归界面和安全发布。

## 1. 开发原则

1. `index.html` 是唯一正式产品入口。
2. 单文件架构是产品约束，不为“看起来工程化”而拆成必须构建才能运行的多文件应用。
3. 同一业务能力只保留一套正式实现；失去 UI 入口的旧函数应删除。
4. 关键公式写成纯函数，并用确定输入输出测试。
5. UI 问题必须在真实浏览器中验证，静态检查不能替代浏览器回归。
6. 测试脚本必须用退出码表达成败，不允许“打印失败但返回成功”。
7. 线上制品只包含 `index.html`。

## 2. 环境要求

推荐环境：

- Node.js 22 或更高版本。
- Python 3.13；最低支持 Python 3.8。
- Chromium 浏览器。

安装依赖：

```powershell
python -m pip install -r requirements-dev.txt
```

如果 Windows 中 `python` 命令不可用，请使用实际 Python 路径：

```powershell
& "C:\Path\To\Python313\python.exe" -m pip install -r requirements-dev.txt
```

## 3. 目录职责

```text
UPS选型助手_开发包/
├── index.html                         # 唯一正式产品
├── README.md                          # 项目入口说明
├── UPS选型助手_开发文档.md             # 产品、架构、公式
├── UPS选型助手_开发说明.md             # 本工程手册
├── requirements-dev.txt               # Python 开发依赖
├── netlify.toml                       # Netlify 质量门禁与发布配置
├── .github/workflows/deploy.yml       # GitHub Pages 测试与发布
├── .serena/                           # Serena 项目配置和项目记忆
├── dev_scripts/                       # 测试、审计和开发服务器
├── prompts/                           # AI 提示词参考
├── src/css/                           # 历史样式参考，不是正式加载入口
├── 常用UPS速查表-V8.0.xlsx             # 当前质量检查使用的数据源
└── 归档/                              # 历史资料和待清理垃圾分区
```

历史、生成或调试材料已经从根目录归类到 `归档/`：

- `归档/历史文档/`：`UPS选型助手_backup.html`、`battery_power_data.js`、`full_doc_content.txt`、`temp_spec.txt`、`detailed_params*.txt`、`gen_word*.py` 等。
- `归档/历史数据源与模板/`：旧 Excel / xlsm 模板和历史数据源。
- `归档/历史测试数据/`：早期测试数据和试验脚本。
- `归档/垃圾待清理/`：旧部署输出、旧会话、旧评估目录和确认可删除前的垃圾暂存区。

正式页面本身不引用 `归档/` 下文件。删除 `归档/垃圾待清理/` 前，仍建议先看一眼是否有外部流程临时需要。

## 4. 常用命令

### 4.1 快速检查

```powershell
python dev_scripts/test.py --quick
```

执行：

- 开发环境与关键文件检查。
- HTML 基础结构检查。
- 版本一致性检查。
- HTML/JavaScript 结构审计。
- 核心业务公式测试。

### 4.2 完整检查

```powershell
python dev_scripts/test.py --all
```

在快速检查基础上增加：

- AI 提示词功能检查。
- Excel 数据结构检查。
- 所有内联 JavaScript 的 Node.js 语法检查。
- 产品 JSON 深度检查。
- 双栏数据库视图检查。

### 4.3 构建验证

```powershell
python dev_scripts/build.py --verify
```

该命令会：

1. 检查验证脚本是否齐全。
2. 执行基础质量检查。
3. 真实运行 `test.py --all`。
4. 任一检查失败时返回非零退出码。

### 4.4 本地服务器

```powershell
python dev_scripts/serve.py
python dev_scripts/serve.py --no-open
python dev_scripts/serve.py --port 9000
python dev_scripts/serve.py --watch
```

未安装 `watchdog` 时，普通服务器仍可启动；只有 `--watch` 会使用降级轮询。

## 5. 测试体系

| 文件 | 作用 |
|---|---|
| `test.py` | 统一入口，聚合结果并正确返回退出码 |
| `scan_js.py` | 用 Node.js 编译每个内联 script |
| `audit_html.py` | 检查 HTML 层级、隐藏祖先、重复 DOM ID、重复函数和失效 DOM 引用 |
| `test_business_rules.js` | 测试断路器、电池电气量、传感器和电压等级 |
| `check_version.py` | 检查页面与三份文档版本一致 |
| `check_html.py` | 检查产品 JSON、关键函数和脚本边界 |
| `check_prompt_feature.py` | 检查提示词设置与调用链 |
| `verify.py` | 检查双栏数据库视图 |
| `inspect_excel.py` | 检查产品 Excel Sheet 和表头 |

### 5.1 为什么需要 HTML 层级审计

浏览器会容忍不完整的 HTML 标签。一个缺失的 `</div>` 可能让整个客户需求卡片嵌套进 `display:none` 面板：

- JavaScript 语法仍然通过。
- DOM ID 仍然存在。
- 关键词检查仍然通过。
- 页面却只显示页头和页脚。

因此 `audit_html.py` 明确验证核心面板是 `.container` 的直接子元素，并确认客户需求卡片没有隐藏祖先。

### 5.2 核心业务测试

`test_business_rules.js` 直接从 `index.html` 提取并执行正式函数，不复制另一套公式。当前覆盖：

- 断路器向上选档和异常输入。
- 12V/2V 单格数。
- 单体功率、最大放电电流和分组电流。
- 单组/多组传感器电流口径。
- 传感器量程边界。
- 250VDC、500VDC、750VDC 电压等级边界。

新增或修改公式时，必须先增加边界测试，再修改正式函数。

## 6. 浏览器回归

推荐使用 Playwright CLI 或人工浏览器完成。

最低回归清单：

1. 输入访问码并进入主界面。
2. 确认默认停在"智能选型"标签页，客户需求卡片可见。
3. 依次切换顶部标签页，确认为单视图切换（切到目标面板、其余隐藏、当前标签高亮）：
   - UPS 与电池配置
   - 后备时间反算
   - 电池计算（方法一/锂电）
   - 数据中心校核
   - 产品数据库
4. 打开设置和历史弹窗。
5. 完成一次数据中心容量校核。
6. 完成一次统一电池配置计算。
7. 完成一次后备时间反算。
8. 检查浏览器控制台无 error。
9. 在 1280px 桌面宽度和窄屏宽度各检查一次页头及主要表单。

浏览器截图和 trace 放入：

```text
output/playwright/<任务名称>/
```

`output/` 不进入正式部署。

## 7. 修改工作流

### 7.1 开始前

```powershell
git status --short --branch
python dev_scripts/test.py --quick
```

确认：

- 工作树中是否已有用户改动。
- 当前页面和测试基线是否健康。
- 需求是否涉及工程公式；不确定时先确认业务规则。

### 7.2 修改中

- 用函数名、DOM ID 和业务对象定位代码，不依赖文档中的旧行号。
- 修改下拉枚举时，全局搜索同一类别的标签、映射表和导出逻辑。
- 新增配置项时同步检查：输入、计算、`projectSummary`、渲染、Excel、技术说明。
- 不直接拼接未经转义的用户输入到导出 HTML。
- 不新增生产 `console.log`；临时调试使用 `debugLog`，提交前保持 `DEBUG_MODE=false`。

### 7.3 完成后

```powershell
python dev_scripts/test.py --all
python dev_scripts/build.py --verify
git diff --check
git status --short
```

然后执行真实浏览器回归。

## 8. 业务修改检查表

### 8.1 电池或开关箱

- [ ] 明确功率来源是负载功率还是 UPS 额定功率。
- [ ] 明确 `groups` 是每台 UPS 组数，不是项目总组数。
- [ ] 明确 `upsNum` 只影响项目总数量和开关箱套数。
- [ ] 单组与多组电池边界均测试。
- [ ] 2V 与 12V 电池均测试。
- [ ] 断路器和传感器边界值均测试。

### 8.2 数据中心架构

- [ ] N 不显示故障后容量概念。
- [ ] N+1 的输入 N 与总台数 N+1 不混用。
- [ ] 2N 分别校核 A/B 路，不能只按总台数除二。
- [ ] 架构切换后的字段显示和导入换算正确。
- [ ] 容量不足、目标负载率过高和参数缺失均有提示。

### 8.3 导出

- [ ] 页面显示和导出使用同一数据源。
- [ ] 模块化 UPS 的机框和功率模块拆分正确。
- [ ] 客户指定电池允许空内置型号。
- [ ] 价格列受当前显示开关控制。
- [ ] 用户输入经过 `escapeHtml`。

## 9. 数据更新

### 9.1 UPS 数据

产品 Excel 主要 Sheet：

| 系列 | 基础信息 | 技术规格 |
|---|---|---|
| 太行 UR | 太行UR | UR泰尔 |
| 昆仑 UE | 昆仑UE | UE泰尔 |
| 祁连 UM | 祁连UM | UM泰尔 |
| 泰山 UT | 泰山UT | UT泰尔 |

更新后必须确认：

- 型号唯一。
- 基础表和规格表可正确合并。
- 产品数量变化同步到页面说明和文档。
- 模块化型号解析仍正确。

### 9.2 电池数据

更新 `BATTERY_POWER_DATA` 时：

- 同一型号、截止电压和时间点不能重复。
- 空功率点不得作为推荐候选。
- 时间单位统一为分钟。
- 数值从 Excel 导入后进行合理精度清理。
- 同步验证正向推荐和后备时间反算。
- 稀疏恒功率表只开放实际存在数据的“时间 × 截止电压”组合，禁止补算厂家未提供的数据点。
- 厂家原表存在重复或异常曲线时保留原值并在选型结果中明确提示复核，不静默修正。

## 10. 部署

### 10.1 GitHub Pages

推送 `master` 后：

1. `quality` Job 安装 Node/Python 依赖。
2. 执行 `python dev_scripts/test.py --all`。
3. 只有测试通过才运行 `deploy`。
4. 构建公开目录，只复制 `index.html`。
5. 上传到 GitHub Pages。

线上地址：

<https://xiaochuan1989.github.io/-UPS-Selector/>

### 10.2 Netlify

Netlify 构建命令先执行快速测试，然后只复制：

```text
index.html → public/index.html
```

`public/` 已加入 `.gitignore`。

## 11. 版本管理

升级版本时：

1. 修改 `index.html` 的 `APP_VERSION`。
2. 同步修改：
   - `README.md`
   - `UPS选型助手_开发文档.md`
   - `UPS选型助手_开发说明.md`
3. 更新对应版本说明。
4. 运行完整测试。

`check_version.py` 会阻止版本不一致。

## 12. 安全规则

- 禁止提交真实 API Key、Token 或客户敏感资料。
- `.mcp.json` 包含本机绝对路径，只用于本地开发，不进入 Git 和公开部署制品。
- 客户端访问码和价格码不是安全权限，不应保护真正机密数据。
- API Key 存在 localStorage，公共电脑使用后应清除浏览器数据。
- GitHub Pages 和 Netlify 不得发布 Excel 模板、Serena 记忆、聊天记录或调试文件。

## 13. 故障排查

### 页面只有页头和页脚

1. 运行 `python dev_scripts/audit_html.py`。
2. 检查核心面板是否被错误嵌套进隐藏容器。
3. 用 Playwright 或浏览器检查实际 DOM，而不是只看源码缩进。

### 按钮点击无反应

1. 检查浏览器控制台。
2. 检查函数是否访问不存在的 DOM ID。
3. 检查面板是否实际可见。
4. 运行 `scan_js.py` 和 `audit_html.py`。

### 开发服务器无法启动

1. 运行 `python dev_scripts/serve.py --no-open` 查看错误。
2. 确认端口未占用。
3. 未安装 `watchdog` 不应影响普通启动。

### 电池结果不合理

1. 确认功率来源。
2. 确认每台组数与项目总组数。
3. 确认电池类别、截止电压和时间点存在。
4. 运行 `test_business_rules.js`。
5. 对照厂家恒功率表复核。

## 14. 发布完成标准

- [ ] 用户需求已经实现，而不是只修改文档。
- [ ] 无重复或失去入口的业务实现。
- [ ] 关键公式有自动测试。
- [ ] 快速测试通过。
- [ ] 完整测试通过。
- [ ] 构建验证通过。
- [ ] 浏览器主流程回归通过。
- [ ] 控制台无 error。
- [ ] 文档和 Serena 记忆已更新。
- [ ] 部署制品仅包含 `index.html`。
