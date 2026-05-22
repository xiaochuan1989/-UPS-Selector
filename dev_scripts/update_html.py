# -*- coding: utf-8 -*-
"""Deprecated one-off migration script.

This project now uses index.html as the single source of truth. The old
update_html.py script patched an earlier HTML layout and is intentionally
disabled so it cannot rewrite current production code by accident.
"""

import sys

sys.stdout.reconfigure(encoding="utf-8")

print("update_html.py 已停用：当前请直接维护项目根目录的 index.html。")
sys.exit(0)
