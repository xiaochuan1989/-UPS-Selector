# UPS 智能选型助手

**版本**: v1.8.22

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
- 电池数据：新增 JYC-GFM-2V 常规 10 款和 JYC-HR-2V 高倍率 6 款，支持正向推荐、后备时间反算和 2V 监控配置
- 开关计算：电池开关电流支持按“UPS容量 × 功率因数”或“负载功率”选择计算依据
- 多套 UPS 项目：同一项目可保存多套不同 UPS 与电池配置；顶部“开始新配置”用于定位并清空填写区，底部“加入项目并新增下一套”用于保存当前配置；支持载入修改、删除和连续新增，项目汇总会自动合并相同型号物料数量并保留配置来源
- UPS 型号搜索：标准型号选择框支持输入任意关键字实时筛选，例如输入 `600` 会列出所有型号中包含 `600` 的选项；支持鼠标选择及方向键、回车、Esc 操作
- 产品数据库：上下双表自动占满浏览器剩余高度，支持拖动分隔条调整高度并记忆比例；可拖动表头列边界调整列宽，普通拖动可选择文字，按住 `Shift` 拖动可横向查看；单击任一型号可打开“型号数据全景”卡片；型号可在双表或详情卡片中收藏，并用“只看收藏”与搜索条件组合筛选；对照 `常用UPS速查表-V8.0.xlsx` 与 iTeaQ 2026-04 目录价 PDF，32 条 UPS 数据库行已补充目录中存在的机柜/模块编码和单价，同型号多目录版本并列保留
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
- `归档/历史数据源与模板/`：旧 Excel / xlsm 模板和历史数据源；当前测试依赖的 `常用UPS速查表-V8.0.xlsx` 保留在根目录。
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
