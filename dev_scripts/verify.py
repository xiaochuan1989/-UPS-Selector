import sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
all_ok = True

PROJECT_ROOT = Path(__file__).resolve().parents[1]

with open(PROJECT_ROOT / 'index.html', encoding='utf-8') as f:
    html = f.read()

checks = [
    ('双表HTML-上栏', 'db-table-top'),
    ('双表HTML-下栏', 'db-table-bot'),
    ('双表分栏容器', 'id="db-split-layout"'),
    ('可拖动分隔条', 'id="db-splitter"'),
    ('分隔条初始化', 'function initDatabaseSplitter'),
    ('双表横向拖动', 'function initDatabaseHorizontalDrag'),
    ('列宽拖动功能', 'function initDatabaseColumnResizer'),
    ('列宽拖动提示', '拖动表头边界调整列宽'),
    ('产品信息标签', '产品信息'),
    ('泰尔规格标签', '技术规格（泰尔参数）'),
    ('DB_TOP_SET', 'const DB_TOP_SET'),
    ('buildTableHead', 'function buildTableHead'),
    ('buildRow', 'function buildRow'),
    ('悬停联动', 'db-row-hover'),
    ('sortDataTable双section', 'dbSortSection'),
    ('正则已修复', 'kw.replace(/[.*+?^${}()|['),
]
for name, key in checks:
    found = key in html
    mark = 'OK' if found else 'XX'
    print(f'  [{mark}] {name}')
    all_ok = all_ok and found

raise SystemExit(0 if all_ok else 1)
