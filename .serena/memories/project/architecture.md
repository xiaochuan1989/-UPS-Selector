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
| `BATTERY_POWER_DATA` | ~822行后 | 电池恒功率数据（73个型号） |
| `DOMContentLoaded` 初始化 | ~537 | 加载配置 + IndexedDB数据恢复 |
| `callAI()` | ~601 | 统一AI调用（兼容OpenAI/Anthropic） |
| `importExcel()` | ~1025 | Excel导入主函数 |
| `openDatabase()` | ~1210 | IndexedDB打开 |
| `saveProductsToDB()` | ~1225 | 保存产品到IndexedDB |
| `loadProductsFromDB()` | ~1243 | 从IndexedDB加载产品 |
| `clearProductsDB()` | ~1275 | 清除IndexedDB |
| `restoreBuiltinData()` | ~1286 | 恢复内置数据 |

## 铅酸电池选型功能（v1.2.5 新增）
| 函数 | 说明 |
|------|------|
| `switchLeadMethodTab()` | 切换方法1/方法2子Tab |
| `showBatteryCategory()` | 切换普通/高功率/2V分类 |
| `calcLeadBatteryMethod2()` | 方法2计算和推荐 |
| `getBatteryRecommendationsByPower()` | 根据恒功率查找推荐电池 |
| `renderBatteryRecommendations()` | 渲染推荐结果 |
| `openBatteryDataTable()` | 打开恒功率数据表弹窗 |
| `closeBatteryDataTable()` | 关闭恒功率数据表弹窗 |
| `renderBatteryDataTable()` | 渲染恒功率数据表 |
| `filterBatteryDataTable()` | 筛选恒功率数据 |

## 恒功率数据
- `BATTERY_POWER_DATA` 数组（约191KB，73个电池型号）
- 来源：A-电池选型模板-A02.xlsm 数据表 Sheet
- 分类：普通电池16个、高功率电池45个、2V电池12个

## 外部依赖（CDN）
- SheetJS 0.20.3 — Excel解析
- mammoth.js 1.6.0 — DOCX解析

## 数据存储
- `localStorage["ups_config"]` — API配置（provider/model/apikey/baseurl）
- `localStorage["ups_custom_prompt"]` — 自定义提示词
- `IndexedDB["ups_data_db"]` — 导入的产品数据持久化
