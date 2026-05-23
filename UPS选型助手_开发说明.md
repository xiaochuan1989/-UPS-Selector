# UPS 智能选型助手 - 工程化开发环境

> 版本：v1.6.8
> 更新日期：2026-05-23

## 当前结论

- 当前主程序只有一个：`index.html`。
- 不再维护旧版中文命名 HTML 和 `index.html` 两份同步文件。
- GitHub Pages 直接发布仓库根目录，入口为 `index.html`。
- Netlify 备选部署也应访问根目录的 `index.html`。
- `dev_scripts/` 是辅助开发脚本；脚本默认入口应指向项目根目录的 `index.html`。

## 项目结构

```
UPS选型助手_开发包/
├── index.html                # 主程序文件（单文件产品）
├── 常用UPS速查表-V7.5.xlsx   # UPS产品数据源
├── 锂电池-选型模板-A00.xlsx  # 锂电池选型参考模板
├── UPS选型助手_开发文档.md    # 产品开发文档
├── UPS选型助手_开发说明.md    # 本文件
├── netlify.toml              # Netlify 部署配置
├── .gitignore               # Git 忽略配置
│
├── .mcp.json                 # MCP 服务器配置（Serena 等）
│
├── .serena/                  # Serena MCP 项目配置
│   └── project.yml          # 项目语言、编码等设置
│
├── src/                      # 源代码目录（工程化用）
│   └── css/
│       └── style.css        # 样式表（已提取）
│
├── dist/                     # 构建输出目录（预留）
│
├── dev_scripts/              # 开发辅助脚本
│   ├── build.py             # 构建信息/质量检查/开发服务
│   ├── serve.py             # 开发服务器
│   ├── test.py              # 统一测试入口
│   ├── check_prompt_feature.py
│   ├── verify.py
│   ├── check_html.py
│   ├── scan_js.py
│   └── inspect_excel.py
│
└── test_data/               # 测试数据
    └── 常用UPS速查表-V7 测试.xlsx
```

## 快速开始

### 1. 构建命令

```bash
# 显示构建信息
python dev_scripts/build.py --info

# 运行质量检查
python dev_scripts/build.py --verify

# 生成开发说明
python dev_scripts/build.py --readme

# 启动开发服务器
python dev_scripts/build.py --serve
```

### 2. 开发服务器

```bash
# 启动开发服务器（默认端口 8080）
python dev_scripts/serve.py

# 指定端口
python dev_scripts/serve.py --port 9000

# 不自动打开浏览器
python dev_scripts/serve.py --no-open

# 开启文件监听（需安装 watchdog）
python dev_scripts/serve.py --watch
```

### 3. 统一测试入口

```bash
# 快速检查（环境 + HTML）
python dev_scripts/test.py --quick

# 运行所有测试
python dev_scripts/test.py --all

# 单独运行某项测试
python dev_scripts/test.py --prompt    # 提示词验证
python dev_scripts/test.py --excel     # Excel 验证
python dev_scripts/test.py --html      # HTML 验证
python dev_scripts/test.py --js        # JS 代码扫描
python dev_scripts/test.py --env       # 环境检查
```

## 工程化说明

### 已实现功能

| 功能 | 状态 | 说明 |
|------|------|------|
| CSS 独立文件 | ✅ | 提取到 `src/css/style.css` |
| 构建脚本 | ✅ | `build.py` - 构建信息/质量检查/生成文档 |
| 开发服务器 | ✅ | `serve.py` - HTTP 服务/文件监听 |
| 统一测试入口 | ✅ | `test.py` - 整合所有验证工具 |

### 开发流程

```
1. 修改代码
   ↓
2. 运行测试 (python dev_scripts/test.py --quick)
   ↓
3. 用浏览器测试 (python dev_scripts/serve.py)
   ↓
4. 验证通过后提交并推送到 GitHub
   git add .
   git commit -m "描述更新内容"
   git push origin master
   ↓
5. GitHub Pages 自动部署（约1-2分钟）
   访问 https://xiaochuan1989.github.io/-UPS-Selector/ 查看
```

