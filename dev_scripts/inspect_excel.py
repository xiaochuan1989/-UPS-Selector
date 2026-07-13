import sys, openpyxl
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = Path(__file__).resolve().parents[1]
EXCEL_FILE = PROJECT_ROOT / 'test_data' / '常用UPS速查表-V7 测试.xlsx'
if not EXCEL_FILE.exists():
    EXCEL_FILE = PROJECT_ROOT / '常用UPS速查表-V8.0.xlsx'

wb = openpyxl.load_workbook(EXCEL_FILE, data_only=True)
print('所有Sheet名称:', wb.sheetnames)
print()

for name in wb.sheetnames:
    ws = wb[name]
    print(f'=== Sheet: {name} ===')
    print(f'  行数: {ws.max_row}, 列数: {ws.max_column}')
    # 显示第1行（表头）
    headers = [str(ws.cell(1, c).value or '') for c in range(1, min(ws.max_column+1, 15))]
    print(f'  表头: {headers}')
    # 显示前3行数据
    for r in range(2, min(5, ws.max_row+1)):
        row = [str(ws.cell(r, c).value or '') for c in range(1, min(ws.max_column+1, 8))]
        if any(v.strip() for v in row):
            print(f'  行{r}: {row}')
    print()
