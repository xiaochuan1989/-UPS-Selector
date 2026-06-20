import sys, re, json
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
all_ok = True

PROJECT_ROOT = Path(__file__).resolve().parents[1]

with open(PROJECT_ROOT / 'index.html', encoding='utf-8') as f:
    html = f.read()

# 检查1: </script> 在产品数据里
prod_start = html.find('const PRODUCTS')
prod_end = html.find('const PROVIDER_MODELS')
prod_section = html[prod_start:prod_end]
bad_script_end = '</script>' in prod_section
print('检查1 - 产品数据含</script>:', 'BAD!' if bad_script_end else 'OK')
all_ok = all_ok and not bad_script_end

# 检查2: 产品数据里有没有反引号
has_backtick = '`' in prod_section
print('检查2 - 产品数据含反引号:', 'BAD! 会破坏模板字符串' if has_backtick else 'OK')
all_ok = all_ok and not has_backtick
if has_backtick:
    idx = prod_section.index('`')
    print('  位置附近:', repr(prod_section[max(0,idx-50):idx+50]))

# 检查3: 统计整个script中的反引号数量
script_start = html.find('<script>')
script_end = html.rfind('</script>')
js = html[script_start:script_end]
bt = js.count('`')
print(f'检查3 - 反引号数量: {bt} ({"OK" if bt%2==0 else "ERROR-奇数"})')
all_ok = all_ok and bt % 2 == 0

# 检查4: 关键函数存在
for fn in ['function saveConfig', 'function testApi', 'async function analyze', 'function onProviderChange', 'function renderResult', 'function exportDoc']:
    found = fn in html
    print(f'检查 {fn}:', 'OK' if found else 'MISSING')
    all_ok = all_ok and found

# 检查5: 产品JSON有效性（用分号定位结尾）
# 找产品数组的起止位置
p_start = html.find('const PRODUCTS = [') + len('const PRODUCTS = ')
# 找对应的 ];
depth = 0
p_end = p_start
for i, c in enumerate(html[p_start:], p_start):
    if c == '[': depth += 1
    elif c == ']':
        depth -= 1
        if depth == 0:
            p_end = i + 1
            break
prod_json = html[p_start:p_end]
print(f'检查5 - 产品数组长度: {len(prod_json)} 字符')
try:
    products = json.loads(prod_json)
    print(f'检查5 - 产品JSON解析: OK ({len(products)}条)')
except Exception as e:
    all_ok = False
    print(f'检查5 - 产品JSON解析ERROR: {e}')
    # 找出错误附近的内容
    err_str = str(e)
    m = re.search(r'char (\d+)', err_str)
    if m:
        pos = int(m.group(1))
        print(f'  错误位置附近: {repr(prod_json[max(0,pos-100):pos+100])}')

print('\n完成')
raise SystemExit(0 if all_ok else 1)