### 代码修改后测试

1. **方式一：直接打开**
   - 双击 `index.html` 在浏览器中打开

2. **方式二：开发服务器**
   ```bash
   python dev_scripts/serve.py
   ```
   - 自动打开浏览器
   - 开启文件监听模式（可选）

3. **方式三：验证脚本**
   ```bash
   # 快速检查
   python dev_scripts/test.py --quick

   # 完整验证
   python dev_scripts/test.py --all
   ```

## 现有脚本说明

| 脚本 | 用途 |
|------|------|
| `build.py` | 构建工具：显示信息、质量检查、启动服务 |
| `serve.py` | 开发服务器：HTTP 服务、文件监听、自动打开浏览器 |
| `test.py` | 测试入口：整合所有验证工具 |
| `check_prompt_feature.py` | 验证提示词功能是否正确嵌入 |
| `verify.py` | 验证双表数据库视图功能 |
| `check_html.py` | HTML 基础结构检查 |
| `scan_js.py` | JS 代码扫描（检测可疑引号等） |
| `inspect_excel.py` | 检查 Excel 数据结构 |

## 线上部署

### 网站地址
**https://xiaochuan1989.github.io/-UPS-Selector/**

### GitHub 仓库

| 项目 | 说明 |
|------|------|
| 仓库地址 | https://github.com/xiaochuan1989/-UPS-Selector |

### GitHub Pages 部署

| 项目 | 说明 |
|------|------|
| 部署方式 | GitHub Actions 自动部署 ⭐ |
| Workflow 文件 | `.github/workflows/deploy.yml` |

**首次设置步骤：**
1. 进入仓库 **Settings** → **Pages**
2. 在 **Build and deployment** 下，Source 选择 **GitHub Actions**
3. 点击 **Save**

**后续部署流程（每次功能更新）：**
```bash
# 1. 进入项目目录
cd "D:\Claude 安装\UPS选型助手_开发包"

# 2. 提交修改并推送到 GitHub
git add .
git commit -m "描述更新内容"
git push origin master

# 3. 等待约1分钟，GitHub Actions 自动部署

# 4. 访问 https://xiaochuan1989.github.io/-UPS-Selector/ 查看更新
```

### Netlify 部署（备选）

当 GitHub Pages 不可用时可使用 Netlify：

| 项目 | 说明 |
|------|------|
| Site ID | c662b019-245f-4a7f-af88-53c9b72502da |
| 部署方式 | Git 自动部署 |

### 关联 GitHub 仓库（首次设置）

1. 打开 https://app.netlify.com
2. 选择站点 **ups-selector**
3. 点击 **Site settings**
4. 找到 **Build & deploy** → 点击 **Link repository**
5. 选择 **GitHub**，授权后选择 **`-UPS-Selector`** 仓库
6. 点击 **Save**

### 后续部署流程（每次功能更新）

```bash
# 1. 进入项目目录
cd "D:\Claude 安装\UPS选型助手_开发包"

# 2. 提交修改并推送到 GitHub
git add .
git commit -m "描述更新内容"
git push origin master

# 3. 等待约1-2分钟，Netlify 自动部署

# 4. 访问 https://ups-selector.netlify.app 查看更新
```

### 注意事项

⚠️ **重要**：每次修改代码后，一定要执行 `git add .` 把文件添加到暂存区，否则文件不会提交到 GitHub。

⚠️ **不要删除 index.html 文件**，这是主程序文件，必须保留在项目文件夹中。

### 手动部署（备选）

如果自动部署未关联，可以手动部署：

```bash
# 方式一：手动上传
# 打开 https://app.netlify.com/sites/ups-selector
# 拖拽 index.html 到页面

# 方式二：使用 Netlify CLI
netlify deploy --dir . --prod --site c662b019-245f-4a7f-af88-53c9b72502da
```

## 注意事项

