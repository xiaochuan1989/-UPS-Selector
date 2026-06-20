#!/usr/bin/env python3
"""Validate every inline JavaScript block with Node.js."""

import shutil
import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = PROJECT_ROOT / "index.html"


def main() -> int:
    node = shutil.which("node")
    if not node:
        print("❌ 未找到 Node.js")
        return 1

    checker = r"""
const fs = require("fs");
const html = fs.readFileSync(process.argv[1], "utf8");
const scripts = [...html.matchAll(/<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/gi)];
for (const [index, match] of scripts.entries()) {
  try {
    new Function(match[1]);
    console.log(`✅ script ${index + 1}`);
  } catch (error) {
    console.error(`❌ script ${index + 1}: ${error.message}`);
    process.exitCode = 1;
  }
}
console.log(`共检查 ${scripts.length} 个内联 script`);
"""
    result = subprocess.run(
        [node, "-e", checker, str(HTML_PATH)],
        cwd=PROJECT_ROOT,
        text=True,
        encoding="utf-8",
    )
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
