# 已修复的Bug与开发注意事项

## 已修复Bug

### 1. IndexedDB 持久化初始化顺序Bug（2026-03-09）
- **症状**: 刷新页面后导入数据丢失，控制台报错 `Cannot access 'db' before initialization`
- **原因**: `loadProductsFromDB()` 在第1230行定义，但在第537行的IIFE中就被调用。IIFE立即执行时函数尚未定义
- **修复**: 将 `(function init(){...})()` 改为 `document.addEventListener('DOMContentLoaded', function(){...})`
- **关键**: IndexedDB相关函数（openDatabase/saveProductsToDB/loadProductsFromDB）必须在DOMContentLoaded回调之前定义

### 2. 开关盒计算JS语法错误（2026-03-12）
- **症状**: 按钮点击无反应
- **原因**: 修改代码时出现语法错误，如 `if !battNum)` 缺少左括号、`constFloat` 等错误
- **修复**: 仔细检查代码语法，特别是修改后的函数
- **关键**: 每次修改代码后用浏览器测试，确保功能正常

### 3. Netlify部署配置错误（2026-03-12）
- **症状**: Netlify报错 "deploy directory is not a directory"
- **原因**: `netlify.toml` 中 `publish = "UPS选型助手.html"` 是文件而非目录
- **修复**: 改为 `publish = "."`，并添加重定向规则指向入口文件
- **关键**: Netlify的publish必须是目录，不能是文件

## 开发注意事项
1. **函数定义顺序**: 所有在初始化阶段调用的函数，必须定义在调用位置之前，或使用DOMContentLoaded延迟调用
2. **file://协议**: 工具通过双击HTML文件使用（file://协议），IndexedDB在此协议下可用但有限制
3. **单文件约束**: 所有代码内联在一个HTML文件中，修改时注意不要破坏script标签结构
4. **产品数据量**: PRODUCTS数组约179条，嵌入在HTML中，占用较大空间
5. **Netlify配置**: publish必须是目录，使用重定向规则指定入口文件
6. **代码修改后测试**: 每次修改代码后必须用浏览器测试，确保功能正常
7. **部署选择**: Netlify 团队账户有月度使用限制（build minutes），建议优先使用 GitHub Pages（免费无限）
8. **GitHub Pages**: 需要创建 `.github/workflows/deploy.yml` 文件，并在 Settings → Pages 中启用
9. **v1.2.5新增（2026-03-14）**: 铅酸电池恒功率数据更新为完整版
   - 电池型号数：61个（普通型26个，高功率型35个）
   - 截止电压：1.60V, 1.65V, 1.67V, 1.70V, 1.75V, 1.80V, 1.85V
   - 放电时间：5, 10, 15, 20, 25, 30, 45, 60, 90, 120, 180, 240, 300, 360, 480, 600, 1200分钟
   - 数据来源：A-电池选型模板-A02.xlsm 数据表Sheet
   - 文件：battery_power_data.js（备用，约466KB）
1. **函数定义顺序**: 所有在初始化阶段调用的函数，必须定义在调用位置之前，或使用DOMContentLoaded延迟调用
2. **file://协议**: 工具通过双击HTML文件使用（file://协议），IndexedDB在此协议下可用但有限制
3. **单文件约束**: 所有代码内联在一个HTML文件中，修改时注意不要破坏script标签结构
4. **产品数据量**: PRODUCTS数组约179条，嵌入在HTML中，占用较大空间
5. **Netlify配置**: publish必须是目录，使用重定向规则指定入口文件
6. **代码修改后测试**: 每次修改代码后必须用浏览器测试，确保功能正常
7. **部署选择**: Netlify 团队账户有月度使用限制（build minutes），建议优先使用 GitHub Pages（免费无限）
8. **GitHub Pages**: 需要创建 `.github/workflows/deploy.yml` 文件，并在 Settings → Pages 中启用
