# UPS 智能选型助手

**版本**: v1.8.2

面向销售和技术人员的本地 Web 工具，支持粘贴客户需求后由 AI 自动匹配 UPS 产品型号。单文件架构，无需安装，双击即可运行。

**线上地址**: https://xiaochuan1989.github.io/-UPS-Selector/

## 当前开发入口

- 主程序文件：`index.html`
- 本地预览：直接打开 `index.html`，推荐运行 `python dev_scripts/serve.py --no-open`
- 快速验证：`python dev_scripts/test.py --quick`
- 完整验证：`python dev_scripts/test.py --all`
- 构建门禁：`python dev_scripts/build.py --verify`
- 部署入口：GitHub Pages / Netlify 构建时仅复制并发布 `index.html`
- 新增入口：顶部 `数据中心方案校核`，用于容量、冗余架构和风险提示校核
- 第二阶段入口：顶部 `电池后备时间反算`，用于按已知电池配置反推预计后备时间
- 汇总导出：`项目配置汇总清单` 区域支持自定义增加行、上下调整顺序、删除当前行、非标描述、手工补充编码/单价，并导出 Excel 清单、快速报价单和客户可读 HTML 技术说明
- 页面布局：桌面端主容器放宽，便于查看宽表和多列配置结果

---

## 目录结构

- `index.html`：当前唯一正式页面入口，页面、样式、脚本和内置数据都在这里。
- `dev_scripts/`：开发校验脚本，常用命令为 `python dev_scripts/test.py --quick`、`python dev_scripts/test.py --all` 和 `python dev_scripts/build.py --verify`。
- `prompts/`：AI 选型提示词资料。
- `src/css/`：历史拆分样式文件，目前线上页面仍以 `index.html` 内联样式为准。
- `.github/`、`netlify.toml`：部署相关配置。
- `.serena/`：Serena 项目配置和项目记忆；`.mcp.json` 是本机配置，保留本地但不再纳入版本控制。
- `归档/历史文档/`：旧备份页面、历史参数文本、早期生成脚本和旧电池数据。
- `归档/历史数据源与模板/`：旧 Excel / xlsm 模板和历史数据源；当前测试仍依赖的 `常用UPS速查表-V7.5.xlsx` 保留在根目录。
- `归档/历史测试数据/`：早期测试数据和试验脚本。
- `归档/垃圾待清理/`：生成物、旧会话、旧部署目录和确认可删除前的垃圾暂存区。

## 本地临时文件规则

- `.codex/`、Office 锁文件 `~$*`、`liantong_result_*`、`*.docx` 不纳入版本控制。
- `归档/垃圾待清理/` 的内容只用于本地复核，确认无价值后可整目录删除。
- 新增版本时先改 `index.html` 中的 `APP_VERSION`，再运行 `python dev_scripts/test.py --quick` 检查页面和文档版本是否一致。
- `dev_scripts/audit_html.py` 会检查 JS 语法、重复函数、重复 DOM ID 和活动代码中的失效 DOM 引用。

## 开发环境

```powershell
python -m pip install -r requirements-dev.txt
python dev_scripts/serve.py --no-open
```

项目没有 npm 依赖；Node.js 只作为 JavaScript 测试运行时，Python 用于结构审计、Excel 检查和开发服务器。

---

详细开发文档：
- [UPS选型助手_开发文档.md](UPS选型助手_开发文档.md) — 产品功能、技术架构、计算公式
- [UPS选型助手_开发说明.md](UPS选型助手_开发说明.md) — 工程工作流、测试、回归和部署
