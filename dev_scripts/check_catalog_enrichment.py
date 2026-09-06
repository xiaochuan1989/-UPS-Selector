#!/usr/bin/env python3
"""校验 UPS 目录价对照表与 V8.0 速查表、内置数据库及目录 PDF 的一致性。"""

import json
import re
import sys
from pathlib import Path

import openpyxl

try:
    from pypdf import PdfReader
except ModuleNotFoundError:
    PdfReader = None


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = PROJECT_ROOT / "index.html"
WORKBOOK_PATH = PROJECT_ROOT / "常用UPS速查表-V8.0.xlsx"
CATALOG_PATH = PROJECT_ROOT / "解决方案产品目录价汇总（CM-CR-BM-BL-UPS）-iTeaQ-2026-04-V1.0 .pdf.pdf"
EXPECTED_MATCH_COUNT = 32


def normalize(value):
    return re.sub(r"\s+", "", str(value or "")).lower()


def parse_products(html):
    start = html.index("const PRODUCTS = [") + len("const PRODUCTS = ")
    depth = 0
    for index in range(start, len(html)):
        char = html[index]
        if char == "[":
            depth += 1
        elif char == "]":
            depth -= 1
            if depth == 0:
                return json.loads(html[start:index + 1])
    raise ValueError("未找到 PRODUCTS 数组结尾")


def decode_js_string(value):
    return json.loads('"' + value + '"')


def parse_enrichments(html):
    start = html.index("const UPS_CATALOG_ENRICHMENTS = [")
    end = html.index("function normalizeCatalogMatchText", start)
    block = html[start:end]
    pattern = re.compile(
        r'\{\s*model:\s*"((?:\\.|[^"])*)",\s*'
        r'description:\s*"((?:\\.|[^"])*)",\s*'
        r'code:\s*"((?:\\.|[^"])*)",\s*'
        r'price:\s*"((?:\\.|[^"])*)"'
        r'(?:,\s*note:\s*"((?:\\.|[^"])*)")?\s*\}',
        re.S,
    )
    return [
        {
            "model": decode_js_string(model),
            "description": decode_js_string(description),
            "code": decode_js_string(code),
            "price": decode_js_string(price),
            "note": decode_js_string(note) if note is not None else "",
        }
        for model, description, code, price, note in pattern.findall(block)
    ]


def workbook_pairs():
    workbook = openpyxl.load_workbook(WORKBOOK_PATH, read_only=True, data_only=True)
    pairs = set()
    for sheet_name in ("太行UR", "昆仑UE", "祁连UM", "泰山UT"):
        sheet = workbook[sheet_name]
        for model, description in sheet.iter_rows(min_row=2, min_col=2, max_col=3, values_only=True):
            if model and description:
                pairs.add((normalize(model), normalize(description)))
    workbook.close()
    return pairs


def catalog_text():
    if not CATALOG_PATH.exists() or PdfReader is None:
        return None
    reader = PdfReader(CATALOG_PATH)
    return "\n".join((page.extract_text() or "") for page in reader.pages[53:66])


def main():
    html = HTML_PATH.read_text(encoding="utf-8")
    products = parse_products(html)
    enrichments = parse_enrichments(html)
    product_pairs = [(normalize(item.get("型号")), normalize(item.get("描述"))) for item in products]
    excel_pairs = workbook_pairs()
    pdf_text = catalog_text()
    pdf_compact = re.sub(r"[\s,¥]", "", pdf_text) if pdf_text is not None else None

    errors = []
    if len(enrichments) != EXPECTED_MATCH_COUNT:
        errors.append(f"目录对照条数应为 {EXPECTED_MATCH_COUNT}，实际为 {len(enrichments)}")

    seen = set()
    for item in enrichments:
        pair = (normalize(item["model"]), normalize(item["description"]))
        if pair in seen:
            errors.append(f"重复匹配：{item['model']}")
        seen.add(pair)
        if product_pairs.count(pair) != 1:
            errors.append(f"内置数据库未唯一命中：{item['model']}")
        if pair not in excel_pairs:
            errors.append(f"V8.0 速查表型号/描述未命中：{item['model']}")
        codes = re.findall(r"\b\d{8}(?:-\d{2})?\b", item["code"])
        prices = re.findall(r"¥([\d,]+)", item["price"])
        if not codes or not prices:
            errors.append(f"编码或目录价格式无效：{item['model']}")
        if pdf_compact is not None:
            for code in codes:
                if code not in pdf_compact:
                    errors.append(f"目录 PDF 未找到编码 {code}：{item['model']}")
            for price in prices:
                if price.replace(",", "") not in pdf_compact:
                    errors.append(f"目录 PDF 未找到价格 {price}：{item['model']}")
        if "模块" in item["code"] and not item["note"]:
            errors.append(f"组合式 UPS 缺少单价或缺项说明：{item['model']}")
        if len(codes) > 1 and not item["note"]:
            errors.append(f"多编码 UPS 缺少版本说明：{item['model']}")

    mapped_codes = " ".join(item["code"] for item in enrichments)
    required_multi_version_codes = {
        "01021048", "01020404", "01021049", "01020405", "01021050", "01020406",
        "01020391", "01020401", "01020392", "01020402", "01020393", "01020403",
        "01021044", "01021127", "01021045", "01021128",
    }
    missing_variants = sorted(code for code in required_multi_version_codes if code not in mapped_codes)
    if missing_variants:
        errors.append("未完整保留多版本编码：" + ", ".join(missing_variants))

    forbidden_wrong_variant_codes = {
        "01021068", "01021069", "01021070", "01021071",
        "01021214", "01021215", "01021216", "99090462", "99090463",
    }
    wrong_variants = sorted(code for code in forbidden_wrong_variant_codes if code in mapped_codes)
    if wrong_variants:
        errors.append("错误混入 PF0.9 或 BL5.0 专用编码：" + ", ".join(wrong_variants))

    if errors:
        for error in errors:
            print("❌", error)
        return 1

    counts = {
        "太行UR": sum(item["model"].startswith("太行") for item in enrichments),
        "昆仑UE": sum(item["model"].startswith("昆仑") for item in enrichments),
        "祁连UM": sum(item["model"].startswith("祁连") for item in enrichments),
    }
    print(f"✅ 目录价对照校验通过：{len(enrichments)} 条数据库行，均唯一命中内置数据库与 V8.0 速查表")
    print("✅ 目录覆盖：" + "，".join(f"{name} {count} 条" for name, count in counts.items()))
    print("✅ 同型号多目录版本全部保留；PF0.9、锂电版和 BL5.0 专用版本未错误混入")
    if pdf_compact is None:
        print(f"⚠️ 未找到本地目录 PDF，已跳过 PDF 编码/价格原文核验：{CATALOG_PATH.name}")
    else:
        print("✅ 目录 PDF 编码与价格原文核验通过")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
