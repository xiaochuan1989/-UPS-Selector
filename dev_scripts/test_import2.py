import sys, re, openpyxl
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = Path(__file__).resolve().parents[1]
EXCEL_FILE = PROJECT_ROOT / 'test_data' / '常用UPS速查表-V7 测试.xlsx'
if not EXCEL_FILE.exists():
    EXCEL_FILE = PROJECT_ROOT / '常用UPS速查表-V7.5.xlsx'

wb = openpyxl.load_workbook(EXCEL_FILE, data_only=True)

MODEL_PATTERNS = [r'^型号$', r'产品型号', r'^产品编码$', r'^编号$']
SERIES_PATTERNS = [r'^系列$', r'所属.*系列', r'产品系列', r'^类别$']
DESC_PATTERNS   = [r'^描述$', r'产品描述', r'备注']

def match(s, patterns):
    return any(re.search(p, s) for p in patterns)

SERIES_MAP = [
    {"base": "太行UR", "spec": "UR泰尔", "name": "太行UR"},
    {"base": "昆仑UE", "spec": "UE泰尔", "name": "昆仑UE"},
    {"base": "祁连UM", "spec": "UM泰尔", "name": "祁连UM"},
    {"base": "泰山UT", "spec": "UT泰尔", "name": "泰山UT"},
]
SKIP  = {"UR泰尔","UE泰尔","UM泰尔","UT泰尔","电池泰尔","配置计算公式"}
STD   = {s["base"] for s in SERIES_MAP}

products = []
info = []

# 标准 UPS 系列（简化版）
for s in SERIES_MAP:
    ws = wb[s["base"]]
    hdrs = [str(ws.cell(1,c).value or '').strip() for c in range(1, ws.max_column+1)]
    cnt = sum(1 for r in range(2, ws.max_row+1) if str(ws.cell(r,2).value or '').strip())
    products += [{"系列": s["name"], "型号": f"mock_{i}"} for i in range(cnt)]
    info.append(f"{s['name']}×{cnt}")

# 非标准 Sheet：智能扫描
for sname in wb.sheetnames:
    if sname in SKIP or sname in STD: continue

    ws = wb[sname]
    raw = []
    for r in range(1, ws.max_row+1):
        row = [str(ws.cell(r,c).value or '').strip().replace('\n',' ')
               for c in range(1, ws.max_column+1)]
        raw.append(row)

    # 扫描前5行找表头行
    header_idx = -1
    model_col_idx = -1
    for i in range(min(len(raw), 5)):
        row = raw[i]
        mIdx = next((j for j,c in enumerate(row) if match(c, MODEL_PATTERNS)), -1)
        if mIdx >= 0:
            header_idx = i
            model_col_idx = mIdx
            break

    if header_idx < 0:
        print(f'  跳过 [{sname}]：未找到型号列，首行={raw[0][:4]}')
        continue

    headers = raw[header_idx]
    data_rows = raw[header_idx+1:]
    series_col = next((j for j,h in enumerate(headers) if match(h, SERIES_PATTERNS)), -1)
    desc_col   = next((j for j,h in enumerate(headers) if match(h, DESC_PATTERNS)), -1)

    print(f'  [{sname}] 表头行={header_idx}, 型号列={headers[model_col_idx]}, '
          f'系列列={"None" if series_col<0 else headers[series_col]}, '
          f'描述列={"None" if desc_col<0 else headers[desc_col]}')

    cnt = 0
    for rawrow in data_rows:
        model = rawrow[model_col_idx] if model_col_idx < len(rawrow) else ''
        if not model: continue

        sv = rawrow[series_col].strip() if series_col >= 0 and series_col < len(rawrow) else ''
        series_val = sv or sname

        combined = {'系列': series_val}
        for j,h in enumerate(headers):
            if not h or h == '序号': continue
            v = rawrow[j] if j < len(rawrow) else ''
            if not v: continue
            if re.search(r'产品型号', h) and '型号' not in combined: combined['型号'] = v
            elif match(h, DESC_PATTERNS) and '描述' not in combined:  combined['描述'] = v
            elif re.search(r'所属.*系列', h):                          combined['产品系列'] = v
            elif h not in combined:                                    combined[h] = v
        if '型号' not in combined: combined['型号'] = model

        products.append(combined)
        cnt += 1
    if cnt: info.append(f"{sname}×{cnt}")

print(f'\n导入汇总: {", ".join(info)}')
print(f'合计 {len(products)} 款产品\n')

# 显示电池架数据
print('「电池架」导入数据：')
for p in products:
    if p.get('系列','') not in {'太行UR','昆仑UE','祁连UM','泰山UT','配电柜'}:
        print(' ', {k:v for k,v in list(p.items())[:5]})
