# UPS智能选型助手 - 项目概览

## 基本信息
- **版本**: v1.2
- **类型**: 单文件本地 Web 工具（UPS选型助手.html，约260KB）
- **主文件**: `UPS选型助手.html`（HTML + CSS + JS 全部内联）
- **用途**: 销售/技术人员粘贴客户需求，AI自动匹配UPS产品型号

## 核心功能
1. AI智能选型（支持 OpenAI/DeepSeek/Moonshot/Claude 等 API）
2. Excel 导入产品数据（SheetJS解析，IndexedDB持久化）
3. 电池配置计算（铅酸/锂电池/开关盒）
4. 多轮对话追问
5. 导出HTML推荐方案
6. 双栏产品数据库查看器

## 内置数据
- 179款产品，4个系列：太行UR(21)、昆仑UE(39)、祁连UM(22)、泰山UT(97)
- 数据源：常用UPS速查表-V7.5.xlsx