- 当前主要代码在 `index.html` 中
- 当前已是单文件主线，不再做两个 HTML 文件同步
- `src/` 目录的模块化是渐进式的，不会影响现有功能
- 修改 `index.html` 后可直接在浏览器测试
- 需要 Python 3.8+ 环境
- IndexedDB 持久化相关函数（`openDatabase`、`saveProductsToDB`、`loadProductsFromDB`）必须定义在 `DOMContentLoaded` 回调之前，否则页面加载时会报 `Cannot access 'db' before initialization` 错误
- Serena MCP 配置在 `.serena/project.yml` 中，全局配置在 `C:\Users\woaig\.claude.json` 中

## ⚠️ 核心开发教训（v1.4.2-v1.4.6 血泪总结）

### 传感器量程选择 Bug 修复过程（连续5次失败）

| 次数 | 假设的公式 | 结果 |
|------|-----------|------|
| 第1次 | `singleGroupCurrent = maxCurrent / groups` | ❌ |
| 第2次 | 修复描述显示问题 | 没解决根本 |
| 第3次 | 改 calcMonitorConfig 的公式 | ❌ |
| 第4次 | 又改回 singleGroupCurrent | ❌ |
| 第5次 | 用户说"根据分开关电流"后才对 | ✓ |

### 正确公式（用户确认）

```
传感器量程基于【分开关电流】选择：
- 当 groups >= 2: 传感器电流 = maxCurrent / (groups - 1)
- 当 groups = 1: 传感器电流 = maxCurrent
```

### 根本教训

| 错误 | 说明 | 改进措施 |
|------|------|----------|
| **不理解业务就动手** | 凭自己假设公式 | 涉及公式时，先问"正确规则是什么？" |
| **不主动询问** | 不确定时不问，直接猜 | 让用户提供原始公式或参考文档 |
| **用户说错时继续猜** | "还是错的"时继续改代码 | 停下来问"我可能理解错了，正确规则是什么？" |
| **验证走过场** | 只读代码不验证业务 | 让用户确认业务逻辑是否正确 |

### 开发流程改进

```
❌ 错误流程：凭理解直接改代码 → 用户说错了 → 继续猜 → 再改 → 再错

✓ 正确流程：
1. 涉及业务逻辑/公式时，先问用户"正确规则是什么？"
2. 让用户指出"Excel里怎么算的"或"文档在哪"
3. 用户说"还是错的"时，停下来问清楚，不要继续猜
4. 修改后让用户确认业务逻辑是否正确
```

## 依赖安装（可选）

```bash
# 文件监听功能（可选）
pip install watchdog
```

## ⚠️ 核心教训（v1.4.2-v1.4.6 传感器量程修复）

### 问题回顾
修复传感器量程选择时，连续5次改错，浪费大量时间。

### 根本原因
| 问题 | 表现 |
|------|------|
| **不理解业务逻辑就动手** | 凭自己假设"单组正常工作电流"，实际是"分开关电流" |
| **不确定时不主动询问** | 不问用户正确规则，直接猜测 |
| **用户说"还是错的"时继续猜** | 不停下来问清楚，继续修改代码 |
| **验证走过场** | 只读代码不验证业务逻辑 |

### 正确做法（必读！）

```
❌ 锭误：凭理解直接改代码
✓ 正确：先问"正确规则是什么？公式来源是什么？"

❌ 错误：用户说"还是错的"时继续猜测
✓ 正确：停下来问"我可能理解错了，正确规则是什么？"

❌ 错误：说"我验证了"但只读了代码
✓ 正确：让用户确认或提供原始公式/参考文档
```

### 传感器量程选择公式（已确认）
```javascript
// 传感器量程基于【分开关电流】选择
// 分开关电流 = 总电流 / (groups - 1)，当 groups >= 2
// 分开关电流 = 总电流，当 groups = 1
const sensorCurrent = groups >= 2 ? groupCurrent : maxCurrent;
```

## ⚠️ v1.4.7 教训：组件遗漏（测试线缆）

### 问题回顾
`calcAllBatteryConfig` 函数中缺少测试线缆配置，用户提醒后才发现。

