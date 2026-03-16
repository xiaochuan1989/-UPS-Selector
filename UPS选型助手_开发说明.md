# UPS 智能选型助手 - 工程化开发环境

> 版本：v1.3.3
> 更新日期：2026-03-16

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
- `src/` 目录的模块化是渐进式的，不会影响现有功能
- 修改 `UPS选型助手.html` 后可直接在浏览器测试
- 需要 Python 3.8+ 环境
- IndexedDB 持久化相关函数（`openDatabase`、`saveProductsToDB`、`loadProductsFromDB`）必须定义在 `DOMContentLoaded` 回调之前，否则页面加载时会报 `Cannot access 'db' before initialization` 错误
- Serena MCP 配置在 `.serena/project.yml` 中，全局配置在 `C:\Users\woaig\.claude.json` 中

## 依赖安装（可选）

```bash
# 文件监听功能（可选）
pip install watchdog
```

---
*由 Claude Code 自动生成*
*创建时间: 2026-03-09 | 最后更新: 2026-03-10*
