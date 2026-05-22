"""
模拟浏览器 importExcel 的导入逻辑（Python版），用来验证新逻辑是否正确
"""
import sys, openpyxl
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = Path(__file__).resolve().parents[1]
EXCEL_FILE = PROJECT_ROOT / 'test_data' / '常用UPS速查表-V7 测试.xlsx'
if not EXCEL_FILE.exists():
    EXCEL_FILE = PROJECT_ROOT / '常用UPS速查表-V7.5.xlsx'

wb = openpyxl.load_workbook(EXCEL_FILE, data_only=True)

SERIES_MAP = [
    {"base": "太行UR", "spec": "UR泰尔", "name": "太行UR"},
    {"base": "昆仑UE", "spec": "UE泰尔", "name": "昆仑UE"},
    {"base": "祁连UM", "spec": "UM泰尔", "name": "祁连UM"},
    {"base": "泰山UT", "spec": "UT泰尔", "name": "泰山UT"},
]
SKIP_SHEETS = {"UR泰尔","UE泰尔","UM泰尔","UT泰尔","电池泰尔","配置计算公式"}
STD_BASE = {s["base"] for s in SERIES_MAP}

def sheet_to_rows(ws):
    headers = [str(ws.cell(1,c).value or '').strip() for c in range(1, ws.max_column+1)]
    rows = []
    for r in range(2, ws.max_row+1):
        row = {}
        for c, h in enumerate(headers, 1):
            v = ws.cell(r, c).value
            row[h] = str(v or '').strip().replace('\n', ' ')
        rows.append(row)
    return rows

products = []
info = []

# 标准 UPS 系列
for s in SERIES_MAP:
    base, spec, name = s["base"], s["spec"], s["name"]
    if base not in wb.sheetnames: continue
    base_rows = sheet_to_rows(wb[base])
    spec_rows = sheet_to_rows(wb[spec]) if spec in wb.sheetnames else []
    spec_map = {}
    for r in spec_rows:
        m = r.get("型号","").strip()
        if m: spec_map[m] = r
    cnt = 0
    for row in base_rows:
        model = row.get("型号","").strip()
        if not model: continue
        combined = {"系列": name}
        for k,v in row.items():
            if k and k != "序号" and v: combined[k] = v
        spec_row = spec_map.get(model, {})
        for k,v in spec_row.items():
            if k and k not in combined and v: combined[k] = v
        products.append(combined)
        cnt += 1
    if cnt: info.append(f"{name}×{cnt}")

# 额外 Sheet（自动识别）
import re
for sname in wb.sheetnames:
    if sname in SKIP_SHEETS or sname in STD_BASE: continue
    ws = wb[sname]
    headers = [str(ws.cell(1,c).value or '').strip() for c in range(1, ws.max_column+1)]

    model_col = next((h for h in headers if h == "型号"), None) or \
                next((h for h in headers if re.search(r'型号', h)), None) or \
                next((h for h in headers if re.search(r'产品编码|编号', h)), None)
    if not model_col:
        print(f'  跳过 {sname}：找不到型号列（headers={headers[:5]}）')
        continue

    series_col = next((h for h in headers if h == "系列"), None) or \
                 next((h for h in headers if re.search(r'所属.*系列|产品系列', h)), None) or \
                 next((h for h in headers if h == "类别"), None)

    print(f'  处理 {sname}: 型号列={model_col}, 系列列={series_col}')

    cnt = 0
    for r in range(2, ws.max_row+1):
        row = {headers[c-1]: str(ws.cell(r,c).value or '').strip().replace('\n',' ')
               for c in range(1, ws.max_column+1) if headers[c-1]}
        model = row.get(model_col,'').strip()
        if not model: continue

        series_val = row.get(series_col,'').strip() if series_col else sname
        combined = {"系列": series_val or sname}

        for k,v in row.items():
            if not k or k == "序号" or not v: continue
            if re.search(r'产品型号', k) and "型号" not in combined: combined["型号"] = v
            elif re.search(r'产品描述', k) and "描述" not in combined: combined["描述"] = v
            elif re.search(r'所属.*系列', k): combined["产品系列"] = v
            else: combined[k] = v
        if "型号" not in combined: combined["型号"] = model

        products.append(combined)
        cnt += 1
    if cnt: info.append(f"{sname}×{cnt}")

print(f'\n导入汇总: {", ".join(info)}')
print(f'合计 {len(products)} 款产品')

# 显示 "123" sheet 的前3条
print('\n"123" 表前3条数据:')
for p in products:
    if p.get("系列","") not in {"太行UR","昆仑UE","祁连UM","泰山UT"}:
        keys = list(p.keys())[:6]
        print(' ', {k: p[k] for k in keys})
        if products.index(p) >= 181: break
