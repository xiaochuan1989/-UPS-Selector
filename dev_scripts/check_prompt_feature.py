import sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
import re

PROJECT_ROOT = Path(__file__).resolve().parents[1]

with open(PROJECT_ROOT / 'index.html', encoding='utf-8') as f:
    html = f.read()

checks = [
    ('DEFAULT_SYSTEM_PROMPT 常量', 'const DEFAULT_SYSTEM_PROMPT'),
    ('getCustomPrompt 函数', 'function getCustomPrompt'),
    ('switchSettingsTab 函数', 'function switchSettingsTab'),
    ('savePrompt 函数', 'function savePrompt'),
    ('resetPrompt 函数', 'function resetPrompt'),
    ('tab-api 按钮', 'id="tab-api"'),
    ('tab-prompt 按钮', 'id="tab-prompt"'),
    ('settings-body-api', 'id="settings-body-api"'),
    ('settings-body-prompt', 'id="settings-body-prompt"'),
    ('custom-prompt textarea', 'id="custom-prompt"'),
    ('analyze 用 getCustomPrompt', 'getCustomPrompt()'),
    ('铁律关键词', '铁律'),
    ('分析输出格式', '需求解析维度'),
]

all_ok = True
for name, key in checks:
    found = key in html
    mark = 'OK' if found else 'XX'
    if not found:
        all_ok = False
    print(f'  [{mark}] {name}')

# 检查反引号平衡
scripts = re.findall(r'<script(?![^>]*src)[^>]*>([\s\S]*?)</script>', html)
print(f'\n  内联script块数量: {len(scripts)}')
for i, s in enumerate(scripts):
    bt = s.count('`')
    balanced = bt % 2 == 0
    print(f'  Block {i+1}: 反引号 {bt} 个, 平衡={balanced}')
    if not balanced:
        all_ok = False

print('\n' + ('✅ 全部通过' if all_ok else '❌ 有问题需修复'))
