#!/usr/bin/env python3
"""
UPS 智能选型助手 - 构建脚本
===========================

使用方法:
  python dev_scripts/build.py          # 显示构建信息
  python dev_scripts/build.py --serve  # 启动开发服务器
  python dev_scripts/build.py --verify # 运行质量门禁
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
    """保留旧入口，但禁止覆盖当前人工维护的开发说明。"""
    print("\n⚠️  --readme 已停用：开发说明现在由人工维护，避免旧模板覆盖当前内容。")
    print("   请直接编辑 UPS选型助手_开发说明.md，并运行 dev_scripts/test.py --quick。")
    return False


def main():
    parser = argparse.ArgumentParser(description="UPS 智能选型助手 - 构建工具")
    parser.add_argument("--dev", action="store_true", help="已停用：单文件产品不再生成开发版")
    parser.add_argument("--verify", action="store_true", help="运行验证")
    parser.add_argument("--info", action="store_true", help="显示构建信息")
    parser.add_argument("--readme", action="store_true", help="已停用：避免旧模板覆盖开发说明")
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
        sys.exit(0 if create_readme() else 1)

    if args.dev:
        print("\n⚠️  --dev 已停用：当前正式入口是单文件 index.html，不再生成开发版。")
        print("   本地调试请使用 python dev_scripts/serve.py --no-open。")
        sys.exit(1)

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