### 根本原因
| 问题 | 说明 |
|------|------|
| **没有组件清单意识** | 修改监控配置时，没有先列出"应该包含哪些组件" |
| **未对照参考实现** | 没有对照已有的 `calcMonitorConfig` 函数逐项核对 |
| **修复范围太窄** | 只看传感器问题，没检查整个配置 |

### 组件清单核对（新增！）

```
⚠️ 修改配置类代码时：

❌ 错误：直接上手改代码，想到什么写什么
✓ 正确：
   1. 先列出"应该包含哪些组件"
   2. 对照参考实现逐项核对
   3. 确认每个组件都有正确的参数来源
```

### 监控配置组件清单（参考）
| 组件 | 产品编码 | 说明 |
|------|----------|------|
| 主机 | 88091156 | 必选 |
| HMI | 88091157 | 选配 |
| 单体测量模块 | 88091145/88091146 | 根据电池类型 |
| **测试线缆** | 88091147/88091148/88091149 | **根据端子类型** ⚠️ |
| 电压采集 | 88091150 | 选配 |
| 电流监控 | 88091138 | 必选 |
| 电流传感器 | 88091139-88091144 | 根据电流量程 |

## ⚠️ v1.4.8 教训：函数返回值解构错误

### 问题回顾
`calcAllBatteryConfig` 中调用 `getVoltLevel()` 后直接使用返回值，导致显示 `[object Object]`。

### 根本原因
| 问题 | 说明 |
|------|------|
| **未确认函数返回类型** | `getVoltLevel` 返回对象 `{level, levelNum, maxChargeVoltage}`，但调用处直接当字符串使用 |
| **历史双文件不同步** | 旧版本曾同时维护两个 HTML，容易出现函数返回类型不一致 |

### 正确做法

```javascript
// ❌ 错误：直接使用返回值
const voltLevel = getVoltLevel(cells, battType);
// voltLevel 是对象，显示时变成 "[object Object]"

// ✓ 正确：解构返回值
const voltResult = getVoltLevel(cells, battType);
const voltLevel = voltResult.level;  // 获取字符串
```

### 电压等级新公式（v1.4.8 更新）
```
最大充电电压 = 2.35V × 单格数 × 电池节数
- 2V电池：单格数=1
- 12V电池：单格数=6

电压等级判断：
- ≤250V → 250VDC
- 251~500V → 500VDC
- >500V → 750VDC
```

---

## ⚠️ v1.4.11-v1.4.12 教训：需求确认与功能范围

### v1.4.11 经验：祁连UM模块化UPS分两行

**实现要点**：
- 模块化UPS = 机框 + 功率模块
- 选型结果表格、项目汇总清单、导出Excel三处都要支持
- 数据结构扩展：`isModular`, `frame`, `module`, `moduleQty`, `maxModules`

**注意事项**：
- 只有祁连UM系列需要拆分（判断条件：`series.includes('UM')`）
- 太行UR、昆仑UE、泰山UT是塔式UPS，不需要拆分
- 测试时确认边界情况：非UM系列不应该被错误拆分

### v1.4.12 经验：非标UPS和可编辑字段

**需求背景**：
- 客户使用的UPS可能不在内置数据表中（其他品牌、定制型号）
- 电池推荐型号可能不满足客户需求，需要手动修改

**实现方案**：
| 字段 | 可编辑 | 优先级 |
|------|--------|--------|
| UPS型号 | ✅（非标模式） | customModel > model |
| UPS描述 | ✅（非标模式） | customDesc > capacity |
| 电池型号 | ✅ | customModel > model |
| 电池描述 | ✅ | customDesc > 默认计算值 |
| 开关箱 | ❌ | 自动生成 |
| 监控 | ❌ | 自动生成 |

**关键代码**：
```javascript
// 非标UPS数据结构
window.projectSummary.ups = {
  model: '',
  isCustom: false,     // 是否非标
  customDesc: '',      // 用户输入的描述
  // ...
}

// 电池可编辑字段
window.projectSummary.battery = {
  model: '',           // 推荐型号
  customModel: '',     // 用户修改后的型号（优先）
  customDesc: '',      // 用户修改后的描述（优先）
  // ...
}
```

