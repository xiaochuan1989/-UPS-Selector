#!/usr/bin/env python3
"""
UPS 智能选型助手 - 构建脚本
===========================

使用方法:
  python dev_scripts/build.py          # 显示构建信息
  python dev_scripts/build.py --dev    # 构建开发版本（带调试信息）
  python dev_scripts/build.py --serve  # 启动开发服务器
"""

import os
import sys
import re
import argparse
import hashlib
import subprocess
from pathlib import Path
from datetime import datetime

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

# 项目根目录
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
DIST_DIR = PROJECT_ROOT / "dist"
DEV_SCRIPTS_DIR = PROJECT_ROOT / "dev_scripts"

# 源文件路径
TEMPLATE_FILE = PROJECT_ROOT / "index.html"
CSS_FILE = SRC_DIR / "css" / "style.css"
JS_FILE = SRC_DIR / "js" / "app.js"  # 预留，未来模块化使用


def read_file(path: Path) -> str:
    """读取文件内容"""
    if not path.exists():
        print(f"⚠️  文件不存在: {path}")
        return ""
    return path.read_text(encoding='utf-8')


def extract_html_parts(html_content: str) -> dict:
    """从原始HTML中提取各部分"""
    parts = {}

    # 提取 <style> 内容
    style_match = re.search(r'<style>(.*?)</style>', html_content, re.DOTALL)
    parts['style'] = style_match.group(1) if style_match else ""

    # 提取外部 <script src="...">
    script_matches = re.findall(r'<script src="([^"]+)"', html_content)
    parts['external_scripts'] = script_matches

    # 提取内联 <script> 内容
    inline_script_match = re.search(r'const\s+PRODUCTS\s*=\s*(\[.*?\]);\s*const\s+PROVIDER_MODELS', html_content, re.DOTALL)
    if inline_script_match:
        parts['products_data'] = inline_script_match.group(1)

    # 提取主脚本 (DEFAULT_SYSTEM_PROMPT 后的内容)
    script_start = html_content.find('<script>')
    script_end = html_content.rfind('</script>')
    if script_start > 0 and script_end > script_start:
        parts['main_script'] = html_content[script_start + 8:script_end]

    # 提取 <head> 和 <body>
    head_match = re.search(r'<head>(.*?)</head>', html_content, re.DOTALL)
    if head_match:
        parts['head'] = head_match.group(1)

    body_match = re.search(r'<body>(.*?)</body>', html_content, re.DOTALL)
    if body_match:
        parts['body'] = body_match.group(1)

    return parts


def build_dev_index() -> str:
    """构建开发模式的 index.html（引用模块文件）"""
    html = read_file(TEMPLATE_FILE)

    # 如果 CSS 文件存在，使用外部 CSS
    if CSS_FILE.exists():
        css_content = read_file(CSS_FILE)
        # 替换内联样式
        html = re.sub(r'<style>.*?</style>', f'<link rel="stylesheet" href="src/css/style.css">', html, flags=re.DOTALL)

    return html


def calculate_file_hash(path: Path) -> str:
    """计算文件的 MD5 哈希"""
    if not path.exists():
        return ""
    return hashlib.md5(path.read_bytes()).hexdigest()[:8]


def show_build_info(parts: dict):
    """显示构建信息"""
    print("\n" + "=" * 50)
    print("📦 UPS 智能选型助手 - 构建信息")
    print("=" * 50)

    # 版本信息
    html = read_file(TEMPLATE_FILE)
    version_match = re.search(r'const\s+APP_VERSION\s*=\s*"(v\d+\.\d+\.\d+)"', html)
    version = version_match.group(1) if version_match else "unknown"
    build_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"版本: {version}")
    print(f"构建时间: {build_time}")

    # 文件大小
    if TEMPLATE_FILE.exists():
        size_kb = TEMPLATE_FILE.stat().st_size / 1024
        print(f"主文件大小: {size_kb:.1f} KB")

    # 数据信息
    if 'products_data' in parts:
        try:
            import json
            products = json.loads(parts['products_data'])
            print(f"内置产品数量: {len(products)} 款")
        except:
            pass

    print("=" * 50)


def verify_scripts():
    """验证开发脚本"""
    print("\n🔍 验证开发脚本...")

    scripts = [
        ("check_version.py", "版本一致性检查"),
        ("audit_html.py", "HTML/JavaScript结构审计"),
        ("test_business_rules.js", "核心业务规则测试"),
        ("check_prompt_feature.py", "提示词功能验证"),
        ("verify.py", "双表数据库视图"),
        ("check_html.py", "HTML 基础结构"),
        ("scan_js.py", "JS 代码扫描"),
        ("inspect_excel.py", "Excel 数据结构"),
    ]

    results = []
    for script_name, desc in scripts:
        script_path = DEV_SCRIPTS_DIR / script_name
        if script_path.exists():
            results.append(f"  ✅ {desc}")
        else:
            results.append(f"  ❌ {desc} ({script_name} 不存在)")

    for r in results:
        print(r)

    return len([r for r in results if "✅" in r]) == len(results)


