# 已修复的Bug与开发注意事项

（已更新：2026-04-01 v1.6）

## ⚠️ v1.6 核心教训

### 1. 单文件架构

现在只有一个主文件 `index.html`，不再需要同步两个HTML文件。

### 2. file://协议CDN限制

**问题**：本地双击HTML打开时，浏览器安全策略阻止加载CDN脚本。

**案例**：Tesseract.js OCR库无法加载。

**解决方案**：
```bash
# 使用本地服务器
python -m http.server 8080
# 或使用支持视觉的AI API直接识别图片
```

### 3. AI视觉模型支持

**图片OCR识别需要**：
- kimi2.5（推荐）
- Claude3（Claude 3 Haiku/Sonnet/Opus）
- GPT-4V

**不支持**：普通DeepSeek模型（非VL版本）

### 4. Excel行高自适应

**问题**：固定行高无法适应不同长度的分析内容。

**解决方案**：
```javascript
// 根据内容长度动态计算
const charsPerLine = Math.floor(colWidth * 0.5);
const lines = Math.ceil(content.length / charsPerLine);
ws['!rows'].push({hpt: Math.max(30, lines * 18)});
```

---

## 历史重要教训

### v1.5.4 电池架铜排规格错误

**问题**：单组电池时铜排规格为空。

**正确理解**：
- 单组电池：铜排用主开关规格
- 多组电池：铜排用分开关规格

### v1.6.3 importUpsFromResult属性名错误

**问题**：`lastResult.recommendations` 属性不存在，实际结构是 `recommended` 和 `also_consider`。

**修复**：
```javascript
// 修复前（错误）
if (lastResult.recommendations && lastResult.recommendations.length > 0)

// 修复后
const recs = lastResult.recommended?.length ? lastResult.recommended : (lastResult.also_consider || []);
if (recs.length > 0) { ... }
```

### v1.5.3 变量重复声明

**问题**：`let batteryResult` 声明两次导致语法错误。

**教训**：修改代码后检查变量重复声明。

### v1.5.1 访问不存在的DOM元素

**问题**：`getElementById` 返回 `null`，访问 `null.value` 报错。

**教训**：修改函数时确认引用的元素ID存在。

### v1.4.6 传感器量程公式（连续5次修复失败）

**正确公式**：
```javascript
// 分开关电流
groups >= 2: sensorCurrent = maxCurrent / (groups - 1)
groups = 1: sensorCurrent = maxCurrent
```

**核心教训**：业务逻辑优先，不要凭假设。

---

## 开发注意事项

1. **函数定义顺序**：被调用的函数必须定义在调用位置之前
2. **变量提升**：const/let不会提升，需先定义后使用
3. **单文件架构**：已合并为 index.html，无需多文件同步
4. **组件清单核对**：修改配置类代码时逐项对照
5. **DOM元素验证**：确认getElementById的元素存在
6. **语法检查**：修改代码后用 `node -e "new Function(...)"` 验证
7. **业务逻辑确认**：涉及公式时先问用户，不要猜测
8. **版本更新规范**：提交前更新文档和Serena记忆
