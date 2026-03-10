# 已修复的Bug与开发注意事项

## 已修复Bug

### 1. IndexedDB 持久化初始化顺序Bug（2026-03-09）
- **症状**: 刷新页面后导入数据丢失，控制台报错 `Cannot access 'db' before initialization`
- **原因**: `loadProductsFromDB()` 在第1230行定义，但在第537行的IIFE中就被调用。IIFE立即执行时函数尚未定义
- **修复**: 将 `(function init(){...})()` 改为 `document.addEventListener('DOMContentLoaded', function(){...})`
- **关键**: IndexedDB相关函数（openDatabase/saveProductsToDB/loadProductsFromDB）必须在DOMContentLoaded回调之前定义

## 开发注意事项
1. **函数定义顺序**: 所有在初始化阶段调用的函数，必须定义在调用位置之前，或使用DOMContentLoaded延迟调用
2. **file://协议**: 工具通过双击HTML文件使用（file://协议），IndexedDB在此协议下可用但有限制
3. **单文件约束**: 所有代码内联在一个HTML文件中，修改时注意不要破坏script标签结构
4. **产品数据量**: PRODUCTS数组约179条，嵌入在HTML中，占用较大空间