def run_quality_check():
    """运行质量检查"""
    print("\n🔧 运行质量检查...")

    html = read_file(TEMPLATE_FILE)

    # 检查基本结构
    checks = [
        ("DOCTYPE", "<!DOCTYPE html>" in html),
        ("UTF-8 编码", 'charset="UTF-8"' in html),
        ("APP_VERSION", "const APP_VERSION" in html),
        ("SheetJS CDN", "xlsx-js-style" in html or "sheetjs.com" in html),
        ("mammoth.js CDN", "mammoth" in html),
        ("系统提示词", "DEFAULT_SYSTEM_PROMPT" in html),
        ("产品数据", "PRODUCTS =" in html or "PRODUCTS=" in html),
    ]

    passed = 0
    for name, result in checks:
        status = "✅" if result else "❌"
        print(f"  {status} {name}")
        if result:
            passed += 1

    print(f"\n通过: {passed}/{len(checks)}")
    return passed == len(checks)


def create_readme():
    """创建开发说明文档"""
    readme_content = """# UPS 智能选型助手 - 工程化开发环境

## 项目结构

```
UPS选型助手_开发包/
├── index.html                # 主程序文件（单文件产品）
├── 常用UPS速查表-V7.5.xlsx   # 产品数据源
├── UPS选型助手_开发文档.md   # 产品开发文档
│
├── src/                      # 源代码目录（工程化用）
│   ├── css/
│   │   └── style.css         # 样式表
│   └── js/
│       └── app.js            # JavaScript 模块（未来使用）
│
├── dist/                     # 构建输出目录
│
├── dev_scripts/              # 开发辅助脚本
│   ├── build.py             # 构建脚本
│   ├── serve.py             # 开发服务器
│   └── ...                  # 其他验证脚本
│
└── test_data/               # 测试数据
```

## 快速开始

### 1. 构建命令

```bash
# 构建生产版本
python dev_scripts/build.py --info

# 构建开发版本
python dev_scripts/build.py --dev

# 启动开发服务器（带热重载）
python dev_scripts/build.py --serve
```

### 2. 开发脚本

| 脚本 | 用途 |
|------|------|
| `check_prompt_feature.py` | 验证提示词功能 |
| `verify.py` | 验证双表数据库视图 |
| `check_html.py` | HTML 基础结构检查 |
| `scan_js.py` | JS 代码扫描 |
| `inspect_excel.py` | Excel 数据结构检查 |

### 3. 修改代码后测试

1. 直接用浏览器打开 `index.html`
2. 或使用 `python dev_scripts/serve.py` 启动本地服务器

## 工程化说明

### 当前状态
- **已实现**: 提取 CSS 到独立文件、构建脚本、质量检查
- **进行中**: JavaScript 模块化拆分
- **待实现**: 开发热重载、CSS/JS 独立加载

### 模块化计划
1. ✅ CSS 独立文件 (`src/css/style.css`)
2. 🔄 JS 模块拆分（数据层、UI层、服务层）
3. ⏳ 开发热重载
4. ⏳ 构建优化（压缩、版本控制）

## 注意事项

- 当前主要代码在 `index.html` 中
- `src/` 目录的模块化是渐进式的，不会影响现有功能
- 修改 `index.html` 后可直接在浏览器测试

---
*由 Claude Code 自动生成*
"""

    readme_path = PROJECT_ROOT / "UPS选型助手_开发说明.md"
    readme_path.write_text(readme_content, encoding='utf-8')
    print(f"\n📄 已创建开发说明文档: {readme_path}")


def main():
    parser = argparse.ArgumentParser(description="UPS 智能选型助手 - 构建工具")
    parser.add_argument("--dev", action="store_true", help="开发模式")
    parser.add_argument("--verify", action="store_true", help="运行验证")
    parser.add_argument("--info", action="store_true", help="显示构建信息")
    parser.add_argument("--readme", action="store_true", help="生成开发说明文档")
    parser.add_argument("--serve", action="store_true", help="启动开发服务器")

    args = parser.parse_args()

    print("⚡ UPS 智能选型助手 - 构建系统")
    print("-" * 40)

    # 提取 HTML 各部分
    html_content = read_file(TEMPLATE_FILE)
    if not html_content:
        print("❌ 无法读取主模板文件")
        sys.exit(1)

    parts = extract_html_parts(html_content)

    # 显示构建信息
    if args.info:
        show_build_info(parts)
        sys.exit(0)

    # 质量检查
    if args.verify:
        scripts_ok = verify_scripts()
        quality_ok = run_quality_check()
        tests_ok = subprocess.run(
            [sys.executable, str(DEV_SCRIPTS_DIR / "test.py"), "--all"],
            cwd=PROJECT_ROOT
        ).returncode == 0
        sys.exit(0 if scripts_ok and quality_ok and tests_ok else 1)

    # 生成开发说明
    if args.readme:
        create_readme()
        sys.exit(0)

    # 启动开发服务器
    if args.serve:
        print("\n🚀 启动开发服务器...")
        import http.server
        import socketserver

        PORT = 8080
        os.chdir(PROJECT_ROOT)

        Handler = http.server.SimpleHTTPRequestHandler

        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print(f"\n✅ 开发服务器已启动: http://localhost:{PORT}")
            print(f"   打开 index.html 即可测试")
            print(f"\n按 Ctrl+C 停止服务器")
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\n\n👋 服务器已停止")
        sys.exit(0)

    # 默认：显示构建信息
    show_build_info(parts)
    print("\n📋 可用命令:")
    print("  python dev_scripts/build.py --info     显示构建信息")
    print("  python dev_scripts/build.py --verify   运行质量检查")
    print("  python dev_scripts/build.py --readme   生成开发说明")
    print("  python dev_scripts/build.py --serve    启动开发服务器")


if __name__ == "__main__":
    main()
