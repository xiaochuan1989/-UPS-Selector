# UPS 智能选型助手 - 工程化开发环境

> 版本：v1.5.3
> 更新日期：2026-03-31

## 项目结构

```
UPS选型助手_开发包_v1.2/
├── UPS选型助手.html          # 最终发布的单文件产品
├── 常用UPS速查表-V7.5.xlsx   # UPS产品数据源
├── 锂电池-选型模板-A00.xlsx  # 锂电池选型参考模板
├── UPS选型助手_开发文档.md    # 产品开发文档
├── UPS选型助手_开发说明.md    # 本文件
├── netlify.toml              # Netlify 部署配置 ⭐
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
├── deploy/                   # Netlify 部署目录
│   └── index.html           # 部署文件（从 UPS选型助手.html 复制）
│
├── dev_scripts/              # 开发辅助脚本
│   ├── build.py             # 构建脚本 ⭐
│   ├── serve.py             # 开发服务器 ⭐
│   ├── test.py              # 统一测试入口 ⭐
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
# 进入开发脚本目录
cd dev_scripts

# 显示构建信息
python build.py --info

# 运行质量检查
python build.py --verify

# 生成开发说明
python build.py --readme

# 启动开发服务器
python build.py --serve

# 启动开发服务器（指定端口）
python build.py --serve --port 9000
```

### 2. 开发服务器

```bash
# 启动开发服务器（默认端口 8080）
python serve.py

# 指定端口
python serve.py --port 9000

# 不自动打开浏览器
python serve.py --no-open

# 开启文件监听（需安装 watchdog）
python serve.py --watch
```

### 3. 统一测试入口

```bash
# 快速检查（环境 + HTML）
python test.py --quick

# 运行所有测试
python test.py --all

# 单独运行某项测试
python test.py --prompt    # 提示词验证
python test.py --excel     # Excel 验证
python test.py --html      # HTML 验证
python test.py --js        # JS 代码扫描
python test.py --env       # 环境检查
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
2. 运行测试 (python test.py --quick)
   ↓
3. 用浏览器测试 (python serve.py)
   ↓
4. 验证通过后提交并推送到 GitHub
   git add .
   git commit -m "描述更新内容"
   git push origin master
   ↓
5. Netlify 自动部署（约1-2分钟）
   访问 https://ups-selector.netlify.app 查看
```

### 代码修改后测试

1. **方式一：直接打开**
   - 双击 `UPS选型助手.html` 在浏览器中打开

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
cd "D:\Claude 安装\UPS选型助手_开发包_v1.2"

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
cd "D:\Claude 安装\UPS选型助手_开发包_v1.2"

# 2. 提交修改并推送到 GitHub
git add .
git commit -m "描述更新内容"
git push origin master

# 3. 等待约1-2分钟，Netlify 自动部署

# 4. 访问 https://ups-selector.netlify.app 查看更新
```

### 注意事项

⚠️ **重要**：每次修改代码后，一定要执行 `git add .` 把文件添加到暂存区，否则文件不会提交到 GitHub。

⚠️ **不要删除 UPS选型助手.html 文件**，这是主程序文件，必须保留在项目文件夹中。

### 手动部署（备选）

如果自动部署未关联，可以手动部署：

```bash
# 方式一：手动上传
# 打开 https://app.netlify.com/sites/ups-selector
# 拖拽 UPS选型助手.html 到页面

# 方式二：使用 Netlify CLI
cp UPS选型助手.html deploy/index.html
cd deploy
netlify deploy --dir . --prod --site c662b019-245f-4a7f-af88-53c9b72502da
```

## 注意事项

- 当前主要代码仍在 `UPS选型助手.html` 中
- ⚠️ **多文件同步**：项目有两个HTML文件，修改代码时必须同时更新：
  - `UPS选型助手.html` - 主开发文件
  - `index.html` - GitHub Pages入口文件（需与主文件保持同步）
- `src/` 目录的模块化是渐进式的，不会影响现有功能
- 修改 `UPS选型助手.html` 后可直接在浏览器测试
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
| **多文件不同步** | `index.html` 中的 `getVoltLevel` 返回字符串，与 `UPS选型助手.html` 不一致 |

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
*由 Claude Code 自动生成*
*创建时间: 2026-03-09 | 最后更新: 2026-03-24*
