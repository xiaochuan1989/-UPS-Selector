#!/usr/bin/env python3
"""Audit JavaScript syntax and the rendered HTML hierarchy without npm packages."""

import re
import shutil
import subprocess
import sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = PROJECT_ROOT / "index.html"


class HtmlNode:
    def __init__(self, tag, attrs, parent):
        self.tag = tag
        self.attrs = dict(attrs)
        self.parent = parent


class StrictStructureParser(HTMLParser):
    VOID_TAGS = {
        "area", "base", "br", "col", "embed", "hr", "img", "input",
        "link", "meta", "param", "source", "track", "wbr",
    }

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.ids = {}
        self.errors = []

    def handle_starttag(self, tag, attrs):
        parent = self.stack[-1] if self.stack else None
        node = HtmlNode(tag, attrs, parent)
        node_id = node.attrs.get("id")
        if node_id:
            self.ids[node_id] = node
        if tag not in self.VOID_TAGS:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in self.VOID_TAGS:
            self.stack.pop()

    def handle_endtag(self, tag):
        if not self.stack:
            self.errors.append(f"多余闭合标签 </{tag}>")
            return
        current = self.stack[-1]
        if current.tag != tag:
            self.errors.append(f"标签闭合错位：期望 </{current.tag}>，实际 </{tag}>")
            return
        self.stack.pop()


def has_hidden_ancestor(node):
    current = node.parent if node else None
    while current:
        style = current.attrs.get("style", "").replace(" ", "").lower()
        if "display:none" in style:
            return True
        current = current.parent
    return False


def main() -> int:
    html = HTML_PATH.read_text(encoding="utf-8")
    scripts = re.findall(r"<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)</script>", html, re.I)
    javascript = "\n".join(scripts)
    failures = []

    node = shutil.which("node")
    if not node:
        failures.append("未找到 Node.js，无法执行 JavaScript 语法检查")
    else:
        node_check = r"""
const fs = require("fs");
const html = fs.readFileSync(process.argv[1], "utf8");
const scripts = [...html.matchAll(/<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/gi)];
for (const [index, match] of scripts.entries()) {
  try { new Function(match[1]); }
  catch (error) {
    console.error(`内联 script ${index + 1}: ${error.message}`);
    process.exit(1);
  }
}
console.log(`✅ JavaScript 语法: ${scripts.length} 个内联 script 均通过`);
"""
        result = subprocess.run(
            [node, "-e", node_check, str(HTML_PATH)],
            cwd=PROJECT_ROOT,
            text=True,
            capture_output=True,
            encoding="utf-8",
        )
        print(result.stdout.strip())
        if result.returncode:
            failures.append(result.stderr.strip() or "JavaScript 语法检查失败")

    parser = StrictStructureParser()
    parser.feed(html)
    if parser.stack:
        parser.errors.append("存在未闭合标签: " + ", ".join(node.tag for node in parser.stack[-5:]))
    if parser.errors:
        failures.extend(parser.errors[:10])
    else:
        print("✅ HTML标签: 闭合顺序正确")

    core_panel_ids = [
        "data-table-panel",
        "dc-check-panel",
        "runtime-calc-panel",
        "battery-calc-v1-panel",
        "battery-calc-panel",
    ]
    for panel_id in core_panel_ids:
        node = parser.ids.get(panel_id)
        parent_classes = node.parent.attrs.get("class", "").split() if node and node.parent else []
        if not node or "container" not in parent_classes:
            failures.append(f"{panel_id} 不是 .container 的直接子元素")
    requirement = parser.ids.get("requirement")
    if not requirement:
        failures.append("未找到客户需求输入框")
    elif has_hidden_ancestor(requirement):
        failures.append("客户需求主卡片被嵌套在隐藏容器中")
    else:
        print("✅ HTML层级: 核心面板和客户需求卡片位置正确")

    ids = re.findall(r"\bid=[\"']([^\"']+)[\"']", html)
    duplicate_ids = sorted(name for name, count in Counter(ids).items() if count > 1)
    if duplicate_ids:
        failures.append("重复 DOM id: " + ", ".join(duplicate_ids))
    else:
        print(f"✅ DOM id 唯一性: {len(ids)} 个 id 无重复")

    function_names = re.findall(
        r"(?:async\s+)?function\s+([A-Za-z_$][\w$]*)\s*\(",
        javascript,
    )
    duplicate_functions = sorted(
        name for name, count in Counter(function_names).items() if count > 1
    )
    if duplicate_functions:
        failures.append("重复函数定义: " + ", ".join(duplicate_functions))
    else:
        print(f"✅ 函数唯一性: {len(function_names)} 个函数无重复")

    declared_ids = set(ids)
    declared_ids.update(re.findall(r"\.id\s*=\s*[\"']([^\"']+)[\"']", javascript))
    referenced_ids = set(
        re.findall(
            r"getElementById\(\s*[\"']([^\"']+)[\"']\s*\)",
            javascript,
        )
    )
    missing_ids = sorted(referenced_ids - declared_ids)
    if missing_ids:
        failures.append("活动代码引用了不存在的 DOM id: " + ", ".join(missing_ids))
    else:
        print(f"✅ DOM 引用: {len(referenced_ids)} 个静态引用均有定义")

    if re.findall(r"^\s*rowNum\+\+;\s*$", javascript, re.M):
        failures.append("项目汇总序号存在模板外重复递增")
    else:
        print("✅ 汇总序号: 每行仅递增一次")

    if failures:
        for failure in failures:
            print("❌ " + failure)
        return 1

    print("HTML/JavaScript 结构审计通过")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