**用户交互设计**：
1. 标准/非标切换放在UPS配置面板顶部
2. 非标模式显示手动输入框
3. 汇总清单中非标UPS显示橙色标签
4. 可编辑字段使用 `<input>` 而非纯文本

---

## ⚠️ v1.5 教训：电池架和电池开关功能

### 功能概述
- **电池架**：项目汇总清单新增电池架项，支持含铜排/电缆选项
- **电池开关**：合资/国产开关选择，显示在开关箱描述中

### 实现要点
| 功能 | 数据字段 | UI选项 | 同步更新位置 |
|------|----------|--------|--------------|
| 电池架 | batteryRack | 电池架含铜排 | 数据结构、渲染、导出 |
| 电池开关 | switchBox.switchType | 合资/国产 | 数据结构、渲染、导出 |

### UI提示图标
```html
<span class="tip-icon" title="重要提示：合资开关为施耐德/ABB/西门子等品牌，国产开关为良信/正泰/天正/德力西等品牌">❗</span>
```

### 经验教训
- 新增配置项需要同步更新：数据结构初始化、渲染函数、导出函数
- 提示图标使用❗配合title属性显示详细信息
- 修改updateXxx函数后需要检查是否需要调用renderProjectSummary

---

## ⚠️ v1.5.1 教训：清除按钮不响应（访问不存在的DOM元素）

### 问题回顾
点击项目汇总清单的"清空"按钮没有任何反应，同时Excel导出功能也受影响。

### 根本原因
| 问题 | 说明 |
|------|------|
| **访问不存在的DOM元素** | `clearProjectSummary()` 函数访问了从未定义的元素ID |
| **旧版本遗留代码** | `summary-ups-model` 等ID可能是旧版本遗留，当前HTML中不存在 |
| **JS报错阻断执行** | `getElementById` 返回 `null`，访问 `null.value` 报错 |

### 错误代码示例
```javascript
function clearProjectSummary() {
  window.projectSummary = { ... };
  document.getElementById('summary-ups-model').value = '';  // ❌ 元素不存在
  document.getElementById('summary-ups-cap').value = '';    // ❌ null.value 报错
}
```

### 修复方案
删除对不存在元素的访问代码。

### 正确做法（必读！）
```
⚠️ 修改函数时，必须确认其中引用的DOM元素确实存在：

❌ 错误：函数中访问了从未定义的DOM元素
✓ 正确：
   1. 搜索 getElementById 调用
   2. 验证每个元素ID在HTML中确实定义
   3. 不能假设"以前能用"就永远能用
   4. 清理旧版本遗留的无效代码引用
```

---

## ⚠️ v1.6 教训：选型历史记录功能

### 功能概述（v1.6）

**新增功能**：
- 选型历史记录保存（最多50条）
- 历史搜索和过滤
- 导出Excel
- 恢复历史选型结果

**实现要点**：
| 组件 | 说明 |
|------|------|
| 数据存储 | `localStorage["ups_selection_history"]` |
| UI入口 | 顶部工具栏"📋 历史"按钮 |
| 弹窗 | `#history-modal` + `#history-panel` |

### 实现经验

1. **历史双文件同步成本高**：v1.6 历史记录功能曾需要同时修改两份 HTML，容易遗漏
2. **数据版本管理**：使用 `version: 1` 字段便于后续升级
3. **数量限制**：超出50条时 `slice(0, 50)` 自动清理

### 经验教训

```
⚠️ 当前已改为单文件主线

✓ 正确流程：
   1. 修改 index.html
   2. 验证 JS 语法和关键交互
   3. 同步更新相关文档
```

---

## ⚠️ v1.6 教训：图片OCR识别功能

### 功能概述（v1.6）

**实现历程**：
1. 最初尝试使用本地 OCR 库 → 失败（CORS限制，本地file://无法加载CDN）
2. 改用 AI 视觉识别 → 成功

**API多模态支持**：
```javascript
// callAI 函数支持 images 参数
async function callAI(userMessage, systemPrompt, images) {
  // images: base64格式的图片数组
  // 支持 GPT-4V、Claude3、kimi2.5 等视觉模型
}
```

