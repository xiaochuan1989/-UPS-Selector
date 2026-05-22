# UPS 智能选型助手

**版本**: v1.6.7

面向销售和技术人员的本地 Web 工具，支持粘贴客户需求后由 AI 自动匹配 UPS 产品型号。单文件架构，无需安装，双击即可运行。

**线上地址**: https://xiaochuan1989.github.io/-UPS-Selector/

## 当前开发入口

- 主程序文件：`index.html`
- 本地预览：直接打开 `index.html`，或在 Python 可用时运行 `python dev_scripts/serve.py --no-open`
- 基线验证：`node -e "const fs=require('fs'); const html=fs.readFileSync('index.html','utf8'); [...html.matchAll(/<script[^>]*>([\\s\\S]*?)<\\/script>/gi)].forEach((m,i)=>new Function(m[1])); console.log('JS syntax OK')"`
- 部署入口：GitHub Pages 直接发布仓库根目录的 `index.html`

---

详细开发文档：
- [UPS选型助手_开发文档.md](UPS选型助手_开发文档.md) — 产品功能、技术架构、计算公式
- [UPS选型助手_开发说明.md](UPS选型助手_开发说明.md) — 工程化开发环境、经验教训
