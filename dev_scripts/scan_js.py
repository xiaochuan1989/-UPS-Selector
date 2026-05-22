import sys, re
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = Path(__file__).resolve().parents[1]

with open(PROJECT_ROOT / 'index.html', encoding='utf-8') as f:
    html = f.read()

# 提取所有内联 script 内容
scripts = re.findall(r'<script(?![^>]*src)[^>]*>([\s\S]*?)</script>', html)
js = '\n'.join(scripts)

# 跳过产品数据，取后半段JS
after = js[js.find('const PROVIDER_MODELS'):]
lines = after.split('\n')
print(f'共 {len(lines)} 行')

suspicious_lines = []
for i, line in enumerate(lines, 1):
    # 标记含有 ") 或 "( 的行（可能是引号问题）
    stripped = line.strip()
    suspicious = (
        '")' in line or
        '"(' in line or
        "missing" in line.lower() or
        ('"' in line and line.count('"') % 2 != 0)
    )
    if suspicious:
        suspicious_lines.append((i, line[:120]))

print(f'可疑行数量: {len(suspicious_lines)}')
for i, line in suspicious_lines[:50]:
    print(f'{i:5d}: {line} <<< SUSPICIOUS')
if len(suspicious_lines) > 50:
    print(f'... 其余 {len(suspicious_lines) - 50} 行已省略')
