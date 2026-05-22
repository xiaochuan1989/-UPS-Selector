import sys, re, openpyxl
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = Path(__file__).resolve().parents[1]
EXCEL_FILE = PROJECT_ROOT / 'test_data' / '常用UPS速查表-V7 测试.xlsx'
if not EXCEL_FILE.exists():
    EXCEL_FILE = PROJECT_ROOT / '常用UPS速查表-V7.5.xlsx'

wb = openpyxl.load_workbook(EXCEL_FILE, data_only=True)

MODEL_PATS  = [r'^型号$', r'产品型号', r'^产品编码$', r'^编号$']
SERIES_PATS = [r'^系列$', r'所属.*系列', r'产品系列', r'^类别$']
DESC_PATS   = [r'^描述$', r'^产品描述$', r'备注']

def find_by_priority(headers, patterns):
    for pat in patterns:
        for j, h in enumerate(headers):
            if re.search(pat, h):
                return j
    return -1

def is_header_val(v):
    return any(re.search(p, v) for p in MODEL_PATS + SERIES_PATS)

SERIES_MAP = [
    {"base":"太行UR","spec":"UR泰尔","name":"太行UR"},
    {"base":"昆仑UE","spec":"UE泰尔","name":"昆仑UE"},
    {"base":"祁连UM","spec":"UM泰尔","name":"祁连UM"},
    {"base":"泰山UT","spec":"UT泰尔","name":"泰山UT"},
]
SKIP = {"UR泰尔","UE泰尔","UM泰尔","UT泰尔","电池泰尔","配置计算公式"}
STD  = {s["base"] for s in SERIES_MAP}

products, info = [], []

for s in SERIES_MAP:
    ws = wb[s["base"]]
    cnt = sum(1 for r in range(2, ws.max_row+1)
              if str(ws.cell(r,2).value or '').strip())
    products += [{"系列": s["name"], "型号": f"mock"}] * cnt
    info.append(f"{s['name']}×{cnt}")

for sname in wb.sheetnames:
    if sname in SKIP or sname in STD: continue
    ws = wb[sname]
    raw = []
    for r in range(1, ws.max_row+1):
        raw.append([str(ws.cell(r,c).value or '').strip().replace('\n',' ')
                    for c in range(1, ws.max_column+1)])

    header_idx, model_col = -1, -1
    for i in range(min(len(raw), 5)):
        m = find_by_priority(raw[i], MODEL_PATS)
        if m >= 0:
            header_idx, model_col = i, m
            break

    if header_idx < 0:
        print(f'  跳过 [{sname}]')
        continue

    headers = raw[header_idx]
    series_col = find_by_priority(headers, SERIES_PATS)
    desc_col   = find_by_priority(headers, DESC_PATS)

    print(f'\n[{sname}] 表头行={header_idx}, 型号列="{headers[model_col]}", '
          f'系列列={"无" if series_col<0 else headers[series_col]!r}, '
          f'描述列={"无" if desc_col<0 else headers[desc_col]!r}')

    cnt = 0
    for rawrow in raw[header_idx+1:]:
        if model_col >= len(rawrow): continue
        model = rawrow[model_col].strip()
        if not model or is_header_val(model):
            if model:
                print(f'  → 跳过重复表头行: {model!r}')
            continue

        sv = rawrow[series_col].strip() if series_col>=0 and series_col<len(rawrow) else ''
        series_val = (sv if sv and not is_header_val(sv) else '') or sname

        combined = {'系列': series_val}
        for j,h in enumerate(headers):
            if not h or h == '序号': continue
            v = rawrow[j] if j<len(rawrow) else ''
            if not v: continue
            if re.search(r'产品型号', h) and '型号' not in combined: combined['型号'] = v
            elif any(re.search(p,h) for p in DESC_PATS) and '描述' not in combined: combined['描述'] = v
            elif re.search(r'所属.*系列', h): combined['产品系列'] = v
            elif h not in combined: combined[h] = v
        if '型号' not in combined: combined['型号'] = model

        products.append(combined)
        cnt += 1

    info.append(f"{sname}×{cnt}")
    # 显示前2条
    extra = [p for p in products if p.get('系列') not in {'太行UR','昆仑UE','祁连UM','泰山UT'}]
    for p in extra[-cnt:][:2]:
        print(f'  样例: 系列={p["系列"]}, 型号={p.get("型号","?")}, 描述={p.get("描述","")[:40]}')

print(f'\n\n导入汇总: {", ".join(info)}')
print(f'合计 {len(products)} 款产品')
