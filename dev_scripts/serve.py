#!/usr/bin/env python3
"""
UPS 智能选型助手 - 开发服务器
=============================

功能:
  - 本地 HTTP 服务器
  - 文件变化监听（开发时自动刷新）
  - 自动打开浏览器

使用方法:
  python dev_scripts/serve.py              # 默认端口 8080
  python dev_scripts/serve.py --port 9000  # 指定端口
  python dev_scripts/serve.py --no-open    # 不自动打开浏览器
  python dev_scripts/serve.py --watch      # 监听文件变化
"""

import os
import sys
import webbrowser
import http.server
import socketserver
import argparse
from pathlib import Path
from datetime import datetime
import threading
import time

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    WATCHDOG_AVAILABLE = True
except ImportError:
    WATCHDOG_AVAILABLE = False
    FileSystemEventHandler = object


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_HTML = "index.html"


class ChangeHandler(FileSystemEventHandler):
    """文件变化处理器"""

    def __init__(self, callback=None):
        self.callback = callback
        self.last_modified = {}
        self.debounce_time = 1.0  # 秒

    def on_modified(self, event):
        if event.is_directory:
            return

        file_path = Path(event.src_path)
        if file_path.suffix not in ['.html', '.py', '.js', '.css']:
            return

        # 防抖
        now = time.time()
        last_time = self.last_modified.get(str(file_path), 0)
        if now - last_time < self.debounce_time:
            return
        self.last_modified[str(file_path)] = now

        print(f"\n📝 检测到文件变化: {file_path.name}")
        if self.callback:
            self.callback()


def simple_file_watch(folder: Path, callback):
    """简单的文件监听（无需 watchdog）"""
    print("📁 开启文件监听模式...")

    import time
    mtimes = {}

    while True:
        for ext in ['.html', '.py', '.js', '.css']:
            for f in folder.rglob(f'*{ext}'):
                try:
                    mtime = f.stat().st_mtime
                    if str(f) not in mtimes:
                        mtimes[str(f)] = mtime
                    elif mtime > mtimes[str(f)]:
                        mtimes[str(f)] = mtime
                        print(f"\n📝 检测到变化: {f.relative_to(folder)}")
                        callback()
                except:
                    pass
        time.sleep(1)


class QuietHTTPHandler(http.server.SimpleHTTPRequestHandler):
    """安静的 HTTP 处理器（减少日志输出）"""

    def log_message(self, format, *args):
        # 只记录错误
        if args and '404' in str(args[0]):
            super().log_message(format, *args)

    def end_headers(self):
        # 添加 CORS 头（允许跨域访问 API）
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()


def print_banner(port: int, html_file: str):
    """打印启动横幅"""
    print("\n" + "=" * 50)
    print("⚡ UPS 智能选型助手 - 开发服务器")
    print("=" * 50)
    print(f"🌐 访问地址: http://localhost:{port}/{html_file}")
    print(f"📁 工作目录: {PROJECT_ROOT}")
    print("-" * 50)
    print("提示:")
    print("  • 修改 HTML/JS/CSS 后刷新浏览器即可")
    print("  • 按 Ctrl+C 停止服务器")
    print("=" * 50 + "\n")


def main():
    parser = argparse.ArgumentParser(description="UPS 开发服务器")
    parser.add_argument("--port", type=int, default=8080, help="端口号 (默认: 8080)")
    parser.add_argument("--no-open", action="store_true", help="不自动打开浏览器")
    parser.add_argument("--watch", action="store_true", help="开启文件监听")
    parser.add_argument("--html", default=DEFAULT_HTML, help="默认 HTML 文件")

    args = parser.parse_args()

    # 切换到项目根目录
    os.chdir(PROJECT_ROOT)

    port = args.port
    html_file = args.html

    # 检查 HTML 文件是否存在
    if not Path(html_file).exists():
        print(f"❌ 文件不存在: {html_file}")
        # 尝试查找
        html_files = list(PROJECT_ROOT.glob("*.html"))
        if html_files:
            print(f"📋 可用的 HTML 文件:")
            for f in html_files:
                print(f"   - {f.name}")
            html_file = html_files[0].name
            print(f"\n✅ 使用: {html_file}")
        else:
            sys.exit(1)

    # 打印横幅
    print_banner(port, html_file)

    # 自动打开浏览器
    if not args.no_open:
        def open_browser():
            time.sleep(1)
            webbrowser.open(f"http://localhost:{port}/{html_file}")

        thread = threading.Thread(target=open_browser)
        thread.daemon = True
        thread.start()

    # 文件监听
    if args.watch:
        if WATCHDOG_AVAILABLE:
            event_handler = ChangeHandler()
            observer = Observer()
            observer.schedule(event_handler, str(PROJECT_ROOT), recursive=True)
            observer.start()
            print("✅ 使用 watchdog 进行文件监听")
        else:
            print("⚠️  watchdog 未安装，使用简单文件监听")
            print("   安装方法: pip install watchdog")

            def on_change():
                print("📝 文件已更改，请刷新浏览器")

            thread = threading.Thread(target=simple_file_watch, args=(PROJECT_ROOT, on_change))
            thread.daemon = True
            thread.start()

    # 启动服务器
    with socketserver.TCPServer(("", port), QuietHTTPHandler) as httpd:
        try:
            print(f"🚀 服务器运行中...\n")
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n👋 服务器已停止")


if __name__ == "__main__":
    main()
