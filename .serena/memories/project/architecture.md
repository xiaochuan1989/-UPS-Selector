# 技术架构与关键代码位置

## 文件结构
```
UPS选型助手_开发包_v1.2/
├── UPS选型助手.html          # 主程序
├── .serena/project.yml       # Serena MCP 配置
├── .mcp.json                 # MCP 服务器配置
├── src/css/style.css         # 样式表
├── dev_scripts/              # 开发脚本（build/serve/test）
└── test_data/                # 测试数据
```

## 关键函数位置（UPS选型助手.html）
| 函数 | 行号(约) | 说明 |
|------|---------|------|
| `PRODUCTS` | ~461 | 内置产品数据数组（const） |
| `DOMContentLoaded` 初始化 | ~537 | 加载配置 + IndexedDB数据恢复 |
| `callAI()` | ~601 | 统一AI调用（兼容OpenAI/Anthropic） |
| `importExcel()` | ~1025 | Excel导入主函数 |
| `openDatabase()` | ~1210 | IndexedDB打开 |
| `saveProductsToDB()` | ~1225 | 保存产品到IndexedDB |
| `loadProductsFromDB()` | ~1243 | 从IndexedDB加载产品 |
| `clearProductsDB()` | ~1275 | 清除IndexedDB |
| `restoreBuiltinData()` | ~1286 | 恢复内置数据 |

## 外部依赖（CDN）
- SheetJS 0.20.3 — Excel解析
- mammoth.js 1.6.0 — DOCX解析

## 数据存储
- `localStorage["ups_config"]` — API配置（provider/model/apikey/baseurl）
- `localStorage["ups_custom_prompt"]` — 自定义提示词
- `IndexedDB["ups_data_db"]` — 导入的产品数据持久化
