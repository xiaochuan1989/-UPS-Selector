# 技术架构与关键代码位置

（已更新：2026-03-21）

## 文件结构
```
UPS选型助手_开发包/
├── index.html               # 主程序（单一文件，已合并）
├── .serena/project.yml       # Serena MCP 配置
├── .mcp.json                 # MCP 服务器配置
├── src/css/style.css         # 样式表
├── dev_scripts/              # 开发脚本（build/serve/test）
└── test_data/                # 测试数据
```

## 当前版本
**v1.6.1** (2026-04-11)

## 最近更新
- 电压等级公式改为基于最大充电电压计算
- 新增 UPS 中性线选项
- 项目汇总表头添加备注列
- 术语调整："从控模块" → "单体测量模块"

## 文件体积分布
| 区块 | 行号 | 大小 | 占比 |
|------|------|------|------|
| BATTERY_POWER_DATA（73个电池型号） | 2286-27632 | ~456KB | 56.7% |
| PRODUCTS（179个UPS产品） | 844（单行） | ~174KB | 21.6% |
| 实际业务代码+HTML+CSS | 其余 | ~174KB | 21.6% |

> 78% 的文件体积是静态数据，实际代码约 2937 行、60个函数。

## 关键函数位置（index.html）

### 认证与配置
| 函数 | 行号 | 说明 |
|------|------|------|
| `checkAuth()` | ~163 | 密码验证 |
| `getCustomPrompt()` | ~916 | 读取自定义/默认提示词 |
| `onProviderChange()` | ~959 | API提供商切换 |
| `getBaseUrl()` | ~972 | 获取API Base URL |
| `saveConfig()` | ~980 | 保存API配置 |

### AI 选型核心
| 函数 | 行号 | 说明 |
|------|------|------|
| `buildProductSummary()` | ~1038 | 构建产品摘要（公共函数） |
| `callAI()` | ~993 | 统一AI调用（兼容OpenAI/Anthropic） |
| `analyze()` | ~1045 | 首次选型主流程 |
| `sendFollowup()` | ~1168 | 多轮追问 |
| `validateModels()` | ~1283 | 防幻觉：过滤不存在的型号 |

### 结果展示与交互
| 函数 | 行号 | 说明 |
|------|------|------|
| `renderResult()` | ~1124 | 渲染选型结果（双分区） |
| `buildProductRow()` | ~1100 | 构建产品表格行 |
| `showDetail()` | ~1309 | 弹出产品详情 |
| `showCompare()` | ~1384 | 产品对比 |
| `exportDoc()` | ~1474 | 导出HTML推荐方案 |
| `appendChat()` | ~1270 | 追加对话消息 |

### Excel 导入与数据持久化
| 函数 | 行号 | 说明 |
|------|------|------|
| `importExcel()` | ~1529 | Excel导入主函数 |
| `openDatabase()` | ~1715 | IndexedDB打开 |
| `saveProductsToDB()` | ~1730 | 保存产品到IndexedDB |
| `loadProductsFromDB()` | ~1748 | 从IndexedDB加载产品 |
| `clearProductsDB()` | ~1780 | 清除IndexedDB |
| `restoreBuiltinData()` | ~1791 | 恢复内置数据 |

### 电池监控配置（v1.3.2）
| 函数 | 行号 | 说明 |
|------|------|------|
| `calcMonitorConfig()` | ~1858 | 监控配置计算 |
| `renderMonitorConfigTable()` | ~2076 | 渲染配置表格 |
| `exportMonitorConfig()` | ~2111 | 导出监控配置 |

### 铅酸电池选型
| 函数 | 行号 | 说明 |
|------|------|------|
| `calcLeadBattery()` | ~2229 | 方法1计算 |
| `switchLeadMethodTab()` | ~27633 | 切换方法1/方法2子Tab |
| `calcLeadBatteryMethod2()` | ~27664 | 方法2计算和推荐 |
| `getBatteryRecommendationsByPower()` | ~27703 | 根据恒功率查找推荐电池 |
| `renderBatteryRecommendations()` | ~27745 | 渲染推荐结果 |
| `openBatteryDataTable()` | ~27803 | 打开恒功率数据表弹窗 |
| `renderBatteryDataTable()` | ~27805 | 渲染恒功率数据表 |

### 锂电池与开关盒
| 函数 | 行号 | 说明 |
|------|------|------|
| `calcLithiumBattery()` | ~27856 | 锂电池配置计算 |
| `calcSwitchBox()` | ~27994 | 开关盒配置计算 |
| `getNextBreakerSize()` | ~27985 | 断路器规格向上取整 |

### 数据库查看器
| 函数 | 行号 | 说明 |
|------|------|------|
| `toggleDataTable()` | ~28146 | 展开/折叠数据库 |
| `buildDataTable()` | ~28157 | 构建双栏数据库表格 |
| `filterDataTable()` | ~28249 | 数据库搜索过滤 |
| `sortDataTable()` | ~28254 | 数据库排序 |

### 设置与文档上传
| 函数 | 行号 | 说明 |
|------|------|------|
| `openSettings()` | ~28368 | 打开设置弹窗 |
| `savePrompt()` | ~28392 | 保存自定义提示词 |
| `handleDocUpload()` | ~28411 | 文档上传解析（TXT/DOCX/PDF） |

## 内嵌数据
| 数据 | 行号 | 大小 | 说明 |
|------|------|------|------|
| `PRODUCTS` | 844 | ~174KB | 179款UPS产品JSON（单行） |
| `MONITOR_PRODUCTS` | 1840-1856 | ~1KB | 15个电池监控产品 |
| `BATTERY_POWER_DATA` | 2286-27632 | ~456KB | 73个电池型号恒功率数据 |

## 外部依赖（CDN）
- SheetJS(xlsx-js-style) 1.2.0 — Excel解析+样式写入
- mammoth.js 1.6.0 — DOCX解析
- PDF.js 3.11.174 — PDF解析

## 数据存储
- `localStorage["ups_config"]` — API配置（provider/model/apikey/baseurl）
- `localStorage["ups_custom_prompt"]` — 自定义提示词
- `IndexedDB["ups_data_db"]` — 导入的产品数据持久化

## 代码结构评估（2026-03-17）
- 项目结构健康，不需要大规模重构
- 单文件约束是刻意的设计选择（零安装、双击即用）
- 实际代码量小（~2937行），模块边界清晰
- 拆分多文件需引入构建工具，违背产品定位
- 数据必须内嵌保证离线可用
