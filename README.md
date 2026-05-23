# UPS 智能选型助手

**版本**: v1.6.15

面向销售和技术人员的本地 Web 工具，支持粘贴客户需求后由 AI 自动匹配 UPS 产品型号。单文件架构，无需安装，双击即可运行。

**线上地址**: https://xiaochuan1989.github.io/-UPS-Selector/

## 当前开发入口

- 主程序文件：`index.html`
- 本地预览：直接打开 `index.html`，或在 Python 可用时运行 `python dev_scripts/serve.py --no-open`
- 基线验证：`node -e "const fs=require('fs'); const html=fs.readFileSync('index.html','utf8'); [...html.matchAll(/<script[^>]*>([\\s\\S]*?)<\\/script>/gi)].forEach((m,i)=>new Function(m[1])); console.log('JS syntax OK')"`
- 部署入口：GitHub Pages 直接发布仓库根目录的 `index.html`
- 新增入口：顶部 `数据中心方案校核`，用于容量、冗余架构和风险提示校核

---

## 目录结构

- `index.html`：当前唯一正式页面入口，页面、样式、脚本和内置数据都在这里。
- `dev_scripts/`：开发校验脚本，常用命令为 `python dev_scripts/test.py --quick` 和 `python dev_scripts/build.py --verify`。
- `prompts/`：AI 选型提示词资料。
- `src/css/`：历史拆分样式文件，目前线上页面仍以 `index.html` 内联样式为准。
- `.github/`、`netlify.toml`：部署相关配置。
- `.serena/`、`.mcp.json`：本地 AI/Serena 开发辅助配置。
- `*.xlsx`、`*.xlsm`、`*.txt`、`*_backup.html`：历史数据源、模板、调试文本或备份文件，改动前需确认是否仍被脚本引用。

## 本地临时文件规则

- `.codex/`、Office 锁文件 `~$*`、`liantong_result_*`、`*.docx` 不纳入版本控制。
- 新增版本时先改 `index.html` 中的 `APP_VERSION`，再运行 `python dev_scripts/test.py --quick` 检查页面和文档版本是否一致。

---

详细开发文档：
- [UPS选型助手_开发文档.md](UPS选型助手_开发文档.md) — 产品功能、技术架构、计算公式
- [UPS选型助手_开发说明.md](UPS选型助手_开发说明.md) — 工程化开发环境、经验教训
