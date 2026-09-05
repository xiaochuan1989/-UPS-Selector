# Multi-UPS Project Configuration and Model Search — Design QA

## Evidence

- Source UI: `artifacts/design-qa/ups-multi-config-source-ui-v1.8.17.png`.
- Business reference: `artifacts/design-qa/ups-multi-config-source-list-v1.8.17.png`.
- Side-by-side comparison: `artifacts/design-qa/ups-multi-config-comparison.html`.
- Model-search source UI: `artifacts/design-qa/ups-model-search-source-v1.8.19.png`.
- Model-search side-by-side comparison: `artifacts/design-qa/ups-model-search-comparison.html`.
- Implementation checked through v1.8.19 at 1826 × 1027 CSS pixels and at the narrower 1075 px browser width.
- Test project: `太行 UR-0100TPL × 2台` plus `昆仑 UE-0200TPL × 1台`.

## Comparison state

The supplied application screenshot establishes the existing UPS configuration visual language. The supplied Excel screenshot establishes the business need for multiple independent UPS systems and one consolidated bill of materials. The implementation adds a project-level manager above the existing input form without changing the original calculation cards.

## Findings

- Layout: passed. Saved configurations are visible before the form, use the existing blue panel treatment, and reduce from three to two to one columns with viewport width.
- Visual hierarchy: passed. Project count and “开始新配置” remain prominent; each saved card exposes name, model, UPS quantity, battery model, material count, load, and delete actions.
- Workflow: passed. “开始新配置” locates and focuses the input area, while “加入项目并新增下一套” validates and saves; two different UPS configurations can be added, loaded for modification, resaved, renamed, or deleted independently.
- Validation: passed. Empty standard and nonstandard UPS models cannot be added to the project, preventing incomplete configuration cards.
- Model discovery: passed. The native long select is replaced by a search combobox; entering `600` narrows the 105-product catalogue to eight matching model values and displays the match count beside the field.
- Search interaction: passed. Mouse selection, ArrowUp/ArrowDown navigation, Enter confirmation, and Esc/Tab/outside-click closing are implemented. A partial keyword cannot be saved as a standard UPS model.
- Search readability: passed. The floating candidate panel follows the existing blue-and-white visual language, preserves the full-width form layout, keeps the highlighted result obvious, and caps its height with an internal scrollbar.
- Aggregation: passed. Identical material models are merged in the project summary while distinct UPS models remain separate. In the checked scenario, `SP12-38b` merged from 128 + 64 into 192 batteries and preserved both configuration calculations in the description.
- Traceability: passed. Aggregated rows show `配置 1、配置 2` sources in the category badge and notes.
- Export continuity: passed. Excel, quotation, and technical-description exports consume the consolidated multi-configuration rows through the existing summary pipeline.
- Existing feature consistency: passed. Battery recommendation, switch cabinet sizing, monitoring quantities, editable summary fields, row ordering, price visibility, and custom summary rows remain available.
- Responsive behavior: passed. Cards and the input grid remain readable at both checked widths; the full-width desktop state matches the supplied application density.
- Console: passed. No application console errors were observed in the verified multi-UPS flow.

## Severity summary

- P0: none
- P1: none
- P2: none
- P3: none requiring remediation

## Final result

passed
