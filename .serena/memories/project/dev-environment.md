# 开发环境与部署

## 项目结构
```
UPS选型助手_开发包/
├── index.html            # 主程序文件（单一文件，已合并）
├── src/css/style.css     # 样式表（已提取）
├── dev_scripts/          # 开发脚本
│   ├── build.py         # 构建信息/质量检查/生成文档
│   ├── serve.py         # HTTP服务/文件监听
│   ├── test.py          # 统一测试入口
│   └── inspect_excel.py # Excel数据结构检查
└── deploy/              # Netlify部署目录
```

## 快速命令
```bash
cd dev_scripts

# 质量检查
python build.py --verify

# 启动开发服务器（端口8080）
python serve.py --port 9000 --watch

# 统一测试
python test.py --quick   # 快速检查
python test.py --all     # 全部测试
```

## 线上部署
- **GitHub Pages**: https://xiaochuan1989.github.io/-UPS-Selector/
- **Netlify备选**: https://ups-selector.netlify.app

## 部署命令
```bash
git add .
git commit -m "更新内容"
git push origin master
# 等待1-2分钟自动部署
```

## 注意事项
- ⚠️ IndexedDB相关函数必须在DOMContentLoaded之前定义
- ⚠️ 主文件是 index.html，所有修改都在此文件上进行
