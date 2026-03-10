# 开发环境配置

## Serena MCP 配置
- 项目配置: `.serena/project.yml`（语言: typescript，编码: utf-8）
- 全局配置: `C:\Users\woaig\Downloads\serena-main\serena_config.yml`
- 全局MCP: `C:\Users\woaig\.claude.json`（user scope）
- 启动脚本: `C:\Users\woaig\.local\bin\serena.bat`

## 重要: ignored_paths 配置
必须忽略以下目录，否则TypeScript LSP启动超时：
```yaml
ignored_paths:
  - "test_data/node_modules/**"
  - "serena/**"
  - "fix_history/**"
  - "*.png"
  - "*.xlsx"
```

## Serena 功能可用性
| 功能 | 状态 | 说明 |
|------|------|------|
| 文件列表/读取 | ✅ | 正常 |
| 代码搜索 | ✅ | search_for_pattern 正常 |
| 内容替换 | ✅ | replace_content 正常 |
| 记忆功能 | ✅ | 正常 |
| 符号分析 | ❌ | HTML文件不支持TypeScript LSP符号提取 |

## 工具链
- uv: `C:\Users\woaig\.local\bin\uv.exe`（Python包管理器）
- Python: 3.11.15（通过uv安装）
- Node.js/npm: 全局可用