### 实现经验

1. **file://协议限制**：从本地文件打开HTML时，浏览器安全策略阻止加载外部CDN脚本
2. **解决方案**：
   - 使用本地服务器（`python -m http.server`）
   - 或使用支持视觉识别的AI API直接识别

2. **OCR vs AI视觉**：
   - 本地OCR：需加载模型，识别精度一般，且本地 file:// 场景容易受限
   - AI视觉：调用云端API，识别精度高，但需要支持视觉的模型

3. **粘贴事件处理**：
   - 在整个 `document` 上监听 `paste` 事件
   - 而不是只在 `textarea` 上监听

### 经验教训

```
⚠️ 本地HTML文件使用外部CDN的限制

✓ 正确做法：
   1. 使用本地服务器运行（python -m http.server）
   2. 或使用内嵌版本的 OCR 库文件
   3. 或依赖浏览器不限制的API（如AI视觉识别）

❌ 直接双击HTML打开时，某些CDN资源会被浏览器阻止
```

---

## ⚠️ v1.6 教训：Excel导出行高自适应

### 问题描述

导出选型历史到Excel时，分析内容列显示不全。

### 解决过程

| 尝试 | 方法 | 结果 |
|------|------|------|
| 第1次 | 固定行高60pt | ❌ 不够 |
| 第2次 | 固定行高200pt | ❌ 还是不够 |
| 第3次 | 固定行高300pt | ⚠️ 勉强够 |
| 第4次 | 动态计算行高 | ✅ 根据内容长度自动调整 |

### 正确做法

```javascript
// 根据内容长度动态计算行高
const colWidths = [6, 18, 45, 35, 35, 80]; // 每列宽度
for (let r = 1; r < wsData.length; r++) {
  let maxLines = 1;
  for (let c = 0; c < 6; c++) {
    const content = String(wsData[r][c] || '');
    const charsPerLine = Math.floor(colWidths[c] * 0.5);
    const lines = Math.max(1, Math.ceil(content.length / charsPerLine));
    maxLines = Math.max(maxLines, lines);
  }
  ws['!rows'].push({hpt: Math.max(30, maxLines * 18)});
}
```

### 经验教训

```
⚠️ Excel行高自适应不能用固定值

✓ 正确做法：
   1. 根据列宽和内容长度估算行数
   2. 每行约18pt高度
   3. 设置最小行高保证可读性
```

---

## 📋 版本更新规范（v1.6）

### 提交信息格式

```
[版本] 功能/修复描述

示例：
git commit -m "[v1.6] 新增选型历史记录和图片OCR识别功能"
```

### 文档更新清单

每次版本更新需要同步更新：

| 文档 | 更新内容 |
|------|----------|
| `UPS选型助手_开发文档.md` | 功能变更、版本历史 |
| `UPS选型助手_开发说明.md` | 经验教训、工程规范 |
| Serena Memory | 项目概览、待办事项 |

### 单文件更新检查清单

每次代码修改后：

```
□ index.html 已修改
□ 相关文档已更新
□ 功能测试通过
□ GitHub 已推送
```

---

## v1.6.7 更新记录（2026-05-22）

### 功能优化
- `UPS与电池配置计算`中的标准UPS型号控件由 `input + datalist` 改为真正的 `select` 下拉框。
- 选择过一个UPS型号后，再次点击下拉框可直接切换其他型号，无需先删除已选文本。
- 非标UPS仍通过“非标型号”模式手动输入，不影响原有非标流程。

### 工程化同步
- 主程序入口统一为 `index.html`，README、开发说明、Netlify配置和开发脚本同步更新。
- 移除未使用的本地OCR外部依赖引用，favicon改为内嵌SVG，减少外部资源失效风险。
- 开发脚本默认读取项目根目录的 `index.html`，并修复Windows控制台UTF-8输出和Excel检查脚本旧绝对路径问题。

### 验证
- `index.html` 7个script块语法检查通过。
- `dev_scripts/test.py --all`：5/5通过。
- `dev_scripts/build.py --verify`：6/6通过。

