# UPS选型助手 项目规范

## 文件结构
- **只有一个主文件**: `index.html`
- 不要创建 `UPS选型助手.html` 或其他副本
- 所有修改都在 `index.html` 上进行

## GitHub Pages
- 仓库: `xiaochuan1989/-UPS-Selector`
- Pages URL: `https://xiaochuan1989.github.io/-UPS-Selector/`
- 推送到master分支后自动部署（约1-2分钟）

## 开发流程
1. 直接编辑 `index.html`
2. 核心公式优先提炼为纯函数并补 `test_business_rules.js`
3. 运行 `python dev_scripts/test.py --all`
4. 运行 `python dev_scripts/build.py --verify`
5. 使用真实浏览器回归主要面板
6. 检查文档和Serena记忆
7. 提交并推送

## 重要教训
- 本地能用但GitHub不能用 → 首先 `diff` 比较文件是否同步
- 不要创建多个功能相同的HTML文件
- JavaScript语法通过不代表HTML层级正确，必须运行 `audit_html.py`
- UI问题必须浏览器实测
- 不保留失去UI入口的旧函数
