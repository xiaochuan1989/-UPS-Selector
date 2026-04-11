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
2. `git add index.html`
3. `git commit -m "描述"`
4. `git push origin master`

## 重要教训
- 本地能用但GitHub不能用 → 首先 `diff` 比较文件是否同步
- 不要创建多个功能相同的HTML文件