---

## v1.6.8 更新记录（2026-05-23）

### 版本号防漏机制
- `index.html` 新增唯一版本来源：`APP_VERSION`。
- 页面标题和底部 footer 不再硬编码版本号，统一由 `APP_VERSION` 自动填充。
- 新增 `dev_scripts/check_version.py`，自动核对：
  - `index.html` 的 `APP_VERSION`
  - `README.md` 顶部版本
  - `UPS选型助手_开发文档.md` 顶部版本
  - `UPS选型助手_开发说明.md` 顶部版本
- `dev_scripts/test.py --quick/--all` 和 `dev_scripts/build.py --verify` 已接入版本一致性检查。

### 后续版本更新规则
- 升级版本时，先改 `index.html` 中的 `APP_VERSION`。
- 同步更新 README 和两份开发文档顶部版本。
- 执行 `python dev_scripts/test.py --quick`，版本不一致时检查会失败。
- 不再在页面可见文本中直接写死 `vX.Y.Z`。

---

## ⚠️ v1.6.1 教训：电池开关箱与电池功率计算公式差异

### 问题描述
用户指出：电池开关箱/柜和电池功率计算公式中，功率P的来源应区分：
- **电池开关箱**：始终用 `UPS容量 × 功率因数`（按UPS额定功率计算）
- **电池功率计算**：若填负载功率则用负载功率，否则用 `UPS容量 × 功率因数`

### 实现要点
| 计算项 | 功率来源 | 代码变量 |
|--------|----------|----------|
| 电池功率计算 | `loadKw > 0 ? loadKw * 1000 : upsCap * pf * 1000` | `loadW` |
| 电池开关箱计算 | `upsCap * pf * 1000` | `switchW` |

### 经验教训
```
⚠️ 同一业务场景中，不同子功能的计算逻辑可能不同

✓ 正确做法：
   1. 区分不同子功能各自的计算规则
   2. 使用独立的变量（如 loadW / switchW）
   3. 不要假设"负载功率"的定义在所有地方都一致
```

---



## ⚠️ v1.6.3 教训：importUpsFromResult属性名错误

### 问题描述
函数访问了不存在的属性 `lastResult.recommendations`，实际结构是 `recommended` 和 `also_consider`。

### 修复方案
```javascript
// 修复前（错误）
if (lastResult.recommendations && lastResult.recommendations.length > 0)

// 修复后
const recs = lastResult.recommended?.length ? lastResult.recommended : (lastResult.also_consider || []);
if (recs.length > 0) { ... }
```

### 经验教训
```
⚠️ 访问嵌套属性前，先确认实际数据结构
✓ 正确做法：
   1. 查看相同变量在其他地方的用法（如 renderResult）
   2. 使用可选链 ?. 避免空指针
   3. 提供 fallback 备选方案
```

*由 Claude Code 自动生成*
*创建时间: 2026-03-09 | 最后更新: 2026-05-06*

---

## ⚠️ v1.6.3-v1.6.5 教训：电池分类更新导致多处不匹配

### 问题回顾

电池分类名更新（12V铅酸→SP12V 等）后，出现多个问题：
- 下拉选择 SP12V 但结果推荐其他类型
- 选择某类型后无输出
- JS 报错 null 引用

### 根本原因

| 问题 | 说明 |
|------|------|
| **两套计算函数并存** | `calcLeadBatteryMethod2`（dead code）引用不存在的 `lead2-*` 元素ID |
| **下拉框遗漏更新** | 只更新了数据表下拉框，遗漏 `unified-batt-type` |
| **映射表未同步** | `categoryLabels` 对象未更新 |
| **跨分类 fallback** | 选某类型后 fallback 到其他分类 |
| **空结果无输出** | 无匹配电池时无任何显示 |

### 修复方案

1. **删除死代码**：`calcLeadBatteryMethod2`、`showBatteryCategory`
2. **同步所有下拉框**：`unified-batt-type` 和 `battType` 保持一致
3. **同步映射表**：`categoryLabels` 与 UI 选项名一致
4. **限制分类搜索**：只搜索用户选定的分类，不 fallback
5. **空结果也输出**：显示计算参数 + 手动输入提示

