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
    ('横向拖动不拦截文字选择', 'event.button === 0 && event.shiftKey'),
    ('文字选择交互提示', '可选择文字；按住 Shift 拖动可横向查看'),
    ('列宽拖动功能', 'function initDatabaseColumnResizer'),
    ('列宽拖动提示', '拖动列宽 · Shift+拖动横移'),
    ('型号详情弹窗', 'id="db-detail-modal"'),
    ('型号详情打开逻辑', 'function openDatabaseProductDetail'),
    ('型号详情产品信息卡片', 'db-detail-product-grid'),
    ('型号详情泰尔参数卡片', 'db-detail-tech-grid'),
    ('文字选择不触发行详情', 'selection && !selection.isCollapsed'),
    ('横向平移不误触详情', "scroller.dataset.suppressRowClick = 'true'"),
    ('多套UPS配置管理区', 'id="multi-ups-list"'),
    ('保存并新增下一套', 'function saveCurrentUpsConfigurationAndStartNext'),
    ('新配置按钮定位表单', "showImportToast('已开始新配置，请选择或填写 UPS 型号')"),
    ('空UPS型号禁止加入项目', "请先选择 UPS 型号，再加入项目"),
    ('载入已保存配置', 'function loadSavedUpsConfiguration'),
    ('相同物料自动合并', 'function collectSavedConfigurationRows'),
    ('多配置导出链路', 'collectProjectSummaryRows({ includeSaved: false })'),
    ('数据库视图占满剩余高度', 'body.db-view-active #data-table-panel'),
    ('数据库视图状态切换', "document.body.classList.toggle('db-view-active', key === 'db')"),
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