### 预防机制

| 层级 | 机制 | 说明 |
|------|------|------|
| **机制级** | `pre-push hook` | push 前自动验证 JS 语法 |
| **规则级** | 全局 grep | 修改下拉/分类时搜索所有相关引用 |
| **认知级** | 删除前确认 | 删除代码前先 grep 确认无引用 |

### 经验教训

```
⚠️ 修改批量名称时，必须全局搜索所有相关引用

✓ 正确流程：
   1. 修改下拉选项 → 全局 grep 所有同功能元素
   2. 修改分类名 → 同步 categoryLabels 等映射表
   3. 删除函数 → grep 确认无引用再删
   4. 同一功能只留一套实现
```

---

## ⚠️ JS 语法验证：pre-push hook 已部署

### 功能说明

自动验证 `index.html` 中的 JavaScript 语法，在 git push 前拦截错误。

### 位置

`.git/hooks/pre-push`

### 验证方式

提取所有 `<script>` 标签内容，用 `new Function()` 验证语法。

### 效果

- 不再依赖人工记得去验证
- JS 语法错误会在 push 前被拦截

### 示例输出

```
Running pre-push hook: validating index.html...
Script block 1: OK
Script block 2: OK
Script block 3: OK
Script block 4: OK
All script blocks validated successfully.
JS syntax validation passed.
Pre-push check completed.
```

---

## ⚠️ v1.6.6 教训：GPT12-10小时率数据添加与UI可见性问题

### 问题回顾

增加新电池类别 `dianneng10h`（电能GBT12-10小时率，8个型号），添加后"一键计算全部"按钮点击无反应。

### 排查过程（耗时2小时）

| 步骤 | 方法 | 结果 |
|------|------|------|
| 1 | 代码分析：JS语法正确，无重复函数定义 | ✅ |
| 2 | 数据验证：BATTERY_POWER_DATA包含62个电池 | ✅ |
| 3 | 逻辑验证：Node.js模拟计算流程正常 | ✅ |
| 4 | **在浏览器中打开文件测试** | ✅ 正常显示 |

### 根本原因

**UI可见性问题**：电池配置面板默认 `style="display:none"`，用户点击按钮后没有任何反馈，但按钮本身正常工作。

这不是代码逻辑问题，是用户根本没看到计算结果区域。

### 错误清单

| 错误 | 说明 |
|------|------|
| **需求理解错误** | "10小时率"是电池容量标定标准（10HR），不是放电时间 |
| **正则提取失败** | `[\s\S]*?` 非贪婪匹配提前结束，改用括号计数法 |
| **浮点精度问题** | Excel→JS数值出现 `86.7600000000001`，需 `Math.round(x*100)/100` |
| **null显示错误** | 电池功率null直接显示为"null"而非"-" |
| **分类映射遗漏** | 新增category后多处映射未同步更新 |
| **排查方向错误** | UI问题用代码分析，找不到根因 |

### 经验教训

```
⚠️ UI交互问题必须用浏览器实测，不能纯代码分析

❌ 错误：花2小时分析语法、函数定义、数据逻辑
✓ 正确：先在浏览器中打开页面，确认UI是否可见

❌ 错误："按钮点击无反应"→ 代码逻辑问题
✓ 正确："按钮点击无反应"→ 先确认按钮所在区域是否可见

遇到问题时的正确顺序：
1. 浏览器实测（确认UI可见性）
2. 浏览器控制台（确认是否有JS错误）
3. 代码分析（最后才用）
```

### 预防措施

| 层级 | 机制 | 说明 |
|------|------|------|
| **认知级** | UI问题先实测 | 遇到交互问题，先用浏览器测试 |
| **认知级** | 专业术语先确认 | "10小时率"等术语必须先问用户含义 |
| **规则级** | 数值精度处理 | Excel→JS数值用 `Math.round(x*100)/100` |
| **规则级** | null值显示 | 显示前检查，null→"-" |
